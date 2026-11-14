#version 330 core

uniform vec3 lightColor;
uniform vec3 lightDir;
uniform float lightIntensity;
uniform vec3 viewPos;
uniform int displayMode;
uniform bool clearSurface;
uniform bool mapContext;
in float terrainAltitude;
uniform float planetRadius;
uniform float kmPerWaterMass;
uniform samplerCube noiseCubemap;
uniform sampler2D terrainNormalMap;
uniform sampler2D waterNormalMap;
uniform vec3 selectedVertexPos;
uniform bool compactSelection;
uniform vec3 vegetationColor;

in vec3 worldNormal;
in vec3 worldPosition;
in float interpData;
in float waterElevation;
in float vegetation;
in float outSelected;
in vec3 tangentViewPos;
in vec3 tangentFragPos;

out vec4 fragColor;

// Return a single noise value from 0 to 1 computed from data that stays the same frame to frame
float noiseValue() {
	return texture(noiseCubemap, worldPosition / planetRadius).x;
}

float getDepth(vec2 coords) {
	return texture(terrainNormalMap, coords).x;
}

vec2 parallaxMapping(vec2 texCoords, vec3 viewDir) {
	float heightScale = 100.0;
	float height = 1.0 - getDepth(texCoords);
	vec2 p = viewDir.xy / viewDir.z * (height * heightScale);
	return texCoords - p;
}

// Whiteout blend from https://bgolus.medium.com/normal-mapping-for-a-triplanar-shader-10bf39dca05a
vec3 getNormal(vec3 viewDir) {
	float waterBlend = 1.0 - exp(-waterElevation * 1.0);

	float scale = 0.003;
	float strength = 0.8;
	vec2 uvX = parallaxMapping(worldPosition.zy * scale, viewDir);
	vec2 uvY = parallaxMapping(worldPosition.xz * scale, viewDir);
	vec2 uvZ = parallaxMapping(worldPosition.xy * scale, viewDir);

	vec3 normalX = mix(texture(terrainNormalMap, uvX).xyz, texture(waterNormalMap, uvX).xyz, waterBlend);
	vec3 normalY = mix(texture(terrainNormalMap, uvY).xyz, texture(waterNormalMap, uvY).xyz, waterBlend);
	vec3 normalZ = mix(texture(terrainNormalMap, uvZ).xyz, texture(waterNormalMap, uvZ).xyz, waterBlend);

	normalX = vec3(normalX.xy + worldNormal.zy, abs(normalX.z) * worldNormal.x);
	normalY = vec3(normalY.xy + worldNormal.xz, abs(normalY.z) * worldNormal.y);
	normalZ = vec3(normalZ.xy + worldNormal.xy, abs(normalZ.z) * worldNormal.z);

	vec3 blend = normalize(abs(worldNormal));

	return mix(worldNormal, normalize(
		normalX.zyx * blend.x + normalY.xzy * blend.y + normalZ.xyz * blend.z
	), strength);
}

vec3 hsv2rgb(vec3 c) {
	vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
	vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
	return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}


void main() {
	if (displayMode == 0) {
        // Readable planet-laboratory map. Colors represent the actual simulation
        // fields, not a painted backdrop; planting changes this branch directly.
        if (clearSurface) {
            float height = length(worldPosition) - planetRadius;
            vec3 bare = mix(vec3(0.64, 0.40, 0.16), vec3(0.37, 0.23, 0.10), smoothstep(0.0, 110.0, height));
            vec3 land = mix(bare, vec3(0.10, 0.55, 0.15), clamp(vegetation, 0.0, 1.0));
            vec3 water = mix(vec3(0.03, 0.48, 0.70), vec3(0.015, 0.11, 0.40), 1.0-exp(-waterElevation*0.5));
            float wet = smoothstep(0.001, 0.03, waterElevation);
            vec3 mapColor = mix(land, water, wet);
            float ice = wet * (1.0-smoothstep(268.15, 273.15, interpData));
            mapColor = mix(mapColor, vec3(0.80, 0.90, 0.96), ice);
            float relief = 0.72 + 0.28 * max(dot(normalize(worldNormal), lightDir), 0.0);
            mapColor *= relief;
            if(mapContext) {
                // Hypsometric/contour map of interpolated real terrain. No texture noise.
                float h=terrainAltitude;
                vec3 low=vec3(0.55,0.53,0.34);
                vec3 high=vec3(0.79,0.71,0.49);
                vec3 ground=mix(low,high,smoothstep(-4.0,10.0,h));
                ground=mix(ground,vec3(0.16,0.49,0.28),clamp(vegetation,0.0,1.0));
                vec3 sea=mix(vec3(0.14,0.47,0.53),vec3(0.035,0.17,0.28),1.0-exp(-waterElevation*0.35));
                mapColor=mix(ground,sea,wet);
                float band=h/1.0;
                float delta=max(fwidth(band),0.0001);
                float nearest=abs(fract(band+0.5)-0.5);
                float contour=1.0-smoothstep(delta*0.5,delta*1.5,nearest);
                mapColor*=1.0-contour*0.08*(1.0-wet);
                float shore=4.0*wet*(1.0-wet);
                mapColor=mix(mapColor,vec3(0.68,0.76,0.62),shore*0.28);
                mapColor*=0.85+0.15*max(dot(normalize(worldNormal),lightDir),0.0);
                mapColor=mix(mapColor,vec3(0.80,0.90,0.96),ice);
            }
            float ringDistance = length(worldPosition-selectedVertexPos);
            float ring = 1.0-smoothstep(3.0, 7.0, abs(ringDistance-90.0));
            if (!compactSelection) mapColor = mix(mapColor, vec3(1.0, 0.85, 0.15), ring*0.85);
            fragColor = vec4(mapColor, 1.0);
            return;
        }
		vec3 ambient = (0.05 + lightIntensity / 10.0) * lightColor;

		vec3 nViewDir = normalize(tangentViewPos - tangentFragPos);
		vec3 nNormal = getNormal(nViewDir);
		// TODO: texture coords
		
		vec3 diffuse = max(dot(nNormal, lightDir) * lightIntensity, 0.0) * lightColor;

		float specularStrength = 0.1;
		float specularPower = 64.0;
		vec3 terrainColor = mix(vec3(0.5f, 0.4f, 0.3f), vegetationColor, vegetation);
		vec3 objectColor = terrainColor * (noiseValue() / 20.0 + 1.0);

		float waterTreshold = 0.1 + (noiseValue() * 2.0 - 1.0) * 0.025;
		if (interpData < 280.15) {
			waterTreshold = 0.0002 + (noiseValue() * 2.0 - 1.0) * 0.0001;
		}
		
		// totalElevation = elevation + water (km)
		// partialWaterElevation = water (km)
		float partialWaterElevation = waterElevation * 10.0;
		if (partialWaterElevation >= waterTreshold) {
			float depthMultiplier = 0.2;
			float alphaMultiplier = 1.0;

			float opticalDepth = 1.0 - exp(-partialWaterElevation * depthMultiplier);
			float alpha = 1.0 - exp(-partialWaterElevation * alphaMultiplier);

			// vec3 waterColor = mix(vec3(0.1f, 0.3f, 0.8f), vec3(0.05f, 0.2f, 0.4f), min(opticalDepth, 1)); // ocean blue
			// objectColor = mix(objectColor, waterColor, alpha);

			float iceLevel = min(1.0, exp((-interpData + 272.15) / 5.0));
			objectColor = mix(objectColor, vec3(1.0f, 1.0f, 1.0f), iceLevel * min(1.0, alpha*10.0));
			if (interpData > 273.15) {
				specularPower = mix(16.0, 256.0, min(partialWaterElevation*1.0*(1.0-iceLevel), 1.0));
				specularStrength = 0.5;
			} else {
				specularPower = 64.0;
				specularStrength = 0.5;
			}
		}

		vec3 viewDir = normalize(viewPos - worldPosition);
		vec3 reflectDir = reflect(-lightDir, nNormal);
		float spec = pow(max(dot(viewDir, reflectDir), 0.0), specularPower);
		vec3 specular = specularStrength * spec * lightColor * lightIntensity;

		vec3 result = (ambient + diffuse + specular) * objectColor;
		float selected = 1.0 - length(worldPosition - selectedVertexPos) / 100.0;
		if (selected > 0.0) {
			float selectedE = 1.0 - (1.0 - selected) * (1.0 - selected);
			result = mix(result, vec3(0.1f, 0.1f, 0.9f), selectedE);
		}
		fragColor = vec4(result, 1.0f);
	} else if (displayMode == 1) { // temperature
		vec3 cold = vec3(234.0f / 360.0f, 1.0f, 0.5f);
		vec3 hot  = vec3(  0.0f / 360.0f, 1.0f, 0.33f);
		// Default range of -50°C - 50°C
		vec3 result = hsv2rgb(mix(cold, hot, clamp((interpData - 273.15 + 50.0) / 100.0, 0.0, 1.0)));
		fragColor = vec4(result, 1.0f);
	} else if (displayMode == 2) { // water vapor
		vec3 cold = vec3(0.0f, 0.0f, 0.0f);
		vec3 hot  = vec3(1.0f, 1.0f, 0.0f);
		float waterKm = interpData * kmPerWaterMass;
		vec3 result = mix(cold, hot, (waterKm) / 0.001);
		fragColor = vec4(result, 1.0f);
	} else if (displayMode == 3) { // wind
		// From 0 to 200 km/h
		float right = interpData * 3600.0 / 200.0;
		float up = waterElevation * 3600.0 / 200.0;
		vec3 result = vec3(right / 2.0, sqrt(right * right + up * up), up / 2.0);
		fragColor = vec4(result, 1.0f);
	} else if (displayMode == 4) { // rainfall
		// for rainfall, colors are in HSV (in order to make a smooth color gradient)
		vec3 cold = vec3( 25.0f / 360.0f, 1.0f, 0.33f);
		vec3 hot  = vec3(234.0f / 360.0f, 1.0f, 0.5f);
		float waterKm = interpData * kmPerWaterMass;
		vec3 result = hsv2rgb(mix(cold, hot, clamp((waterKm) / 0.03, 0.0, 1.0)));
		fragColor = vec4(result, 1.0f);
	}
}


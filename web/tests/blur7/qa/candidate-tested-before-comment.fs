#version 330 core
#define M_PI 3.1415926535897932384626433832795
#define BLUR_KERNEL_SIZE 5

// Parameters
uniform vec3 viewPos;
uniform vec3 lightDir;
uniform float lightIntensity;
uniform float planetRadius;
uniform float atmosphereRadius;
uniform mat4 projMatrix;
uniform mat4 viewMatrix;
uniform bool enableAtmosphere;
uniform bool enableBloom;

// Samplers
uniform sampler2D screenTexture;
uniform sampler2D bloomTexture;
uniform sampler2D screenDepth;

// Operations
uniform bool doBrightTexture;
uniform bool doBlurring;
uniform bool horizontalBlurring;

in vec2 texCoords;

out vec4 fragColor;

#define pos_infinity uintBitsToFloat(0x7F800000U)

// Returns vector (dstToSphere, dstThroughSphere)
vec2 raySphere(float sphereRadius, vec3 rayOrigin, vec3 rayDir) {
	vec3 offset = rayOrigin;
	float a = 1.0;
	float b = 2.0 * dot(offset, rayDir);
	float c = dot(offset, offset) - sphereRadius * sphereRadius;
	float d = b * b - 4.0 * a * c;
	
	if (d > 0.0) {
		float s = sqrt(d);
		float dstNear = max(0.0, (-b - s) / (2.0 * a));
		float dstFar = (-b + s) / (2.0 * a);
		if (dstFar >= 0.0) {
			return vec2(dstNear, dstFar - dstNear);
		}
	}
	
	// TODO: vec2(infinity, 0)
	return vec2(pos_infinity, 0.0);
}

float densityAtPoint(vec3 point) {
	float radius = planetRadius - 100.0;
	float height = length(point) - radius;
	float heightScaled = height / (atmosphereRadius - radius);
	float densityFalloff = 4.00; // TODO: variable depending on composition?
	float localDensity = exp(-heightScaled * densityFalloff) * (1.0 - heightScaled);
	return localDensity;
}

// TODO: optimise by storing in a LUT
float opticalDepth(vec3 rayOrigin, vec3 rayDir, float rayLength) {
	vec3 point = rayOrigin;
	int numOpticalDepthPoints = 10;
	float stepSize = rayLength / float(numOpticalDepthPoints);
	float opticalDepth = 0.0;
	
	for (int i = 0; i < numOpticalDepthPoints; i++) {
		float localDensity = densityAtPoint(point);
		opticalDepth += localDensity * stepSize;
		point += rayDir * stepSize;
	}
	return opticalDepth;
}

vec3 calculateLight(vec3 rayOrigin, vec3 rayDir, float rayLength, vec3 originalColor) {
	int numInScatteringPoints = 10; // TODO: configurable quality level
	
	vec3 inScatterPoint = rayOrigin;
	float stepSize = rayLength / float(numInScatteringPoints);
	vec3 inScatteredLight = vec3(0.0);
	vec3 dirToSun = lightDir;
	
	vec3 wavelengths = vec3(700.0, 530.0, 440.0);
	vec3 scatteringCoefficients = pow(400.0 / wavelengths, vec3(4.0));
	float scatteringStrength = 1.0;
	scatteringCoefficients *= scatteringStrength;
	float viewRayOpticalDepth;
	
	for (int i = 0; i < numInScatteringPoints; i++) {
		float sunRayLength = raySphere(atmosphereRadius, inScatterPoint, dirToSun).y;
		float sunRayOpticalDepth = opticalDepth(inScatterPoint, dirToSun, sunRayLength);
		viewRayOpticalDepth = opticalDepth(inScatterPoint, -rayDir, stepSize * float(i));
		//sunRayOpticalDepth = 0;
		vec3 transmittance = exp(-(sunRayOpticalDepth + viewRayOpticalDepth) * scatteringCoefficients);
		float localDensity = densityAtPoint(inScatterPoint);
		
		inScatteredLight += localDensity * transmittance * scatteringCoefficients * stepSize;
		inScatterPoint += rayDir * stepSize;
	}
	
	//float originalColorTransmittance = exp(-viewRayOpticalDepth);
	float originalColorTransmittance = 1.0;
	return originalColor * originalColorTransmittance + inScatteredLight * lightIntensity;
}

float linearizeDepth(float d, float zNear, float zFar) {
	float z_n = 2.0 * d - 1.0;
	return 2.0 * zNear * zFar / (zFar + zNear - z_n * (zFar - zNear));
}

void drawBrightTexture() {
	vec3 color = texture(screenTexture, texCoords).rgb;
	float brightness = dot(color.rgb, vec3(0.2126, 0.7152, 0.0722));
	if (brightness > 1.0) {
		fragColor = vec4(color.rgb, 1.0);
	} else {
		fragColor = vec4(0.0, 0.0, 0.0, 1.0);
	}
}

void drawBlurredTexture() {
    vec2 stepSize = 1.0 / vec2(textureSize(screenTexture, 0));
    vec2 axis = horizontalBlurring ? vec2(stepSize.x, 0.0) : vec2(0.0, stepSize.y);
    vec3 result = texture(screenTexture, texCoords).rgb * 0.227027;
    result += texture(screenTexture, texCoords + axis * 1.5).rgb * 0.1945946;
    result += texture(screenTexture, texCoords - axis * 1.5).rgb * 0.1945946;
    result += texture(screenTexture, texCoords + axis * 3.181818059504092).rgb * 0.1486486;
    result += texture(screenTexture, texCoords - axis * 3.181818059504092).rgb * 0.1486486;
    result += texture(screenTexture, texCoords + axis * 5.37499710935874).rgb * 0.043243;
    result += texture(screenTexture, texCoords - axis * 5.37499710935874).rgb * 0.043243;
    fragColor = vec4(result, 1.0);
}

void main() {
	// Post-process
	if (doBrightTexture) {
		drawBrightTexture();
		return;
	} else if (doBlurring) {
		drawBlurredTexture();
		return;
	}

	vec3 color = texture(screenTexture, texCoords).rgb;
	// Browser scenes disable atmosphere; avoid reconstructing unused rays.
	// Bloom and HDR mapping remain unchanged, including emissive animals.
	vec3 result = color;
	if (enableAtmosphere) {
		float depth = texture(screenDepth, texCoords).r;

		mat4 projViewMatrix = projMatrix * viewMatrix;

		float zFar = planetRadius * 5.0;
		float zNear = zFar / 10000.0;

		vec4 fragNear = inverse(projViewMatrix) * vec4((texCoords.xy - vec2(0.5, 0.5))*2.0, 0.0, 1.0);
		vec4 fragFar = fragNear + inverse(projViewMatrix)[2];
		fragNear.xyz /= fragNear.w;
		fragFar.xyz /= fragFar.w;
		vec4 fragDir = fragFar - fragNear;

		vec3 rayDir = normalize(fragDir.xyz);
		vec2 hitInfo = raySphere(atmosphereRadius, viewPos, rayDir);

		float dstToAtmosphere = hitInfo.x;
		//float dstToSurface = linearizeDepth(depth, zNear, zFar); // TODO: make it work
		float dstToSurface = dstToAtmosphere + 500.0;
		float dstThroughAtmosphere = min(hitInfo.y, dstToSurface - dstToAtmosphere);
		if (depth == 1.0) {
			dstToSurface = dstToAtmosphere + 500.0;
		}

		float factor = dstThroughAtmosphere / atmosphereRadius / 2.0;

		if (dstThroughAtmosphere > 0.0) {
			vec3 pointInAtmosphere = viewPos + rayDir * dstToAtmosphere;
			if (depth == 1.0) { // skybox
				color = vec3(0.0);
			}
			vec3 light = calculateLight(pointInAtmosphere, rayDir, dstThroughAtmosphere, color);
			result = light;
			//result = pointInAtmosphere / vec3(10000);
		} else {
			result = color;
		}
		//result = mix(result, vec3((dstToSurface - dstToAtmosphere - 500) / 10), 0.9);
		// result = vec3(dstThroughAtmosphere / (planetRadius * 2));

	}

	// Apply bloom
	vec3 bloomColor = enableBloom ? texture(bloomTexture, texCoords).rgb : vec3(0.0);
	result += bloomColor;

	if (false) {
		float ghostSpacing = 0.25;
		float ghostTreshold = 0.1;
		int ghostCount = 5;
		
		vec2 uv = vec2(1.0) - texCoords;
		vec3 ret = vec3(0.0);
		vec2 ghostVec = (vec2(0.5) - uv) * ghostSpacing;
		result -=  result;

		for (int i = 0; i < ghostCount; i++) {
			vec2 suv = fract(uv + ghostVec * vec2(i));
			float d = distance(suv, vec2(0.5));
			float weight = 1.0 - smoothstep(0.0, 0.75, d);
			vec3 s = max(color - vec3(ghostTreshold), vec3(0.0)); // apply treshold
			result += s * weight;
		}
	}
	
	// HDR
	float gamma = 1.0; // 2.2
	float exposure = 1.0;
	fragColor = vec4(pow(vec3(1.0) - exp(-result * exposure), vec3(1.0 / gamma)), 1.0f);
}


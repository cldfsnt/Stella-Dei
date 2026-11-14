#!/usr/bin/env python3
"""Validate original GLSL330 and adapted GLSL ES300 shader pairs.

Usage: GLSLANG_VALIDATOR=/path/to/glslangValidator python3 web/validate_shaders.py
Requires Khronos glslangValidator. Static validation is not GPU/gameplay testing.
"""
import os
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
validator = os.environ.get('GLSLANG_VALIDATOR', 'glslangValidator')
with tempfile.TemporaryDirectory(prefix='stella-shaders-') as tmp:
    folder = Path(tmp)
    for web in (False, True):
        for vertex in sorted((root / 'src/shaders').glob('*.vs')):
            paths = []
            for suffix, stage in (('.vs', '.vert'), ('.fs', '.frag')):
                source = vertex.with_suffix(suffix).read_text()
                if web:
                    source = source.replace('#version 330 core\n', '#version 300 es\nprecision highp float;\nprecision highp int;\n', 1)
                target = folder / (vertex.stem + stage)
                target.write_text(source)
                paths.append(str(target))
            subprocess.run([validator, '-l', *paths], check=True)
    shaders = root / 'deps/nanovg/src/glsl'
    vertex = folder / 'nanovg.vert'
    fragment = folder / 'nanovg.frag'
    vertex.write_text('#version 300 es\n#define attribute in\n#define varying out\n' + (shaders / 'fill.vert').read_text())
    for antialias in (False, True):
        prefix = '#version 300 es\nprecision mediump float;\n#define varying in\n#define texture2D texture\nout vec4 webglFragColor;\n#define gl_FragColor webglFragColor\n'
        if antialias:
            prefix += '#define EDGE_AA 1\n'
        fragment.write_text(prefix + (shaders / 'fill.frag').read_text())
        subprocess.run([validator, '-l', str(vertex), str(fragment)], check=True)
print('PASS: 6 desktop pairs, 6 ES300 pairs, NanoVG ES300 with and without antialiasing')

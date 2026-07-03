#!/usr/bin/env python3
"""
Unreal Engine 4 Lite - Shader Compiler Configuration
Configures shader compilation for mobile optimization
"""

import os
import json
import sys
from pathlib import Path

class ShaderCompilerConfig:
    """Configure shader compilation for mobile"""
    
    def __init__(self, engine_root):
        self.engine_root = Path(engine_root)
        self.shader_dir = self.engine_root / 'Engine' / 'Shaders'
        self.config_dir = self.engine_root / 'Engine' / 'Config'
    
    def create_mobile_shader_config(self):
        """Create mobile shader compilation configuration"""
        
        config = {
            "ShaderFormats": [
                {
                    "Format": "GLSL_ES3_1",
                    "Platform": "Android",
                    "Compression": "ETC2"
                },
                {
                    "Format": "Vulkan",
                    "Platform": "Android",
                    "Compression": "ASTC"
                }
            ],
            "DisabledFeatures": [
                "ATMOSPHERIC_FOG",
                "SKY_ATMOSPHERE",
                "VOLUMETRIC_FOG",
                "DISTANCE_FIELD_SHADOWS",
                "WHOLE_SCENE_SHADOWS",
                "STATIONARY_SKYLIGHT",
                "GLOBAL_DISTANCE_FIELD",
                "GLOBAL_ILLUMINATION",
                "RAY_TRACING",
                "NANITE",
                "VIRTUAL_TEXTURES"
            ],
            "EnabledFeatures": [
                "MOBILE_FORWARD_RENDERING",
                "UNLIT_MATERIALS",
                "SIMPLE_LIGHTING",
                "EARLY_Z_PASS",
                "LOD_STREAMING"
            ],
            "CompilerSettings": {
                "MaxTextureSamplers": 5,
                "EnableShaderCache": True,
                "EnableShaderPipelining": True,
                "OptimizationLevel": "Aggressive",
                "StripDebugInfo": True
            }
        }
        
        config_file = self.config_dir / "Android" / "ShaderCompilerConfig.json"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✓ Created shader compiler config: {config_file}")
        return config
    
    def create_shader_compilation_rules(self):
        """Create shader compilation rules for Lite"""
        
        rules = """// UE4 Lite - Shader Compilation Rules
// Applied during shader compilation for mobile optimization

// Feature levels
#define FEATURE_LEVEL_ES3_1 1
#define FEATURE_LEVEL_ES3_2 0
#define FEATURE_LEVEL_SM4 0
#define FEATURE_LEVEL_SM5 0
#define FEATURE_LEVEL_SM6 0

// Material features
#define NUM_MATERIAL_TEXCOORDS 3
#define NUM_DYNAMIC_DECAL_SLOTS 1
#define MATERIAL_FULLY_ROUGH 0
#define MATERIAL_USE_LM_DIRECTIONALITY 0
#define MATERIAL_USE_PRECOMPUTED_AO 0

// Rendering features
#define SUPPORTS_INDEPENDENT_SAMPLERS 0
#define SUPPORTS_DEPTH_BOUNDS_TEST 0
#define SUPPORTS_TEXTURE_GATHER 0
#define SUPPORTS_VARIABLE_RATE_SHADING 0

// Optimization passes
#define ENABLE_AGGRESSIVE_OPTIMIZATION 1
#define ENABLE_UNIFORM_BUFFER_LAYOUT_OPTIMIZATION 1
#define ENABLE_SHADER_PERMUTATION_REDUCTION 1
"""
        
        rules_file = self.shader_dir / "Definitions" / "LiteCompilationRules.ush"
        rules_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(rules_file, 'w') as f:
            f.write(rules)
        
        print(f"✓ Created shader compilation rules: {rules_file}")
    
    def create_permutation_reduction_config(self):
        """Create shader permutation reduction config"""
        
        config = {
            "PermutationReduction": {
                "MaxPermutations": 1000,
                "PruneUnusedPermutations": True,
                "AggresiveReduction": True,
                "TargetCompilationTime": 30  # seconds
            },
            "MaterialFeaturePermutations": {
                "UseHeightFog": False,
                "UseVolumeFog": False,
                "UseDistance": False,
                "UseVertexFog": True,
                "UseWorldPositionOffset": False,
                "UsePlanarReflections": False
            }
        }
        
        config_file = self.config_dir / "Android" / "PermutationReduction.json"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✓ Created permutation reduction config: {config_file}")

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: configure-shader-compiler.py <engine_root>")
        sys.exit(1)
    
    engine_root = sys.argv[1]
    
    if not Path(engine_root).exists():
        print(f"Error: Engine root not found: {engine_root}")
        sys.exit(1)
    
    print("Configuring shader compiler for UE4 Lite...")
    
    compiler = ShaderCompilerConfig(engine_root)
    compiler.create_mobile_shader_config()
    compiler.create_shader_compilation_rules()
    compiler.create_permutation_reduction_config()
    
    print("\n✓ Shader compiler configuration complete!")

if __name__ == '__main__':
    main()

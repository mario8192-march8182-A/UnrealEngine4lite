#!/bin/bash
# Disable expensive shaders and rendering features for UE4 Lite
# This script modifies shader compilation flags to remove heavy features

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ENGINE_ROOT="$(cd $SCRIPT_DIR/../../../.. && pwd)"
SHADER_DIR="$ENGINE_ROOT/Engine/Shaders"

echo "Disabling expensive shaders and features for Android Lite..."

# Create shader compilation flags file
cat > "$SHADER_DIR/Definitions/LiteMobileShaders.h" << 'EOF'
// Unreal Engine 4 Lite - Mobile Shader Compilation Flags
// These flags disable expensive rendering features

#pragma once

// Atmospheric effects - DISABLED for Lite
#define ENABLE_ATMOSPHERIC_FOG 0
#define ENABLE_SKY_ATMOSPHERE 0
#define ENABLE_VOLUMETRIC_FOG 0
#define ENABLE_VOLUMETRIC_CLOUDS 0

// Advanced shadows - DISABLED for Lite
#define ENABLE_DISTANCE_FIELD_SHADOWS 0
#define ENABLE_WHOLE_SCENE_SHADOWS 0
#define ENABLE_STATIONARY_SKYLIGHT 0
#define ENABLE_VIRTUAL_SHADOW_MAPS 0
#define ENABLE_CASCADED_SHADOW_MAPS 0

// Advanced lighting - DISABLED for Lite
#define ENABLE_GLOBAL_DISTANCE_FIELD 0
#define ENABLE_GLOBAL_ILLUMINATION 0
#define ENABLE_LUMEN_GI 0
#define ENABLE_DYNAMIC_GLOBAL_ILLUMINATION 0

// Post-processing - DISABLED for Lite
#define ENABLE_BLOOM 0
#define ENABLE_MOTION_BLUR 0
#define ENABLE_DEPTH_OF_FIELD 0
#define ENABLE_SCREEN_SPACE_REFLECTIONS 0
#define ENABLE_AMBIENT_OCCLUSION 0
#define ENABLE_SCREEN_SPACE_AMBIENT_OCCLUSION 0

// Advanced materials - DISABLED for Lite
#define ENABLE_HAIR_STRANDS 0
#define ENABLE_CLOTH_SIMULATION 0
#define ENABLE_DISTANCE_FUNCTIONS 0
#define ENABLE_DEFORMATION_MATERIALS 0

// Ray tracing - DISABLED for Lite
#define ENABLE_RAY_TRACING 0
#define ENABLE_RAY_TRACED_REFLECTIONS 0
#define ENABLE_RAY_TRACED_SHADOWS 0
#define ENABLE_RAY_TRACED_AMBIENT_OCCLUSION 0

// Nanite - DISABLED for Lite
#define ENABLE_NANITE 0
#define ENABLE_NANITE_MATERIALS 0

// Virtual textures - DISABLED for Lite
#define ENABLE_VIRTUAL_TEXTURES 0
#define ENABLE_RUNTIME_VIRTUAL_TEXTURE 0

// Mobile-optimized features
#define ENABLE_MOBILE_FORWARD_RENDERING 1
#define ENABLE_UNLIT_MATERIALS 1
#define ENABLE_SIMPLE_LIGHTING 1
#define ENABLE_EARLY_Z_PASS 1
#define ENABLE_LOD_STREAMING 1

// Material features - LIMITED for Lite
#define MAX_MATERIAL_TEXTURE_SAMPLERS 5
#define ENABLE_MATERIAL_LAYERS 0
#define ENABLE_SUBSTRATE 0

EOF

echo "✓ Created LiteMobileShaders.h"

# Modify shader compilation settings
cat > "$SHADER_DIR/Private/MaterialTemplate.ush.patch" << 'EOF'
--- a/Engine/Shaders/Private/MaterialTemplate.ush
+++ b/Engine/Shaders/Private/MaterialTemplate.ush
@@ -1,5 +1,10 @@
 // Unreal Engine Material Shader Template
 
+// LITE MOBILE OPTIMIZATION
+#include "/Engine/Shaders/Definitions/LiteMobileShaders.h"
+
+#if ENABLE_ATMOSPHERIC_FOG || ENABLE_SKY_ATMOSPHERE
+#error "Atmospheric effects disabled in UE4 Lite"
+#endif
 
 // Include common shader utilities
 #include "/Engine/Shaders/Common.ush"
EOF

echo "✓ Created MaterialTemplate.ush patch"

# Create plugin disabling configuration
cat > "$ENGINE_ROOT/Engine/Plugins/Lite/DisabledPlugins.uplugin" << 'EOF'
{
  "FileVersion": 3,
  "Version": 1,
  "VersionName": "1.0",
  "FriendlyName": "UE4 Lite - Disabled Plugins Configuration",
  "Description": "Disables VR, AR, and other expensive plugins for mobile",
  "Category": "Mobile",
  "CreatedBy": "UE4 Lite Team",
  "CreatedByURL": "https://github.com/mario8192-march8182-A/UnrealEngine4lite",
  "DocsURL": "",
  "MarketplaceURL": "",
  "SupportURL": "",
  "EngineVersion": "4.22.0",
  "CanContainContent": false,
  "Installed": false,
  "Modules": []
}
EOF

echo "✓ Created DisabledPlugins.uplugin"

# Create list of plugins to disable
cat > "$ENGINE_ROOT/Engine/Build/Android/disabled-plugins.txt" << 'EOF'
# VR Plugins - DISABLED for Lite
SteamVR
GoogleVR
OculusVR
OpenVR
LeapMotion
MagicLeap
OSVRClientKit
WindowsMixedReality

# AR Plugins - DISABLED for Lite
ARCore
ARKit
MagicLeapPassthrough
MagicLeapHandTracking

# Advanced Graphics Plugins - DISABLED for Lite
Alembic
GeometryCaching
HairStrands
ClothingSystem
ChaosDynamics
ChaosCloth
ChaosDestruction
ChaosFlesh
ChaosNiagara

# Audio Plugins - KEEP MINIMAL
WwiseSoundEngine
MetaAudio

# Networking Plugins - KEEP MINIMAL
Networking
Replication

# Development Tools - DISABLED for Runtime
EditorScriptingUtilities
DeveloperSettings
ClassViewer
TimelineEditor
CurveEditorTools
Sequencer
EOF

echo "✓ Created disabled-plugins.txt"

echo -e "\n\033[92m=== Shader Optimization Complete ==="
echo "Modified files:"
echo "  - $SHADER_DIR/Definitions/LiteMobileShaders.h"
echo "  - $ENGINE_ROOT/Engine/Build/Android/disabled-plugins.txt"
echo -e "\nNext: Run GenerateProjectFiles to rebuild shader cache\033[0m"

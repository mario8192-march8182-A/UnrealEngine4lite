#!/bin/bash
# Remove unnecessary plugins from UE4 Lite build
# Keeps only essential plugins for mobile gameplay

set -e

ENGINE_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../../../.." && pwd )"
PLUGINS_DIR="$ENGINE_ROOT/Engine/Plugins"

echo "Removing unnecessary plugins for UE4 Lite..."
echo "Engine Root: $ENGINE_ROOT"

# Array of plugins to remove (VR/AR/Advanced Graphics)
PLUGINS_TO_REMOVE=(
    # VR Plugins
    "Platforms/SteamVR"
    "Platforms/GoogleVR"
    "Platforms/OculusVR"
    "Platforms/OpenVR"
    "Platforms/LeapMotion"
    "Platforms/MagicLeap"
    "Platforms/WindowsMixedReality"
    
    # AR Plugins
    "Platforms/ARCore"
    "Platforms/ARKit"
    
    # Advanced Graphics/Animation
    "Importers/Alembic"
    "Animation/LiveLink"
    "Animation/MotionWarping"
    "Chaos/ChaosCloth"
    "Chaos/ChaosDestruction"
    "Chaos/ChaosNiagara"
    
    # Advanced Features
    "FX/Niagara"
    "Procedural/PCG"
    "AI/MassEntity"
    
    # Developer Tools
    "Editor/EditorScriptingUtilities"
    "Developer/ClassViewer"
    "Developer/DeveloperSettings"
)

# Function to safely remove plugin
remove_plugin() {
    local plugin_path="$PLUGINS_DIR/$1"
    if [ -d "$plugin_path" ]; then
        echo "Removing: $1"
        rm -rf "$plugin_path"
        echo "✓ Removed $1"
    else
        echo "⚠ Not found (optional): $1"
    fi
}

# Remove each plugin
for plugin in "${PLUGINS_TO_REMOVE[@]}"; do
    remove_plugin "$plugin"
done

# Create plugins config for Lite
cat > "$ENGINE_ROOT/Engine/Plugins/Lite/.gitkeep" << 'EOF'
# UE4 Lite Plugins Directory
# Contains only essential plugins for mobile
EOF

echo -e "\n\033[92m=== Plugin Removal Complete ==="
echo "Removed $(( ${#PLUGINS_TO_REMOVE[@]} )) plugin categories"
echo -e "\nNext: Run Setup.sh to regenerate project files\033[0m"

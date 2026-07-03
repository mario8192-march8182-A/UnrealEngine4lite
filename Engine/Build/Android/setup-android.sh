#!/bin/bash
# Setup script for Android build environment (UE4 Lite)
# Configures Android NDK, SDK, and build tools

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
ANDROID_NDK_VERSION="r19c"
ANDROID_SDK_VERSION="30"
GRADLE_VERSION="6.8"
MIN_API_LEVEL="21"
TARGET_API_LEVEL="30"

echo -e "${GREEN}=== Unreal Engine 4 Lite - Android Setup ===${NC}"

# Function to check if tool exists
check_tool() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}Error: $1 not found${NC}"
        return 1
    fi
    echo -e "${GREEN}✓ $1 found${NC}"
}

# Function to download and extract
download_and_extract() {
    local url=$1
    local dest=$2
    local name=$3
    
    if [ ! -d "$dest" ]; then
        echo -e "${YELLOW}Downloading $name...${NC}"
        mkdir -p "$dest"
        wget -q --show-progress "$url" -O /tmp/${name}.zip
        unzip -q /tmp/${name}.zip -d "$dest"
        rm /tmp/${name}.zip
        echo -e "${GREEN}✓ $name installed${NC}"
    else
        echo -e "${YELLOW}$name already exists, skipping...${NC}"
    fi
}

# Check Java
echo -e "${YELLOW}Checking prerequisites...${NC}"
check_tool "java" || exit 1
check_tool "git" || exit 1

# Set Android directories
ANDROID_HOME="${ANDROID_HOME:=$HOME/Android/Sdk}"
ANDROID_NDK_HOME="${ANDROID_NDK_HOME:=$ANDROID_HOME/ndk/$ANDROID_NDK_VERSION}"

echo -e "${YELLOW}Using Android SDK: $ANDROID_HOME${NC}"
echo -e "${YELLOW}Using Android NDK: $ANDROID_NDK_HOME${NC}"

# Create directories
mkdir -p "$ANDROID_HOME/ndk"
mkdir -p "$ANDROID_HOME/platforms"
mkdir -p "$ANDROID_HOME/build-tools"

# Download Android NDK (simplified - normally handled via SDK manager)
if [ ! -d "$ANDROID_NDK_HOME" ]; then
    echo -e "${YELLOW}Installing Android NDK $ANDROID_NDK_VERSION...${NC}"
    # Note: In production, use sdkmanager to download NDK
    echo -e "${YELLOW}Please install Android NDK manually or use Android Studio SDK Manager${NC}"
fi

# Create local.properties for Gradle
echo -e "${YELLOW}Creating local.properties...${NC}"
cat > ../local.properties << EOF
# Android SDK and NDK paths
sdk.dir=$ANDROID_HOME
ndk.dir=$ANDROID_NDK_HOME
ndk.version=$ANDROID_NDK_VERSION

# Gradle and build settings
gradle.version=$GRADLE_VERSION
android.useAndroidX=true
android.enableJetifier=true

# Unreal Engine 4 Lite settings
ue4.min.api=$MIN_API_LEVEL
ue4.target.api=$TARGET_API_LEVEL
ue4.lite.mode=true
ue4.optimize.shaders=true
ue4.optimize.textures=true
EOF

echo -e "${GREEN}✓ local.properties created${NC}"

# Create gradle.properties
cat > ../gradle.properties << EOF
# Gradle optimization for faster builds
org.gradle.parallel=true
org.gradle.workers.max=8
org.gradle.jvmargs=-Xmx4096m

# Android build optimization
android.enableR8=true
android.enableD8=true

# Unreal Engine 4 Lite optimizations
ue4.minify=true
ue4.strip.symbols=true
ue4.compress.apk=true
EOF

echo -e "${GREEN}✓ gradle.properties created${NC}"

# Verify setup
echo -e "${YELLOW}Verifying setup...${NC}"

if [ ! -d "$ANDROID_HOME" ]; then
    echo -e "${RED}Error: Android SDK not found at $ANDROID_HOME${NC}"
    exit 1
fi

if [ ! -d "$ANDROID_NDK_HOME" ]; then
    echo -e "${RED}Error: Android NDK not found at $ANDROID_NDK_HOME${NC}"
    echo -e "${YELLOW}Please install Android NDK $ANDROID_NDK_VERSION and try again${NC}"
    exit 1
fi

# Create environment script
cat > ../android-env.sh << EOF
#!/bin/bash
export ANDROID_HOME=$ANDROID_HOME
export ANDROID_NDK_HOME=$ANDROID_NDK_HOME
export PATH=\$PATH:\$ANDROID_HOME/tools:\$ANDROID_HOME/platform-tools
export PATH=\$PATH:\$ANDROID_NDK_HOME
EOF

chmod +x ../android-env.sh

echo -e "${GREEN}✓ Environment script created: android-env.sh${NC}"

# Summary
echo -e "${GREEN}"
echo "=== Setup Complete ==="
echo -e "${NC}"
echo "Next steps:"
echo "1. Source the environment: source android-env.sh"
echo "2. Run: ./build-apk.sh to build APK"
echo ""
echo "Configuration Summary:"
echo "  Android SDK: $ANDROID_HOME"
echo "  Android NDK: $ANDROID_NDK_HOME"
echo "  Min API: $MIN_API_LEVEL"
echo "  Target API: $TARGET_API_LEVEL"
echo ""


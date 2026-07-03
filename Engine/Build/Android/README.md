# Unreal Engine 4 Lite - Android Build System

## Quick Start

### 1. Setup Environment
```bash
cd Engine/Build/Android
chmod +x setup-android.sh
./setup-android.sh
```

### 2. Configure Build
```bash
cp local.properties.template local.properties
# Edit local.properties with your Android SDK/NDK paths
```

### 3. Build APK
```bash
chmod +x build-apk.sh
./build-apk.sh release arm64-v8a
```

### 4. Deploy to Device
```bash
adb install Build/Output/Android/app-release.apk
```

## Files Description

- **setup-android.sh**: Configure Android NDK, SDK, and Gradle
- **build-apk.sh**: Build optimized APK with Gradle
- **build.gradle**: Gradle build configuration
- **local.properties.template**: Template for local build configuration
- **proguard-rules.pro**: Code obfuscation and shrinking rules
- **AndroidEngine.ini**: Engine rendering configuration

## Build Options

### Debug Build
```bash
./build-apk.sh debug arm64-v8a
```

### Release Build (Optimized)
```bash
./build-apk.sh release arm64-v8a
```

### Universal APK (Multiple ABIs)
```bash
./build-apk.sh release universal
```

## Optimization Flags

- **Symbol Stripping**: Reduces APK size by removing debug symbols
- **R8 Code Shrinking**: Removes unused code and optimizes bytecode
- **Resource Compression**: Minimizes resource files
- **Asset Optimization**: Compresses textures and audio

## Troubleshooting

### NDK Not Found
```bash
export ANDROID_NDK_HOME=/path/to/ndk/r19c
```

### SDK Not Found
```bash
export ANDROID_HOME=/path/to/Android/Sdk
```

### Gradle Build Failed
- Check Java version: `java -version` (requires JDK 11+)
- Clean build: `./build-apk.sh release arm64-v8a --clean`
- Check logs: `cat build/outputs/logs/build.log`

## Performance Tips

1. Use ARMv8 (arm64-v8a) for better performance
2. Enable resource shrinking for smaller APK
3. Strip debug symbols in release builds
4. Use texture compression (ETC2/ASTC)
5. Optimize assets before building

## References

- [Android NDK Documentation](https://developer.android.com/ndk)
- [Gradle Build System](https://gradle.org/)
- [R8 Code Shrinking](https://developer.android.com/studio/build/shrink-code)

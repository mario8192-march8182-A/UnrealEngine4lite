# Unreal Engine 4 Lite - Complete Setup Checklist

## Pre-Build Checklist

### Environment Setup
- [ ] Java Development Kit (JDK 11+) installed
- [ ] Android SDK installed at proper location
- [ ] Android NDK (r19+) installed
- [ ] Git configured with proper credentials
- [ ] Sufficient disk space (50-100GB)

### Repository Setup
- [ ] Clone UnrealEngine4lite repository
- [ ] Checkout `android-lite-setup` branch
- [ ] Run `Setup.sh` to download binaries
- [ ] Generate project files

### Android Build Setup
- [ ] Navigate to `Engine/Build/Android`
- [ ] Run `./setup-android.sh`
- [ ] Configure `local.properties` with SDK/NDK paths
- [ ] Verify Android tools installed

## Optimization Steps

### Phase 1: Disable Heavy Shaders
- [ ] Run `./disable-expensive-shaders.sh`
- [ ] Verify shader definitions created
- [ ] Check compilation flags applied

### Phase 2: Remove Unnecessary Plugins
- [ ] Run `./remove-unnecessary-plugins.sh`
- [ ] Verify VR/AR plugins removed
- [ ] Check plugin list

### Phase 3: Configure Shader Compiler
- [ ] Run `python3 configure-shader-compiler.py <engine_root>`
- [ ] Verify mobile shader formats configured
- [ ] Check permutation reduction settings

### Phase 4: Optimize Assets
- [ ] Prepare asset directories (Textures, Meshes, Audio)
- [ ] Run `python3 Scripts/optimize-assets.py <source> <output>`
- [ ] Verify optimization report generated

### Phase 5: Build APK
- [ ] Source Android environment: `source Engine/Build/Android/android-env.sh`
- [ ] Run `./build-apk.sh release arm64-v8a`
- [ ] Verify APK generated in `Build/Output/Android/`
- [ ] Check APK size

## Testing

### Device Testing
- [ ] Deploy APK: `adb install app-release.apk`
- [ ] Test on Android 5.0+ device
- [ ] Check performance metrics
- [ ] Verify shader loading
- [ ] Test input/touch controls

### Performance Testing
- [ ] Use Android Profiler
- [ ] Monitor CPU usage
- [ ] Monitor GPU usage
- [ ] Monitor memory usage
- [ ] Check frame rate stability

### Compatibility Testing
- [ ] Test on various screen sizes
- [ ] Test on different GPU architectures
- [ ] Test on devices with 512MB-2GB RAM
- [ ] Test on Android 5.0 to 11.0

## Troubleshooting

### Build Issues
- [ ] Check Java version: `java -version`
- [ ] Verify Android SDK/NDK paths
- [ ] Check NDK API level compatibility
- [ ] Review Gradle build logs
- [ ] Validate ProGuard rules

### Runtime Issues
- [ ] Check logcat: `adb logcat | grep UE4`
- [ ] Verify shader compilation on device
- [ ] Check memory allocations
- [ ] Validate texture loading
- [ ] Test on multiple devices

### Performance Issues
- [ ] Profile GPU usage
- [ ] Check draw call count
- [ ] Verify LOD distances
- [ ] Optimize texture sizes
- [ ] Review shader complexity

## Deliverables

### Code
- [ ] Optimized shader library
- [ ] Mobile renderer configuration
- [ ] Simplified lighting system
- [ ] Asset optimization tools

### Build System
- [ ] Gradle build configuration
- [ ] Build scripts (setup, build, deploy)
- [ ] Configuration files (properties, INI)
- [ ] ProGuard rules

### Documentation
- [ ] Build guide
- [ ] Architecture overview
- [ ] Troubleshooting guide
- [ ] Performance optimization tips

### APK
- [ ] Optimized APK (target < 100MB)
- [ ] Debug APK for testing
- [ ] Build metadata and info

## Performance Targets

### APK Size
- Target: < 100MB (compressed)
- Limit: < 150MB (maximum)

### Runtime Performance
- Frame Rate: 30-60 FPS (stable)
- Memory: < 512MB (peak usage)
- Draw Calls: < 500 per frame
- Shader Complexity: Low (minimal instructions)

### Compilation Time
- Initial Build: < 60 minutes
- Incremental Build: < 15 minutes
- APK Size Target: < 30 minutes

## Next Steps

1. Complete environment setup
2. Clone and setup repository
3. Run Android build setup
4. Execute optimization phases
5. Build and test APK
6. Iterate on performance
7. Validate on multiple devices
8. Document results

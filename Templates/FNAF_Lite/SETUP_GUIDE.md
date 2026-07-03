# FNAF Lite - Unreal Engine 4 Lite Template Setup Guide

## 📋 Quick Setup

### Step 1: Clone and Setup

```bash
git clone -b android-lite-setup https://github.com/mario8192-march8182-A/UnrealEngine4lite.git
cd UnrealEngine4lite
./Setup.sh
./GenerateProjectFiles.sh
```

### Step 2: Create FNAF Project

```bash
mkdir -p Projects/FNAF_Lite
cp -r Templates/FNAF_Lite/* Projects/FNAF_Lite/
```

### Step 3: Setup Android Build

```bash
cd Engine/Build/Android
./setup-android.sh
cp local.properties.template local.properties
# Edit local.properties with your paths
```

### Step 4: Optimize and Build

```bash
# Disable expensive shaders
./disable-expensive-shaders.sh

# Remove unnecessary plugins
./remove-unnecessary-plugins.sh

# Configure shader compiler
python3 ../../Scripts/configure-shader-compiler.py ../../..

# Build APK
source android-env.sh
./build-apk.sh release arm64-v8a
```

### Step 5: Deploy and Test

```bash
adb install Build/Output/Android/app-release.apk
adb shell am start -n com.unrealengine.lite/.MainActivity
adb logcat | grep UE4
```

---

## 🎮 Gameplay Systems

### Night Structure
- Duration: 6 hours (12 AM - 6 AM)
- Speed: 1 real minute = 10 game minutes
- Nights: 1-5 (increasing difficulty)

### Power System
- Starting Power: 100%
- Camera Active: -0.5% per hour
- Door Closed: -1% per hour
- Light On: -0.5% per hour
- Game Over: Power = 0%

### Animatronics

| Animatronic | Aggression Night 1 | Speed | Behavior |
|-------------|-------------------|-------|----------|
| Freddy | 1/5 | Slow | Sleepy |
| Bonnie | 2/5 | Fast | Active |
| Chica | 1/5 | Medium | Timid |
| Foxy | 0/5 | Very Fast | Hidden |

---

## 📊 Performance Checklist

- [ ] APK size < 150MB
- [ ] FPS stable 30+
- [ ] Memory peak < 512MB
- [ ] Draw calls < 500/frame
- [ ] Shader compilation < 5 minutes
- [ ] Load time < 10 seconds

---

## 🐛 Common Issues

### APK Won't Install

```bash
adb shell getprop ro.build.version.sdk
adb install -r Build/Output/Android/app-release.apk
```

### Game Crashes on Startup

```bash
adb logcat | grep -E "FNAF|Crash|Error"
grep "Shader" Build/Logs/*.log
```

### Frame Rate Too Low

1. Reduce camera resolution
2. Lower animatronic LOD
3. Disable IR vision
4. Reduce draw distance

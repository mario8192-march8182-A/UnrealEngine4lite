#!/usr/bin/env python3
"""
FNAF Lite - Quick Setup Script for Android Build
Simplifies the entire setup process
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def print_step(step, desc):
    """Print step indicator"""
    print(f"  [{step}] {desc}")

def run_command(cmd, description):
    """Run a shell command"""
    print(f"  ▶ {description}...")
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"  ✓ {description} complete")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ {description} failed: {e}")
        return False

def setup_fnaf_build():
    """Setup FNAF Lite for Android build"""
    
    print_header("FNAF Lite - Android Build Setup")
    
    # Step 1: Verify prerequisites
    print_step("1/5", "Verifying prerequisites")
    
    if not run_command("java -version", "Checking Java"):
        print("  ✗ Java not found. Please install JDK 11+")
        return False
    
    if not run_command("git --version", "Checking Git"):
        print("  ✗ Git not found")
        return False
    
    # Step 2: Clone repository
    print_step("2/5", "Cloning UE4 Lite repository")
    
    if not run_command(
        "git clone -b android-lite-setup https://github.com/mario8192-march8182-A/UnrealEngine4lite.git",
        "Cloning repository"
    ):
        print("  Note: Repository may already exist")
    
    os.chdir("UnrealEngine4lite")
    
    # Step 3: Setup Android
    print_step("3/5", "Setting up Android NDK/SDK/Gradle")
    
    if not run_command(
        "cd Engine/Build/Android && ./setup-android.sh",
        "Android setup"
    ):
        print("  ✗ Android setup failed")
        return False
    
    # Step 4: Optimize engine
    print_step("4/5", "Optimizing UE4 Lite for mobile")
    
    if not run_command(
        "cd Engine/Build/Android && ./disable-expensive-shaders.sh",
        "Disabling expensive shaders"
    ):
        print("  ⚠ Shader optimization had issues")
    
    if not run_command(
        "cd Engine/Build/Android && ./remove-unnecessary-plugins.sh",
        "Removing unnecessary plugins"
    ):
        print("  ⚠ Plugin removal had issues")
    
    # Step 5: Build APK
    print_step("5/5", "Building APK")
    
    if not run_command(
        "cd Engine/Build/Android && source android-env.sh && ./build-apk.sh release arm64-v8a",
        "Building APK"
    ):
        print("  ✗ APK build failed")
        return False
    
    print_header("Setup Complete!")
    print("  ✓ APK ready: Build/Output/Android/app-release.apk\n")
    print("  Next steps:")
    print("    1. adb install Build/Output/Android/app-release.apk")
    print("    2. adb shell am start -n com.unrealengine.lite/.MainActivity")
    print("    3. adb logcat | grep UE4\n")
    
    return True

if __name__ == "__main__":
    try:
        if setup_fnaf_build():
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n  ✗ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n  ✗ Unexpected error: {e}")
        sys.exit(1)

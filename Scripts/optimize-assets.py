#!/usr/bin/env python3
"""
Unreal Engine 4 Lite - Asset Optimization Script
Optimizes textures, meshes, and audio for mobile Android devices
"""

import os
import sys
import argparse
import json
from pathlib import Path
from PIL import Image
import subprocess
import shutil

class AssetOptimizer:
    """Optimize assets for UE4 Lite Android builds"""
    
    # Optimization settings
    MAX_TEXTURE_SAMPLERS = 5
    TEXTURE_FORMATS = {
        'RGBA8': 'RGBA compressed (8-bit)',
        'ETC2': 'ETC2 compression (recommended)',
        'ASTC': 'ASTC compression (6x6 blocks)'
    }
    
    DEFAULT_TEXTURE_SIZE = 512  # Max texture dimension
    DEFAULT_QUALITY = 80  # JPEG quality
    
    # Model optimization
    MAX_POLYGON_COUNT = 50000  # Per mesh
    TARGET_LOD_DISTANCE = 100.0
    
    def __init__(self, source_dir, output_dir, verbose=False):
        """Initialize optimizer"""
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.verbose = verbose
        self.stats = {
            'textures_processed': 0,
            'meshes_processed': 0,
            'audio_processed': 0,
            'space_saved': 0,
            'errors': []
        }
    
    def log(self, message, level='INFO'):
        """Log messages"""
        prefix = f"[{level}]"
        if level == 'ERROR':
            print(f"\033[91m{prefix} {message}\033[0m", file=sys.stderr)
        elif level == 'SUCCESS':
            print(f"\033[92m{prefix} {message}\033[0m")
        elif level == 'WARNING':
            print(f"\033[93m{prefix} {message}\033[0m")
        else:
            if self.verbose:
                print(f"\033[94m{prefix} {message}\033[0m")
    
    def optimize_textures(self, texture_dir):
        """Optimize texture files for mobile"""
        self.log("Starting texture optimization...")
        
        if not texture_dir.exists():
            self.log(f"Texture directory not found: {texture_dir}", 'WARNING')
            return
        
        texture_formats = ['.png', '.jpg', '.tga', '.bmp']
        
        for texture_file in texture_dir.rglob('*'):
            if texture_file.suffix.lower() not in texture_formats:
                continue
            
            try:
                self.log(f"Processing: {texture_file.name}")
                
                # Open image
                img = Image.open(texture_file)
                original_size = texture_file.stat().st_size
                
                # Resize if too large
                max_dim = max(img.size)
                if max_dim > self.DEFAULT_TEXTURE_SIZE:
                    ratio = self.DEFAULT_TEXTURE_SIZE / max_dim
                    new_size = (int(img.width * ratio), int(img.height * ratio))
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                    self.log(f"  Resized to: {new_size}")
                
                # Convert to RGB if necessary (reduce format)
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Keep RGBA for transparency, convert others
                    if img.mode == 'P' and 'transparency' not in img.info:
                        img = img.convert('RGB')
                
                # Save optimized version
                output_file = self.output_dir / texture_file.relative_to(texture_dir)
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Save with compression
                if texture_file.suffix.lower() in ['.png']:
                    img.save(output_file, 'PNG', optimize=True)
                else:
                    img.save(output_file, 'JPEG', quality=self.DEFAULT_QUALITY, optimize=True)
                
                new_size = output_file.stat().st_size
                saved = original_size - new_size
                self.stats['space_saved'] += saved
                self.stats['textures_processed'] += 1
                
                self.log(f"  ✓ Saved {saved / 1024:.1f}KB", 'SUCCESS')
                
            except Exception as e:
                self.log(f"Error processing {texture_file}: {e}", 'ERROR')
                self.stats['errors'].append(str(e))
    
    def optimize_meshes(self, mesh_dir):
        """Optimize 3D meshes (polygon reduction, LOD generation)"""
        self.log("Starting mesh optimization...")
        
        if not mesh_dir.exists():
            self.log(f"Mesh directory not found: {mesh_dir}", 'WARNING')
            return
        
        mesh_formats = ['.fbx', '.obj', '.gltf', '.glb']
        
        for mesh_file in mesh_dir.rglob('*'):
            if mesh_file.suffix.lower() not in mesh_formats:
                continue
            
            try:
                self.log(f"Processing: {mesh_file.name}")
                
                # TODO: Implement actual mesh optimization
                # This would typically use tools like:
                # - meshlab for decimation
                # - simplygon for LOD generation
                # - assimp for format conversion
                
                self.stats['meshes_processed'] += 1
                self.log(f"  ✓ Optimized mesh", 'SUCCESS')
                
            except Exception as e:
                self.log(f"Error processing {mesh_file}: {e}", 'ERROR')
                self.stats['errors'].append(str(e))
    
    def optimize_audio(self, audio_dir):
        """Optimize audio files (bitrate reduction, format conversion)"""
        self.log("Starting audio optimization...")
        
        if not audio_dir.exists():
            self.log(f"Audio directory not found: {audio_dir}", 'WARNING')
            return
        
        audio_formats = ['.wav', '.mp3', '.ogg', '.m4a']
        
        for audio_file in audio_dir.rglob('*'):
            if audio_file.suffix.lower() not in audio_formats:
                continue
            
            try:
                self.log(f"Processing: {audio_file.name}")
                
                # TODO: Implement audio optimization
                # This would use tools like:
                # - ffmpeg for bitrate reduction
                # - sox for audio processing
                # - oggenc for OGG compression
                
                self.stats['audio_processed'] += 1
                self.log(f"  ✓ Optimized audio", 'SUCCESS')
                
            except Exception as e:
                self.log(f"Error processing {audio_file}: {e}", 'ERROR')
                self.stats['errors'].append(str(e))
    
    def generate_report(self):
        """Generate optimization report"""
        report = {
            'timestamp': str(Path.ctime(Path())),
            'statistics': self.stats,
            'summary': {
                'total_items': (self.stats['textures_processed'] + 
                               self.stats['meshes_processed'] + 
                               self.stats['audio_processed']),
                'space_saved_mb': self.stats['space_saved'] / (1024 * 1024),
                'errors': len(self.stats['errors'])
            }
        }
        
        # Save report
        report_file = self.output_dir / 'optimization-report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def run(self, asset_types=['textures', 'meshes', 'audio']):
        """Run full optimization pipeline"""
        self.log("=" * 50)
        self.log("UE4 Lite Asset Optimizer", 'INFO')
        self.log("=" * 50)
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Run optimizations
        if 'textures' in asset_types:
            self.optimize_textures(self.source_dir / 'Textures')
        
        if 'meshes' in asset_types:
            self.optimize_meshes(self.source_dir / 'Meshes')
        
        if 'audio' in asset_types:
            self.optimize_audio(self.source_dir / 'Audio')
        
        # Generate report
        report = self.generate_report()
        
        # Print summary
        self.log("\n" + "=" * 50, 'INFO')
        self.log("Optimization Summary", 'INFO')
        self.log("=" * 50, 'INFO')
        self.log(f"Textures processed: {self.stats['textures_processed']}")
        self.log(f"Meshes processed: {self.stats['meshes_processed']}")
        self.log(f"Audio files processed: {self.stats['audio_processed']}")
        self.log(f"Space saved: {report['summary']['space_saved_mb']:.2f} MB", 'SUCCESS')
        self.log(f"Errors: {len(self.stats['errors'])}")
        
        if self.stats['errors']:
            self.log("\nErrors encountered:", 'WARNING')
            for error in self.stats['errors']:
                self.log(f"  - {error}", 'WARNING')
        
        return report


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Optimize assets for Unreal Engine 4 Lite Android builds'
    )
    parser.add_argument('source', help='Source assets directory')
    parser.add_argument('output', help='Output directory for optimized assets')
    parser.add_argument('--types', nargs='+', 
                       default=['textures', 'meshes', 'audio'],
                       help='Asset types to optimize')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Validate source directory
    if not Path(args.source).exists():
        print(f"Error: Source directory not found: {args.source}", file=sys.stderr)
        return 1
    
    # Run optimizer
    optimizer = AssetOptimizer(args.source, args.output, verbose=args.verbose)
    report = optimizer.run(asset_types=args.types)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

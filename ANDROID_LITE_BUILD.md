# Unreal Engine 4 Lite - Android Build Guide

## Objetivo
Criar uma versão "Lite" da Unreal Engine 4 otimizada para compilação e execução em dispositivos Android de entrada.

## Arquitetura do Projeto

### 1. Requisitos de Sistema
- **Plataforma de Build**: Windows 10/11 ou Linux
- **Android NDK**: r19 ou superior
- **Android SDK**: API Level 21+ (Android 5.0)
- **Java Development Kit**: JDK 11+
- **Gradle**: 6.0+
- **Espaço em Disco**: 50-100GB (engine + build artifacts)

### 2. Estrutura de Diretórios

```
UnrealEngine4lite/
├── Engine/
│   ├── Shaders/              # Shaders otimizados
│   ├── Plugins/              # Plugins selecionados (sem VR/AR)
│   ├── Build/
│   │   └── Android/          # Scripts de build Android
│   └── Source/               # Código fonte otimizado
├── Build/
│   ├── build.gradle          # Gradle principal
│   └── local.properties      # Config Android NDK/SDK
├── Scripts/
│   ├── setup-android.sh      # Setup Android
│   ├── build-apk.sh          # Build APK
│   └── optimize-assets.py    # Otimização de assets
└── ANDROID_LITE_BUILD.md     # Este arquivo
```

## Fases de Implementação

### Fase 1: Configuração do Build System (NDK/SDK/Gradle)
**Arquivos a criar:**
- `Engine/Build/Android/setup-android.sh`
- `Engine/Build/Android/build.gradle`
- `Engine/Build/Android/local.properties.template`

### Fase 2: Remoção de Shaders Pesados
**Alvos:**
- Atmospheric Fog
- Sky Atmosphere
- Whole Scene Shadows
- Stationary Skylight

**Arquivos a modificar:**
- `Engine/Shaders/Common/` - Remover includes pesados
- `Engine/Source/Runtime/Renderer/` - Desabilitar passes caros

### Fase 3: Simplificação do Renderer
**Estratégias:**
- Usar apenas shaders Unlit (sem lighting computado)
- Implementar Low Poly rendering (LOD reduzido)
- Suporte básico 2D com Canvas

**Arquivos a criar:**
- `Engine/Shaders/Private/MobileLiteShaders.usf`
- `Engine/Source/Runtime/Renderer/Private/MobileLiteRenderer.cpp`

### Fase 4: Otimização de Assets
**Metas:**
- Texture Packing (máx 5 samplers)
- Compressão ETC2/ASTC
- Redução de modelos 3D (polygon decimation)

**Arquivos a criar:**
- `Scripts/optimize-assets.py`
- `Engine/Build/Android/asset-optimization.cfg`

### Fase 5: Scripts de Build Automático
**Arquivos a criar:**
- `build-apk.sh` / `build-apk.bat`
- `ci-android.yml` (GitHub Actions)

### Fase 6: Testes e Validação
**Plataformas alvo:**
- Dispositivos Android 5.0+ com RAM 512MB-2GB
- Resoluções: 720p a 1080p

---

## Próximas Tarefas
1. ✅ Criar branch `android-lite-setup`
2. ⏳ Configurar scripts de setup Android
3. ⏳ Implementar build system Gradle
4. ⏳ Remover shaders pesados
5. ⏳ Simplificar renderer
6. ⏳ Otimizar assets
7. ⏳ Criar scripts de build APK
8. ⏳ Testar em dispositivos reais


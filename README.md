# Unreal Engine 4 Lite - Android Build System

## 📱 Visão Geral

Este repositório contém uma versão otimizada da Unreal Engine 4 especificamente configurada para compilar e executar em dispositivos Android de entrada (512MB-2GB RAM).

### ✨ Características Principais

- **Build System Android**: Scripts completos para NDK, SDK e Gradle
- **Shaders Otimizados**: Apenas shaders essenciais (Unlit, Low Poly, 2D)
- **Renderer Simplificado**: Forward rendering sem efeitos caros
- **Otimização de Assets**: Compressão de texturas e áudio
- **APK Leve**: Alvo < 100MB (compressed)
- **Plugins Reduzidos**: Remove VR/AR e sistemas complexos

---

## 🚀 Quick Start

### 1. Clonar e Setup Inicial

```bash
# Clone o repositório
git clone https://github.com/mario8192-march8182-A/UnrealEngine4lite.git
cd UnrealEngine4lite

# Checkout na branch de desenvolvimento
git checkout android-lite-setup

# Download binários
./Setup.sh

# Gerar arquivos de projeto
./GenerateProjectFiles.sh
```

### 2. Configurar Android Build

```bash
cd Engine/Build/Android
chmod +x *.sh

# Setup Android NDK/SDK/Gradle
./setup-android.sh

# Configurar local.properties
cp local.properties.template local.properties
# Editar local.properties com seus caminhos
```

### 3. Otimizar Engine

```bash
# Desabilitar shaders pesados
./disable-expensive-shaders.sh

# Remover plugins desnecessários
./remove-unnecessary-plugins.sh

# Configurar compilação de shaders
python3 ../../Scripts/configure-shader-compiler.py ../../..
```

### 4. Otimizar Assets

```bash
# Otimizar texturas, meshes e áudio
python3 Scripts/optimize-assets.py <source_dir> <output_dir>
```

### 5. Build APK

```bash
# Source do ambiente
source Engine/Build/Android/android-env.sh

# Build release APK
Engine/Build/Android/build-apk.sh release arm64-v8a

# APK gerado em: Build/Output/Android/
```

### 6. Deploy e Teste

```bash
# Instalar no dispositivo
adb install Build/Output/Android/app-release.apk

# Executar
adb shell am start -n com.unrealengine.lite/.MainActivity

# Ver logs
adb logcat | grep UE4
```

---

## 📁 Estrutura de Arquivos

```
UnrealEngine4lite/
├── ANDROID_LITE_BUILD.md           # Guia de arquitetura e fases
├── SETUP_CHECKLIST.md              # Checklist completo de setup
├── README.md                        # Este arquivo
│
├── Engine/
│   ├── Build/Android/
│   │   ├── setup-android.sh         # Setup NDK/SDK/Gradle
│   │   ├── build-apk.sh             # Script de build APK
│   │   ├── build.gradle             # Configuração Gradle
│   │   ├── local.properties.template # Template de config
│   │   ├── proguard-rules.pro       # Regras de obfuscação
│   │   ├── AndroidEngine.ini        # Configuração de renderer
│   │   ├── disable-expensive-shaders.sh
│   │   ├── remove-unnecessary-plugins.sh
│   │   └── README.md                # Docs build system
│   │
│   ├── Config/Android/
│   │   ├── AndroidEngine.ini        # Configuração engine
│   │   ├── ShaderCompilerConfig.json
│   │   └── PermutationReduction.json
│   │
│   └── Shaders/
│       ├── Private/
│       │   └── MobileLiteShaders.usf # Shaders otimizados
│       └── Definitions/
│           ├── LiteMobileShaders.h
│           └── LiteCompilationRules.ush
│
├── Scripts/
│   ├── optimize-assets.py           # Otimizador de assets
│   └── configure-shader-compiler.py # Configurador de shaders
│
└── Build/Output/Android/
    └── (APKs gerados aqui)
```

---

## 🛠️ Componentes Principais

### 1. **Build System** (`Engine/Build/Android/`)

**Arquivos:**
- `setup-android.sh`: Configura NDK, SDK, Gradle
- `build-apk.sh`: Compila APK otimizado
- `build.gradle`: Configuração Gradle com otimizações
- `proguard-rules.pro`: Obfuscação e shrinking de código

**Características:**
- Suporte a arm64-v8a e armeabi-v7a
- R8 code shrinking automático
- Compressão de recursos
- Symbol stripping

### 2. **Shaders Otimizados** (`Engine/Shaders/`)

**Arquivo Principal:** `MobileLiteShaders.usf`

**Shaders Inclusos:**
- `LiteUnlitShader`: Sem cálculos de lighting
- `LiteLowPolyShader`: Lighting simples (1 luz direcional)
- `Lite2DCanvasShader`: Para UI e elementos 2D

**Otimizações:**
- Máximo 5 samplers de textura
- Texture packing (Normal + ARM em canais)
- Early Z-pass habilitado
- Forward rendering apenas

### 3. **Configuração de Renderer** (`Engine/Config/Android/`)

**AndroidEngine.ini:**
- Rendering settings móvel
- Desabilita: atmospheric fog, sky atmosphere, shadows globais
- Enable: forward rendering, early Z-pass
- Limita shadow resolution a 512x512

### 4. **Asset Optimization** (`Scripts/optimize-assets.py`)

**Funcionalidades:**
- Redimensiona texturas para máximo 512x512
- Compressão PNG/JPEG com qualidade otimizada
- Suporte para meshes e áudio (framework)
- Relatório de espaço economizado

---

## 📊 Performance Targets

### APK Size
```
├── Ideal:   < 80MB (compressed)
├── Target:  < 100MB (compressed)
└── Max:     < 150MB (compressed)
```

### Runtime Performance
```
├── FPS:           30-60 (stable)
├── Memory Peak:   < 512MB
├── Draw Calls:    < 500/frame
└── Shader Cost:   Low (minimal instructions)
```

### Device Support
```
├── Min API:       21 (Android 5.0)
├── Target API:    30 (Android 11)
├── Min RAM:       512MB
└── Tested RAM:    2GB+
```

---

## 🔧 Configuração Avançada

### Customizar Shaders

Editar `Engine/Shaders/Private/MobileLiteShaders.usf`:

```glsl
// Adicione novos shaders otimizados
void CustomLiteShader(/* params */) {
    // Implementação
}
```

### Ajustar Qualidade de Renderização

Modificar `Engine/Config/Android/AndroidEngine.ini`:

```ini
[/Script/Engine.RendererSettings]
r.MaxAnisotropy=2              ; Aumentar para qualidade
r.Shadow.MaxResolution=512     ; Aumentar resolução de sombras
r.MobileHDR=False              ; Manter False para performance
```

### Configurar Assets

Editar `Scripts/optimize-assets.py`:

```python
DEFAULT_TEXTURE_SIZE = 512  # Aumentar resolução
DEFAULT_QUALITY = 80        # Aumentar qualidade JPEG
MAX_POLYGON_COUNT = 50000   # Aumentar complexidade de meshes
```

---

## 🐛 Troubleshooting

### Erro: "NDK not found"

```bash
export ANDROID_NDK_HOME=/path/to/ndk/r19c
./Engine/Build/Android/setup-android.sh
```

### Erro: "Gradle build failed"

```bash
# Verificar Java version
java -version  # Deve ser 11+

# Limpar e rebuild
cd Engine/Build/Android
./gradlew clean
./build-apk.sh release arm64-v8a
```

### Erro: "Shader compilation failed"

```bash
# Reconfigurar shader compiler
python3 Scripts/configure-shader-compiler.py $(pwd)

# Regenerar project files
./GenerateProjectFiles.sh
```

### Device: "App crashes on startup"

```bash
# Ver logs detalhados
adb logcat | grep -i ue4
adb logcat | grep -i error

# Testar com debug APK
./Engine/Build/Android/build-apk.sh debug arm64-v8a
```

---

## 📚 Documentação Adicional

- **[ANDROID_LITE_BUILD.md](ANDROID_LITE_BUILD.md)**: Arquitetura e fases de implementação
- **[SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)**: Checklist completo de setup
- **[Engine/Build/Android/README.md](Engine/Build/Android/README.md)**: Build system específico

---

## 📋 Roadmap

### Fase 1: Build System ✅
- [x] Scripts Android NDK/SDK/Gradle
- [x] Configuração Gradle
- [x] Build APK script

### Fase 2: Otimização de Shaders ✅
- [x] Desabilitar atmospheric fog, sky atmosphere
- [x] Desabilitar whole scene shadows, stationary skylight
- [x] Criar shaders móvel otimizados

### Fase 3: Simplificação de Renderer ✅
- [x] Configuração de renderer móvel
- [x] Forward rendering apenas
- [x] Limitar texture samplers a 5

### Fase 4: Otimização de Assets ✅
- [x] Script de otimização de assets
- [x] Compressão de texturas
- [x] Relatório de otimização

### Fase 5: Testes 🔄
- [ ] Teste em Android 5.0-11.0
- [ ] Validação de performance
- [ ] Teste em múltiplos dispositivos

### Fase 6: Documentação 🔄
- [x] Guia de build
- [x] Arquitetura do projeto
- [x] Checklist de setup
- [ ] Guia de troubleshooting avançado

---

## 🤝 Contribuindo

Pull requests são bem-vindos! Por favor:

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/melhoria`)
3. Commit suas mudanças (`git commit -am 'Add melhoria'`)
4. Push para a branch (`git push origin feature/melhoria`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto segue a licença da Unreal Engine (EULA). Veja LICENSE para detalhes.

---

## 📞 Suporte

- **Issues**: Use GitHub Issues para reportar bugs
- **Discussões**: Use GitHub Discussions para perguntas
- **Documentação**: Veja os arquivos .md neste repositório

---

## 🎯 Status do Projeto

**Branch**: `android-lite-setup`  
**Status**: Em Desenvolvimento Ativo  
**Última Atualização**: 2026-07-03  

```
[████████████████████████████░░] 90% Completo

✅ Build System completo
✅ Shaders otimizados
✅ Renderer simplificado
✅ Asset optimization
⏳ Testes em dispositivos reais
```

---

**Desenvolvido por**: UE4 Lite Team  
**Baseado em**: Unreal Engine 4.22  
**Alvo**: Android 5.0+ (API 21+)  

# Five Nights at Freddy's (FNAF) - Unreal Engine 4 Lite Template

## 🎮 Overview

Template otimizado de FNAF para UE4 Lite Android com foco em performance em dispositivos de entrada.

### Características

- **Gameplay Loop**: 5 noites, 6 horas por noite
- **Câmeras de Segurança**: Sistema low-poly de múltiplas câmeras
- **Inimigos Animatrônicos**: AI simplificado com pathfinding básico
- **Sistema de Energia**: Gerenciamento de recursos
- **UI Mobile**: Interface otimizada para touch
- **Audio**: Sistema de som ambiente e alertas
- **Assets**: Modelos e texturas comprimidos

---

## 📁 Estrutura de Projeto

```
Projects/FNAF_Lite/
├── Content/
│   ├── Characters/           # Animatrônicos e personagens
│   │   ├── Freddy/
│   │   ├── Bonnie/
│   │   ├── Chica/
│   │   └── Foxy/
├── Environments/         # Cenários (Office, Hallways)
│   │   ├── MainOffice/
│   │   └── Hallways/
├── Cameras/              # Sistema de câmeras
├── UI/                   # Interface do jogo
├── Audio/                # Sons e música
└── Materials/            # Shaders otimizados
```

---

## 🎯 Sistemas Principais

### 1. Game Manager
- Controla fase do jogo (menu, night active, game over)
- Gerencia tempo (6 horas por noite)
- Rastreia progresso

### 2. Sistema de Câmeras
- 12 câmeras de segurança estáticas
- Interface low-poly para visualização
- Switch entre câmeras via UI

### 3. AI dos Animatrônicos
- Pathfinding simplificado
- Estados (ativo, dormindo, atacando)
- Detecção de portas fechadas

### 4. Sistema de Energia
- Energia máxima: 100%
- Consumo por câmera ativa, luz, porta
- Game over quando energia = 0%

### 5. UI Mobile
- Botões grandes para touch
- Câmeras em grid (3x4)
- Indicador de energia e hora
- Status de portas/luzes

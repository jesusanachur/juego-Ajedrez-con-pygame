# ♟️ Juego de Ajedrez con Pygame  

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Pygame](https://img.shields.io/badge/Pygame-2.0+-green) ![Licencia](https://img.shields.io/badge/Licencia-MIT-orange)  

Un juego de ajedrez completo implementado en Python usando la biblioteca Pygame, con interfaz gráfica y reglas básicas.  

![Captura del Juego](screenshot.png) *(Reemplaza con tu propia imagen)*  

## 🚀 Características  
- ✅ Movimientos válidos para todas las piezas  
- ✅ Turnos alternados (blancas/negras)  
- ✅ Detección de capturas  
- ✅ Tablero interactivo con selección visual  
- ❌ *Próximamente*: Enroque, jaque mate y promoción de peones  

## 🛠️ Estructura del Código  
```plaintext
/ajedrez_pygame  
│── /assets                # Imágenes/sonidos (opcional)  
│── main.py                # Lógica principal del juego  
│── piezas.py              # Clases para cada pieza  
│── README.md              # Este archivo  
│── requirements.txt       # Dependencias




👨‍💻 Instalación
git clone https://github.com/tu-usuario/ajedrez-pygame.git
Instala dependencias:
pip install -r requirements.txt
Ejecuta el juego:
python main.py

🎮 Cómo Jugar
Acción	Descripción
Click izquierdo	Selecciona una pieza de tu color
Click derecho	Mueve la pieza a la casilla destino
Turnos	Alterna automáticamente
📌 Reglas Implementadas
Pieza	Movimientos Válidos
Peón	Avance recto (captura diagonal)
Torre	Horizontal/vertical sin saltos
Caballo	Movimiento en "L"
Alfil	Diagonal sin saltos
Reina	Combinación de torre y alfil
Rey	1 casilla en cualquier dirección
🧩 Lógica Clave (Fragmento)

def mover_peon(tablero, inicio, fin, turno_blancas):
    # Lógica de movimiento para peones
    direccion = -1 if turno_blancas else 1
    if inicio[1] == fin[1]:  # Movimiento recto
        if tablero[fin[0]][fin[1]] == '..':
            return True
    elif abs(inicio[1] - fin[1]) == 1:  # Captura diagonal
        if tablero[fin[0]][fin[1]] != '..':
            return True
    return False

📅 Roadmap
Implementar enroque

Añadir imágenes para piezas

Detectar jaque mate


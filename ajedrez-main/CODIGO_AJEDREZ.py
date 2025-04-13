import pygame
import sys

# Inicializar pygame
pygame.init()

# Configuración del tablero
TAMANO_CASILLA = 80
MARGEN = 50
ANCHO = 8 * TAMANO_CASILLA + 2 * MARGEN
ALTO = 8 * TAMANO_CASILLA + 2 * MARGEN

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
MARRON_CLARO = (222, 184, 135)
MARRON_OSCURO = (139, 69, 19)
AZUL_SELECCION = (100, 149, 237, 150)
ROJO = (255, 0, 0)

# Configuración de la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ajedrez con Pygame")
reloj = pygame.time.Clock()

# Fuente para las letras y números
fuente = pygame.font.SysFont('Arial', 20)

# Tablero inicial
tablero = [
    ['to', 'ca', 'al', 'qu', 'ki', 'al', 'ca', 'to'],
    ['pe', 'pe', 'pe', 'pe', 'pe', 'pe', 'pe', 'pe'],
    ['..', '..', '..', '..', '..', '..', '..', '..'],
    ['..', '..', '..', '..', '..', '..', '..', '..'],
    ['..', '..', '..', '..', '..', '..', '..', '..'],
    ['..', '..', '..', '..', '..', '..', '..', '..'],
    ['PE', 'PE', 'PE', 'PE', 'PE', 'PE', 'PE', 'PE'],
    ['TO', 'CA', 'AL', 'QU', 'KI', 'AL', 'CA', 'TO']
]

# Cargar imágenes de las piezas (simuladas con texto en este ejemplo)
def cargar_imagenes():
    imagenes = {}
    piezas = ['pe', 'PE', 'al', 'AL', 'ca', 'CA', 'to', 'TO', 'qu', 'QU', 'ki', 'KI']
    
    for pieza in piezas:
        # En una implementación real, cargarías imágenes desde archivos
        # Aquí usamos texto como placeholder
        imagenes[pieza] = pieza.upper() if pieza.islower() else pieza.lower()
    
    return imagenes

imagenes_piezas = cargar_imagenes()
seleccionado = None
turno = 'blancas'  # Las blancas comienzan

def dibujar_tablero():
    # Dibujar el fondo
    pantalla.fill(MARRON_CLARO)
    
    # Dibujar las letras y números de las coordenadas
    letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    numeros = ['1', '2', '3', '4', '5', '6', '7', '8']
    
    for i, letra in enumerate(letras):
        texto = fuente.render(letra, True, NEGRO)
        pantalla.blit(texto, (MARGEN + i * TAMANO_CASILLA + TAMANO_CASILLA // 2 - 10, MARGEN // 2))
        pantalla.blit(texto, (MARGEN + i * TAMANO_CASILLA + TAMANO_CASILLA // 2 - 10, ALTO - MARGEN // 2))
    
    for i, numero in enumerate(numeros):
        texto = fuente.render(numero, True, NEGRO)
        pantalla.blit(texto, (MARGEN // 2 - 10, MARGEN + i * TAMANO_CASILLA + TAMANO_CASILLA // 2))
        pantalla.blit(texto, (ANCHO - MARGEN // 2 - 10, MARGEN + i * TAMANO_CASILLA + TAMANO_CASILLA // 2))
    
    # Dibujar las casillas del tablero
    for fila in range(8):
        for columna in range(8):
            color = MARRON_CLARO if (fila + columna) % 2 == 0 else MARRON_OSCURO
            pygame.draw.rect(pantalla, color, 
                            (MARGEN + columna * TAMANO_CASILLA, 
                             MARGEN + fila * TAMANO_CASILLA, 
                             TAMANO_CASILLA, TAMANO_CASILLA))
            
            # Resaltar casilla seleccionada
            if seleccionado and seleccionado == (fila, columna):
                s = pygame.Surface((TAMANO_CASILLA, TAMANO_CASILLA), pygame.SRCALPHA)
                s.fill((100, 149, 237, 150))
                pantalla.blit(s, (MARGEN + columna * TAMANO_CASILLA, MARGEN + fila * TAMANO_CASILLA))
            
            # Dibujar las piezas
            pieza = tablero[fila][columna]
            if pieza != '..':
                # En una implementación real, dibujarías la imagen de la pieza
                # Aquí usamos texto como placeholder
                color_texto = BLANCO if pieza.isupper() else NEGRO
                texto = fuente.render(imagenes_piezas[pieza], True, color_texto)
                pantalla.blit(texto, 
                             (MARGEN + columna * TAMANO_CASILLA + TAMANO_CASILLA // 2 - 10, 
                              MARGEN + fila * TAMANO_CASILLA + TAMANO_CASILLA // 2 - 10))
    
    # Mostrar de quién es el turno
    texto_turno = fuente.render(f"Turno: {'Blancas' if turno == 'blancas' else 'Negras'}", True, NEGRO)
    pantalla.blit(texto_turno, (ANCHO // 2 - 50, 20))

def obtener_casilla_desde_posicion(pos):
    x, y = pos
    if (MARGEN <= x < ANCHO - MARGEN) and (MARGEN <= y < ALTO - MARGEN):
        fila = (y - MARGEN) // TAMANO_CASILLA
        columna = (x - MARGEN) // TAMANO_CASILLA
        return fila, columna
    return None

def mover_peon(tab, fila, columna, fila_final, columna_final):
    pieza = tab[fila][columna]
    destino = tab[fila_final][columna_final]
    
    # Peones blancos (minúsculas) se mueven hacia arriba (disminuye fila)
    if pieza == 'pe':
        # Movimiento hacia adelante
        if columna == columna_final and destino == '..':
            if fila - 1 == fila_final or (fila == 6 and fila - 2 == fila_final and tab[fila-1][columna] == '..'):
                tab[fila_final][columna_final] = pieza
                tab[fila][columna] = '..'
                return True
        # Captura en diagonal
        elif abs(columna - columna_final) == 1 and fila - 1 == fila_final and destino.isupper():
            tab[fila_final][columna_final] = pieza
            tab[fila][columna] = '..'
            return True
    
    # Peones negros (mayúsculas) se mueven hacia abajo (aumenta fila)
    elif pieza == 'PE':
        # Movimiento hacia adelante
        if columna == columna_final and destino == '..':
            if fila + 1 == fila_final or (fila == 1 and fila + 2 == fila_final and tab[fila+1][columna] == '..'):
                tab[fila_final][columna_final] = pieza
                tab[fila][columna] = '..'
                return True
        # Captura en diagonal
        elif abs(columna - columna_final) == 1 and fila + 1 == fila_final and destino.islower():
            tab[fila_final][columna_final] = pieza
            tab[fila][columna] = '..'
            return True
    
    return False

def mover_caballo(tab, fila, columna, fila_final, columna_final):
    pieza = tab[fila][columna]
    destino = tab[fila_final][columna_final]
    
    # Verificar movimiento en L
    if (abs(fila - fila_final) == 2 and abs(columna - columna_final) == 1) or \
       (abs(fila - fila_final) == 1 and abs(columna - columna_final) == 2):
        
        # Verificar que no se capture una pieza del mismo color
        if (pieza.islower() and destino.islower()) or (pieza.isupper() and destino.isupper()):
            return False
        
        tab[fila_final][columna_final] = pieza
        tab[fila][columna] = '..'
        return True
    
    return False

def mover_alfil(tab, fila, columna, fila_final, columna_final):
    pieza = tab[fila][columna]
    destino = tab[fila_final][columna_final]
    
    # Verificar movimiento diagonal
    if abs(fila - fila_final) != abs(columna - columna_final):
        return False
    
    # Verificar que no se capture una pieza del mismo color
    if (pieza.islower() and destino.islower()) or (pieza.isupper() and destino.isupper()):
        return False
    
    # Verificar que no hay piezas en el camino
    paso_fila = 1 if fila_final > fila else -1
    paso_columna = 1 if columna_final > columna else -1
    
    f, c = fila + paso_fila, columna + paso_columna
    while f != fila_final and c != columna_final:
        if tab[f][c] != '..':
            return False
        f += paso_fila
        c += paso_columna
    
    tab[fila_final][columna_final] = pieza
    tab[fila][columna] = '..'
    return True

def mover_torre(tab, fila, columna, fila_final, columna_final):
    pieza = tab[fila][columna]
    destino = tab[fila_final][columna_final]
    
    # Verificar movimiento recto
    if fila != fila_final and columna != columna_final:
        return False
    
    # Verificar que no se capture una pieza del mismo color
    if (pieza.islower() and destino.islower()) or (pieza.isupper() and destino.isupper()):
        return False
    
    # Verificar que no hay piezas en el camino
    if fila == fila_final:  # Movimiento horizontal
        paso = 1 if columna_final > columna else -1
        for c in range(columna + paso, columna_final, paso):
            if tab[fila][c] != '..':
                return False
    else:  # Movimiento vertical
        paso = 1 if fila_final > fila else -1
        for f in range(fila + paso, fila_final, paso):
            if tab[f][columna] != '..':
                return False
    
    tab[fila_final][columna_final] = pieza
    tab[fila][columna] = '..'
    return True

def mover_reina(tab, fila, columna, fila_final, columna_final):
    # La reina combina movimientos de torre y alfil
    return mover_torre(tab, fila, columna, fila_final, columna_final) or \
           mover_alfil(tab, fila, columna, fila_final, columna_final)

def mover_rey(tab, fila, columna, fila_final, columna_final):
    pieza = tab[fila][columna]
    destino = tab[fila_final][columna_final]
    
    # Verificar movimiento de una casilla en cualquier dirección
    if abs(fila - fila_final) > 1 or abs(columna - columna_final) > 1:
        return False
    
    # Verificar que no se capture una pieza del mismo color
    if (pieza.islower() and destino.islower()) or (pieza.isupper() and destino.isupper()):
        return False
    
    tab[fila_final][columna_final] = pieza
    tab[fila][columna] = '..'
    return True

def mover_ficha(tablero, pos, pos_obj):
    f1, c1 = pos
    f2, c2 = pos_obj
    
    pieza = tablero[f1][c1]
    destino = tablero[f2][c2]
    
    # Verificar que no se mueva una casilla vacía
    if pieza == '..':
        return False
    
    # Verificar turno
    if (turno == 'blancas' and pieza.isupper()) or (turno == 'negras' and pieza.islower()):
        return False
    
    # Verificar que no se capture una pieza del mismo color
    if (pieza.islower() and destino.islower()) or (pieza.isupper() and destino.isupper()):
        return False
    
    # Mover según el tipo de pieza
    if pieza.lower() == 'pe':
        movido = mover_peon(tablero, f1, c1, f2, c2)
    elif pieza.lower() == 'ca':
        movido = mover_caballo(tablero, f1, c1, f2, c2)
    elif pieza.lower() == 'al':
        movido = mover_alfil(tablero, f1, c1, f2, c2)
    elif pieza.lower() == 'to':
        movido = mover_torre(tablero, f1, c1, f2, c2)
    elif pieza.lower() == 'qu':
        movido = mover_reina(tablero, f1, c1, f2, c2)
    elif pieza.lower() == 'ki':
        movido = mover_rey(tablero, f1, c1, f2, c2)
    else:
        movido = False
    
    if movido:
        global turno
        turno = 'negras' if turno == 'blancas' else 'blancas'
    
    return movido

def main():
    global seleccionado, turno
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic izquierdo
                    pos = pygame.mouse.get_pos()
                    casilla = obtener_casilla_desde_posicion(pos)
                    
                    if casilla:
                        f, c = casilla
                        if seleccionado is None:
                            # Seleccionar pieza si es del color del turno actual
                            pieza = tablero[f][c]
                            if pieza != '..':
                                if (turno == 'blancas' and pieza.isupper()) or (turno == 'negras' and pieza.islower()):
                                    seleccionado = (f, c)
                        else:
                            # Intentar mover la pieza seleccionada
                            if mover_ficha(tablero, seleccionado, casilla):
                                seleccionado = None
                            elif tablero[f][c] != '..' and ((turno == 'blancas' and tablero[f][c].isupper()) or (turno == 'negras' and tablero[f][c].islower())):
                                # Seleccionar otra pieza del mismo color
                                seleccionado = (f, c)
                            else:
                                seleccionado = None
        
        # Dibujar el tablero
        dibujar_tablero()
        
        # Mostrar mensaje de estado
        if seleccionado:
            f, c = seleccionado
            pieza = tablero[f][c]
            mensaje = f"Seleccionado: {pieza} en {chr(ord('A') + c)}{8 - f}"
            texto = fuente.render(mensaje, True, ROJO)
            pantalla.blit(texto, (20, ALTO - 30))
        
        pygame.display.flip()
        reloj.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
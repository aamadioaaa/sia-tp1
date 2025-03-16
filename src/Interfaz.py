# Interfaz Sokoban en PyGame 

import pygame

# Inicialización de pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 640, 480
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Sokoban alpha')

# Fuente para leyenda
fuente = pygame.font.SysFont("Arial", 16)

# Colores
COLOR_FONDO = (30, 30, 30)
COLOR_CAJA = (160, 82, 45)
COLOR_OBJETIVO = (200, 180, 0)
COLOR_JUGADOR = (0, 100, 255)
COLOR_PARED = (80, 80, 80)
COLOR_TEXTO = (255, 255, 255)

# Tamaño de bloque
TAM_BLOQUE = 40

# Escenario 

escenario = [
    list("WWWWWWWWWWWWWWWW"),
    list("WGW....W.......W"),
    list("W.W.W..W.WWWWW.W"),
    list("W...W.GW.......W"),
    list("WWW.WWWW.WWWWW.W"),
    list("W....C.........W"),
    list("W.WWW.WWWW.WWWWW"),
    list("W.....P........W"),
    list("WWWWWWWWWWWWWWWW")
]

# Guardar posiciones iniciales de objetivos
objetivos = [(x, y) for y, fila in enumerate(escenario) for x, bloque in enumerate(fila) if bloque == 'G']

# Buscar posición inicial del jugador
def encontrar_jugador():
    for y, fila in enumerate(escenario):
        for x, bloque in enumerate(fila):
            if bloque == 'P':
                return x, y

# Mover jugador y empujar cajas
def mover(dx, dy):
    global escenario
    x, y = encontrar_jugador()
    nuevo_x, nuevo_y = x + dx, y + dy
    siguiente_x, siguiente_y = nuevo_x + dx, nuevo_y + dy

    if escenario[nuevo_y][nuevo_x] in '.G':
        escenario[y][x] = 'G' if (x, y) in objetivos else '.'
        escenario[nuevo_y][nuevo_x] = 'P'
    elif escenario[nuevo_y][nuevo_x] == 'C' and escenario[siguiente_y][siguiente_x] in '.G':
        escenario[y][x] = 'G' if (x, y) in objetivos else '.'
        escenario[nuevo_y][nuevo_x] = 'P'
        escenario[siguiente_y][siguiente_x] = 'C'

# Dibujar el escenario
def dibujar_escenario():
    pantalla.fill(COLOR_FONDO)
    for y, fila in enumerate(escenario):
        for x, elemento in enumerate(fila):
            rect = pygame.Rect(x*TAM_BLOQUE, y*TAM_BLOQUE, TAM_BLOQUE, TAM_BLOQUE)
            if elemento == 'W':
                pygame.draw.rect(pantalla, COLOR_PARED, rect)
            elif elemento == 'P':
                pygame.draw.rect(pantalla, COLOR_JUGADOR, rect)
            elif elemento == 'C':
                pygame.draw.rect(pantalla, COLOR_CAJA, rect)
            elif elemento == 'G':
                pygame.draw.rect(pantalla, COLOR_OBJETIVO, rect)

    # Leyenda
    leyenda = [
        "P: Jugador (azul)",
        "C: Caja (marrón)",
        "G: Objetivo (amarillo)",
        "W: Pared (gris)"
    ]

    for i, texto in enumerate(leyenda):
        superficie_texto = fuente.render(texto, True, COLOR_TEXTO)
        pantalla.blit(superficie_texto, (10, ALTO - (len(leyenda)-i)*20 - 10))

# Ciclo principal
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                mover(-1, 0)
            elif evento.key == pygame.K_RIGHT:
                mover(1, 0)
            elif evento.key == pygame.K_UP:
                mover(0, -1)
            elif evento.key == pygame.K_DOWN:
                mover(0, 1)

    dibujar_escenario()
    pygame.display.flip()
    pygame.time.Clock().tick(60)




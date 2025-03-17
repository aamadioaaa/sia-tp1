# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 15:06:50 2025

@author: aru_a
"""

# Interfaz Sokoban en PyGame usando el archivo original sokoban.py con verificación de victoria

import pygame
from sokoban import Sokoban

# Inicialización de pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 640, 480
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Sokoban con Leyenda')

# Fuente para leyenda
fuente = pygame.font.SysFont("Arial", 16)
fuente_grande = pygame.font.SysFont("Arial", 32)

# Colores
COLOR_FONDO = (30, 30, 30)
COLOR_CAJA = (160, 82, 45)
COLOR_OBJETIVO = (200, 180, 0)
COLOR_JUGADOR = (0, 100, 255)
COLOR_PARED = (80, 80, 80)
COLOR_TEXTO = (255, 255, 255)
COLOR_VICTORIA = (0, 255, 0)

# Tamaño de bloque
TAM_BLOQUE = 40

# Escenario en formato del archivo original
basic_grid = """\
#######
#     #
#.$@  #
#     #
#######"""

# Crear objeto Sokoban
juego = Sokoban(basic_grid)

# Dibujar el escenario actualizado correctamente
def dibujar_escenario():
    pantalla.fill(COLOR_FONDO)
    filas, columnas = juego.grid.shape
    for y in range(filas):
        for x in range(columnas):
            rect = pygame.Rect(x*TAM_BLOQUE, y*TAM_BLOQUE, TAM_BLOQUE, TAM_BLOQUE)
            if juego.grid[y, x] == juego.WALL:
                pygame.draw.rect(pantalla, COLOR_PARED, rect)
            elif (y, x) == juego.player:
                pygame.draw.rect(pantalla, COLOR_JUGADOR, rect)
            elif (y, x) in juego.boxes:
                pygame.draw.rect(pantalla, COLOR_CAJA, rect)
            elif (y, x) in juego.goals:
                pygame.draw.rect(pantalla, COLOR_OBJETIVO, rect)

    # Leyenda
    leyenda = [
        "@: Jugador (azul)",
        "$: Caja (marrón)",
        ".: Objetivo (amarillo)",
        "#: Pared (gris)"
    ]

    for i, texto in enumerate(leyenda):
        superficie_texto = fuente.render(texto, True, COLOR_TEXTO)
        pantalla.blit(superficie_texto, (10, ALTO - (len(leyenda)-i)*20 - 10))
    
    # Verificación de victoria
    if juego.is_finished():
        texto_victoria = fuente_grande.render("¡Nivel completado!", True, COLOR_VICTORIA)
        pantalla.blit(texto_victoria, (ANCHO // 4, ALTO // 2))

# Ciclo principal
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                juego.move_left()
            elif evento.key == pygame.K_RIGHT:
                juego.move_right()
            elif evento.key == pygame.K_UP:
                juego.move_up()
            elif evento.key == pygame.K_DOWN:
                juego.move_down()

    dibujar_escenario()
    pygame.display.flip()
    pygame.time.Clock().tick(60)

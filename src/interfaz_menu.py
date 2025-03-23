"""
Para correr esta interfaz, simplemente ejecutá el archivo y seleccioná un archivo de configuración desde el cuadro de diálogo.
"""

import pygame
import os
import sys
import tkinter as tk
from tkinter import filedialog
from sokoban import Sokoban
from tree import recorre_arbol

# --- Selección del archivo de configuración mediante un cuadro de diálogo ---
root = tk.Tk()
root.withdraw()  # Oculta la ventana principal de Tkinter

configfile = filedialog.askopenfilename(
    title="Selecciona un archivo de configuración",
    filetypes=[("Archivos Python", "*.py")]
)

if not configfile:
    print("No se seleccionó ningún archivo.")
    sys.exit()

sys.path.insert(0, os.path.dirname(configfile))
config = __import__(os.path.basename(configfile).replace(".py", ""))

# Inicialización de pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 640, 480
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Sokoban con Solución Automática')

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
COLOR_DERROTA = (255, 255, 0)
COLOR_BOTON = (100, 100, 255)
COLOR_BOTON_TEXTO = (255, 255, 255)

# Tamaño de bloque
TAM_BLOQUE = 40

# Crear objeto Sokoban y cargar el nivel
juego = Sokoban()
juego.parse_grid(config.mapa)

# Función para dibujar el escenario
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

    # Dibujar botones
    boton_bfs = pygame.Rect(10, 10, 120, 30)
    pygame.draw.rect(pantalla, COLOR_BOTON, boton_bfs)
    texto_bfs = fuente.render("Resolver BFS", True, COLOR_BOTON_TEXTO)
    pantalla.blit(texto_bfs, (20, 15))

    boton_dfs = pygame.Rect(150, 10, 120, 30)
    pygame.draw.rect(pantalla, COLOR_BOTON, boton_dfs)
    texto_dfs = fuente.render("Resolver DFS", True, COLOR_BOTON_TEXTO)
    pantalla.blit(texto_dfs, (160, 15))

    boton_greedy = pygame.Rect(290, 10, 120, 30)
    pygame.draw.rect(pantalla, COLOR_BOTON, boton_greedy)
    texto_greedy = fuente.render("Resolver Greedy", True, COLOR_BOTON_TEXTO)
    pantalla.blit(texto_greedy, (300, 15))

    boton_a_star = pygame.Rect(430, 10, 120, 30)
    pygame.draw.rect(pantalla, COLOR_BOTON, boton_a_star)
    texto_a_star = fuente.render("Resolver A-star", True, COLOR_BOTON_TEXTO)
    pantalla.blit(texto_a_star, (440, 15))

    # Mensajes de estado
    if juego.is_finished():
        texto_victoria = fuente_grande.render("\u00a1Nivel completado!", True, COLOR_VICTORIA)
        pantalla.blit(texto_victoria, (ANCHO // 4, ALTO // 2))

    if juego.is_deadlocked():
        texto_derrota = fuente_grande.render("El juego se ha trabado", True, COLOR_DERROTA)
        pantalla.blit(texto_derrota, (ANCHO // 4, ALTO // 2))

    return boton_bfs, boton_dfs, boton_greedy, boton_a_star

# Ciclo principal
solucion = ""
corriendo = True
while corriendo:
    pantalla.fill(COLOR_FONDO)
    boton_bfs, boton_dfs, boton_greedy, boton_a_star = dibujar_escenario()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                nuevo_estado = juego.move_left()
            elif evento.key == pygame.K_RIGHT:
                nuevo_estado = juego.move_right()
            elif evento.key == pygame.K_UP:
                nuevo_estado = juego.move_up()
            elif evento.key == pygame.K_DOWN:
                nuevo_estado = juego.move_down()
            juego = nuevo_estado if nuevo_estado else juego

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_bfs.collidepoint(evento.pos):
                config.algoritmo = "bfs"
                solucion = recorre_arbol(juego, config)["movimientos"]

            elif boton_dfs.collidepoint(evento.pos):
                config.algoritmo = "dfs"
                solucion = recorre_arbol(juego, config)["movimientos"]

            elif boton_greedy.collidepoint(evento.pos):
                config.algoritmo = "greedy"
                solucion = recorre_arbol(juego, config)["movimientos"]

            elif boton_a_star.collidepoint(evento.pos):
                config.algoritmo = "a_star"
                solucion = recorre_arbol(juego, config)["movimientos"]

            if not solucion:
                print("Juego Terminado")

    # Ejecutar la solución paso a paso
    if solucion:
        movimiento = solucion[0]
        solucion = solucion[1:]

        if movimiento == 'l':
            nuevo_estado = juego.move_left()
        elif movimiento == 'r':
            nuevo_estado = juego.move_right()
        elif movimiento == 'u':
            nuevo_estado = juego.move_up()
        elif movimiento == 'd':
            nuevo_estado = juego.move_down()

        pygame.time.delay(300)
        juego = nuevo_estado if nuevo_estado else juego

    pygame.display.flip()
    pygame.time.Clock().tick(60)


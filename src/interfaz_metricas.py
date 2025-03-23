# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 09:49:25 2025

@author: aru_a
"""
"""
Para correr esta interfaz, simplemente seleccionar un archivo de configuración desde el cuadro de diálogo.
"""

import pygame
import os
import sys
import time
import tkinter as tk
from tkinter import filedialog
import networkx as nx
import matplotlib.pyplot as plt
from sokoban import Sokoban
from tree2 import recorre_arbol  # Ahora recorre_arbol también devuelve relaciones padre-hijo y un grafo del recorrido

# --- Selección del archivo de configuración mediante un cuadro de diálogo ---
def seleccionar_configuracion():
    root = tk.Tk()
    root.withdraw()
    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo de configuración",
        filetypes=[("Archivos Python", "*.py")]
    )
    if not archivo:
        print("No se seleccionó ningún archivo.")
        sys.exit()
    sys.path.insert(0, os.path.dirname(archivo))
    return __import__(os.path.basename(archivo).replace(".py", ""))

config = seleccionar_configuracion()

# Inicialización de pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 900, 600
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
COLOR_EVAL = (100, 255, 100)
COLOR_MSJ = (255, 150, 0)
COLOR_MEJOR = (255, 255, 0)

# Tamaño de bloque
TAM_BLOQUE = 40

juego = Sokoban()
juego.parse_grid(config.mapa)

resultados_eval = {}
mejor_algoritmo = None
ultimo_grafo = None
ultimo_nombre = None

# Función para mostrar el grafo

def mostrar_grafo(grafo_dict, nombre):
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()

    for idx, (alg, grafo) in enumerate(grafo_dict.items()):
        G = nx.DiGraph()
        for padre, hijos in grafo.items():
            for hijo in hijos:
                G.add_edge(padre, hijo)

        pos = nx.spring_layout(G)
        nx.draw(G, pos, ax=axes[idx], with_labels=False, node_size=50, arrows=True, edge_color="#AAAAAA")

        nodos = list(G.nodes())
        if nodos:
            nx.draw_networkx_nodes(G, pos, nodelist=[nodos[0]], node_color='green', node_size=100, ax=axes[idx], label='Inicio')
            nx.draw_networkx_nodes(G, pos, nodelist=[nodos[-1]], node_color='red', node_size=100, ax=axes[idx], label='Meta')
            axes[idx].legend()

        axes[idx].set_title(f"{alg.upper()}")
        axes[idx].axis('off')

    plt.tight_layout()
    plt.show()

# Función para dibujar el escenario
def dibujar_escenario(mensaje=None):
    pantalla.fill(COLOR_FONDO)
    filas, columnas = juego.grid.shape
    offset_x = 300
    for y in range(filas):
        for x in range(columnas):
            rect = pygame.Rect(offset_x + x*TAM_BLOQUE, 100 + y*TAM_BLOQUE, TAM_BLOQUE, TAM_BLOQUE)
            if juego.grid[y, x] == juego.WALL:
                pygame.draw.rect(pantalla, COLOR_PARED, rect)
            elif (y, x) == juego.player:
                pygame.draw.rect(pantalla, COLOR_JUGADOR, rect)
            elif (y, x) in juego.boxes:
                pygame.draw.rect(pantalla, COLOR_CAJA, rect)
            elif (y, x) in juego.goals:
                pygame.draw.rect(pantalla, COLOR_OBJETIVO, rect)

    boton_comenzar = pygame.Rect(20, 20, 250, 30)
    pygame.draw.rect(pantalla, COLOR_BOTON, boton_comenzar)
    pantalla.blit(fuente.render("Evaluar todos los algoritmos", True, COLOR_BOTON_TEXTO), (30, 25))

    boton_cargar = pygame.Rect(20, 60, 250, 30)
    pygame.draw.rect(pantalla, COLOR_BOTON, boton_cargar)
    pantalla.blit(fuente.render("Cargar otro escenario", True, COLOR_BOTON_TEXTO), (30, 65))

    boton_grafo = pygame.Rect(20, 100, 250, 30)
    pygame.draw.rect(pantalla, COLOR_BOTON, boton_grafo)
    pantalla.blit(fuente.render("Mostrar grafo del recorrido", True, COLOR_BOTON_TEXTO), (30, 105))

    if mensaje:
        pantalla.blit(fuente_grande.render(mensaje, True, COLOR_MSJ), (offset_x, 40))

    encabezado = fuente.render("ALG  |     T (s) |  M  |   N   |  P  | t/N (s)", True, COLOR_TEXTO)
    pantalla.blit(encabezado, (20, 150))

    descripcion1 = fuente.render("T: tiempo total del algoritmo", True, COLOR_TEXTO)
    descripcion2 = fuente.render("M: cantidad de movimientos", True, COLOR_TEXTO)
    descripcion3 = fuente.render("N: nodos explorados en la búsqueda", True, COLOR_TEXTO)
    descripcion4 = fuente.render("P: profundidad máxima alcanzada", True, COLOR_TEXTO)
    descripcion5 = fuente.render("t/N: tiempo promedio por nodo", True, COLOR_TEXTO)
    pantalla.blit(descripcion1, (650, 30))
    pantalla.blit(descripcion2, (650, 50))
    pantalla.blit(descripcion3, (650, 70))
    pantalla.blit(descripcion4, (650, 90))
    pantalla.blit(descripcion5, (650, 110))

    for idx, (alg, res) in enumerate(resultados_eval.items()):
        color = COLOR_MEJOR if alg == mejor_algoritmo else COLOR_EVAL
        texto = fuente.render(
            f"{alg.upper():<6}  {res['tiempo']:>6.2f}   {len(res['movimientos']):>4}   {len(res['nodos_explorados']):>5}   {res['profundidad_maxima']:>4}   {res['tiempo_por_nodo']:>7.4f}",
            True, color)
        pantalla.blit(texto, (20, 170 + idx * 20))

    return boton_comenzar, boton_cargar, boton_grafo

# Evaluación de todos los algoritmos
def evaluar_todos_los_algoritmos():
    global resultados_eval, mejor_algoritmo, juego, ultimo_grafo, ultimo_nombre
    algoritmos = ["bfs", "dfs", "greedy", "a_star"]
    resultados = {}

    for alg in algoritmos:
        juego = Sokoban()
        juego.parse_grid(config.mapa)

        dibujar_escenario(mensaje=f"Ejecutando {alg.upper()}...")
        pygame.display.flip()
        time.sleep(1)

        config.algoritmo = alg
        resultado = recorre_arbol(juego, config)
        resultado['profundidad_maxima'] = len(resultado['movimientos'])
        resultado['tiempo_por_nodo'] = resultado['tiempo'] / max(1, len(resultado['nodos_explorados']))
        resultados[alg] = resultado

        grafo_por_algoritmo = resultado["grafo"]
        if "todos_grafos" not in globals():
            globals()["todos_grafos"] = {}
        globals()["todos_grafos"][alg] = grafo_por_algoritmo

        juego = Sokoban()
        juego.parse_grid(config.mapa)
        for movimiento in resultado['movimientos']:
            if movimiento == 'l': juego = juego.move_left()
            elif movimiento == 'r': juego = juego.move_right()
            elif movimiento == 'u': juego = juego.move_up()
            elif movimiento == 'd': juego = juego.move_down()

            dibujar_escenario(mensaje=f"{alg.upper()}")
            pygame.display.flip()
            time.sleep(0.1)

        time.sleep(0.5)

    resultados_eval = resultados
    mejor_algoritmo = min(resultados, key=lambda a: len(resultados[a]['movimientos']))

# Loop principal
solucion = ""
corriendo = True
while corriendo:
    pantalla.fill(COLOR_FONDO)
    boton_comenzar, boton_cargar, boton_grafo = dibujar_escenario()

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
            elif evento.key == pygame.K_e:
                evaluar_todos_los_algoritmos()
            juego = nuevo_estado if nuevo_estado else juego

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_comenzar.collidepoint(evento.pos):
                evaluar_todos_los_algoritmos()
            elif boton_cargar.collidepoint(evento.pos):
                config = seleccionar_configuracion()
                juego = Sokoban()
                juego.parse_grid(config.mapa)
                resultados_eval = {}
                mejor_algoritmo = None
            elif boton_grafo.collidepoint(evento.pos):
                if "todos_grafos" in globals():
                    mostrar_grafo(todos_grafos, "Todos")
                    #mostrar_grafo(ultimo_grafo, ultimo_nombre)

    pygame.display.flip()
    pygame.time.Clock().tick(60)


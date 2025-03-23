# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 10:52:14 2025

@author: aru_a
"""

def recorre_arbol(root, config):
    import time

    def equal_nodes(state_1, state_2):
        return (state_1.grid == state_2.grid).all()

    def dfs_limitado(nodo, limite):
        stack = [(nodo, 0)]
        visitados = []
        while stack:
            actual, profundidad = stack.pop()
            visitados.append(actual)
            if actual.is_finished():
                return actual, visitados
            if profundidad < limite:
                for move in actual.get_possible_moves():
                    nuevo = move()
                    if not nuevo or nuevo.is_deadlocked():
                        continue
                    if any(equal_nodes(nuevo, v) for v in nodos_explorados + visitados):
                        continue
                    nuevo.movements = actual.movements + nuevo.movements[-1:]  # acumulación correcta
                    stack.append((nuevo, profundidad + 1))
                    relaciones.setdefault(id(actual), []).append(id(nuevo))
                    padres[id(nuevo)] = id(actual)
        return None, visitados

    t_inicial = time.time()
    max_nivel_alcanzado = 0
    root.movements = ""
    frontera = [root]
    nodos_explorados = []
    relaciones = {}
    padres = {id(root): None}

    if config.algoritmo == "iddfs":
        current = None
        profundidad = 0
        while not current and profundidad <= 100:
            current, nuevos = dfs_limitado(root, profundidad)
            nodos_explorados.extend(nuevos)
            profundidad += 1
        if not current:
            current = root  # fallback si falla
    else:
        while frontera:
            if config.algoritmo == "bfs":
                current = frontera.pop(0)
            elif config.algoritmo == "dfs":
                current = frontera.pop()
            elif config.algoritmo == "greedy":
                frontera.sort(key=lambda s: s.get_heuristic(config.heuristicas))
                current = frontera.pop(0)
            elif config.algoritmo == "a_star":
                frontera.sort(key=lambda s: (
                    s.get_actual_cost() + s.get_heuristic(config.heuristicas),
                    s.get_heuristic(config.heuristicas),
                ))
                current = frontera.pop(0)
            else:
                raise ValueError("Algoritmo Invalido")

            if config.verbose:
                print(f"Nodo {len(nodos_explorados)}\tMov. {len(current.movements)}\t{current.movements}")

            if current.is_finished():
                if config.verbose:
                    print("Solucion Encontrada")
                break

            nodos_explorados.append(current)
            max_nivel_alcanzado = max(max_nivel_alcanzado, len(current.movements))

            for move in current.get_possible_moves():
                new_state = move()
                if not new_state or new_state.is_deadlocked():
                    continue
                if any(equal_nodes(new_state, prev) for prev in nodos_explorados):
                    continue
                frontera.append(new_state)
                relaciones.setdefault(id(current), []).append(id(new_state))
                padres[id(new_state)] = id(current)

    t_final = time.time()

    return {
        "tiempo": t_final - t_inicial,
        "nodos_explorados": nodos_explorados,
        "solucion": current,
        "movimientos": current.movements,
        "grafo": relaciones,
        "padres": padres
    }

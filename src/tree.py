import time

def equal_nodes(state_1, state_2):
    return (state_1.grid == state_2.grid).all()


def recorre_arbol(root, config):
    """Recorrido del arbol de posibles estados del Sokoban.
    En funcion de la configuración se elige un algoritmo u otro.

    Solo devuelve una solución posible. No la óptima.

    Args:
        root (Sokoban): estado inicial del juego.

    Returns:
        Sokoban: estado final del juego.
    """

    # Estadisticas del algoritmo
    t_inicial = time.time()
    max_nivel_alcanzado = 0
    
    # inicio del algoritmo
    root.movements = ""
    frontera = [root]
    nodos_explorados = []
    while frontera:

        # Elige el nodo a visitar
        if config.algoritmo == "bfs":
            current = frontera.pop(0)

        elif config.algoritmo == "dfs":
            current = frontera.pop()

        elif config.algoritmo == "greedy":
            frontera.sort(key= lambda s: s.get_heuristic(config.heuristicas))
            current = frontera.pop(0)  # Visita el nodo con menor heuristica

        elif config.algoritmo == "a_star":
            frontera.sort(key= lambda s: (
                s.get_actual_cost() + s.get_heuristic(config.heuristicas), # 1 nivel de ordenamiento
                s.get_heuristic(config.heuristicas),                       # 2 nivel de ordenamiento
            ))
            current = frontera.pop(0)  # Visita el nodo con menor costo

        else:
            raise ValueError("Algoritmo Invalido")


        if config.verbose: print("Nodo {}".format(len(nodos_explorados)), end="\t")
        if config.verbose: print("Mov. {}".format(len(current.movements)), end="\t")
        if config.verbose: print(current.movements)
        
        
        if current.is_finished():
            if config.verbose: print("Solucion Encontrada")
            break

        # inserta el nodo en los nodos ya visitados
        nodos_explorados.append(current)
        max_nivel_alcanzado = max(max_nivel_alcanzado, len(current.movements))

        
        # expande el nodo y suma a la lista los estados no prohibidos
        for move in current.get_possible_moves():
            new_state = move()

            if not new_state: continue
            if new_state.is_deadlocked(): continue
            was_visited = any([equal_nodes(new_state, prev_state) for prev_state in nodos_explorados])
            if was_visited: continue
            
            frontera.append(new_state)
                
    t_final = time.time()

    results = {
        "tiempo": t_final - t_inicial,
        "nodos_explorados": nodos_explorados,        
        "solucion": current,
        "movimientos": current.movements
    }

    return results

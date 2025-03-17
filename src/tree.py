def bfs(root):
    """Recorrido del arbol de posibles estados del Sokoban a traves de
    Breadth First Search. Busqueda en el arbol primero hacía los costados.

    Solo devuelve una solución posible. No la óptima.

    Args:
        root (Sokoban): estado inicial del juego.

    Returns:
        Sokoban: estado final del juego.
    """
    queue = []
    queue.append(root)
    while queue:
        current = queue.pop(0)
        if current.is_finished():
            print("Found solution")
            break

        for move in current.get_possible_moves():
            new_state = move()

            if new_state and not new_state.is_deadlocked():
                queue.append(new_state)

    return current


def dfs(root):
    """Recorrido del arbol de posibles estados del Sokoban a traves de
    Depth First Search. Busqueda en el arbol primero hacía abajo.

    Solo devuelve una solución posible. No la óptima.

    Args:
        root (Sokoban): estado inicial del juego.

    Returns:
        Sokoban: estado final del juego.
    """
    queue = []
    queue.append(root)
    while queue:
        current = queue.pop()  # En DFS se toma el primer elemento que entro
        if current.is_finished():
            print("Found solution")
            break

        for move in current.get_possible_moves():
            new_state = move()

            if new_state and not new_state.is_deadlocked():
                queue.append(new_state)

    return current

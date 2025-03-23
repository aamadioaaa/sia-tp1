import numpy as np


class Sokoban:
    """
    Clase que representa el tablero del juego Sokoban como un estado.
    En caso de que se realice una modificación (movimiento), se devuelve una
    nueva instancia de la clase como si fuera un nuevo estado.
    """

    PLAYER = "@"
    BOX = "$"
    WALL = "#"
    EMPTY = " "
    GOAL = "."
    GOAL_AND_BOX = "*"
    GOAL_AND_PLAYER = "+"

    def __init__(self):
        """Inicializa datos de la clase"""
        self.player = None
        self.boxes = []
        self.goals = []
        self.grid = np.array([])
        self.movements = ""

    def parse_grid(self, grid: str) -> np.ndarray:
        """Transforma el tablero de juego en un array de numpy

        Args:
            grid (str): tablero en formato ASCII de acuerdo a http://www.game-sokoban.com/

        Returns:
            np.ndarray: tablero de juego en formato de array de numpy
        """
        gridlines = grid.split("\n")
        rows = len(gridlines)
        cols = max([len(row) for row in gridlines])
        self.grid = np.full((rows, cols), self.EMPTY)
        for i, row in enumerate(gridlines):
            for j, cell in enumerate(row):
                if cell == self.WALL:
                    self.grid[i, j] = self.WALL
                elif cell in self.BOX:
                    self.grid[i, j] = self.BOX
                    self.boxes.append((i, j))
                elif cell == self.GOAL:
                    self.goals.append((i, j))
                elif cell == self.GOAL_AND_BOX:
                    self.grid[i, j] = self.BOX
                    self.boxes.append((i, j))
                    self.goals.append((i, j))
                elif cell == self.PLAYER:
                    self.grid[i, j] = self.PLAYER
                    self.player = (i, j)
                    gridlines = grid.split("\n")
                elif cell == self.GOAL_AND_PLAYER:
                    self.grid[i, j] = self.GOAL
                    self.goals.append((i, j))
                    self.player = (i, j)

                

    def _move(self, x: int, y: int):
        """Mueve el jugador en la dirección indicada.

        Args:
            x (int): movimiento en horizontal
            y (int): movimiento en vertical

        Returns:
            Sokoban: nueva instancia del tablero o None si el movimiento es inválido
        """
        i, j = self.player

        invalid_moves = [
            self.grid[i + x, j + y] == self.WALL,
            self.grid[i + x, j + y] == self.BOX
            and self.grid[i + 2 * x, j + 2 * y] == self.WALL,
            self.grid[i + x, j + y] == self.BOX
            and self.grid[i + 2 * x, j + 2 * y] == self.BOX,
        ]
        if any(invalid_moves):
            return

        # Crea una nueva instancia del tablero con el movimiento ejecutado
        other = Sokoban()
        other.grid = self.grid.copy()
        other.boxes = self.boxes.copy()
        other.goals = self.goals.copy()
        other.player = self.player
        other.movements = self.movements

        if other.grid[i + x, j + y] == self.BOX:
            other.grid[i + 2 * x, j + 2 * y] = self.BOX
            box_index = other.boxes.index((i + x, j + y))
            other.boxes[box_index] = (i + 2 * x, j + 2 * y)

        other.grid[i, j] = self.EMPTY
        other.grid[i + x, j + y] = self.PLAYER
        other.player = (i + x, j + y)
        return other

    def move_up(self):
        """Mueve el jugador hacia arriba y devuelve una nueva clase.
        Si es imposible realizar el movimiento, devuelve None.
        """
        other = self._move(-1, 0)
        if other:
            other.movements += "u"
        return other

    def move_down(self):
        """Mueve el jugador hacia abajo y devuelve una nueva clase.
        Si es imposible realizar el movimiento, devuelve None.
        """
        other = self._move(1, 0)
        if other:
            other.movements += "d"
        return other

    def move_left(self):
        """Mueve el jugador hacia la izquierda y devuelve una nueva clase.
        Si es imposible realizar el movimiento, devuelve None.
        """
        other = self._move(0, -1)
        if other:
            other.movements += "l"
        return other

    def move_right(self):
        """Mueve el jugador hacia la derecha y devuelve una nueva clase.
        Si es imposible realizar el movimiento, devuelve None.
        """
        other = self._move(0, 1)
        if other:
            other.movements += "r"
        return other

    def get_possible_moves(self):
        """Devuelve una lista con los posibles movimientos para cambiar a otro
        estado.

        Returns:
            list: funciones de movimiento del jugador
        """
        return [
            self.move_down,
            self.move_up,
            self.move_right,
            self.move_left,
        ]


    def is_finished(self) -> bool:
        """Verifica si el juego ha sido completado exitosamente.

        Returns:
            bool: indicador de si el juego ha sido completado exitosamente
        """
        return all([box in self.goals for box in self.boxes])


    def is_deadlocked(self) -> bool:
        """Verifica que el juego no se encuentre en un estado sin solución.
        Esto significa que la caja se queda en una esquina y no puede ser movida.

        Returns:
            bool: indicador de si el juego está en un estado sin solución
        """

        if self.is_finished(): return False

        for box in self.boxes:
            # Es un deadlock si una caja llega a una esquina, se excluye cajas en esquinas que son GOAL
            if self._is_in_corner(*box) and box not in self.goals:
                return True
            
            # Es un deadlock si una caja queda sobre una pared y solo puede moverse sobre ella
            if self._is_wall_deadlock(*box):
                return True
        
        # Si llegamos aca no hay deadlock
        return False


    def _is_in_corner(self, i:int, j:int):
        """dada una posicion, indica si se encuentra en una esquina del tablero

        Args:
            i (int): posicion horizontal
            j (int): posicion vertical

        Returns:
            bool: indicacione si esta en el tablero
        """
        if self.grid[i - 1, j] == self.WALL and self.grid[i, j - 1] == self.WALL:
            return True
        if self.grid[i - 1, j] == self.WALL and self.grid[i, j + 1] == self.WALL:
            return True
        if self.grid[i + 1, j] == self.WALL and self.grid[i, j - 1] == self.WALL:
            return True
        if self.grid[i + 1, j] == self.WALL and self.grid[i, j + 1] == self.WALL:
            return True
        return False
    

    def _is_wall_deadlock(self, i:int, j:int):
        """Verifica que la caja esta en una posicion donde es imposible llevarla
        hacia un goal. Por ejemplo debajos se ve que la caja ($) es imposible
        llevarla al goal (.)

        #########
        #    $  #
        #  .    #

        Args:
            i (int): posicion horizontal de la caja
            j (int): posicion vertical de la caja
        """
        grid = self.grid

        # Horizontal
        l_offset = 0
        r_offset = 0
        while True:
            move_r_offset = 1 if grid[i, j + r_offset] != self.WALL else 0
            move_l_offset = 1 if grid[i, j - l_offset] != self.WALL else 0
            r_offset += move_r_offset
            l_offset += move_l_offset
            if move_l_offset == 0 and move_r_offset == 0:
                break

        all_wall_up   = all(grid[i-1, j-l_offset+1:j+r_offset] == self.WALL)
        all_wall_down = all(grid[i+1, j-l_offset+1:j+r_offset] == self.WALL)
        goal_in_row = any([(g[0] == i) and (j-l_offset+1 <= g[1] <= j+r_offset) for g in self.goals])

        if (not goal_in_row and all_wall_down) or (not goal_in_row and all_wall_up):
            return True

        # Vertical
        u_offset = 0
        d_offset = 0
        while True:
            move_u_offset = 1 if grid[i - u_offset, j] != self.WALL else 0
            move_d_offset = 1 if grid[i + d_offset, j] != self.WALL else 0
            u_offset += move_u_offset
            d_offset += move_d_offset
            if move_u_offset == 0 and move_d_offset == 0:
                break

        all_wall_left  = all(grid[i-u_offset+1:i+d_offset , j-1] == self.WALL)
        all_wall_right = all(grid[i-u_offset+1:i+d_offset , j+1] == self.WALL)
        goal_in_row = any([(g[1] == j) and (i-u_offset+1 <= g[0] <= i+d_offset) for g in self.goals])

        if (not goal_in_row and all_wall_left) or (not goal_in_row and all_wall_right):
            return True

        # En caso de que no sea deadlock
        return False


    def get_actual_cost(self):
        """
        Devuelve la cantidad de pasos para llegar a ese estado

        Returns:
            int: costo del nodo actual

        """
        return len(self.movements)
    

    def get_heuristic(self, heuristics_names):
        """Devuelve la combinacion de heuristicas del nodo (costo estimado a la solucion)
        
        Args:
            heuristics_names (_type_): listado de heuriticas a usar

        Returns:
            int: posible costo hasta alcanzar la solucion
        """

        if not heuristics_names: # si no se pasa una heuristica retorna 0
            return 0

        valores_heuristica = []
        for heuristica_name in heuristics_names:
            heuristica = getattr(self, "heuristica_{}".format(heuristica_name))
            valores_heuristica.append(heuristica())

        return max(valores_heuristica)
    

    def heuristica_manhattan(self):
        """Distancia Manhattan para llevar todas las cajas a un goal.

        Heuristica 1 de la consigna

        Returns:
            float: suma de la distancia o norma 0 entre caja y goal más proximo
        """
        goals = np.array(self.goals)
        boxes = np.array(self.boxes)        
        return sum([min([sum(abs(box - goal)) for goal in goals]) for box in boxes])

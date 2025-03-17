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

    def __init__(self):
        """Inicializa datos de la clase"""
        self.player = None
        self.boxes = []
        self.goals = []
        self.grid = np.array([])
        self.movements = ""

    def parse_grid(self, grid: str) -> np.ndarray:
        """Transforma el tableto de juego en un array de numpy

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
                elif cell == self.BOX:
                    self.grid[i, j] = self.BOX
                    self.boxes.append((i, j))
                elif cell == self.GOAL:
                    self.goals.append((i, j))
                elif cell == self.PLAYER:
                    self.grid[i, j] = self.PLAYER
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

        if not self.movements:
            return [
                self.move_up,
                self.move_down,
                self.move_right,
                self.move_left,
            ]

        # esto es para evitar que el jugador vaya hacia arriba y hacia abajo
        # infinitamente. Con solo retornar toda la lista de movimientos 
        # funcionaria bien en el BFS pero no en el DFS.
        if self.movements[-1] == "u":
            return [
                self.move_up,
                self.move_right,
                self.move_left,
            ]
        elif self.movements[-1] == "d":
            return [
                self.move_down,
                self.move_right,
                self.move_left,
            ]
        elif self.movements[-1] == "r":
            return [
                self.move_up,
                self.move_down,
                self.move_right,
            ]
        elif self.movements[-1] == "l":
            return [
                self.move_up,
                self.move_down,
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
        for i, j in self.boxes:
            if (i,j,) in self.goals: # Evita deadlock si la caja está en un goal
                continue
            if self.grid[i - 1, j] == self.WALL and self.grid[i, j - 1] == self.WALL:
                return True
            if self.grid[i - 1, j] == self.WALL and self.grid[i, j + 1] == self.WALL:
                return True
            if self.grid[i + 1, j] == self.WALL and self.grid[i, j - 1] == self.WALL:
                return True
            if self.grid[i + 1, j] == self.WALL and self.grid[i, j + 1] == self.WALL:
                return True
        return False

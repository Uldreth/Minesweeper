from src.board_element import BoardElement, BoardElementState
from random import sample
from enum import Enum


class GameState(Enum):
    INITIALIZED = 0
    STARTED = 1
    WIN = 2
    LOSS = -1


class Board:
    def __init__(self, number_of_rows: int, number_of_columns: int, number_of_mines: int):
        if number_of_rows <= 0 or number_of_columns <= 0:
            raise ValueError("The board must have a positive number of rows and columns.")
        if number_of_rows > 30 or number_of_columns > 30:
            raise ValueError("The board size cannot exceed 30x30.")
        if number_of_mines <= 0:
            raise ValueError("The board must have at least one mine.")
        self._number_of_rows = number_of_rows
        self._number_of_columns = number_of_columns
        self._number_of_elements = number_of_rows * number_of_columns
        if number_of_mines >= self._number_of_elements:
            raise ValueError("The number of mines must be less than the number of board elements.")
        self._number_of_mines = number_of_mines
        self._game_state = GameState.INITIALIZED
        self._elements: list[BoardElement] = self._set_up_board()

    def __getitem__(self, coordinates: int | tuple[int, int]):
        if isinstance(coordinates, int):
            return self.elements[coordinates]
        if isinstance(coordinates, tuple) and len(coordinates) == 1:
            return self.elements[coordinates[0]]
        if isinstance(coordinates, tuple) and len(coordinates) == 2:
            idx = self.coordinates_to_index(*coordinates)
            return self.elements[idx]
        if isinstance(coordinates, tuple) and len(coordinates) != 2:
            raise IndexError("The number of indices must be one or two.")
        raise TypeError(f"Invalid argument. Expected int or tuple of two ints, got {type(coordinates)} instead.")

    @property
    def number_of_rows(self):
        return self._number_of_rows

    @property
    def number_of_columns(self):
        return self._number_of_columns

    @property
    def number_of_elements(self):
        return self._number_of_elements

    @property
    def number_of_mines(self):
        return self._number_of_mines

    @property
    def game_state(self):
        return self._game_state

    @game_state.setter
    def game_state(self, value: GameState):
        if self.game_state != GameState.LOSS:
            self._game_state = value

    @property
    def elements(self):
        return self._elements

    def index_to_coordinates(self, idx: int):
        if idx < 0 or idx >= self.number_of_elements:
            raise IndexError(f"Invalid board index: {idx}")
        return idx // self.number_of_columns, idx % self.number_of_columns

    def coordinates_to_index(self, row: int, col: int):
        if row < 0 or row >= self.number_of_rows or col < 0 or col >= self.number_of_columns:
            raise IndexError(f"Invalid board coordinates: {row}, {col}")
        return row * self.number_of_columns + col

    def swap_mine_with_empty_element(self, row: int, col: int):
        idx_mine = self.coordinates_to_index(row, col)
        idx_empty = sample([(idx, element) for (idx, element) in enumerate(self.elements) if not element.is_mine],
                           k=1)[0][0]
        self._elements[idx_mine], self._elements[idx_empty] = self._elements[idx_empty], self._elements[idx_mine]

    def calculate_proximities(self):
        empty_elements = ((idx, element) for (idx, element) in enumerate(self.elements) if not element.is_mine)
        for idx, element in empty_elements:
            row, col = self.index_to_coordinates(idx)
            proximity = self._calculate_proximity_for_single_element(row, col)
            element.proximity = proximity

    def check_win_state(self):
        all_mines_flagged = all(element.state == BoardElementState.FLAGGED for element in self.elements if element.is_mine)
        all_non_mines_revealed = all(element.state == BoardElementState.REVEALED
                                     for element in self.elements if not element.is_mine)
        self.game_state = GameState.WIN if all_mines_flagged and all_non_mines_revealed \
                                           and not self.game_state == GameState.LOSS else GameState.LOSS

    def reveal_element(self, row: int, col: int):
        element = self[row, col]
        if element.state == BoardElementState.REVEALED:
            return
        element.state = BoardElementState.REVEALED
        if element.is_mine:
            self.game_state = GameState.LOSS
            return
        if element.proximity == 0:
            nearby_coords = self._get_neighbouring_indices(row, col)
            for coords in nearby_coords:
                self.reveal_element(*coords)

    def _set_up_board(self):
        bomb_indices = sample(range(0, self.number_of_elements), k=self.number_of_mines)
        list_of_elements = [BoardElement(mined=True) if idx in bomb_indices else BoardElement(mined=False)
                            for idx in range(0, self.number_of_elements)]
        return list_of_elements

    def _calculate_proximity_for_single_element(self, row: int, col: int):
        coords_of_elements_in_proximity = self._get_neighbouring_indices(row, col)
        return len([self[i, j] for i, j in coords_of_elements_in_proximity if self[i, j].is_mine])

    def _get_neighbouring_indices(self, row: int, col: int):
        index_offset = (-1, 0, 1)
        return ((row + i, col + j) for i in index_offset for j in index_offset
                if not (i == 0 and j == 0) and (0 <= row + i < self.number_of_rows)
                and (0 <= col + j < self.number_of_columns))

    def __str__(self):
        horizontal_separator = "*" * (self.number_of_columns * 2 + 1) + "\n"
        def get_elements_in_row(row_number: int):
            return (self[row_number, j] for j in range(0, self.number_of_columns))
        string_rep_list = [horizontal_separator]
        for i in range(0, self.number_of_rows):
            row_rep_list = "".join(['*'] + [str(element) + "*" for element in get_elements_in_row(i)] + ["\n" + horizontal_separator])
            string_rep_list += row_rep_list
        return "".join(string_rep_list)


if __name__ == "__main__":
    board = Board(number_of_rows=4, number_of_columns=6, number_of_mines=4)
    board.calculate_proximities()
    print(board)


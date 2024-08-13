from src.board_element import BoardElement, BoardElementState
from random import sample
from enum import Enum


class GameState(Enum):
    """Enum representing the state of the game."""
    INITIALIZED = 0
    """Board has been set up, but game not started yet."""
    STARTED = 1
    """Game in-progress."""
    WIN = 2
    """Game has been won by the player."""
    LOSS = -1
    """Game has been lost by the player."""


class Board:
    """
    Class representing the game board.
    """
    def __init__(self, number_of_rows: int, number_of_columns: int, number_of_mines: int):
        """
        Constructor method for the game board.
        :param number_of_rows: Number of rows on the game board, must be an integer between 1 and 30 (inclusive).
        :param number_of_columns: Number of columns on the game board, must be an integer between 1 and 30 (inclusive).
        :param number_of_mines: Number of hidden mines scattered throughout the game board. Must be an integer
        between 1 and N - 1, where N is the total number of fields on the board.
        """
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
        """
        Returns a BoardElement based on indices or coordinates
        :param coordinates: Can be a single int or a tuple of two ints. In the former case, it specifies a board element
        in a row-continuous manner, and in the latter case by zero-indexed (row, column) coordinates.
        :return: Returns the board element to which the index or coordinates refer to.
        """
        if isinstance(coordinates, int):
            return self.elements[coordinates]
        if isinstance(coordinates, tuple) and len(coordinates) == 1:
            idx = coordinates[0]
            if not isinstance(idx, int):
                raise ValueError(f"Invalid argument. Expected int or tuple of two ints, got {type(idx)} instead.")
            return self.elements[coordinates[0]]
        if isinstance(coordinates, tuple) and len(coordinates) == 2:
            idx = self.coordinates_to_index(*coordinates)
            return self.elements[idx]
        if isinstance(coordinates, tuple) and len(coordinates) != 2:
            raise IndexError("The number of indices must be one or two.")
        raise TypeError(f"Invalid argument. Expected int or tuple of two ints, got {type(coordinates)} instead.")

    def __str__(self):
        """
        :return: Returns a string representation of the board displaying elements as mines ('m') or their
        proximity numbers (for empty fields).
        """
        horizontal_separator = "*" * (self.number_of_columns * 4 + 1) + "\n"
        def get_elements_in_row(row_number: int):
            return (self[row_number, j] for j in range(0, self.number_of_columns))
        string_rep_list = [horizontal_separator]
        for i in range(0, self.number_of_rows):
            row_rep_list = "".join(['*'] + [' ' +  str(element) + " " + "*" for element in get_elements_in_row(i)]
                                   + ["\n" + horizontal_separator])
            string_rep_list += row_rep_list
        return "".join(string_rep_list)

    @property
    def number_of_rows(self):
        """The number of rows on the board. This attribute is immutable."""
        return self._number_of_rows

    @property
    def number_of_columns(self):
        """The number of columns on the board. This attribute is immutable."""
        return self._number_of_columns

    @property
    def number_of_elements(self):
        """The total number of fields on the board. This attribute is immutable."""
        return self._number_of_elements

    @property
    def number_of_mines(self):
        """The total number of mines on the board. This attribute is immutable."""
        return self._number_of_mines

    @property
    def game_state(self):
        """The state of the game. Can be INITIALIZED, STARTED, WIN or LOSS."""
        return self._game_state

    @game_state.setter
    def game_state(self, value: GameState):
        if self.game_state != GameState.LOSS:
            self._game_state = value

    @property
    def elements(self):
        """List of all the fields on the board. This attribute is immutable."""
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
        """
        Specify a board element. If it is a mine, it will be swapped with a random empty element.
        :param row: Row index of the board element.
        :param col: Column index of the board element.
        """
        idx_mine = self.coordinates_to_index(row, col)
        idx_empty = sample([(idx, element) for (idx, element) in enumerate(self.elements) if not element.is_mine],
                           k=1)[0][0]
        self._elements[idx_mine], self._elements[idx_empty] = self._elements[idx_empty], self._elements[idx_mine]

    def calculate_proximities(self):
        """
        Computes the proximity numbers for all board elements (i.e. how many mines are nearby).
        """
        empty_elements = [(idx, element) for (idx, element) in enumerate(self.elements) if not element.is_mine]
        for idx, element in empty_elements:
            row, col = self.index_to_coordinates(idx)
            proximity = self._calculate_proximity_for_single_element(row, col)
            element.proximity = proximity

    def check_win_state(self):
        """
        Checks whether the game is in a win state and updates the game_state field accordingly.
        """
        all_mines_flagged = all([element.state == BoardElementState.FLAGGED for element in self.elements if element.is_mine])
        all_non_mines_revealed = all([element.state == BoardElementState.REVEALED
                                     for element in self.elements if not element.is_mine])
        if all_mines_flagged and all_non_mines_revealed and not self.game_state == GameState.LOSS:
            self.game_state = GameState.WIN

    def reveal_element(self, row: int, col: int):
        """
        Reveals the specified board element if it is not already revealed. If the element has zero proximity number,
        all neighbours will also be revealed in a recursive manner.
        :param row: Row index of the board element to be revealed.
        :param col: Column index of the board element to be revealed.
        """
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

    def toggle_flag_on_element(self, row: int, col: int):
        element = self[row, col]
        if element.state == BoardElementState.REVEALED:
            return
        is_flagged = element.state == BoardElementState.FLAGGED
        element.state = BoardElementState.FLAGGED if not is_flagged else BoardElementState.HIDDEN

    def auto_reveal(self, row: int, col: int):
        element = self[row, col]
        if element.state == BoardElementState.REVEALED and not element.is_mine and element.proximity > 0:
            coords_of_nearby_elements = self._get_neighbouring_indices(row, col)
            number_of_nearby_flags = sum(1 for i, j in coords_of_nearby_elements
                                         if self[i, j].state == BoardElementState.FLAGGED)
            if number_of_nearby_flags == element.proximity:
                for i, j in coords_of_nearby_elements:
                    if self[i, j].state == BoardElementState.HIDDEN:
                        self.reveal_element(i, j)

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
        return [(row + i, col + j) for i in index_offset for j in index_offset
                if not (i == 0 and j == 0) and (0 <= row + i < self.number_of_rows)
                and (0 <= col + j < self.number_of_columns)]


if __name__ == "__main__":
    board = Board(number_of_rows=4, number_of_columns=6, number_of_mines=4)
    board.calculate_proximities()
    print(board)


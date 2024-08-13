from src.board_element import BoardElement
from src.board import Board

class BoardGenerator:
    def __init__(self, *rows: list[str]):
        self.matrix = [row for row in rows]
        self._validate_matrix_size()
        self.number_of_rows = len(self.matrix)
        self.number_of_columns = len(self.matrix[0])
        self.number_of_mines = self._validate_matrix_elements()

    def create_board(self):
        board_elements = []
        for row in self.matrix:
            for item in row:
                is_mine = True if item == 'm' else False
                board_element = BoardElement(is_mine)
                board_elements.append(board_element)
        board = Board(self.number_of_rows, self.number_of_columns, 1)
        board._elements = board_elements
        board._number_of_mines = self.number_of_mines
        return board

    def _validate_matrix_size(self):
        if not bool(self.matrix):
            raise ValueError("Matrix is empty.")
        is_valid = True
        initial_row_length = len(self.matrix[0])
        for row in self.matrix:
            if len(row) != initial_row_length:
                is_valid = False
        if is_valid:
            return
        raise ValueError("Matrix is jagged.")

    def _validate_matrix_elements(self):
        valid_elements = ('m', 'e')
        number_of_mines = 0
        for row in self.matrix:
            for element in row:
                if element not in valid_elements:
                    raise ValueError("Matrix must only contain strings 'm' and 'e'.")
                if element == 'm':
                    number_of_mines += 1
        return number_of_mines




if __name__ == "__main__":
    matrix = [['m', 'm', 'e', 'e', 'e'],
              ['e', 'e', 'e', 'm', 'e'],
              ['e', 'm', 'm', 'e', 'e']]
    board = BoardGenerator(*matrix).create_board()
    board.calculate_proximities()
    print(board)
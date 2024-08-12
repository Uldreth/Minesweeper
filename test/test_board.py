import unittest
from src.board import Board, GameState
from src.board_element import BoardElementState, BoardElement
from random import sample


class TestBoard(unittest.TestCase):
    def test_board_creation(self):
        board = Board(number_of_rows=4, number_of_columns=6, number_of_mines=4)
        num_of_elements = len(board.elements)
        num_of_mines = len([element for element in board.elements if element.is_mine])

        self.assertEqual(num_of_elements, 24)
        self.assertEqual(num_of_mines, 4)

    def test_board_getitem(self):
        board = Board(number_of_rows=4, number_of_columns=6, number_of_mines=4)
        board._elements = ['0', '1', '2', '3', '4', '5',
                           '6', '7', '8', '9', '10', '11',
                           '12', '13', '14', '15', '16', '17',
                           '18', '19', '20', '21', '22', '23']
        element_by_index_1 = board[9]
        element_by_index_2 = board[19]
        element_by_coords_1 = board[1, 4]
        element_by_coords_2 = board[3, 5]
        self.assertEqual(element_by_index_1, '9')
        self.assertEqual(element_by_index_2, '19')
        self.assertEqual(element_by_coords_1, '10')
        self.assertEqual(element_by_coords_2, '23')

    def test_swap_mine(self):
        board = Board(number_of_rows=9, number_of_columns=9, number_of_mines=10)
        mine_element_idx = sample([idx for idx, element in enumerate(board.elements) if element.is_mine], k=1)[0]
        self.assertEqual(board[mine_element_idx].is_mine, True)
        row, col = board.index_to_coordinates(mine_element_idx)
        board.swap_mine_with_empty_element(row, col)
        self.assertEqual(board[mine_element_idx].is_mine, False)

    def test_check_win_state(self):
        board = Board(number_of_rows=9, number_of_columns=9, number_of_mines=10)
        for element in board.elements:
            if element.is_mine:
                element.state = BoardElementState.FLAGGED
        board.check_win_state()
        self.assertEqual(board.game_state, GameState.WIN)

    def test_reveal_element_cascade(self):
        board = Board(number_of_rows=5, number_of_columns=4, number_of_mines=1)
        new_board_elements = [BoardElement(True), BoardElement(True), BoardElement(True), BoardElement(True),
                              BoardElement(True), BoardElement(False), BoardElement(False), BoardElement(False),
                              BoardElement(True), BoardElement(False), BoardElement(False), BoardElement(False),
                              BoardElement(True), BoardElement(False), BoardElement(False), BoardElement(False),
                              BoardElement(False), BoardElement(True), BoardElement(True), BoardElement(True)]
        board._elements = new_board_elements
        board._number_of_mines = 15
        board.calculate_proximities()
        board.reveal_element(2, 2)
        hidden_coords = [(2, 0), (0, 2), (4, 3), (4, 0)]
        revealed_coords = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]
        for coords in hidden_coords:
            self.assertEqual(board[coords].state, BoardElementState.HIDDEN)
        for coords in revealed_coords:
            self.assertEqual(board[coords].state, BoardElementState.REVEALED)

    def test_reveal_element_mine(self):
        board = Board(number_of_rows=5, number_of_columns=4, number_of_mines=1)
        new_board_elements = [BoardElement(True), BoardElement(True), BoardElement(True), BoardElement(True),
                              BoardElement(True), BoardElement(False), BoardElement(False), BoardElement(False),
                              BoardElement(True), BoardElement(False), BoardElement(False), BoardElement(False),
                              BoardElement(True), BoardElement(False), BoardElement(False), BoardElement(False),
                              BoardElement(False), BoardElement(True), BoardElement(True), BoardElement(True)]
        board._elements = new_board_elements
        board._number_of_mines = 15
        board.calculate_proximities()
        board.reveal_element(0, 0)
        self.assertEqual(board[0, 0].state, BoardElementState.REVEALED)
        self.assertEqual(board[0, 1].state, BoardElementState.HIDDEN)
        self.assertEqual(board[1, 0].state, BoardElementState.HIDDEN)
        self.assertEqual(board[1, 1].state, BoardElementState.HIDDEN)
        self.assertEqual(board.game_state, GameState.LOSS)



if __name__ == '__main__':
    unittest.main()

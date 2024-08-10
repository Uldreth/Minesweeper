import unittest
from src.board import Board


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



if __name__ == '__main__':
    unittest.main()

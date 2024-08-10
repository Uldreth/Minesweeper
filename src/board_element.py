

class BoardElement:
    def __init__(self, mined: bool):
        self._is_mine = mined
        self._is_revealed = False
        self._is_flagged = False
        self._proximity = 0

    @property
    def is_mine(self):
        return self._is_mine

    @property
    def is_revealed(self):
        return self._is_revealed

    @property
    def is_flagged(self):
        return self._is_flagged

    @property
    def proximity(self):
        return self._proximity

    @proximity.setter
    def proximity(self, value: int):
        if not isinstance(value, int):
            raise ValueError("Proximity must be an integer.")
        if value < 0 or value > 8:
            raise ValueError("Proximity must be between 0 and 8.")
        self._proximity = value

    def toggle_mine(self):
        self._is_mine = not self._is_mine

    def toggle_flag(self):
        self._is_flagged = not self._is_flagged

    def reveal(self):
        self._is_revealed = True

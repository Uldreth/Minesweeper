from enum import Enum


class BoardElementState(Enum):
    HIDDEN = 0
    FLAGGED = 1
    REVEALED = 2


class BoardElement:
    def __init__(self, mined: bool):
        self._is_mine: bool = mined
        self._state = BoardElementState.HIDDEN
        self._proximity = 0

    @property
    def is_mine(self):
        return self._is_mine

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: BoardElementState):
        self._state = value

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

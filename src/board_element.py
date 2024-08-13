from enum import Enum


class BoardElementState(Enum):
    """Enum representing the state of the field."""
    HIDDEN = 0
    """The contents of the field are not visible to the player."""
    FLAGGED = 1
    """The player has marked the field with a flag."""
    REVEALED = 2
    """The contents of the field are visible to the player."""


class BoardElement:
    """
    Represents a field in the Minesweeper board.
    """
    def __init__(self, mined: bool):
        """
        Constructs a board element. The default state is HIDDEN, and with unassigned proximity (-1).
        :param mined: Whether the field contains a mine or not.
        """
        self._is_mine: bool = mined
        self._state = BoardElementState.HIDDEN
        self._proximity = -1

    def __str__(self):
        """
        String representation of a board element.
        :return: Returns 'm' for mine and the proximity number (0..8) for an empty element.
        """
        return "m" if self.is_mine else str(self.proximity)

    @property
    def is_mine(self):
        """Whether the field is a mine or empty. This attribute is immutable."""
        return self._is_mine

    @property
    def state(self):
        """The state of the field, which can be HIDDEN, FLAGGED or REVEALED."""
        return self._state

    @state.setter
    def state(self, value: BoardElementState):
        self._state = value

    @property
    def proximity(self):
        """The number of nearby fields with mines on them. Has a value of -1 before proper initialization and for mines."""
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

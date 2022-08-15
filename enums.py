from enum import Enum


class Navigation(str, Enum):
    NEXT = "Next"
    PREV = "Pref"
    BACK = "Back"

class Verify(str, Enum):
    YES = "Yes"
    NO = "No"

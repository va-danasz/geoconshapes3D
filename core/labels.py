from enum import StrEnum

class Concept(StrEnum):
    ALONE = "ALONE"
    CLOSE = "CLOSE"
    FAR = "FAR"
    OVERLAP = "OVERLAP"

class Shape(StrEnum):
    CONE = "CONE"
    CUBE = "CUBE"
    SPHERE = "SPHERE"

class Color(StrEnum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
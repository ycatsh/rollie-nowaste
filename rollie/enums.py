import enum


class TrashType(enum.Enum):
    ORGANIC = 'organic'
    PAPER = 'paper'
    HOUSEHOLD = 'household'


class UserRole(enum.Enum):
    USER = "user"
    PLANT_OPERATOR = "plant_operator"
    SCANNER= "scanner"

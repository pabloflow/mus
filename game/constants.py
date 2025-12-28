from enum import Enum, auto

class Phase(Enum):
    MUS = auto()
    GRANDE = auto()
    CHICA = auto()
    PARES = auto()
    JUEGO = auto()
    RECUENTO = auto()

class Action(Enum):
    MUS = auto()
    NOMUS = auto()
    PASO = auto()
    ENVIDO = auto()
    REENVIDO = auto()
    QUIERO = auto()
    NOQUIERO = auto()
    ORDAGO = auto()

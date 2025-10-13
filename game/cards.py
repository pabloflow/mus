import random

RANKS = [1,2,3,4,5,6,7,10,11,12]
SUITS = ['oros','copas','espadas','bastos']

class Card:
    def __init__(self, rank:int, suit:str):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank} de {self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(r,s) for r in RANKS for s in SUITS]

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, n:int):
        drawn = self.cards[:n]
        self.cards = self.cards[n:]
        return drawn

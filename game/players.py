from .evaluator import HandEvaluator, card_game_value
import random
from typing import List 
from .cards import Card


class Player:
    def __init__(self, name:str, hand:List[Card]=None):
        self.name = name
        self.hand:List[Card] = hand if hand else []
    def receive(self, cards:List[Card]):
        self.hand = cards
    def decide_mus(self) -> bool:
        raise NotImplementedError
    def choose_discards(self) -> List[int]:
        raise NotImplementedError
    def show_hand(self):
        print("Tus cartas son:")
        for i, c in enumerate(self.hand, 1):
            print(f"  {i}. {c}")

class RandomPlayer(Player):
    def decide_mus(self) -> bool:
        return random.random() < 0.5
    def choose_discards(self) -> List[int]:
        k = random.randint(0,4)
        return random.sample(range(4), k) if k>0 else []

class RulePlayer(Player):
    def decide_mus(self) -> bool:
        pares_tipo, _ = HandEvaluator.pares_value(self.hand)
        juego_tipo, juego_val = HandEvaluator.juego_value(self.hand)
        if pares_tipo > 1:
            return False
        if juego_tipo==2:
            return False
        s = sum(card_game_value(c) for c in self.hand)
        return s < 20
    def choose_discards(self) -> List[int]:
        values = [card_game_value(c) for c in self.hand]
        idx_sorted = sorted(range(4), key=lambda i: values[i])
        discards = [i for i in idx_sorted if values[i] <= 5]
        return discards[:3]
    
class AutoPlayer(Player):
    """Jugador automático (decisiones aleatorias)."""
    def decide_raise(self):
        return random.choice([2,3,5])
    
    def decide_ordago(self):
        return random.choice(['s', 'n'])

    def decide_action(self, ronda, apuesta_actual):
        

        if apuesta_actual == 0:
            posibles = ["p", "e", "o"]
        else:
            posibles = ["q", "n", "r", "o"]

        accion = random.choice(posibles)
        print(f"{self.name} elige: {accion.upper()}")
        return accion
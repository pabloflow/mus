from typing import List, Tuple, Dict
from .cards import Card
from collections import Counter


# Orden: 12 y 3 equivalentes, 1 y 2 equivalentes
_ORDER_GROUPS = [[2,1],[4],[5],[6],[7],[10],[11],[12,3]]
_ORDER_IDX = {}
for idx, group in enumerate(_ORDER_GROUPS):
    for r in group:
        _ORDER_IDX[r] = idx

def card_game_value(card:Card)->int:
    if card.rank in (12,3,11,10):
        return 10
    if card.rank in (1,2):
        return 1
    return card.rank

class HandEvaluator:
    @staticmethod
    def grande_value(hand:List[Card]) -> Tuple:
        ranks = sorted([_ORDER_IDX[c.rank] for c in hand], reverse=True)
        return tuple(ranks)

    @staticmethod
    def chica_value(hand:List[Card]) -> Tuple:
        ranks = sorted([_ORDER_IDX[c.rank] for c in hand])
        return tuple(ranks)

    @staticmethod
    def pares_value(hand:List[Card]) -> Tuple[int, List[int]]:
        counts = Counter([_ORDER_IDX[c.rank] for c in hand])
        pares = [r for r,c in counts.items() if c==2]
        medias = [r for r,c in counts.items() if c==3]
        duples = [r for r,c in counts.items() if c==4]
        if duples:
            return (4, sorted(duples, reverse=True))
        if medias:
            return (3, sorted(medias, reverse=True))
        if len(pares)==2:
            return (4, sorted(pares, reverse=True))
        if len(pares)==1:
            return (2, sorted(pares, reverse=True))
        return (1, [])

    @staticmethod
    def juego_value(hand:List[Card]) -> Tuple[int, int]:
        s = sum(card_game_value(c) for c in hand)
        if s >= 31:
            order = [31,32,40,37,36,35,34,33]
            if s in order:
                rank = order.index(s)
            else:
                rank = len(order) - 1
            return (2, -rank)
        else:
            return (1, s)

    @staticmethod
    def evaluate_all(hand:List[Card]) -> Dict:
        return {
            'grande': HandEvaluator.grande_value(hand),
            'chica': HandEvaluator.chica_value(hand),
            'pares': HandEvaluator.pares_value(hand),
            'juego': HandEvaluator.juego_value(hand),
        }
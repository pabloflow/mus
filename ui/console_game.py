from game.cards import Card
from game.players import RandomPlayer, RulePlayer, AutoPlayer
from game.engine import Game

def play_console():
    # Ejemplo de asignación manual de cartas (opcional)
    # mano_adri = [Card(12,'oros'), Card(12,'copas'), Card(6,'bastos'), Card(5,'espadas')]
    # mano_pablo = [Card(3,'oros'), Card(3,'copas'), Card(6,'bastos'), Card(5,'espadas')]

    p1 = AutoPlayer('Adri')
    p2 = RandomPlayer('Pablo')

    g = Game(p1, p2, mano=p2)
    piedras = {p1.name: 0, p2.name: 0}

    while piedras[p1.name] < 40 and piedras[p2.name] < 40:
        piedras, results, evals = g.play(piedras)
        print(p1.name, p1.hand, evals[0])
        print(p2.name, p2.hand, evals[1])
        print("Resultados por ronda:", results)
        print("Puntuación final:", piedras)
        print("La mano fue:", g.mano.name)
        g.mano = p1 if g.mano == p2 else p2

# opcional: permite ejecutar directamente este archivo
if __name__ == "__main__":
    play_console()

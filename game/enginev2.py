from .cards import Deck
from .evaluator import HandEvaluator
from .players import Player, AutoPlayer
import random
import constants as c

class MusState:
    """almacena la foto actual del juego"""
    def __init__(self):
        self.phase = c.Phase.GRANDE
        self.scores = {0:0, 1:0}
        self.pot = 0  #apuesta acumulada
        self.current_bet = 0 #apuesta actual
        self.active_player_idx = 0 #jugador que tiene el turno
        self.hand_player = 0 #jugador que va de mano (ventaja)

        self.pending_resolution = {} # guardamos que pasa en cada fase luego resolvemos ejemplo: 'grande': {'winner': 0, 'stones': 2, 'accepted': True}
        self.history = []  #luego para CFR

class MusEngine:
    def __init__(self, p1: Player, p2: Player):
        self.players = [p1,p2]
        self.deck = Deck()
        #haria falta shuffle aqui?
        self.state = MusState()
    
    def reset(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.players[0].receive(self.deck.draw(4))
        self.players[1].receive(self.deck.draw(4))

        self.state = MusState()
        self.state.phase = c.Phase.GRANDE #saltamos mus para testear
        self.state.active_player_idx = self.state.hand_player

        return self.state 

    def switch_turn(self):
        self.state.active_player_idx = 1 - self.state.active_player_idx

    def step(self, action: c.Action, amount = 0):
        """Devuelve: state, reward, done"""
        player = self.state.active_player_idx
        opponent = 1 - self.state.active_player_idx

        print(f"[{self.state.phase.name}] {player.name} hace: {action.name} (Cant: {amount})")

        if action == c.Action.PASO:
            if self.state.current_bet == 0:
                if self.state.active_player_idx == self.state.hand_player:
                    self.switch_turn()
                else:
                    self._close_phase(accepted=True, bet_value=0)
            else:
                raise ValueError("No puedes pasar, te han envidado")
        
        elif action == c.Action.ENVIDO:
            self.state.current_bet = 2
            self.switch_turn()
        
        elif action == c.Action.REENVIDO:
            raise_val = amount if amount > 0 else 2
            self.state.current_bet += raise_val
            self.switch_turn()
        
        elif action == c.Action.ORDAGO:
            self.state.current_bet = 40
            self.switch_turn()
        
        elif action == c.Action.QUIERO:
            self._close_phase(accepted=True, bet_value=self.state.current_bet)

        elif action == c.Action.NOQUIERO:
            winner_idx = 1 - self.state.active_player_idx
            self.state.scores[winner_idx] += self.state.current_bet
            self._close_phase(accepted=False, bet_value=0)

        return self.state
        
    def _close_phase(self, accepted:bool, bet_value:int):
        """Avanza a la siguiente fase y guarda las apuestas pendientes"""
        current_phase_name = self.state.phase.name.lower()

        if accepted and bet_value > 0:
            print(f" -> Apuesta de {bet_value} aceptada en {current_phase_name}. Se verá al final")
            self.state.pending_resolution[current_phase_name] = bet_value
        elif accepted and bet_value == 0 and current_phase_name in ["grande", "chica"]:
            self.state.pending_resolution[current_phase_name] = 1
        else:
            self.state.pending_resolution[current_phase_name] = 0

        self._next_phase()
    
    def _next_phase(self):
        phases = [ c.Phase.MUS, c.Phase.GRANDE, c.Phase.CHICA, c.Phase.RECUENTO]

        for i, p in enumerate(phases):
            if p == self.state.phase:
                curr_idx = i
                break
        
        if curr_idx < len(phases) - 1:
            self.state.phase = phases[curr_idx + 1]
            self.state.current_bet = 0
            self.state.active_player_idx = self.state.hand_player

            print(f"\n--- CAMBIO DE FASE: {self.state.phase.name} ---")

            if self.state.phase == c.Phase.RECUENTO:
                self._resolve_game()
        else:
            print("fin de la mano")

    def _resolve_game(self):

        print("--- RECUENTO FINAL ---")
        h1 = self.players[0].hand
        h2 = self.players[1].hand

        e1 = HandEvaluator.evaluate_all(h1)
        e2 = HandEvaluator.evaluate_all(h2)

        phases_order = ['grande', 'chica', 'pares', 'juego']

        for phase_name in phases_order:
            if phase_name in self.state.pending_resolution:
                bet_value = self.state.pending_resolution[phase_name]
                winner_idx = self._compare_hands(phase_name , e1, e2)
                self.state.scores[winner_idx] += bet_value

                winner_name = self.players[winner_idx].name
                print(f" -> {phase_name.upper()}: Gana {winner_name} (+{bet_value})")    

        print(f"\nResultado final de la mano: {self.state.scores}")

    def _compare_hands(self, phase, e1, e2) -> int:
        """compara las cartas de los jugadores segun la fase, devuelve el indice del ganador
        en caso de empate gana la mano"""

        hand_idx = self.state.hand_player

        winner = -1

        if phase in ('grande', 'chica'):
            val1 = e1[phase]
            val2 = e2[phase]

            if val1 == val2:
                winner = hand_idx
            elif val1 > val2:
                winner = 0
            else:
                winner = 1


        elif phase == 'pares':
            # e['pares'] es una tupla: (tipo, [valores])
            # tipo: 4=Duples, 3=Medias, 2=Par, 1=Nada
            p1_type, p1_vals = e1['pares']
            p2_type, p2_vals = e2['pares']
            
            if p1_type > p2_type:
                winner = 0
            elif p2_type > p1_type:
                winner = 1
            else:
                if p1_vals == p2_vals:
                    winner = hand_idx
                else:
                    winner = 0 if p1_vals > p2_vals else 1

        elif phase == 'juego':
            # e['juego'] es (tipo, valor). 
            # tipo 2 = Tiene Juego, tipo 1 = Tiene Punto (menor de 31)
            # valor: Para juego es negativo (-rank) para ordenar facil, o directo
            # REVISANDO TU EVALUATOR:
            # Devuelve (2, -rank) para juego. (1, suma) para punto.
            j1_type, j1_val = e1['juego']
            j2_type, j2_val = e2['juego']

            
        

        






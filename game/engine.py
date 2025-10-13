from .cards import Deck
from .evaluator import HandEvaluator
from .players import Player
import random


class Game:
    def __init__(self, player1:Player, player2:Player, mano:Player=None, seed=None):
        self.p1 = player1
        self.p2 = player2
        self.mano = mano if mano else player1  # por defecto empieza p1 como mano
        if seed is not None:
            random.seed(seed)

    def deal(self):
        
        deck = Deck()
        deck.shuffle()
        self.p1.receive(deck.draw(4))
        self.p2.receive(deck.draw(4))
        self.deck = deck

    def mus_phase(self):
        p1_wants = self.p1.decide_mus()
        p2_wants = self.p2.decide_mus()
        if not (p1_wants and p2_wants):
            return
        for p in (self.p1, self.p2):
            disc_idx = sorted(p.choose_discards(), reverse=True)
            for idx in disc_idx:
                del p.hand[idx]
            need = 4 - len(p.hand)
            if need>0:
                drawn = self.deck.draw(need)
                p.hand.extend(drawn)

    def compare_round(self, key:str, e1, e2) -> int:
        if key in ('grande','chica'):
            if e1[key] == e2[key]:
                return 1 if self.mano==self.p1 else -1
            if key=='grande':
                return 1 if e1[key] > e2[key] else -1
            else:
                return 1 if e1[key] < e2[key] else -1
        elif key=='pares':
            if e1[key][0] == e2[key][0]:
                if e1[key][1] == e2[key][1]:
                    return 1 if self.mano==self.p1 else -1
                return 1 if e1[key][1] > e2[key][1] else -1
            return 1 if e1[key][0] > e2[key][0] else -1
        elif key=='juego':
            if e1[key][0]==e2[key][0]==2:
                if e1[key][1] == e2[key][1]:
                    return 1 if self.mano==self.p1 else -1
                return 1 if e1[key][1] > e2[key][1] else -1
            elif e1[key][0]==2:
                return 1
            elif e2[key][0]==2:
                return -1
            else:
                if e1[key][1]==e2[key][1]:
                    return 1 if self.mano==self.p1 else -1
                return 1 if e1[key][1] > e2[key][1] else -1

    def betting_round(self, key, e1, e2):

      apuesta_actual = 0
      apuesta_anterior = 0
      ronda_activa = True
      turno = self.mano
      otro = self.p2 if turno == self.p1 else self.p1
      ultimo_apostador = None
      ordago = False

      print(f"\n💬 Ronda de {key.upper()} — Comienza {turno.name} (mano)")

      while ronda_activa:
          print(f"\nTurno de {turno.name}:")
          print(f"➡ Apuesta actual: {apuesta_actual if apuesta_actual > 0 else 'ninguna'}")

          # --- Opciones según el contexto ---
          if apuesta_actual == 0:
              accion = input(f"{turno.name}, ¿qué haces? (paso / envido / ordago): ").strip().lower()
          else:
              accion = input(f"{turno.name}, ¿qué haces? (quiero / no quiero / reenvido / ordago): ").strip().lower()

          # --- Procesar acción ---
          if accion == "p":
              if ultimo_apostador == "p":
                  print("⚖ Ambos pasan. No hay apuesta en esta ronda.")
                  return None, 0, False
              else:
                  ultimo_apostador = "p"
                  turno, otro = otro, turno
                  continue

          elif accion == "e":
              apuesta_actual = 2
              ultimo_apostador = turno
              print(f"💰 {turno.name} envida {apuesta_actual} piedras.")
              turno, otro = otro, turno
              continue

          elif accion == "r":
              subida = int(input(f"{turno.name}, ¿cuántas piedras subes? (+2 mínimo): ").strip() or "2")
              apuesta_anterior = apuesta_actual
              apuesta_actual += subida
              ultimo_apostador = turno
              print(f"💰 {turno.name} reenvida. Nueva apuesta total: {apuesta_actual} piedras.")
              turno, otro = otro, turno
              continue

          elif accion == "q":
              print(f"✅ {turno.name} quiere la apuesta de {apuesta_actual} piedras.")
              ronda_activa = False
              cmp = self.compare_round(key, e1, e2)
              ganador = self.p1 if cmp == 1 else self.p2

              return ganador, apuesta_actual, ordago

          elif accion == "n":
              print(f"🚫 {turno.name} no quiere.")
              recompensa = apuesta_anterior if apuesta_actual > 2 else 1
              print(f"💎 {otro.name} gana {recompensa} piedra(s) por no querer.")
              return otro, recompensa, ordago

          elif accion == "o":
              apuesta_anterior = apuesta_actual
              print(f"🔥 ¡ÓRDAGO! {turno.name} apuesta TODO el juego (40 piedras).")
              respuesta = input(f"{otro.name}, ¿quieres el órdago? (s/n): ").strip().lower()
              
              if respuesta == "s":
                  print("🃏 Se acepta el órdago. ¡Se decide el juego completo ahora!")
                  cmp = self.compare_round(key, e1, e2)
                  ganador = self.p1 if cmp == 1 else self.p2
                  ordago = True
                  return ganador, 40, ordago
              else:
                  recompensa = apuesta_anterior if apuesta_actual > 2 else 1
                  print(f"❌ {otro.name} no quiere el órdago. {turno.name} gana {recompensa} piedra.")
                  return turno, recompensa, ordago

          else:
              print("⚠️ Opción no válida. Intenta de nuevo.")
              continue


    def play(self, piedras):

        self.deal()
        self.p2.show_hand()
        #self.mus_phase()
        e1 = HandEvaluator.evaluate_all(self.p1.hand)
        e2 = HandEvaluator.evaluate_all(self.p2.hand)
       
        results = {}

        for key in ['grande', 'chica', 'pares', 'juego']:
        # --- Condiciones especiales ---
          if key == 'pares':
            if e1['pares'][0] == 1 and e2['pares'][0] == 1:
                print("\nNingún jugador tiene pares. No se juega esta ronda.")
                continue
            elif e1['pares'][0] == 1 or e2['pares'][0] == 1:
                ganador = self.p1 if e1['pares'][0] > e2['pares'][0] else self.p2
                
                results['pares'] = f"{ganador.name} (pares automáticos)"
                print(f"\nSolo {ganador.name} tiene pares.")
                continue

          if key == 'juego':
            if e1['juego'][0] == 1 and e2['juego'][0] == 1:
                print("\nNingún jugador tiene juego. Se jugará al PUNTO.")
                key = 'punto'
            elif e1['juego'][0] == 1 or e2['juego'][0] == 1:
                ganador = self.p1 if e1['juego'][0] > e2['juego'][0] else self.p2
                
                results['juego'] = f"{ganador.name} (juego automático)"
                print(f"\nSolo {ganador.name} tiene juego.")
                continue

        # --- Apuestas con reenvido ---
          print(f"\nRonda de {key.upper()}")

          ganador, piedras_ganadas, ordago = self.betting_round(key, e1, e2)

          if ganador is None:
              print(f"🤝 No hubo apuesta en {key}. Nadie gana piedras.")
              continue

          if ordago:
              print(f"🏆 ¡{ganador.name} gana la partida por ÓRDAGO!")
              # Devolvemos inmediatamente con victoria total
              piedras[ganador.name] = float("inf")
              return piedras, {key: ganador.name}, (e1, e2)

          # Si fue una ronda normal:
          piedras[ganador.name] += piedras_ganadas
          results[key] = ganador.name
          print(f"💎 {ganador.name} gana {piedras_ganadas} piedra(s) en {key}.")

        return piedras, results, (e1,e2)
        # for key in ['grande','chica','pares','juego']:
        #     cmp = self.compare_round(key, e1, e2)
        #     if cmp==1:
        #         scores[self.p1.name]+=1
        #         results[key] = self.p1.name
        #     elif cmp==-1:
        #         scores[self.p2.name]+=1
        #         results[key] = self.p2.name
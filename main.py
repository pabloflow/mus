from ui.console_game import play_console
from ui.pygame_ui import play_gui

if __name__ == "__main__":
    print("🎮 Elige modo de juego:")
    print("1️⃣  Consola")
    print("2️⃣  Interfaz gráfica (Pygame)")
    choice = input("Opción (1/2): ").strip()

    if choice == "1":
        play_console()
    else:
        play_gui()

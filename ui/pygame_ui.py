import pygame   # pyright: ignore[reportMissingImports]


def play_gui():
    pygame.init()
    WIDTH, HEIGHT = 1024, 1024
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mus - GUI")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    FONT = pygame.font.SysFont("Arial", 28)

    # 🔹 Cargar imagen de fondo
    BACKGROUND = pygame.image.load("./assets/tapeteMaestro.png").convert()


    
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(30)

        # 🔹 Dibujar fondo cada frame
        WIN.blit(BACKGROUND, (0, 0))

        # (Opcional) Dibujar algo más encima
        
       

        # 🔹 Actualizar pantalla
        pygame.display.update()

        # 🔹 Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(f"Clic en {pos}")

    pygame.quit()

if __name__ == "__main__":
    play_gui()

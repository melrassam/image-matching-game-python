import pygame,sys
from button import Button
from Hard import HardGame
from Easy import EasyGame
from util import load_font, load_image

pygame.init()

def Menu():
    background = load_image("assets/GUI/Menu background.png")
    screen = pygame.display.set_mode((1000, 600))

    easy_btn = Button(
        image=load_image("assets/GUI/Play Rect.png"),
        pos=(500, 250), 
        text_input="Easy",
        font=load_font("assets/Font/BAUHS93.TTF", 75),
        base_color="#d7fcd4",
        hovering_color="White"
    )

    hard_btn = Button(
        image=load_image("assets/GUI/Quit Rect.png"),
        pos=(500, 400),
        text_input="Hard",
        font=load_font("assets/Font/BAUHS93.TTF", 75),
        base_color="#d7fcd4",
        hovering_color="White"
    )

    menu_text = load_font("assets/Font/BAUHS93.TTF", 100).render("MAIN MENU", True, "darkgreen")
    menu_rect = menu_text.get_rect(center=(500, 100))

    while True:
        screen.blit(background, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        screen.blit(menu_text, menu_rect)

        easy_btn.changeColor(menu_mouse_pos)
        easy_btn.update(screen)
        hard_btn.changeColor(menu_mouse_pos)
        hard_btn.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Clicking events
            elif event.type == pygame.MOUSEBUTTONUP:
                if easy_btn.checkForInput(menu_mouse_pos):
                    EasyGame()
                elif hard_btn.checkForInput(menu_mouse_pos):
                    HardGame()
        pygame.display.update()

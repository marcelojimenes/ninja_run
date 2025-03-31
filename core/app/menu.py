import pygame

from config.settings import *


class Menu:
    def __init__(self, screen, bg):
        self.screen = screen
        self.bg = bg
        self.running = True

    def run(self) -> int | None:
        selected_option = 0
        while self.running:
            self.draw(selected_option)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    selected_option = self.get_option(event, selected_option)
                    if event.key == pygame.K_RETURN:
                        return selected_option

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    def draw(self, selected_option: int) -> None:
        self.screen.blit(self.bg, (0, 0))
        self.render_static_text()
        self.render_menu_options(selected_option)
        pygame.display.flip()

    def render_static_text(self) -> None:
        title = [("Ninja", (WIDTH / 2, 80)), ("Run!", ((WIDTH / 2 + 50), 140))]
        for text, position in title:
            self.menu_text(80, text, BLACK, position)

    def render_menu_options(self, selected_option: int) -> None:
        for i, option in enumerate(MENU_OPTIONS):
            color = WHITE if i == selected_option else BLACK
            position = WIDTH / 2, 250 + 30 * i
            self.menu_text(30, option, color, position)

    def menu_text(self, size, text, color, position):
        font = pygame.font.Font(None, size)
        label = font.render(text, True, color)
        rect = label.get_rect(center=position)
        self.screen.blit(label, rect)

    @staticmethod
    def get_option(event, selected_option: int) -> int:
        if event.key == pygame.K_UP:
            return (selected_option - 1) % len(MENU_OPTIONS)
        elif event.key == pygame.K_DOWN:
            return (selected_option + 1) % len(MENU_OPTIONS)

        return selected_option
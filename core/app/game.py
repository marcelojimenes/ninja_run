import pygame
import random
from config.settings import *
from core.app.menu import Menu
from core.database.db import Database
from core.factories.entity import EntityFactory

NEW_GAME = 0
SCORE = 1
EXIT = 2

class Game:
    def __init__(self, db: Database):
        self.db = db
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Ninja Run!")

        self.clock = pygame.time.Clock()
        self.base_obstacle_speed = 3
        self.speed_increment = 0.3

        self.player = EntityFactory.create('player')
        self.obstacles = [
            EntityFactory.create(
                'obstacle',
                x=WIDTH,
                y=HEIGHT,
                width=20,
                height=50,
                speed=5
            )
        ]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.player.handle_input(event)

    def update_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.move()
            if obstacle.is_off_screen():
                obstacle.reset_position()
                self.player.increase_score()
                self.increase_difficulty()

    def draw(self):
        self.screen.fill(WHITE)
        pygame.draw.line(self.screen, BLACK, (0, HEIGHT-50), (WIDTH, HEIGHT-50),)
        player = self.player.draw(self.screen)

        for obstacle in self.obstacles:
            obs = obstacle.draw(self.screen)
            if obs.colliderect(player):
                self.game_over(self.player.get_score())
                break

        self.display_score()
        pygame.display.flip()

    def draw_text(self, text, size, x, y, color=BLACK):
        font = pygame.font.Font(None, size)
        label = font.render(text, True, color)
        self.screen.blit(label, (x, y))

    def display_score(self):
        self.draw_text(f"Score: {self.player.get_score()}", 36, 10, 10)

    def increase_difficulty(self):
        for obstacle in self.obstacles:
            obstacle.increase_speed(self.speed_increment)

    def start(self):
        while self.running:
            self.handle_events()
            self.update_obstacles()
            self.player.update()
            self.draw()
            self.clock.tick(60)

    def game_over(self, final_score):
        while self.running:
            self.screen.fill(WHITE)
            self.draw_text("Game Over", 48, (WIDTH // 2) - 150, 100, RED)
            self.draw_text(f"Your score: {final_score}", 36, (WIDTH // 2) - 150, 180, BLACK)
            self.draw_text("Press ENTER to register your score or ESC to quit.", 24, (WIDTH // 2) - 150, 250,BLUE)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    quit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        player_name = self.get_player_name()

                        if player_name.strip():
                            self.db.save_score(player_name, final_score)
                            self.show_ranking()
                            self.reset()
                            return

                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                        pygame.quit()
                        quit()

    def show_ranking(self):
        start_time = pygame.time.get_ticks()
        while self.running:
            self.screen.fill(WHITE)
            self.draw_text("Ranking - Top 5", 36, (WIDTH // 2) - 100, 50, RED)
            scores = self.db.fetch_scores()
            y_offset = 100

            for i, (name, score) in enumerate(scores[:5], 1):
                self.draw_text(f"{i}. {name}: {score}", 36, (WIDTH // 2) - 100, y_offset)
                y_offset += 40

            elapsed_time = pygame.time.get_ticks() - start_time
            remaining_time = max(0, 5000 - elapsed_time)

            self.draw_text(f"Returning in {remaining_time // 1000}s", 24, (WIDTH // 2) - 100, y_offset+50, BLUE)
            pygame.display.update()

            if remaining_time <= 0:
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    def get_player_name(self) -> str:
        name = ""
        while self.running:
            self.screen.fill(WHITE)
            self.draw_text("Please, enter your name:", 48, (WIDTH // 2) - 150, 100)
            self.draw_text(name, 36, (WIDTH // 2) - 150, 180, BLACK)
            self.draw_text("Press ENTER to confirm.", 24, (WIDTH // 2) - 150, 250, BLUE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if name.strip():
                            return name
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode

            pygame.display.update()

        return name

    def run(self):
        menu = Menu(self.screen)
        while self.running:
            opt = menu.run()
            if opt == NEW_GAME:
                self.reset()
                self.start()
            if opt == SCORE:
                self.show_ranking()
            elif opt == EXIT:
                pygame.quit()
                quit()

    def reset(self):
        self.player = EntityFactory.create('player')
        self.obstacles = [
            EntityFactory.create(
                'obstacle',
                x=WIDTH,
                y=HEIGHT,
                width=20,
                height=50,
                speed=5
            )
        ]
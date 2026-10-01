import random
import pygame
from game.button import ChoiceButton


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.choices = ["ROCK", "PAPER", "SCISSORS"]

        btn_w, btn_h = 130, 50
        gap = 20
        total_w = 3 * btn_w + 2 * gap
        start_x = (width - total_w) // 2
        btn_y = height - 85

        self.buttons = [
            ChoiceButton(
                "ROCK",
                pygame.Rect(start_x, btn_y, btn_w, btn_h),
                (160, 50, 50),
                (200, 70, 70),
            ),
            ChoiceButton(
                "PAPER",
                pygame.Rect(start_x + btn_w + gap, btn_y, btn_w, btn_h),
                (40, 100, 170),
                (60, 130, 210),
            ),
            ChoiceButton(
                "SCISSORS",
                pygame.Rect(start_x + 2 * (btn_w + gap), btn_y, btn_w, btn_h),
                (180, 140, 30),
                (220, 180, 50),
            ),
        ]

        self.player_choice = None
        self.cpu_choice = None
        self.result_text = "Make your move!"
        self.result_color = (220, 225, 235)

        self.player_score = 0
        self.cpu_score = 0

        # Task 2: First to X Wins
        self.target_score = 3
        self.game_over = False
        self.match_winner = None

        # Task 3: Track player's move history
        self.player_move_history = []

        # Task 4: Shake animation
        self.shake_duration = 600
        self.shake_start_time = 0
        self.shaking = False
        self.reveal_moves = True

        self.round_resolved_time = 0
        self.display_duration = 1800
        self.showing_result = False

        self.font_title = pygame.font.SysFont(None, 36)
        self.font_hud = pygame.font.SysFont(None, 26)
        self.font_arena = pygame.font.SysFont(None, 32)
        self.font_icon = pygame.font.SysFont(None, 24)

    def determine_winner(self, player, cpu):
        if player == cpu:
            return "TIE"

        # Task 1: Correct winner mappings
        rules = {
            ("ROCK", "SCISSORS"): "PLAYER",
            ("SCISSORS", "PAPER"): "PLAYER",
            ("PAPER", "ROCK"): "PLAYER",
            ("SCISSORS", "ROCK"): "CPU",
            ("PAPER", "SCISSORS"): "CPU",
            ("ROCK", "PAPER"): "CPU",
        }

        return rules.get((player, cpu), "TIE")

    def choose_cpu_move(self):
        # Task 3: Adaptive CPU
        if len(self.player_move_history) < 3:
            return random.choice(self.choices)

        move_counts = {
            choice: self.player_move_history.count(choice)
            for choice in self.choices
        }

        most_frequent_move = max(
            move_counts,
            key=move_counts.get
        )

        counter_moves = {
            "ROCK": "PAPER",
            "PAPER": "SCISSORS",
            "SCISSORS": "ROCK",
        }

        counter_move = counter_moves[most_frequent_move]

        if random.random() < 0.6:
            return counter_move

        return random.choice(self.choices)

    def play_round(self, choice):
        # Task 2: Do not allow another round after GAME_OVER
        if self.game_over:
            return

        # Task 3: Track player's move
        self.player_move_history.append(choice)
        self.player_choice = choice

        # Task 3: Adaptive CPU
        self.cpu_choice = self.choose_cpu_move()

        outcome = self.determine_winner(
            self.player_choice,
            self.cpu_choice
        )

        if outcome == "PLAYER":
            self.player_score += 1
            self.result_text = (
                f"You Win! {self.player_choice} beats {self.cpu_choice}."
            )
            self.result_color = (80, 230, 120)

        elif outcome == "CPU":
            self.cpu_score += 1
            self.result_text = (
                f"You Lose! {self.cpu_choice} beats {self.player_choice}."
            )
            self.result_color = (240, 80, 80)

        else:
            self.result_text = (
                f"It's a Draw! Both picked {self.player_choice}."
            )
            self.result_color = (240, 210, 80)

        # Task 2: Check match winner
        if self.player_score >= self.target_score:
            self.game_over = True
            self.match_winner = "PLAYER"
            self.result_text = "GAME OVER! PLAYER WINS! Press R to reset."
            self.result_color = (80, 230, 120)

        elif self.cpu_score >= self.target_score:
            self.game_over = True
            self.match_winner = "CPU"
            self.result_text = "GAME OVER! CPU WINS! Press R to reset."
            self.result_color = (240, 80, 80)

        # Task 4: Start shake animation before revealing moves
        self.shaking = True
        self.reveal_moves = False
        self.shake_start_time = pygame.time.get_ticks()

        self.showing_result = True
        self.round_resolved_time = pygame.time.get_ticks()

    def reset_match(self):
        # Task 2: Reset complete match
        self.player_score = 0
        self.cpu_score = 0

        self.player_choice = None
        self.cpu_choice = None

        self.result_text = "Make your move!"
        self.result_color = (220, 225, 235)

        self.game_over = False
        self.match_winner = None

        # Task 3: Reset adaptive CPU history
        self.player_move_history = []

        # Task 4: Reset animation
        self.shaking = False
        self.reveal_moves = True
        self.shake_start_time = 0

        self.showing_result = False
        self.round_resolved_time = 0

    def handle_event(self, event):
        # Task 2: Press R to reset after GAME_OVER
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            if self.game_over:
                self.reset_match()
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.game_over:
                return

            for btn in self.buttons:
                if btn.contains(event.pos):
                    self.play_round(btn.choice_name)
                    break

    def update(self):
        now = pygame.time.get_ticks()

        # Task 4: Handle shake animation
        if self.shaking:
            if now - self.shake_start_time >= self.shake_duration:
                self.shaking = False
                self.reveal_moves = True

        if self.game_over:
            return

        if (
            self.showing_result
            and not self.shaking
            and (now - self.round_resolved_time >= self.display_duration)
        ):
            self.player_choice = None
            self.cpu_choice = None
            self.result_text = "Make your move!"
            self.result_color = (190, 195, 205)
            self.showing_result = False
            self.reveal_moves = True

    def draw_rock(self, screen, x, y):
        pygame.draw.circle(
            screen,
            (170, 170, 180),
            (x, y),
            45
        )

        pygame.draw.circle(
            screen,
            (110, 110, 120),
            (x - 12, y - 12),
            8
        )

        pygame.draw.circle(
            screen,
            (110, 110, 120),
            (x + 15, y + 5),
            6
        )

    def draw_paper(self, screen, x, y):
        paper_rect = pygame.Rect(x - 35, y - 45, 70, 90)

        pygame.draw.rect(
            screen,
            (235, 235, 240),
            paper_rect,
            border_radius=8
        )

        pygame.draw.rect(
            screen,
            (120, 120, 130),
            paper_rect,
            width=3,
            border_radius=8
        )

        pygame.draw.line(
            screen,
            (160, 160, 170),
            (x - 20, y - 20),
            (x + 20, y - 20),
            3
        )

        pygame.draw.line(
            screen,
            (160, 160, 170),
            (x - 20, y),
            (x + 20, y),
            3
        )

        pygame.draw.line(
            screen,
            (160, 160, 170),
            (x - 20, y + 20),
            (x + 20, y + 20),
            3
        )

    def draw_scissors(self, screen, x, y):
        pygame.draw.line(
            screen,
            (220, 90, 90),
            (x - 35, y - 25),
            (x + 30, y + 30),
            8
        )

        pygame.draw.line(
            screen,
            (220, 90, 90),
            (x - 35, y + 25),
            (x + 30, y - 30),
            8
        )

        pygame.draw.circle(
            screen,
            (230, 180, 70),
            (x - 35, y - 25),
            12
        )

        pygame.draw.circle(
            screen,
            (230, 180, 70),
            (x - 35, y + 25),
            12
        )

    def draw_move_icon(self, screen, move, x, y):
        if move == "ROCK":
            self.draw_rock(screen, x, y)

        elif move == "PAPER":
            self.draw_paper(screen, x, y)

        elif move == "SCISSORS":
            self.draw_scissors(screen, x, y)

    def render(self, screen):
        screen.fill((24, 28, 36))

        title_surf = self.font_title.render(
            "Rock Paper Scissors",
            True,
            (245, 245, 245)
        )

        screen.blit(
            title_surf,
            (
                self.width // 2 - title_surf.get_width() // 2,
                14
            )
        )

        p_surf = self.font_hud.render(
            f"Player Score: {self.player_score}",
            True,
            (100, 180, 255)
        )

        c_surf = self.font_hud.render(
            f"CPU Score: {self.cpu_score}",
            True,
            (255, 120, 120)
        )

        screen.blit(p_surf, (35, 52))

        screen.blit(
            c_surf,
            (
                self.width - c_surf.get_width() - 35,
                52
            )
        )

        pygame.draw.line(
            screen,
            (45, 52, 66),
            (25, 82),
            (self.width - 25, 82),
            2
        )

        # Task 4: Move icon positions
        player_x = self.width // 2 - 130
        cpu_x = self.width // 2 + 130
        icon_y = 145

        if self.shaking:
            shake_offset_player = random.randint(-10, 10)
            shake_offset_cpu = random.randint(-10, 10)

            player_x += shake_offset_player
            cpu_x += shake_offset_cpu

            self.draw_move_icon(
                screen,
                "ROCK",
                player_x,
                icon_y
            )

            self.draw_move_icon(
                screen,
                "ROCK",
                cpu_x,
                icon_y
            )

            shake_text = self.font_arena.render(
                "SHAKING...",
                True,
                (240, 210, 80)
            )

            screen.blit(
                shake_text,
                (
                    self.width // 2 - shake_text.get_width() // 2,
                    215
                )
            )

        elif self.reveal_moves:
            if self.player_choice:
                self.draw_move_icon(
                    screen,
                    self.player_choice,
                    player_x,
                    icon_y
                )

            if self.cpu_choice:
                self.draw_move_icon(
                    screen,
                    self.cpu_choice,
                    cpu_x,
                    icon_y
                )

            if self.player_choice:
                player_label = self.font_icon.render(
                    f"You: {self.player_choice}",
                    True,
                    (225, 225, 230)
                )

                screen.blit(
                    player_label,
                    (
                        player_x - player_label.get_width() // 2,
                        200
                    )
                )

            if self.cpu_choice:
                cpu_label = self.font_icon.render(
                    f"CPU: {self.cpu_choice}",
                    True,
                    (225, 225, 230)
                )

                screen.blit(
                    cpu_label,
                    (
                        cpu_x - cpu_label.get_width() // 2,
                        200
                    )
                )

        res_surf = self.font_arena.render(
            self.result_text,
            True,
            self.result_color
        )

        screen.blit(
            res_surf,
            (
                self.width // 2 - res_surf.get_width() // 2,
                250
            )
        )

        for btn in self.buttons:
            btn.render(screen)
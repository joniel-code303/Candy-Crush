import pygame
import random
import sys

# Constants
# Candy Crush
WIDTH_CANDY, HEIGHT_CANDY = 600, 600
GRID_SIZE = 8
CANDY_SIZE = WIDTH_CANDY // GRID_SIZE
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (255, 20, 147)]

# Animation
WIDTH_ANIM, HEIGHT_ANIM = 600, 400
FPS = 60

# Graphical Elements
WIDTH_GUI, HEIGHT_GUI = 800, 600
BUTTON_COLOR = (0, 128, 255)
BUTTON_HOVER_COLOR = (0, 255, 255)

# Simple Platformer
WIDTH_PLATFORM, HEIGHT_PLATFORM = 800, 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

# Load sound effects
candy_crush_sound = pygame.mixer.Sound('sounds/candy_crush.wav')  # Replace with your sound file
move_sound = pygame.mixer.Sound('sounds/move.wav')                # Replace with your sound file
match_sound = pygame.mixer.Sound('sounds/match.wav')              # Sound when candies match
swap_sound = pygame.mixer.Sound('sounds/swap.wav')                # Sound when candies are swapped
fail_sound = pygame.mixer.Sound('sounds/fail.wav')                # Sound for invalid move

# Load background music
pygame.mixer.music.load('music/background_music.mp3') # integrar musica o sonido           # Replace with your music file
pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)

# Start background music
def start_background_music():
    pygame.mixer.music.play(-1)  # -1 means loop indefinitely

# Sound playing functions
def play_move_sound():
    move_sound.play()

def play_match_sound():
    match_sound.play()

def play_swap_sound():
    swap_sound.play()

def play_fail_sound():
    fail_sound.play()

# Generate a random game board for Candy Crush
def generate_board():
    return [[random.choice(COLORS) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Draw the board
def draw_board(board):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(screen_candy, board[row][col], 
                             (col * CANDY_SIZE, row * CANDY_SIZE, CANDY_SIZE, CANDY_SIZE))

# Level Class
class Level:
    def __init__(self, level_number, target_score, target_moves):
        self.level_number = level_number
        self.target_score = target_score
        self.moves_left = target_moves
        self.current_score = 0

    def is_completed(self):
        return self.current_score >= self.target_score or self.moves_left <= 0

    def update_score(self, points):
        self.current_score += points

    def use_move(self):
        if self.moves_left > 0:
            self.moves_left -= 1
        else:
            print("No moves left!")

# Game Class
class Game:
    def __init__(self):
        self.current_level = Level(1, target_score=1000, target_moves=20)

    def play_move(self, points_earned):
        if self.current_level.moves_left > 0:
            self.current_level.update_score(points_earned)
            self.current_level.use_move()

            if self.current_level.is_completed():
                print(f"Level {self.current_level.level_number} completed!")
                self.next_level()
        else:
            print("Game over! No moves left.")

    def next_level(self):
        self.current_level = Level(self.current_level.level_number + 1, 
                                   target_score=1000 * (self.current_level.level_number + 1), 
                                   target_moves=20)

# Check matches
def check_matches(board):
    matches = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if col < GRID_SIZE - 2 and board[row][col] == board[row][col + 1] == board[row][col + 2]:
                matches.append((row, col))
                matches.append((row, col + 1))
                matches.append((row, col + 2))

            if row < GRID_SIZE - 2 and board[row][col] == board[row + 1][col] == board[row + 2][col]:
                matches.append((row, col))
                matches.append((row + 1, col))
                matches.append((row + 2, col))

    return list(set(matches))  # Remove duplicates

# Clear matches by replacing candies
def clear_matches(board, matches):
    for (row, col) in matches:
        board[row][col] = random.choice(COLORS)  # Replace with new candy color

# Main functions
def main_candy_crush():
    global screen_candy
    screen_candy = pygame.display.set_mode((WIDTH_CANDY, HEIGHT_CANDY))
    pygame.display.set_caption("Candy Crush")
    start_background_music()

    clock = pygame.time.Clock()
    board = generate_board()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen_candy.fill((255, 255, 255))  # Clear screen
        draw_board(board)                     # Draw game board
        pygame.display.flip()                 # Update display
        clock.tick(60)                        # Frame rate

    pygame.quit()

def main_animation():
    screen_anim = pygame.display.set_mode((WIDTH_ANIM, HEIGHT_ANIM))
    pygame.display.set_caption("Animation Example")
    rect_x = 0
    rect_y = HEIGHT_ANIM // 2 - 25
    rect_width = 50
    rect_height = 50
    speed = 5
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move the rectangle
        rect_x += speed
        if rect_x > WIDTH_ANIM:
            rect_x = -rect_width  # Reset to the left side

        # Clear the screen
        screen_anim.fill((255, 255, 255))
        # Draw the rectangle
        pygame.draw.rect(screen_anim, (0, 0, 255), (rect_x, rect_y, rect_width, rect_height))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

def draw_button(text, x, y, width, height):
    mouse = pygame.mouse.get_pos()
    rect = pygame.Rect(x, y, width, height)

    # Change color if mouse is over the button
    color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse) else BUTTON_COLOR
    pygame.draw.rect(screen_gui, color, rect)

    # Draw button text
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    screen_gui.blit(text_surface, text_rect)

def main_graphical_elements():
    global screen_gui, font
    screen_gui = pygame.display.set_mode((WIDTH_GUI, HEIGHT_GUI))
    pygame.display.set_caption("Graphical Elements Example")
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen_gui.fill((255, 255, 255))  # Fill the screen with white
        draw_button("Click Me!", 350, 250, 100, 50)  # Draw a button

        # Draw text
        text_surface = font.render("Welcome to the Graphical Elements Example", True, (0, 0, 0))
        screen_gui.blit(text_surface, (150, 100))
        pygame.display.flip()

def main_platformer():
    screen_platform = pygame.display.set_mode((WIDTH_PLATFORM, HEIGHT_PLATFORM))
    pygame.display.set_caption("Simple Platformer")
    player_pos = [100, 500]
    player_size = 50
    player_velocity = 5
    is_jumping = False
    jump_count = 10

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_velocity
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH_PLATFORM - player_size:
            player_pos[0] += player_velocity

        if not is_jumping:
            if keys[pygame.K_SPACE]:
                is_jumping = True
        else:
            if jump_count >= -10:
                neg = 1
                if jump_count < 0:
                    neg = -1
                player_pos[1] -= (jump_count ** 2) * 0.5 * neg
                jump_count -= 1
            else:
                is_jumping = False
                jump_count = 10

        screen_platform.fill(WHITE)  # Clear screen
        pygame.draw.rect(screen_platform, BLUE, (player_pos[0], player_pos[1], player_size, player_size))  # Draw player
        pygame.display.flip()

# Run the main menu
def main_menu():
    while True:
        screen_menu = pygame.display.set_mode((WIDTH_GUI, HEIGHT_GUI))
        screen_menu.fill((255, 255, 255))
        font = pygame.font.Font(None, 74)
        title_surface = font.render("Game Menu", True, (0, 0, 0))
        screen_menu.blit(title_surface, (WIDTH_GUI // 4, HEIGHT_GUI // 8))

        draw_button("Candy Crush", 150, 200, 200, 50)
        draw_button("Animation", 150, 300, 200, 50)
        draw_button("Graphical Elements", 150, 400, 200, 50)
        draw_button("Platformer", 150, 500, 200, 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_x, mouse_y = event.pos
                    if 150 <= mouse_x <= 350 and 200 <= mouse_y <= 250:
                        main_candy_crush()
                    elif 150 <= mouse_x <= 350 and 300 <= mouse_y <= 350:
                        main_animation()
                    elif 150 <= mouse_x <= 350 and 400 <= mouse_y <= 450:
                        main_graphical_elements()
                    elif 150 <= mouse_x <= 350 and 500 <= mouse_y <= 550:
                        main_platformer()

# Start the game
main_menu()

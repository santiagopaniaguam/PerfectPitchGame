import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pitch Awareness Game")

# Define game colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Define game notes and their corresponding keys
NOTES = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
NOTE_KEYS = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

# Load sound effects
note_sounds = [pygame.mixer.Sound(f'sounds/note_{note.lower()}.wav') for note in NOTES]

# Difficulty levels
DIFFICULTY_LEVELS = [0.5, 1, 2]
current_difficulty = 1

# Pitch indicator dimensions
PITCH_INDICATOR_WIDTH = 100
PITCH_INDICATOR_HEIGHT = 400
PITCH_INDICATOR_X = WINDOW_WIDTH - PITCH_INDICATOR_WIDTH - 20
PITCH_INDICATOR_Y = WINDOW_HEIGHT // 2 - PITCH_INDICATOR_HEIGHT // 2

def show_difficulty_selection():
    game_window.fill(BLACK)
    font = pygame.font.Font(None, 48)
    text = font.render("Select Difficulty Level", True, WHITE)
    game_window.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 3 - text.get_height() // 2))

    for i, level in enumerate(DIFFICULTY_LEVELS):
        text = font.render(f"Level {i+1}: {level}x speed", True, WHITE)
        game_window.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 + i * 50))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 0
                elif event.key == pygame.K_2:
                    return 1
                elif event.key == pygame.K_3:
                    return 2

def game_loop(current_difficulty):
    score = 0
    game_over = False
    attempts_remaining = 3
    show_excellent_message = False

    # Generate 3 random notes
    dictated_notes = [random.choice(NOTES) for _ in range(3)]

    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                key_pressed = pygame.key.name(event.key).lower()
                if key_pressed in NOTE_KEYS:
                    note_index = NOTE_KEYS.index(key_pressed)
                    if NOTES[note_index] == dictated_notes[len(dictated_notes) - attempts_remaining]:
                        score += 1
                        play_sound(note_sounds[note_index])
                        attempts_remaining -= 1
                        if attempts_remaining == 0:
                            attempts_remaining = 3
                            dictated_notes = [random.choice(NOTES) for _ in range(3)]
                            show_excellent_message = True
                    else:
                        attempts_remaining -= 1
                        if attempts_remaining == 0:
                            game_over = True

        # Play the dictated notes
        for note in dictated_notes:
            play_sound(note_sounds[NOTES.index(note)])
            time.sleep(DIFFICULTY_LEVELS[current_difficulty])

        # Display the game screen
        game_window.fill(BLACK)

        # Draw the pitch indicator
        for i, note in enumerate(NOTES):
            rect_height = PITCH_INDICATOR_HEIGHT // len(NOTES)
            rect_y = PITCH_INDICATOR_Y + i * rect_height
            if note in dictated_notes:
                pygame.draw.rect(game_window, GREEN, (PITCH_INDICATOR_X, rect_y, PITCH_INDICATOR_WIDTH, rect_height))
            else:
                pygame.draw.rect(game_window, WHITE, (PITCH_INDICATOR_X, rect_y, PITCH_INDICATOR_WIDTH, rect_height))

        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, WHITE)
        game_window.blit(text, (10, 10))
        text = font.render(f"Attempts Remaining: {attempts_remaining}", True, WHITE)
        game_window.blit(text, (10, 40))
        text = font.render(f"Listen and press the corresponding key", True, WHITE)
        game_window.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2))

        if show_excellent_message:
            text = font.render("Excellent!", True, GREEN)
            game_window.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 + 50))
            show_excellent_message = False

        pygame.display.flip()

    # Game over screen
    game_window.fill(BLACK)
    font = pygame.font.Font(None, 48)
    text = font.render(f"Game Over! Final Score: {score}", True, WHITE)
    game_window.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2))
    text = font.render("Press Enter to play again", True, WHITE)
    game_window.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 + text.get_height()))
    pygame.display.flip()

    # Wait for the player to press Enter to play again
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                current_difficulty = show_difficulty_selection()
                game_loop(current_difficulty)

def play_sound(sound):
    sound.play()

current_difficulty = show_difficulty_selection()
game_loop(current_difficulty)   
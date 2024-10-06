import math
import random
import time
import pygame

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

INITIAL_TARGET_INCREMENT = 600  # Initial time interval for target appearance (milliseconds)
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30
BG_COLOR = (200, 162, 100)  # Light purple color
LIVES = 10
TOP_BAR_HEIGHT = 50
LABEL_FONT = pygame.font.SysFont("comicsans", 26)

class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "Red"
    SECOND_COLOR = "white"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)

    def collide(self, x, y):
        dis = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        return dis <= self.size

def draw(win, targets):
    win.fill(BG_COLOR)
    for target in targets:
        target.draw(win)

def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)
    return f"{minutes:02d}:{seconds:02d}.{milli}"

def draw_top_bar(win, elapsed_time, targets_pressed, misses, level):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 0.7, "black")
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 0.7, "black")
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 0.7, "black")
    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 0.7, "black")
    level_label = LABEL_FONT.render(f"Level: {level}", 0.7, "black")
    
    win.blit(time_label, (5, 5))
    win.blit(speed_label, (200, 5)) 
    win.blit(hits_label, (510, 5))
    win.blit(lives_label, (650, 5))
    win.blit(level_label, (400, 5))

def end_screen(win, elapsed_time, targets_pressed, clicks):
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white")
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "white")
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "white")
    accuracy = round(targets_pressed / clicks * 100, 1)
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")

    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(speed_label, (get_middle(speed_label), 200))
    win.blit(hits_label, (get_middle(hits_label), 300))
    win.blit(accuracy_label, (get_middle(accuracy_label), 400))

    # Draw restart button
    button_text = LABEL_FONT.render("Restart", True, "black")
    button_rect = pygame.Rect(get_middle(button_text), 500, button_text.get_width() + 20, button_text.get_height() + 10)
    pygame.draw.rect(win, "white", button_rect)
    win.blit(button_text, (button_rect.x + 10, button_rect.y + 5))

    pygame.display.update()

    # Event loop for end screen
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            # Check for mouse click to restart
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if button_rect.collidepoint(event.pos):  # Check if the click was within the button rect
                        run = False  # Exit the end screen to restart the game

def get_middle(surface):
    return WIDTH / 2 - surface.get_width() / 2

def main():
    run = True
    targets = []
    clock = pygame.time.Clock()
    
    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()
    level = 1
    target_increment = INITIAL_TARGET_INCREMENT  # Time between targets appearing
    pygame.time.set_timer(TARGET_EVENT, target_increment)

    while run:
        clock.tick(100)  # 100 FPS
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == TARGET_EVENT:
                if len(targets) < 4:  # Limit the number of targets on screen to 4
                    x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                    y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                    target = Target(x, y)
                    targets.append(target)
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                targets_pressed += 1

                # Increase difficulty every 10 successful hits
                if targets_pressed % 10 == 0:
                    level += 1
                    target_increment = int(target_increment * 0.9)  # Decrease spawn time by 10%
                    pygame.time.set_timer(TARGET_EVENT, target_increment)

        if misses >= LIVES:
            end_screen(WIN, elapsed_time, targets_pressed, clicks)
            # Reset variables for the new game
            targets.clear()
            targets_pressed = 0
            clicks = 0
            misses = 0
            start_time = time.time()
            level = 1
            target_increment = INITIAL_TARGET_INCREMENT
            pygame.time.set_timer(TARGET_EVENT, target_increment)

        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, targets_pressed, misses, level)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
    
#python3 /Users/stevengobran/VsCode/Aimbot.V3.py   

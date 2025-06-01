import pygame
import sys
import pickle

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Egyszerű Rajzoló Program")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = {
    "piros": (255, 0, 0),
    "zöld": (0, 255, 0),
    "kék": (0, 0, 255)
}

drawing = False
shape = "rectangle" 
fill = True
color = COLORS["piros"]
start_pos = None
elements = []

# Gombterületek
buttons = {
    "rectangle": pygame.Rect(10, 10, 100, 30),
    "circle": pygame.Rect(120, 10, 100, 30),
    "toggle_fill": pygame.Rect(230, 10, 120, 30),
    "save": pygame.Rect(360, 10, 80, 30),
    "load": pygame.Rect(450, 10, 80, 30),
    "color_red": pygame.Rect(540, 10, 30, 30),
    "color_green": pygame.Rect(580, 10, 30, 30),
    "color_blue": pygame.Rect(620, 10, 30, 30),
}


def draw_ui():
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, 50))
    pygame.draw.rect(screen, BLACK, buttons["rectangle"], 2)
    pygame.draw.rect(screen, BLACK, buttons["circle"], 2)
    pygame.draw.rect(screen, BLACK, buttons["toggle_fill"], 2)
    pygame.draw.rect(screen, BLACK, buttons["save"], 2)
    pygame.draw.rect(screen, BLACK, buttons["load"], 2)

    pygame.draw.rect(screen, (255, 0, 0), buttons["color_red"])
    pygame.draw.rect(screen, (0, 255, 0), buttons["color_green"])
    pygame.draw.rect(screen, (0, 0, 255), buttons["color_blue"])

    font = pygame.font.SysFont(None, 24)
    screen.blit(font.render("Téglalap", True, BLACK), (15, 15))
    screen.blit(font.render("Kör", True, BLACK), (135, 15))
    screen.blit(font.render("Kitöltés: " + ("Igen" if fill else "Nem"), True, BLACK), (235, 15))
    screen.blit(font.render("Mentés", True, BLACK), (365, 15))
    screen.blit(font.render("Betöltés", True, BLACK), (455, 15))


def draw_elements():
    for s, c, f, start, end in elements:
        if s == "rectangle":
            rect = pygame.Rect(*start, end[0]-start[0], end[1]-start[1])
            if f:
                pygame.draw.rect(screen, c, rect)
            else:
                pygame.draw.rect(screen, c, rect, 2)
        elif s == "circle":
            radius = int(((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5)
            if f:
                pygame.draw.circle(screen, c, start, radius)
            else:
                pygame.draw.circle(screen, c, start, radius, 2)


def save_drawing():
    with open("drawing.pkl", "wb") as f:
        pickle.dump(elements, f)


def load_drawing():
    global elements
    try:
        with open("drawing.pkl", "rb") as f:
            elements = pickle.load(f)
    except:
        print("Nem sikerült betölteni.")


running = True
while running:
    screen.fill(WHITE)
    draw_ui()
    draw_elements()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if my < 50:
                # UI gombok kezelése
                if buttons["rectangle"].collidepoint(mx, my):
                    shape = "rectangle"
                elif buttons["circle"].collidepoint(mx, my):
                    shape = "circle"
                elif buttons["toggle_fill"].collidepoint(mx, my):
                    fill = not fill
                elif buttons["save"].collidepoint(mx, my):
                    save_drawing()
                elif buttons["load"].collidepoint(mx, my):
                    load_drawing()
                elif buttons["color_red"].collidepoint(mx, my):
                    color = COLORS["piros"]
                elif buttons["color_green"].collidepoint(mx, my):
                    color = COLORS["zöld"]
                elif buttons["color_blue"].collidepoint(mx, my):
                    color = COLORS["kék"]
            else:
                drawing = True
                start_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP and drawing:
            drawing = False
            end_pos = event.pos
            elements.append((shape, color, fill, start_pos, end_pos))

    pygame.display.flip()

pygame.quit()
sys.exit()

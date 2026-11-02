
import pygame
import random
import math
import sys

# ============================================================
# STARBOUND ODYSSEY: VIRTUAL ARCADE EDITION
# Complete futuristic sci-fi RPG
# ============================================================

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1100, 750
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("STARBOUND ODYSSEY | Virtual Arcade")
clock = pygame.time.Clock()

# ============================================================
# COLOUR PALETTE
# ============================================================

BLACK = (3, 5, 12)
NAVY = (7, 12, 27)
PANEL = (13, 22, 42)
PANEL_LIGHT = (22, 37, 65)
WHITE = (240, 246, 255)
TEXT = (220, 235, 255)
SUBTEXT = (125, 150, 185)
BORDER = (42, 67, 100)
DIM_GRAY = (35, 48, 72)

CYAN = (0, 240, 255)
NEON_BLUE = (0, 145, 255)
GREEN = (35, 245, 145)
PURPLE = (185, 75, 255)
GOLD = (255, 210, 75)
RED = (255, 65, 90)
ORANGE = (255, 145, 50)
VOID_PURPLE = (130, 45, 220)

COLOR_OPTIONS = {
    "Cyan": CYAN,
    "Green": GREEN,
    "Gold": GOLD,
    "Purple": PURPLE,
    "Red": RED,
    "Orange": ORANGE
}

COLOR_NAMES = list(COLOR_OPTIONS.keys())

SHIP_CLASSES = {
    "Scout": {
        "hp": 130,
        "energy": 120,
        "credits": 200,
        "desc": "High agility and warp velocity",
        "speed": "HIGH"
    },
    "Destroyer": {
        "hp": 180,
        "energy": 80,
        "credits": 140,
        "desc": "Reinforced armor and heavy hull",
        "speed": "LOW"
    },
    "Cruiser": {
        "hp": 150,
        "energy": 100,
        "credits": 250,
        "desc": "Balanced shielding and wealthy",
        "speed": "MEDIUM"
    }
}

SHIP_NAMES = list(SHIP_CLASSES.keys())

# ============================================================
# FONTS
# ============================================================

FONT_CACHE = {}


def get_font(size, bold=False):
    key = (size, bold)

    if key not in FONT_CACHE:
        FONT_CACHE[key] = pygame.font.SysFont(
            "arial",
            size,
            bold=bold
        )

    return FONT_CACHE[key]


def text(
    message,
    x,
    y,
    size=18,
    color=WHITE,
    bold=False,
    center=False
):
    image = get_font(size, bold).render(
        str(message),
        True,
        color
    )

    rect = image.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    screen.blit(image, rect)
    return rect


# ============================================================
# UI HELPERS
# ============================================================

def panel(rect, border_color=CYAN, fill=PANEL):

    shadow = rect.move(4, 5)

    pygame.draw.rect(
        screen,
        (2, 5, 14),
        shadow,
        border_radius=14
    )

    surface = pygame.Surface(
        (rect.width, rect.height),
        pygame.SRCALPHA
    )

    pygame.draw.rect(
        surface,
        (*fill, 245),
        surface.get_rect(),
        border_radius=14
    )

    screen.blit(surface, rect.topleft)

    pygame.draw.rect(
        screen,
        border_color,
        rect,
        2,
        border_radius=14
    )

    length = 17

    corners = [
        (rect.left, rect.top, 1, 1),
        (rect.right, rect.top, -1, 1),
        (rect.left, rect.bottom, 1, -1),
        (rect.right, rect.bottom, -1, -1)
    ]

    for x, y, dx, dy in corners:

        pygame.draw.line(
            screen,
            WHITE,
            (x, y),
            (x + dx * length, y),
            2
        )

        pygame.draw.line(
            screen,
            WHITE,
            (x, y),
            (x, y + dy * length),
            2
        )


def section_title(label, x, y, color=CYAN):

    pygame.draw.line(
        screen,
        color,
        (x, y + 9),
        (x + 16, y + 9),
        3
    )

    text(
        label.upper(),
        x + 24,
        y,
        12,
        color,
        True
    )


def button(rect, label, color=NEON_BLUE, enabled=True):

    if not enabled:
        color = (48, 57, 77)

    pygame.draw.rect(
        screen,
        (3, 6, 16),
        rect.move(3, 4),
        border_radius=10
    )

    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=10
    )

    pygame.draw.rect(
        screen,
        WHITE if enabled else SUBTEXT,
        rect,
        1,
        border_radius=10
    )

    text(
        label,
        rect.centerx,
        rect.centery,
        15,
        WHITE,
        True,
        True
    )


def draw_bar(x, y, width, height, current, maximum, color):

    pygame.draw.rect(
        screen,
        (30, 43, 65),
        (x, y, width, height),
        border_radius=6
    )

    ratio = max(
        0,
        min(1, current / max(1, maximum))
    )

    fill_width = int(width * ratio)

    if fill_width > 0:

        pygame.draw.rect(
            screen,
            color,
            (x, y, fill_width, height),
            border_radius=6
        )

        pygame.draw.line(
            screen,
            WHITE,
            (x + 3, y + 2),
            (x + max(3, fill_width - 3), y + 2),
            1
        )

    pygame.draw.rect(
        screen,
        BORDER,
        (x, y, width, height),
        1,
        border_radius=6
    )


# ============================================================
# ANIMATED BACKGROUND
# ============================================================

STARS = [
    {
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "size": random.choice([1, 1, 2, 2, 3]),
        "speed": random.uniform(0.2, 1.2)
    }
    for _ in range(150)
]


def draw_starfield():

    for star in STARS:

        star["y"] += star["speed"]

        if star["y"] > HEIGHT:

            star["y"] = 0
            star["x"] = random.randint(0, WIDTH)

        brightness = int(
            120 + 100 * star["speed"] / 1.2
        )

        pygame.draw.circle(
            screen,
            (
                brightness // 2,
                brightness,
                255
            ),
            (
                int(star["x"]),
                int(star["y"])
            ),
            star["size"]
        )


def draw_background():

    for y in range(HEIGHT):

        ratio = y / HEIGHT

        color = (
            int(5 + ratio * 5),
            int(10 + ratio * 9),
            int(23 + ratio * 15)
        )

        pygame.draw.line(
            screen,
            color,
            (0, y),
            (WIDTH, y)
        )

    draw_starfield()

    grid = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    for x in range(0, WIDTH, 40):

        pygame.draw.line(
            grid,
            (30, 80, 120, 20),
            (x, 0),
            (x, HEIGHT)
        )

    for y in range(0, HEIGHT, 40):

        pygame.draw.line(
            grid,
            (30, 80, 120, 20),
            (0, y),
            (WIDTH, y)
        )

    screen.blit(grid, (0, 0))


def scanlines():

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    for y in range(0, HEIGHT, 5):

        pygame.draw.line(
            overlay,
            (0, 0, 0, 17),
            (0, y),
            (WIDTH, y)
        )

    screen.blit(overlay, (0, 0))


def glow_circle(x, y, radius, color):

    surface = pygame.Surface(
        (radius * 4, radius * 4),
        pygame.SRCALPHA
    )

    for r in range(radius * 2, 0, -5):

        alpha = int(
            35 * (1 - r / (radius * 2))
        )

        pygame.draw.circle(
            surface,
            (*color, alpha),
            (radius * 2, radius * 2),
            r
        )

    screen.blit(
        surface,
        (x - radius * 2, y - radius * 2)
    )


# ============================================================
# GALAXY MAPS
# ============================================================

MAIN_MAP = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W...1........W.........W..W",
    "W...WWWWWW...W..2......W..W",
    "W........W.............W..W",
    "W..S.....W......4......W..W",
    "W.........................B",
    "W.........................W",
    "W........W.............W..W",
    "W..3.....W.............W..W",
    "W........W......5......W..W",
    "W.........................W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWW"
]

POST_GAME_MAP = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W...A........W.........W..W",
    "W...WWWWWW...W..V......W..W",
    "W........W.............W..W",
    "W..S.....W......X......W..W",
    "W.........................Ω",
    "W.........................W",
    "W........W.............W..W",
    "W..4.....W.............W..W",
    "W........W......5......W..W",
    "W.........................W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWW"
]

MAP_X = 24
MAP_Y = 112
CELL = 32


# ============================================================
# PLAYER
# ============================================================

class Player:

    def __init__(self, name, color_name, ship_class):

        self.name = name
        self.color_name = color_name
        self.color = COLOR_OPTIONS[color_name]
        self.ship_class = ship_class

        stats = SHIP_CLASSES[ship_class]

        self.hp = stats["hp"]
        self.max_hp = stats["hp"]

        self.energy = stats["energy"]
        self.max_energy = stats["energy"]

        self.credits = stats["credits"]

        self.level = 1

        self.x = 2
        self.y = 5

        self.crew = []
        self.vault_codes = []

        self.inventory = {
            "Nano-Medpac": 3,
            "Energy Cell": 2
        }

        self.in_post_game = False
        self.ultimate_boss_defeated = False

        self.position_history = [
            (self.x, self.y)
        ]

        self.weapons = {
            "Pulse Blaster": {
                "base_atk": 22,
                "desc": "Standard starfleet sidearm"
            }
        }

        self.equipped_weapon = "Pulse Blaster"

    def move(self, dx, dy, world_map):

        nx = self.x + dx
        ny = self.y + dy

        if not (
            0 <= nx < len(world_map[0])
            and 0 <= ny < len(world_map)
        ):
            return

        if world_map[ny][nx] == "W":
            return

        self.x = nx
        self.y = ny

        self.position_history.append(
            (self.x, self.y)
        )

        if len(self.position_history) > 12:
            self.position_history.pop(0)

    def draw(self, current_crew):

        px = MAP_X + self.x * CELL
        py = MAP_Y + self.y * CELL

        pulse = abs(
            math.sin(pygame.time.get_ticks() / 250)
        )

        glow_size = int(7 + pulse * 5)

        glow_circle(
            px + CELL // 2,
            py + CELL // 2,
            glow_size,
            self.color
        )

        points = [
            (px + CELL // 2, py + 3),
            (px + CELL - 4, py + CELL - 6),
            (px + CELL // 2, py + CELL - 12),
            (px + 4, py + CELL - 6)
        ]

        pygame.draw.polygon(
            screen,
            self.color,
            points
        )

        pygame.draw.polygon(
            screen,
            WHITE,
            points,
            1
        )

        pygame.draw.ellipse(
            screen,
            (8, 20, 40),
            (px + 11, py + 10, 10, 12)
        )

        pygame.draw.ellipse(
            screen,
            CYAN,
            (px + 13, py + 12, 6, 7)
        )

        pygame.draw.circle(
            screen,
            ORANGE,
            (px + 10, py + CELL - 7),
            2
        )

        pygame.draw.circle(
            screen,
            ORANGE,
            (px + CELL - 10, py + CELL - 7),
            2
        )

        if (
            "Dr. Vex" in current_crew
            and len(self.position_history) >= 3
        ):

            vx, vy = self.position_history[-3]

            pygame.draw.circle(
                screen,
                GREEN,
                (
                    MAP_X + vx * CELL + CELL // 2,
                    MAP_Y + vy * CELL + CELL // 2
                ),
                6
            )

        if (
            "Sprocket" in current_crew
            and len(self.position_history) >= 6
        ):

            sx, sy = self.position_history[-6]

            pygame.draw.circle(
                screen,
                GOLD,
                (
                    MAP_X + sx * CELL + CELL // 2,
                    MAP_Y + sy * CELL + CELL // 2
                ),
                5
            )


# ============================================================
# LOADING SCREEN
# ============================================================

def loading_screen(message="INITIALIZING STARBOUND ODYSSEY..."):

    start = pygame.time.get_ticks()
    progress = 0

    while progress < 100:

        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(NAVY)
        draw_background()

        cx = WIDTH // 2
        cy = HEIGHT // 2 - 35

        angle = pygame.time.get_ticks() / 400

        for radius, color, offset in [
            (75, CYAN, 0),
            (100, PURPLE, 1.5),
            (125, NEON_BLUE, 3)
        ]:

            pygame.draw.circle(
                screen,
                color,
                (cx, cy),
                radius,
                1
            )

            px = cx + math.cos(angle + offset) * radius
            py = cy + math.sin(angle + offset) * radius

            pygame.draw.circle(
                screen,
                color,
                (int(px), int(py)),
                5
            )

        text(
            "STARBOUND ODYSSEY",
            cx,
            cy,
            35,
            WHITE,
            True,
            True
        )

        text(
            "VIRTUAL GALAXY SIMULATOR",
            cx,
            cy + 155,
            14,
            CYAN,
            True,
            True
        )

        box = pygame.Rect(
            cx - 250,
            cy + 190,
            500,
            105
        )

        panel(box, NEON_BLUE)

        text(
            message,
            cx,
            box.y + 25,
            15,
            WHITE,
            True,
            True
        )

        draw_bar(
            box.x + 30,
            box.y + 55,
            440,
            13,
            progress,
            100,
            GREEN
        )

        text(
            f"{progress}%",
            cx,
            box.y + 83,
            13,
            CYAN,
            True,
            True
        )

        scanlines()
        pygame.display.flip()

        progress = min(
            100,
            int((pygame.time.get_ticks() - start) / 22)
        )


# ============================================================
# START SCREEN / CHARACTER CREATION
# ============================================================

def start_screen():

    name = "Commander Rex"
    color_index = 0
    ship_index = 0
    step = 0

    running = True

    while running:

        clock.tick(FPS)

        screen.fill(NAVY)
        draw_background()

        box = pygame.Rect(
            110,
            65,
            WIDTH - 220,
            HEIGHT - 130
        )

        panel(box, CYAN)

        text(
            "COMMANDER FORGE",
            WIDTH // 2,
            120,
            35,
            GOLD,
            True,
            True
        )

        text(
            "CREATE YOUR IDENTITY IN THE GALAXY",
            WIDTH // 2,
            162,
            13,
            SUBTEXT,
            True,
            True
        )

        # Progress indicators
        for i in range(3):

            color = CYAN if i <= step else BORDER

            pygame.draw.circle(
                screen,
                color,
                (450 + i * 100, 220),
                12
            )

            if i < 2:

                pygame.draw.line(
                    screen,
                    color,
                    (462 + i * 100, 220),
                    (538 + i * 100, 220),
                    3
                )

        if step == 0:

            text(
                "STEP 01 / COMMANDER ID",
                WIDTH // 2,
                295,
                18,
                CYAN,
                True,
                True
            )

            text(
                "Enter your commander call sign",
                WIDTH // 2,
                355,
                23,
                WHITE,
                True,
                True
            )

            name_box = pygame.Rect(
                340,
                400,
                420,
                55
            )

            panel(name_box, NEON_BLUE)

            text(
                name + "_",
                WIDTH // 2,
                428,
                21,
                GOLD,
                True,
                True
            )

            text(
                "Type your name. BACKSPACE deletes.",
                WIDTH // 2,
                475,
                12,
                SUBTEXT,
                False,
                True
            )

        elif step == 1:

            color_name = COLOR_NAMES[color_index]
            color = COLOR_OPTIONS[color_name]

            text(
                "STEP 02 / HOLOGRAM COLOUR",
                WIDTH // 2,
                295,
                18,
                CYAN,
                True,
                True
            )

            text(
                "Choose your ship's identity colour",
                WIDTH // 2,
                355,
                23,
                WHITE,
                True,
                True
            )

            glow_circle(
                WIDTH // 2,
                440,
                42,
                color
            )

            pygame.draw.circle(
                screen,
                color,
                (WIDTH // 2, 440),
                33
            )

            text(
                color_name.upper(),
                WIDTH // 2,
                500,
                19,
                color,
                True,
                True
            )

            text(
                "Use LEFT and RIGHT to browse",
                WIDTH // 2,
                540,
                13,
                SUBTEXT,
                False,
                True
            )

        else:

            ship_name = SHIP_NAMES[ship_index]
            stats = SHIP_CLASSES[ship_name]

            text(
                "STEP 03 / STARSHIP CONFIGURATION",
                WIDTH // 2,
                295,
                18,
                CYAN,
                True,
                True
            )

            text(
                ship_name.upper(),
                WIDTH // 2,
                360,
                28,
                GOLD,
                True,
                True
            )

            text(
                stats["desc"],
                WIDTH // 2,
                402,
                15,
                WHITE,
                False,
                True
            )

            text(
                f"HULL: {stats['hp']}    ENERGY: {stats['energy']}",
                WIDTH // 2,
                455,
                17,
                GREEN,
                True,
                True
            )

            text(
                f"STARTING CREDITS: {stats['credits']}",
                WIDTH // 2,
                490,
                15,
                GOLD,
                True,
                True
            )

            text(
                "Use LEFT and RIGHT to browse",
                WIDTH // 2,
                540,
                13,
                SUBTEXT,
                False,
                True
            )

        button(
            pygame.Rect(380, 590, 340, 50),
            "CONTINUE  >",
            NEON_BLUE
        )

        text(
            "ENTER: CONTINUE     ESC: BACK",
            WIDTH // 2,
            665,
            12,
            SUBTEXT,
            True,
            True
        )

        scanlines()
        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    if step > 0:
                        step -= 1

                elif event.key == pygame.K_RETURN:

                    if step < 2:
                        step += 1
                    else:
                        running = False

                elif event.key == pygame.K_LEFT:

                    if step == 1:
                        color_index = (
                            color_index - 1
                        ) % len(COLOR_NAMES)

                    elif step == 2:
                        ship_index = (
                            ship_index - 1
                        ) % len(SHIP_NAMES)

                elif event.key == pygame.K_RIGHT:

                    if step == 1:
                        color_index = (
                            color_index + 1
                        ) % len(COLOR_NAMES)

                    elif step == 2:
                        ship_index = (
                            ship_index + 1
                        ) % len(SHIP_NAMES)

                elif event.key == pygame.K_BACKSPACE:

                    if step == 0:
                        name = name[:-1]

                elif step == 0:

                    if (
                        len(name) < 16
                        and event.unicode.isprintable()
                        and event.unicode not in "\r\n\t"
                    ):
                        name += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:

                if pygame.Rect(
                    380, 590, 340, 50
                ).collidepoint(event.pos):

                    if step < 2:
                        step += 1
                    else:
                        running = False

    loading_screen("ESTABLISHING NEURAL LINK...")

    return Player(
        name.strip() or "Commander Rex",
        COLOR_NAMES[color_index],
        SHIP_NAMES[ship_index]
    )


# ============================================================
# COMPANION CUTSCENE
# ============================================================

def companion_cutscene(companion, description):

    start = pygame.time.get_ticks()

    color = (
        GREEN if companion == "Dr. Vex"
        else GOLD
    )

    while pygame.time.get_ticks() - start < 1600:

        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(NAVY)
        draw_background()

        box = pygame.Rect(
            110,
            250,
            WIDTH - 220,
            220
        )

        panel(box, color)

        glow_circle(
            WIDTH // 2,
            320,
            40,
            color
        )

        pygame.draw.circle(
            screen,
            color,
            (WIDTH // 2, 320),
            25
        )

        text(
            f"VIRTUAL PROTOCOL: {companion.upper()}",
            WIDTH // 2,
            380,
            27,
            color,
            True,
            True
        )

        text(
            description,
            WIDTH // 2,
            425,
            16,
            WHITE,
            False,
            True
        )

        scanlines()
        pygame.display.flip()

# ============================================================
# STARBOUND ODYSSEY: ANIMATED COMBAT SYSTEM
# ============================================================

def draw_enemy_art(x, y, enemy_name):
    """Draw an enemy ship with a glowing core."""

    glow_circle(int(x), int(y), 55, RED)

    points = [
        (int(x), int(y - 45)),
        (int(x + 55), int(y)),
        (int(x + 25), int(y + 30)),
        (int(x), int(y + 45)),
        (int(x - 25), int(y + 30)),
        (int(x - 55), int(y))
    ]

    pygame.draw.polygon(
        screen,
        (75, 30, 54),
        points
    )

    pygame.draw.polygon(
        screen,
        RED,
        points,
        2
    )

    pygame.draw.circle(
        screen,
        ORANGE,
        (int(x), int(y)),
        12
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (int(x), int(y)),
        5
    )


def draw_player_battle_art(x, y, color):
    """Draw the player's ship."""

    x = int(x)
    y = int(y)

    # Engine glow
    glow_circle(x - 30, y, 28, color)

    # Engine flame
    flame_length = random.randint(12, 23)

    pygame.draw.polygon(
        screen,
        ORANGE,
        [
            (x - 35, y - 8),
            (x - 35 - flame_length, y),
            (x - 35, y + 8)
        ]
    )

    # Main ship
    ship_points = [
        (x - 38, y),
        (x - 12, y - 22),
        (x + 29, y - 15),
        (x + 48, y),
        (x + 29, y + 15),
        (x - 12, y + 22)
    ]

    pygame.draw.polygon(
        screen,
        color,
        ship_points
    )

    pygame.draw.polygon(
        screen,
        WHITE,
        ship_points,
        2
    )

    # Cockpit
    pygame.draw.polygon(
        screen,
        NEON_BLUE,
        [
            (x - 8, y - 10),
            (x + 17, y - 7),
            (x + 29, y),
            (x + 17, y + 7),
            (x - 8, y + 10)
        ]
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (x + 13, y),
        3
    )


def draw_energy_projectile(x, y, color=CYAN, radius=8):
    """Draw a glowing projectile."""

    x = int(x)
    y = int(y)

    glow_circle(x, y, radius + 8, color)

    pygame.draw.circle(
        screen,
        color,
        (x, y),
        radius
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (x, y),
        max(2, radius // 2)
    )


def animate_battle_action(player, enemy_name, direction="player",
                          color=None):
    """
    Animate a ship attacking.

    direction='player': player attacks enemy.
    direction='enemy': enemy attacks player.
    """

    duration = 0.65
    start_time = pygame.time.get_ticks()

    player_home_x = 180
    player_home_y = 270

    enemy_home_x = 480
    enemy_home_y = 235

    projectile_color = color or player.color

    while True:

        clock.tick(FPS)

        elapsed = (
            pygame.time.get_ticks() - start_time
        ) / 1000.0

        progress = min(1.0, elapsed / duration)

        if progress >= 1.0:
            break

        screen.fill(NAVY)
        draw_background()

        text(
            "TACTICAL COMBAT SYSTEM",
            WIDTH // 2,
            35,
            27,
            RED,
            True,
            True
        )

        text(
            player.name,
            player_home_x,
            125,
            17,
            player.color,
            True,
            True
        )

        text(
            enemy_name,
            enemy_home_x,
            125,
            17,
            RED,
            True,
            True
        )

        # Idle movement
        bob = math.sin(elapsed * 7) * 5

        player_x = player_home_x
        player_y = player_home_y + bob

        enemy_x = enemy_home_x
        enemy_y = enemy_home_y + bob

        # Lunge and recoil
        if direction == "player":

            player_x += math.sin(progress * math.pi) * 85

            if progress > 0.60:
                recoil_progress = (progress - 0.60) / 0.40

                enemy_x += (
                    math.sin(recoil_progress * math.pi) * 22
                )

        else:

            enemy_x -= math.sin(progress * math.pi) * 70

            if progress > 0.60:
                recoil_progress = (progress - 0.60) / 0.40

                player_x -= (
                    math.sin(recoil_progress * math.pi) * 25
                )

        # Draw both ships
        draw_player_battle_art(
            player_x,
            player_y,
            player.color
        )

        draw_enemy_art(
            enemy_x,
            enemy_y,
            enemy_name
        )

        # Projectile travels between the ships
        if 0.15 <= progress <= 0.82:

            projectile_progress = (
                (progress - 0.15) / 0.67
            )

            if direction == "player":

                projectile_x = (
                    player_home_x + 45
                    + (enemy_home_x - player_home_x - 45)
                    * projectile_progress
                )

                projectile_y = (
                    player_home_y
                    - math.sin(projectile_progress * math.pi) * 35
                )

            else:

                projectile_x = (
                    enemy_home_x - 45
                    - (enemy_home_x - player_home_x - 45)
                    * projectile_progress
                )

                projectile_y = (
                    enemy_home_y
                    + math.sin(projectile_progress * math.pi) * 35
                )

            draw_energy_projectile(
                projectile_x,
                projectile_y,
                projectile_color
            )

        # Impact effect
        if progress > 0.75:

            impact_progress = min(
                1.0,
                (progress - 0.75) / 0.25
            )

            if direction == "player":
                impact_x = enemy_home_x
                impact_y = enemy_home_y
            else:
                impact_x = player_home_x
                impact_y = player_home_y

            pygame.draw.circle(
                screen,
                projectile_color,
                (int(impact_x), int(impact_y)),
                int(10 + impact_progress * 30),
                3
            )

        if direction == "player":

            text(
                "WEAPON DISCHARGE!",
                WIDTH // 2,
                390,
                19,
                projectile_color,
                True,
                True
            )

        else:

            text(
                "INCOMING HOSTILE FIRE!",
                WIDTH // 2,
                390,
                19,
                RED,
                True,
                True
            )

        scanlines()
        pygame.display.flip()

        # Keep the window responsive during animation.
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def combat_screen(player, enemy_name, enemy_hp):

    enemy_max = enemy_hp

    message = f"TACTICAL ENGAGEMENT: {enemy_name}"

    flash = 0

    while True:

        clock.tick(FPS)

        # ----------------------------------------------------
        # BACKGROUND
        # ----------------------------------------------------

        screen.fill(NAVY)
        draw_background()

        elapsed = pygame.time.get_ticks() / 1000.0

        text(
            "TACTICAL COMBAT SYSTEM",
            WIDTH // 2,
            24,
            27,
            RED,
            True,
            True
        )

        # ----------------------------------------------------
        # ENEMY STATUS
        # ----------------------------------------------------

        enemy_box = pygame.Rect(
            625, 65, 420, 150
        )

        panel(enemy_box, RED)

        text(
            enemy_name,
            enemy_box.x + 20,
            enemy_box.y + 17,
            20,
            WHITE,
            True
        )

        text(
            f"INTEGRITY: {max(0, enemy_hp)} / {enemy_max}",
            enemy_box.x + 20,
            enemy_box.y + 55,
            13,
            SUBTEXT,
            True
        )

        draw_bar(
            enemy_box.x + 20,
            enemy_box.y + 85,
            375,
            14,
            max(0, enemy_hp),
            enemy_max,
            RED
        )

        # ----------------------------------------------------
        # MOVING ENEMY SHIP
        # ----------------------------------------------------

        enemy_bob = math.sin(elapsed * 3.5) * 7
        enemy_sway = math.sin(elapsed * 1.8) * 10

        draw_enemy_art(
            480 + enemy_sway,
            235 + enemy_bob,
            enemy_name
        )

        # ----------------------------------------------------
        # MOVING PLAYER SHIP
        # ----------------------------------------------------

        player_bob = math.sin(elapsed * 4.0 + 1.5) * 6
        player_sway = math.sin(elapsed * 2.2) * 8

        draw_player_battle_art(
            180 + player_sway,
            265 + player_bob,
            player.color
        )

        # ----------------------------------------------------
        # PLAYER STATUS
        # ----------------------------------------------------

        player_box = pygame.Rect(
            35, 340, 450, 195
        )

        panel(player_box, player.color)

        text(
            player.name,
            player_box.x + 20,
            player_box.y + 15,
            22,
            player.color,
            True
        )

        text(
            f"{player.ship_class.upper()} CLASS",
            player_box.x + 20,
            player_box.y + 45,
            12,
            SUBTEXT,
            True
        )

        text(
            f"HULL: {player.hp}/{player.max_hp}",
            player_box.x + 20,
            player_box.y + 78,
            13,
            WHITE
        )

        draw_bar(
            player_box.x + 20,
            player_box.y + 102,
            390,
            13,
            player.hp,
            player.max_hp,
            GREEN
        )

        text(
            f"ENERGY: {player.energy}/{player.max_energy}",
            player_box.x + 20,
            player_box.y + 127,
            13,
            WHITE
        )

        draw_bar(
            player_box.x + 20,
            player_box.y + 151,
            390,
            12,
            player.energy,
            player.max_energy,
            NEON_BLUE
        )

        # ----------------------------------------------------
        # COMBAT COMMANDS
        # ----------------------------------------------------

        command_box = pygame.Rect(
            560, 340, 485, 195
        )

        panel(command_box, CYAN)

        section_title(
            "COMBAT COMMANDS",
            command_box.x + 20,
            command_box.y + 15
        )

        commands = [
            "[1] FIRE WEAPON",
            "[2] SHIELD GENERATOR",
            "[3] DR. VEX MEDICAL OVERHAUL",
            "[4] SPROCKET OVERCLOCK",
            "[5] USE NANO-MEDPAC",
            "[6] USE ENERGY CELL"
        ]

        for i, command in enumerate(commands):

            color = WHITE

            if i == 2 and "Dr. Vex" not in player.crew:
                color = SUBTEXT

            if i == 3 and "Sprocket" not in player.crew:
                color = SUBTEXT

            screen.blit(
                get_font(13, True).render(
                    command,
                    True,
                    color
                ),
                (
                    command_box.x + 20,
                    command_box.y + 43 + i * 23
                )
            )

        # ----------------------------------------------------
        # MESSAGE PANEL
        # ----------------------------------------------------

        msg_box = pygame.Rect(
            35, 560, WIDTH - 70, 95
        )

        panel(msg_box, WHITE)

        text(
            message,
            WIDTH // 2,
            msg_box.centery,
            17,
            WHITE,
            False,
            True
        )

        if flash > 0:

            overlay = pygame.Surface(
                (WIDTH, HEIGHT),
                pygame.SRCALPHA
            )

            overlay.fill((255, 0, 0, 40))

            screen.blit(overlay, (0, 0))

            flash -= 1

        scanlines()
        pygame.display.flip()

        # ----------------------------------------------------
        # INPUT
        # ----------------------------------------------------

        action = None

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    action = 1

                elif event.key == pygame.K_2:
                    action = 2

                elif event.key == pygame.K_3:
                    action = 3

                elif event.key == pygame.K_4:
                    action = 4

                elif event.key == pygame.K_5:
                    action = 5

                elif event.key == pygame.K_6:
                    action = 6

        if action is None:
            continue

        enemy_turn = True

        # ----------------------------------------------------
        # 1. FIRE WEAPON
        # ----------------------------------------------------

        if action == 1:

            animate_battle_action(
                player,
                enemy_name,
                "player",
                player.color
            )

            attack = player.weapons[
                player.equipped_weapon
            ]["base_atk"]

            damage = random.randint(
                max(1, attack - 4),
                attack + 12
            )

            enemy_hp -= damage

            message = (
                f"{player.equipped_weapon} fired! "
                f"{damage} damage dealt."
            )

        # ----------------------------------------------------
        # 2. SHIELD GENERATOR
        # ----------------------------------------------------

        elif action == 2:

            if player.energy >= 15:

                player.energy -= 15

                restored = min(
                    45,
                    player.max_hp - player.hp
                )

                player.hp += restored

                message = (
                    f"Shield generator activated. "
                    f"{restored} hull restored."
                )

            else:

                message = "Insufficient energy reserves."
                enemy_turn = False

        # ----------------------------------------------------
        # 3. DR. VEX
        # ----------------------------------------------------

        elif action == 3:

            if "Dr. Vex" in player.crew:

                companion_cutscene(
                    "Dr. Vex",
                    "Deploying emergency nanite restoration."
                )

                restored = player.max_hp - player.hp

                player.hp = player.max_hp

                message = (
                    f"Dr. Vex restored {restored} HP!"
                )

            else:

                message = "Dr. Vex has not joined your crew."
                enemy_turn = False

        # ----------------------------------------------------
        # 4. SPROCKET OVERCLOCK
        # ----------------------------------------------------

        elif action == 4:

            if "Sprocket" in player.crew:

                animate_battle_action(
                    player,
                    enemy_name,
                    "player",
                    PURPLE
                )

                damage = (
                    player.weapons[
                        player.equipped_weapon
                    ]["base_atk"] * 2
                )

                enemy_hp -= damage

                message = (
                    f"Sprocket's overclock strike dealt "
                    f"{damage} damage!"
                )

            else:

                message = "Sprocket has not joined your crew."
                enemy_turn = False

        # ----------------------------------------------------
        # 5. NANO-MEDPAC
        # ----------------------------------------------------

        elif action == 5:

            if player.inventory["Nano-Medpac"] > 0:

                player.inventory["Nano-Medpac"] -= 1

                restored = min(
                    65,
                    player.max_hp - player.hp
                )

                player.hp += restored

                message = (
                    f"Nano-Medpac used. "
                    f"{restored} HP restored."
                )

            else:

                message = "You have no Nano-Medpacs."
                enemy_turn = False

        # ----------------------------------------------------
        # 6. ENERGY CELL
        # ----------------------------------------------------

        elif action == 6:

            if player.inventory["Energy Cell"] > 0:

                player.inventory["Energy Cell"] -= 1

                restored = min(
                    40,
                    player.max_energy - player.energy
                )

                player.energy += restored

                message = (
                    f"Energy cell used. "
                    f"{restored} energy restored."
                )

            else:

                message = "No energy cells available."
                enemy_turn = False

        # ----------------------------------------------------
        # ENEMY DEFEATED
        # ----------------------------------------------------

        if enemy_hp <= 0:

            screen.fill(NAVY)
            draw_background()

            panel(
                pygame.Rect(160, 240, 780, 220),
                GOLD
            )

            text(
                "SECTOR CLEARED",
                WIDTH // 2,
                310,
                38,
                GOLD,
                True,
                True
            )

            text(
                f"{enemy_name} has been defeated.",
                WIDTH // 2,
                370,
                17,
                WHITE,
                False,
                True
            )

            text(
                "+140 CREDITS     +1 LEVEL",
                WIDTH // 2,
                410,
                17,
                GREEN,
                True,
                True
            )

            pygame.display.flip()
            pygame.time.delay(1800)

            player.credits += 140
            player.level += 1

            return True

        # ----------------------------------------------------
        # ENEMY COUNTERATTACK
        # ----------------------------------------------------

        if enemy_turn:

            animate_battle_action(
                player,
                enemy_name,
                "enemy",
                RED
            )

            damage = random.randint(18, 30)

            player.hp -= damage

            flash = 7

            message += (
                f" Enemy counterattack: {damage} damage!"
            )

            # ------------------------------------------------
            # PLAYER DEFEATED
            # ------------------------------------------------

            if player.hp <= 0:

                player.hp = 0

                screen.fill(NAVY)
                draw_background()

                panel(
                    pygame.Rect(160, 240, 780, 220),
                    RED
                )

                text(
                    "SIMULATION FAILED",
                    WIDTH // 2,
                    310,
                    36,
                    RED,
                    True,
                    True
                )

                text(
                    "Your ship has sustained critical damage.",
                    WIDTH // 2,
                    375,
                    17,
                    WHITE,
                    False,
                    True
                )

                pygame.display.flip()
                pygame.time.delay(2000)

                return False
# ============================================================
# STARBASE MARKET
# ============================================================

def market_screen(player):

    message = "Welcome to Starbase 7. Select a transaction."

    running = True

    while running:

        clock.tick(FPS)

        screen.fill(NAVY)
        draw_background()

        box = pygame.Rect(
            75,
            40,
            WIDTH - 150,
            HEIGHT - 80
        )

        panel(box, NEON_BLUE)

        text(
            "STARBASE 7",
            WIDTH // 2,
            78,
            34,
            GOLD,
            True,
            True
        )

        text(
            "VIRTUAL TRADING BAY",
            WIDTH // 2,
            112,
            13,
            CYAN,
            True,
            True
        )

        text(
            f"CREDITS: {player.credits}",
            WIDTH // 2,
            150,
            18,
            GREEN,
            True,
            True
        )

        options = [
            ("1", "Recruit Dr. Vex", "70 CR", GREEN),
            ("2", "Recruit Sprocket", "85 CR", GOLD),
            ("3", "Purchase Nano-Medpac", "25 CR", WHITE),
            ("4", "Purchase / Equip Plasma Blade", "90 CR", WHITE),
            ("5", "Purchase / Equip Quantum Rifle", "130 CR", WHITE),
            ("6", "Purchase / Equip Void Cannon", "220 CR", PURPLE),
            ("7", "Return to Starship Bridge", "", RED)
        ]

        for i, (key, label, cost, color) in enumerate(options):

            y = 205 + i * 43

            option_rect = pygame.Rect(
                140,
                y,
                820,
                34
            )

            pygame.draw.rect(
                screen,
                PANEL_LIGHT,
                option_rect,
                border_radius=7
            )

            text(
                f"[{key}]",
                160,
                y + 7,
                14,
                CYAN,
                True
            )

            text(
                label,
                210,
                y + 7,
                14,
                color,
                True
            )

            text(
                cost,
                870,
                y + 7,
                13,
                GOLD,
                True
            )

        # Inventory summary
        info = pygame.Rect(
            140,
            520,
            820,
            55
        )

        panel(info, PURPLE)

        text(
            f"CREW: {', '.join(player.crew) if player.crew else 'None'}",
            160,
            535,
            13,
            GREEN
        )

        text(
            f"MEDPACS: {player.inventory['Nano-Medpac']}",
            570,
            535,
            13,
            WHITE
        )

        # Message
        msg_box = pygame.Rect(
            140,
            600,
            820,
            55
        )

        panel(msg_box, CYAN)

        text(
            message,
            msg_box.centerx,
            msg_box.centery,
            14,
            WHITE,
            False,
            True
        )

        text(
            "PRESS 1-7 TO SELECT     ESC TO RETURN",
            WIDTH // 2,
            680,
            12,
            SUBTEXT,
            True,
            True
        )

        scanlines()
        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key in (
                    pygame.K_ESCAPE,
                    pygame.K_7
                ):
                    running = False

                elif event.key == pygame.K_1:

                    if "Dr. Vex" in player.crew:

                        message = "Dr. Vex is already recruited."

                    elif player.credits >= 70:

                        player.credits -= 70
                        player.crew.append("Dr. Vex")

                        player.max_hp += 30
                        player.hp = player.max_hp

                        message = (
                            "Dr. Vex recruited! Maximum hull increased."
                        )

                    else:
                        message = "Insufficient credits."

                elif event.key == pygame.K_2:

                    if "Sprocket" in player.crew:

                        message = "Sprocket is already recruited."

                    elif player.credits >= 85:

                        player.credits -= 85
                        player.crew.append("Sprocket")

                        for weapon in player.weapons.values():
                            weapon["base_atk"] += 12

                        message = (
                            "Sprocket recruited! All weapons upgraded."
                        )

                    else:
                        message = "Insufficient credits."

                elif event.key == pygame.K_3:

                    if player.credits >= 25:

                        player.credits -= 25

                        player.inventory["Nano-Medpac"] += 1

                        message = "Nano-Medpac purchased."

                    else:
                        message = "Insufficient credits."

                elif event.key == pygame.K_4:

                    weapon = "Plasma Blade"

                    if weapon in player.weapons:

                        player.equipped_weapon = weapon
                        message = "Plasma Blade equipped."

                    elif player.credits >= 90:

                        player.credits -= 90

                        bonus = (
                            12 if "Sprocket" in player.crew else 0
                        )

                        player.weapons[weapon] = {
                            "base_atk": 45 + bonus,
                            "desc": "Superheated melee blade"
                        }

                        player.equipped_weapon = weapon

                        message = "Plasma Blade purchased and equipped."

                    else:
                        message = "Insufficient credits."

                elif event.key == pygame.K_5:

                    weapon = "Quantum Rifle"

                    if weapon in player.weapons:

                        player.equipped_weapon = weapon
                        message = "Quantum Rifle equipped."

                    elif player.credits >= 130:

                        player.credits -= 130

                        bonus = (
                            12 if "Sprocket" in player.crew else 0
                        )

                        player.weapons[weapon] = {
                            "base_atk": 65 + bonus,
                            "desc": "Dimensional disruptor rifle"
                        }

                        player.equipped_weapon = weapon

                        message = "Quantum Rifle purchased and equipped."

                    else:
                        message = "Insufficient credits."

                elif event.key == pygame.K_6:

                    weapon = "Void Cannon"

                    if not player.in_post_game:

                        message = "Locked. Unlock the Omega Void first."

                    elif weapon in player.weapons:

                        player.equipped_weapon = weapon
                        message = "Void Cannon equipped."

                    elif player.credits >= 220:

                        player.credits -= 220

                        bonus = (
                            12 if "Sprocket" in player.crew else 0
                        )

                        player.weapons[weapon] = {
                            "base_atk": 95 + bonus,
                            "desc": "Warp-core singularity weapon"
                        }

                        player.equipped_weapon = weapon

                        message = "Legendary Void Cannon acquired."

                    else:
                        message = "Insufficient credits."


# ============================================================
# GALAXY MAP INTERFACE
# ============================================================

def draw_galaxy_interface(player, current_map, status_msg):

    screen.fill(NAVY)
    draw_background()

    # Top header
    header = pygame.Rect(
        18,
        15,
        WIDTH - 36,
        68
    )

    panel(header, CYAN)

    text(
        "STARBOUND ODYSSEY",
        40,
        29,
        27,
        WHITE,
        True
    )

    dimension = (
        "OMEGA VOID"
        if player.in_post_game
        else "PRIME GALAXY"
    )

    text(
        f"SECTOR: {dimension}",
        445,
        39,
        13,
        CYAN,
        True
    )

    text(
        "● SIMULATION ONLINE",
        850,
        39,
        13,
        GREEN,
        True
    )

    # Map panel
    map_rect = pygame.Rect(
        18,
        98,
        875,
        435
    )

    panel(map_rect, NEON_BLUE)

    section_title(
        "GALACTIC NAVIGATION",
        38,
        110
    )

    marker_colors = {
        "S": NEON_BLUE,
        "1": GREEN,
        "A": GREEN,
        "2": PURPLE,
        "V": PURPLE,
        "3": GOLD,
        "X": GOLD,
        "4": ORANGE,
        "5": ORANGE,
        "B": RED,
        "Ω": VOID_PURPLE
    }

    for row in range(len(current_map)):

        for col in range(len(current_map[row])):

            tile = current_map[row][col]

            x = MAP_X + col * CELL
            y = MAP_Y + row * CELL

            rect = pygame.Rect(
                x,
                y,
                CELL - 2,
                CELL - 2
            )

            if tile == "W":

                pygame.draw.rect(
                    screen,
                    (13, 23, 42),
                    rect,
                    border_radius=5
                )

                pygame.draw.rect(
                    screen,
                    (31, 54, 83),
                    rect,
                    1,
                    border_radius=5
                )

            else:

                pygame.draw.rect(
                    screen,
                    (9, 18, 34),
                    rect,
                    border_radius=5
                )

                pygame.draw.rect(
                    screen,
                    (29, 49, 75),
                    rect,
                    1,
                    border_radius=5
                )

            if tile in marker_colors:

                color = marker_colors[tile]

                pulse = abs(
                    math.sin(pygame.time.get_ticks() / 500)
                )

                radius = int(8 + pulse * 2)

                pygame.draw.circle(
                    screen,
                    color,
                    rect.center,
                    radius
                )

                pygame.draw.circle(
                    screen,
                    WHITE,
                    rect.center,
                    radius,
                    1
                )

                text(
                    tile,
                    rect.centerx,
                    rect.centery,
                    12,
                    BLACK,
                    True,
                    True
                )

    player.draw(player.crew)

    # Commander sidebar
    side = pygame.Rect(
        910,
        98,
        172,
        435
    )

    panel(side, PURPLE)

    section_title(
        "COMMANDER",
        925,
        113,
        PURPLE
    )

    text(
        player.name[:14],
        925,
        148,
        19,
        WHITE,
        True
    )

    text(
        player.ship_class.upper(),
        925,
        180,
        12,
        CYAN,
        True
    )

    pygame.draw.line(
        screen,
        BORDER,
        (925, 210),
        (1065, 210),
        1
    )

    section_title(
        "HULL INTEGRITY",
        925,
        225,
        GREEN
    )

    draw_bar(
        925,
        254,
        140,
        12,
        player.hp,
        player.max_hp,
        GREEN
    )

    text(
        f"{player.hp}/{player.max_hp}",
        925,
        274,
        12,
        WHITE
    )

    section_title(
        "ENERGY",
        925,
        310,
        NEON_BLUE
    )

    draw_bar(
        925,
        339,
        140,
        12,
        player.energy,
        player.max_energy,
        NEON_BLUE
    )

    text(
        f"{player.energy}/{player.max_energy}",
        925,
        359,
        12,
        WHITE
    )

    section_title(
        "RESOURCES",
        925,
        396,
        GOLD
    )

    text(
        f"CREDITS: {player.credits}",
        925,
        424,
        12,
        GOLD,
        True
    )

    text(
        f"LEVEL: {player.level}",
        925,
        453,
        12,
        WHITE,
        True
    )

    # Bottom dashboard
    bottom = pygame.Rect(
        18,
        550,
        WIDTH - 36,
        180
    )

    panel(bottom, CYAN)

    section_title(
        "MISSION OBJECTIVES",
        38,
        565,
        GOLD
    )

    objectives = [
        "Explore all marked sectors.",
        "Collect vault codes and supply caches.",
        "Defeat the final sector guardian."
    ]

    for i, objective in enumerate(objectives):

        completed = (
            len(player.vault_codes) >= i + 1
        )

        color = GREEN if completed else TEXT

        text(
            f"{'[OK]' if completed else '[ ]'} {objective}",
            40,
            598 + i * 27,
            12,
            color
        )

    section_title(
        "ACTIVE CREW",
        465,
        565,
        GREEN
    )

    crew_text = (
        ", ".join(player.crew)
        if player.crew
        else "No companions recruited"
    )

    text(
        crew_text[:35],
        465,
        600,
        12,
        WHITE
    )

    section_title(
        "INVENTORY",
        465,
        637,
        PURPLE
    )

    text(
        f"MEDPACS: {player.inventory['Nano-Medpac']}",
        465,
        670,
        12,
        WHITE
    )

    text(
        f"ENERGY CELLS: {player.inventory['Energy Cell']}",
        465,
        692,
        12,
        WHITE
    )

    section_title(
        "SYSTEM MESSAGE",
        820,
        565,
        CYAN
    )

    text(
        status_msg[:29],
        820,
        600,
        12,
        WHITE
    )

    text(
        "W A S D  - MOVE",
        820,
        641,
        12,
        CYAN,
        True
    )

    text(
        "E - INTERACT",
        820,
        665,
        12,
        CYAN,
        True
    )

    text(
        "ESC - PAUSE",
        820,
        689,
        12,
        SUBTEXT
    )

    scanlines()


# ============================================================
# PAUSE MENU
# ============================================================

def pause_screen():

    while True:

        clock.tick(FPS)

        screen.fill(NAVY)
        draw_background()

        box = pygame.Rect(
            270,
            195,
            560,
            350
        )

        panel(box, CYAN)

        text(
            "SIMULATION PAUSED",
            WIDTH // 2,
            275,
            34,
            WHITE,
            True,
            True
        )

        text(
            "Your journey is waiting, Commander.",
            WIDTH // 2,
            325,
            15,
            SUBTEXT,
            False,
            True
        )

        button(
            pygame.Rect(385, 385, 330, 48),
            "RESUME SIMULATION",
            NEON_BLUE
        )

        button(
            pygame.Rect(385, 445, 330, 48),
            "EXIT GAME",
            RED
        )

        scanlines()
        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key in (
                    pygame.K_ESCAPE,
                    pygame.K_RETURN
                ):
                    return True

                if event.key == pygame.K_q:
                    return False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if pygame.Rect(
                    385, 385, 330, 48
                ).collidepoint(event.pos):
                    return True

                if pygame.Rect(
                    385, 445, 330, 48
                ).collidepoint(event.pos):
                    return False


# ============================================================
# ULTIMATE VICTORY SCREEN
# ============================================================

def victory_screen(player):

    running = True

    while running:

        clock.tick(FPS)

        screen.fill(NAVY)
        draw_background()

        box = pygame.Rect(
            100,
            85,
            WIDTH - 200,
            HEIGHT - 170
        )

        panel(box, GOLD)

        glow_circle(
            WIDTH // 2,
            190,
            65,
            GOLD
        )

        pygame.draw.circle(
            screen,
            GOLD,
            (WIDTH // 2, 190),
            37
        )

        text(
            "SIMULATION COMPLETED",
            WIDTH // 2,
            290,
            34,
            GOLD,
            True,
            True
        )

        text(
            "THE VOID HAS BEEN SAVED",
            WIDTH // 2,
            340,
            20,
            CYAN,
            True,
            True
        )

        text(
            f"COMMANDER: {player.name}",
            WIDTH // 2,
            420,
            17,
            WHITE,
            True,
            True
        )

        text(
            f"FINAL LEVEL: {player.level}",
            WIDTH // 2,
            455,
            15,
            WHITE,
            False,
            True
        )

        text(
            f"FINAL CREDITS: {player.credits}",
            WIDTH // 2,
            485,
            15,
            GOLD,
            True,
            True
        )

        text(
            f"ELITE CREW: {', '.join(player.crew) if player.crew else 'Solo Legend'}",
            WIDTH // 2,
            520,
            15,
            GREEN,
            False,
            True
        )

        button(
            pygame.Rect(380, 590, 340, 48),
            "EXIT SIMULATOR",
            NEON_BLUE
        )

        scanlines()
        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key in (
                    pygame.K_ESCAPE,
                    pygame.K_RETURN
                ):
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if pygame.Rect(
                    380, 590, 340, 48
                ).collidepoint(event.pos):
                    running = False

    pygame.quit()
    sys.exit()


# ============================================================
# SECTOR ENCOUNTERS
# ============================================================

def encounter(player, tile):

    if tile in ("1", "A"):

        code = (
            "CODE-7291"
            if not player.in_post_game
            else "VOID-KEY-1"
        )

        enemy = (
            "Zorblaxian Marauder"
            if not player.in_post_game
            else "Void Stalker Phantom"
        )

        hp = 110 if not player.in_post_game else 180

    elif tile in ("2", "V"):

        code = (
            "CODE-4085"
            if not player.in_post_game
            else "VOID-KEY-2"
        )

        enemy = (
            "Cyber-Derelict Drone"
            if not player.in_post_game
            else "Anomaly Behemoth"
        )

        hp = 140 if not player.in_post_game else 220

    elif tile in ("3", "X"):

        code = (
            "CODE-1934"
            if not player.in_post_game
            else "VOID-KEY-3"
        )

        enemy = (
            "Quantum Sanctum Guardian"
            if not player.in_post_game
            else "Nebula Archon"
        )

        hp = 160 if not player.in_post_game else 260

    else:
        return None

    if code in player.vault_codes:
        return None

    won = combat_screen(
        player,
        enemy,
        hp
    )

    if not won:
        return False

    player.vault_codes.append(code)

    return code


# ============================================================
# MAIN GAME
# ============================================================

def main():

    player = start_screen()

    running = True

    status_msg = (
        f"Welcome aboard, Commander {player.name}."
    )

    last_move = 0
    move_delay = 130

    while running:

        clock.tick(FPS)

        current_map = (
            POST_GAME_MAP
            if player.in_post_game
            else MAIN_MAP
        )

        # ----------------------------------------------------
        # Victory check
        # ----------------------------------------------------

        if player.ultimate_boss_defeated:

            victory_screen(player)
            return

        # ----------------------------------------------------
        # Input
        # ----------------------------------------------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    if not pause_screen():
                        running = False

                elif event.key == pygame.K_e:

                    tile = current_map[player.y][player.x]

                    if tile == "S":
                        market_screen(player)

        keys = pygame.key.get_pressed()

        now = pygame.time.get_ticks()

        if now - last_move >= move_delay:

            dx = 0
            dy = 0

            if keys[pygame.K_w] or keys[pygame.K_UP]:
                dy = -1

            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                dy = 1

            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                dx = -1

            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                dx = 1

            if dx != 0 or dy != 0:

                player.move(
                    dx,
                    dy,
                    current_map
                )

                last_move = now

        # ----------------------------------------------------
        # Tile interaction
        # ----------------------------------------------------

        tile = current_map[player.y][player.x]

        # Starbase
        if tile == "S":

            status_msg = (
                "Starbase 7 docked. Press E to trade."
            )

        # Enemy encounters
        elif tile in (
            "1", "2", "3",
            "A", "V", "X"
        ):

            result = encounter(player, tile)

            if result is False:
                running = False

            elif isinstance(result, str):

                status_msg = (
                    f"Sector cleared! Acquired {result}."
                )

        # Supply caches
        elif tile in ("4", "5"):

            if tile not in player.vault_codes:

                player.vault_codes.append(tile)

                player.credits += 75

                player.energy = min(
                    player.max_energy,
                    player.energy + 40
                )

                status_msg = (
                    "Supply cache discovered! "
                    "+75 credits and +40 energy."
                )

        # Main final boss
        elif tile == "B":

            if not player.in_post_game:

                if len(player.vault_codes) >= 5:

                    won = combat_screen(
                        player,
                        "DREADNOUGHT OMEGA AI",
                        350
                    )

                    if won:

                        loading_screen(
                            "ACTIVATING OMEGA VOID PORTAL..."
                        )

                        player.in_post_game = True

                        player.vault_codes.clear()

                        player.x = 2
                        player.y = 5

                        player.position_history = [
                            (player.x, player.y)
                        ]

                        status_msg = (
                            "OMEGA DEFEATED! "
                            "Welcome to the Void."
                        )

                    else:
                        running = False

                else:

                    status_msg = (
                        f"Vault airlock locked. "
                        f"Progress: {len(player.vault_codes)}/5."
                    )

        # Post-game final boss
        elif tile == "Ω":

            if player.in_post_game:

                if len(player.vault_codes) >= 4:

                    won = combat_screen(
                        player,
                        "EMPYREAN VOID OVERLORD",
                        480
                    )

                    if won:

                        player.ultimate_boss_defeated = True

                    else:
                        running = False

                else:

                    status_msg = (
                        f"Void gate sealed. "
                        f"Progress: {len(player.vault_codes)}/4."
                    )

        # ----------------------------------------------------
        # Render
        # ----------------------------------------------------

        draw_galaxy_interface(
            player,
            current_map,
            status_msg
        )

        pygame.display.flip()

    pygame.quit()
    sys.exit()


# ============================================================
# RUN GAME
# ============================================================

if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        pygame.quit()
        sys.exit()

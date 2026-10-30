import random
import sys
import pygame

# Initialize Pygame
pygame.init()
pygame.font.init()

# Game Window Dimensions & Larger Grid Config
WIDTH, HEIGHT = 1100, 750
GRID_SIZE = 40
COLS = WIDTH // GRID_SIZE
ROWS = 12

FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Starbound Odyssey: Expanded Galaxy & Fixed Boss Pathway")
clock = pygame.time.Clock()

# Fonts
FONT = pygame.font.SysFont("arial", 18)
BIG_FONT = pygame.font.SysFont("arial", 26, bold=True)
TITLE_FONT = pygame.font.SysFont("arial", 32, bold=True)
VICTORY_FONT = pygame.font.SysFont("arial", 40, bold=True)

# Color Palette (Deep Space Cyberpunk Theme)
BLACK = (8, 10, 18)
WHITE = (240, 245, 255)
DARK_GRAY = (25, 30, 48)
PANEL_BG = (15, 20, 35)
SPACE_BLUE = (10, 14, 28)
CYAN = (0, 240, 255)
BLUE = (40, 140, 255)
GREEN = (50, 230, 120)
PURPLE = (180, 70, 255)
GOLD = (255, 215, 0)
RED = (255, 60, 80)
VOID_PURPLE = (100, 20, 150)
ORANGE = (255, 140, 0)

COLOR_OPTIONS = {
    "Cyan": CYAN,
    "Green": GREEN,
    "Gold": GOLD,
    "Purple": PURPLE,
    "Red": RED,
    "Orange": ORANGE,
}
COLOR_NAMES = list(COLOR_OPTIONS.keys())

SHIP_CLASSES = {
    "Scout": {"hp": 130, "energy": 120, "credits": 200, "desc": "Fast & High Energy"},
    "Destroyer": {"hp": 180, "energy": 80, "credits": 140, "desc": "Tanky Hull & Armor"},
    "Cruiser": {"hp": 150, "energy": 100, "credits": 250, "desc": "Balanced & Wealthy"},
}
SHIP_NAMES = list(SHIP_CLASSES.keys())

STARS = [
    (random.randint(0, WIDTH), random.randint(0, HEIGHT), random.choice([1, 2, 3]))
    for _ in range(110)
]


# ============================================================================
#                               PLAYER CLASS
# ============================================================================


class Player:

    def __init__(self, name, color_name, ship_class):
        self.name = name
        self.color_name = color_name
        self.color = COLOR_OPTIONS.get(color_name, CYAN)
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
        self.inventory = {"Nano-Medpac": 3, "Energy Cell": 2}
        self.in_post_game = False
        self.ultimate_boss_defeated = False

        self.position_history = [(self.x, self.y)]

        self.weapons = {
            "Pulse Blaster": {
                "base_atk": 22,
                "desc": "Standard starfleet sidearm.",
            }
        }
        self.equipped_weapon = "Pulse Blaster"

    def move(self, dx, dy, world_map):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < COLS and 0 <= new_y < len(world_map):
            if world_map[new_y][new_x] != "W":
                self.x = new_x
                self.y = new_y

                self.position_history.append((self.x, self.y))
                if len(self.position_history) > 10:
                    self.position_history.pop(0)

    def draw(self, surface, current_crew):
        rect = pygame.Rect(
            self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(surface, WHITE, rect.inflate(4, 4), 2, border_radius=10)
        pygame.draw.rect(surface, self.color, rect, border_radius=8)
        pygame.draw.circle(
            surface,
            BLACK,
            (self.x * GRID_SIZE + 12, self.y * GRID_SIZE + 16),
            4,
        )
        pygame.draw.circle(
            surface,
            BLACK,
            (self.x * GRID_SIZE + 28, self.y * GRID_SIZE + 16),
            4,
        )

        history_len = len(self.position_history)
        if "Dr. Vex" in current_crew and history_len >= 2:
            vex_pos = self.position_history[-2]
            vex_rect = pygame.Rect(
                vex_pos[0] * GRID_SIZE, vex_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE
            )
            pygame.draw.rect(surface, GREEN, vex_rect, border_radius=8)
            pygame.draw.circle(
                surface,
                BLACK,
                (vex_pos[0] * GRID_SIZE + 20, vex_pos[1] * GRID_SIZE + 20),
                4,
            )

        if "Sprocket" in current_crew and history_len >= 3:
            sproc_pos = self.position_history[-3]
            sproc_rect = pygame.Rect(
                sproc_pos[0] * GRID_SIZE,
                sproc_pos[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE,
            )
            pygame.draw.rect(surface, GOLD, sproc_rect, border_radius=8)
            pygame.draw.circle(
                surface,
                BLACK,
                (sproc_pos[0] * GRID_SIZE + 20, sproc_pos[1] * GRID_SIZE + 20),
                4,
            )


# ============================================================================
#                       EXPANDED GALAXY MAPS (GUARANTEED OPEN BOSS PATHS)
# ============================================================================
MAIN_MAP = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W...1........W.........W..W",
    "W...WWWWWW...W..2......W..W",
    "W........W.............W..W",
    "W..S.....W......4......W..W",  # Starbase 7 & Cache 4
    "W.........................B",  # Completely open highway straight to Boss (B)
    "W.........................W",
    "W........W.............W..W",
    "W..3.....W.............W..W",
    "W........W......5......W..W",  # Sector 3 & Cache 5
    "W.........................W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWW",
]

POST_GAME_MAP = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W...A........W.........W..W",
    "W...WWWWWW...W..V......W..W",
    "W........W.............W..W",
    "W..S.....W......X......W..W",  # Starbase 7 & Post-game sector
    "W.........................Ω",  # Completely open highway straight to Ultimate Boss (Ω)
    "W.........................W",
    "W........W.............W..W",
    "W..4.....W.............W..W",
    "W........W......5......W..W",  # Post-game caches
    "W.........................W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWW",
]


# ============================================================================
#                       UI & BEAUTY HELPER FUNCTIONS
# ============================================================================
def draw_starfield(surface):
    for star in STARS:
        sx, sy, size = star
        pygame.draw.circle(surface, (200, 220, 255), (sx, sy), size)


def draw_bar(surface, x, y, w, h, current, max_val, color):
    pygame.draw.rect(surface, DARK_GRAY, (x, y, w, h), border_radius=4)
    fill_w = int(w * (max(0, current) / max(1, max_val)))
    if fill_w > 0:
        pygame.draw.rect(surface, color, (x, y, fill_w, h), border_radius=4)
    pygame.draw.rect(surface, WHITE, (x, y, w, h), 1, border_radius=4)


# ============================================================================
#                       START & CUSTOMIZATION SCREEN
# ============================================================================
def start_screen():
    p_name = "Commander Rex"
    color_idx = 0
    ship_idx = 0
    selection_step = 0
    input_active = True

    while input_active:
        clock.tick(FPS)
        screen.fill(BLACK)
        draw_starfield(screen)

        box = pygame.Rect(120, 60, WIDTH - 240, HEIGHT - 120)
        pygame.draw.rect(screen, PANEL_BG, box, border_radius=15)
        pygame.draw.rect(screen, CYAN, box, 3, border_radius=15)

        title = TITLE_FONT.render("🚀 STARBOUND ODYSSEY: COMMANDER FORGE 🚀", True, GOLD)

        if selection_step == 0:
            step_txt = BIG_FONT.render("Step 1: Enter Your Commander Name", True, CYAN)
            val_txt = FONT.render(f"Name: {p_name} _ (Type & press ENTER)", True, WHITE)
        elif selection_step == 1:
            step_txt = BIG_FONT.render("Step 2: Choose Uniform Color [LEFT/RIGHT]", True, CYAN)
            val_txt = FONT.render(f"Color: < {COLOR_NAMES[color_idx]} > (Press ENTER to confirm)", True,
                                  COLOR_OPTIONS[COLOR_NAMES[color_idx]])
        else:
            c_name = SHIP_NAMES[ship_idx]
            c_data = SHIP_CLASSES[c_name]
            step_txt = BIG_FONT.render("Step 3: Select Starship Hull Class [LEFT/RIGHT]", True, CYAN)
            val_txt = FONT.render(
                f"Class: < {c_name} > ({c_data['desc']} | HP:{c_data['hp']} Energy:{c_data['energy']})", True, GOLD)

        launch_hint = FONT.render("Press [ENTER] to advance / launch mission", True, GREEN)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, box.y + 40))
        screen.blit(step_txt, (WIDTH // 2 - step_txt.get_width() // 2, box.y + 140))
        screen.blit(val_txt, (WIDTH // 2 - val_txt.get_width() // 2, box.y + 220))
        screen.blit(launch_hint, (WIDTH // 2 - launch_hint.get_width() // 2, box.y + 350))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if selection_step < 2:
                        selection_step += 1
                    else:
                        input_active = False
                elif event.key == pygame.K_LEFT:
                    if selection_step == 1:
                        color_idx = (color_idx - 1) % len(COLOR_NAMES)
                    elif selection_step == 2:
                        ship_idx = (ship_idx - 1) % len(SHIP_NAMES)
                elif event.key == pygame.K_RIGHT:
                    if selection_step == 1:
                        color_idx = (color_idx + 1) % len(COLOR_NAMES)
                    elif selection_step == 2:
                        ship_idx = (ship_idx + 1) % len(SHIP_NAMES)
                elif event.key == pygame.K_BACKSPACE:
                    if selection_step == 0:
                        p_name = p_name[:-1]
                else:
                    if selection_step == 0 and len(p_name) < 15 and (event.unicode.isalnum() or event.unicode == " "):
                        p_name += event.unicode

    loading_screen("INITIALIZING EXPANDED GALAXY...")
    return Player(
        p_name.strip() if p_name.strip() else "Commander Rex",
        COLOR_NAMES[color_idx],
        SHIP_NAMES[ship_idx],
    )


def loading_screen(message="LOADING SECTOR..."):
    progress = 0
    while progress < 100:
        clock.tick(FPS)
        screen.fill(BLACK)
        draw_starfield(screen)

        load_box = pygame.Rect(WIDTH // 2 - 250, HEIGHT // 2 - 50, 500, 100)
        pygame.draw.rect(screen, PANEL_BG, load_box, border_radius=10)
        pygame.draw.rect(screen, BLUE, load_box, 2, border_radius=10)

        load_txt = BIG_FONT.render(message, True, CYAN)
        screen.blit(load_txt, (WIDTH // 2 - load_txt.get_width() // 2, load_box.y + 15))

        draw_bar(screen, load_box.x + 30, load_box.y + 60, 440, 16, progress, 100, GREEN)

        pygame.display.flip()
        progress += 6


# ============================================================================
#                  COMPANION BATTLE CUTSCENE SYSTEM
# ============================================================================
def play_companion_cutscene(screen, companion_name, action_desc):
    timer = 0
    while timer < 65:
        clock.tick(FPS)
        screen.fill(SPACE_BLUE)
        draw_starfield(screen)

        banner = pygame.Rect(100, HEIGHT // 2 - 90, WIDTH - 200, 180)
        pygame.draw.rect(screen, PANEL_BG, banner, border_radius=12)
        pygame.draw.rect(
            screen,
            GREEN if companion_name == "Dr. Vex" else GOLD,
            banner,
            3,
            border_radius=12,
        )

        c_title = TITLE_FONT.render(
            f"✨ COMPANION ABILITY: {companion_name.upper()} ✨",
            True,
            GREEN if companion_name == "Dr. Vex" else GOLD,
        )
        c_desc = BIG_FONT.render(action_desc, True, WHITE)

        screen.blit(c_title, (WIDTH // 2 - c_title.get_width() // 2, banner.y + 35))
        screen.blit(c_desc, (WIDTH // 2 - c_desc.get_width() // 2, banner.y + 100))

        pygame.display.flip()
        timer += 1


# ============================================================================
#                       POKÉMON-STYLE COMBAT SUITE
# ============================================================================
def trigger_combat(screen, player, enemy_name, enemy_hp):
    combat_active = True
    msg = f"A wild {enemy_name} appeared!"
    enemy_max_hp = enemy_hp
    screen_flash = 0

    while combat_active:
        clock.tick(FPS)
        screen.fill(SPACE_BLUE)
        draw_starfield(screen)

        e_box = pygame.Rect(WIDTH - 450, 40, 400, 110)
        pygame.draw.rect(screen, PANEL_BG, e_box, border_radius=10)
        pygame.draw.rect(screen, RED, e_box, 2, border_radius=10)
        screen.blit(BIG_FONT.render(enemy_name, True, WHITE), (e_box.x + 20, e_box.y + 12))
        screen.blit(FONT.render(f"HP: {max(0, enemy_hp)} / {enemy_max_hp}", True, WHITE), (e_box.x + 20, e_box.y + 45))
        draw_bar(screen, e_box.x + 20, e_box.y + 75, 360, 14, enemy_hp, enemy_max_hp, RED)

        p_box = pygame.Rect(50, HEIGHT - 330, 420, 150)
        pygame.draw.rect(screen, PANEL_BG, p_box, border_radius=10)
        pygame.draw.rect(screen, player.color, p_box, 2, border_radius=10)
        screen.blit(BIG_FONT.render(f"Commander {player.name}", True, player.color), (p_box.x + 20, p_box.y + 12))
        screen.blit(
            FONT.render(f"HP: {max(0, player.hp)} / {player.max_hp}  |  Energy: {player.energy}/{player.max_energy}",
                        True, WHITE), (p_box.x + 20, p_box.y + 45))
        draw_bar(screen, p_box.x + 20, p_box.y + 75, 380, 12, player.hp, player.max_hp, GREEN)
        draw_bar(screen, p_box.x + 20, p_box.y + 98, 380, 10, player.energy, player.max_energy, BLUE)
        screen.blit(FONT.render(f"Weapon: {player.equipped_weapon}", True, GOLD), (p_box.x + 20, p_box.y + 120))

        menu_box = pygame.Rect(WIDTH - 470, HEIGHT - 330, 420, 150)
        pygame.draw.rect(screen, PANEL_BG, menu_box, border_radius=10)
        pygame.draw.rect(screen, CYAN, menu_box, 2, border_radius=10)

        screen.blit(FONT.render("FIGHT COMMANDS:", True, CYAN), (menu_box.x + 20, menu_box.y + 12))
        screen.blit(FONT.render(f"[1] Attack ({player.equipped_weapon})", True, WHITE),
                    (menu_box.x + 20, menu_box.y + 40))
        screen.blit(FONT.render("[2] Shield Gen (-15 Energy, +45 HP)", True, GREEN), (menu_box.x + 20, menu_box.y + 68))
        screen.blit(FONT.render(f"[3] Dr. Vex Heal ({'Ready' if 'Dr. Vex' in player.crew else 'Not Recruited'})", True,
                                GREEN if "Dr. Vex" in player.crew else DARK_GRAY), (menu_box.x + 20, menu_box.y + 96))
        screen.blit(
            FONT.render(f"[4] Sprocket Overclock ({'Ready' if 'Sprocket' in player.crew else 'Not Recruited'})", True,
                        GOLD if "Sprocket" in player.crew else DARK_GRAY), (menu_box.x + 20, menu_box.y + 122))

        msg_box = pygame.Rect(50, HEIGHT - 150, WIDTH - 100, 110)
        pygame.draw.rect(screen, PANEL_BG, msg_box, border_radius=10)
        pygame.draw.rect(screen, WHITE, msg_box, 2, border_radius=10)
        screen.blit(BIG_FONT.render(msg, True, WHITE), (msg_box.x + 25, msg_box.y + 35))

        if screen_flash > 0:
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            s.fill((255, 0, 0, 60))
            screen.blit(s, (0, 0))
            screen_flash -= 1

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    atk = player.weapons[player.equipped_weapon]["base_atk"]
                    dmg = random.randint(atk - 4, atk + 12)
                    enemy_hp -= dmg
                    msg = f"Commander {player.name} used {player.equipped_weapon}! Dealt {dmg} damage."
                elif event.key == pygame.K_2:
                    if player.energy >= 15:
                        player.energy -= 15
                        player.hp = min(player.max_hp, player.hp + 45)
                        msg = "Shield Generator online! Restored 45 HP."
                    else:
                        msg = "Energy too low to raise shields!"
                        continue
                elif event.key == pygame.K_3:
                    if "Dr. Vex" in player.crew:
                        play_companion_cutscene(screen, "Dr. Vex", "Deploying Nano-Nanites! Fully Restored Hull HP!")
                        player.hp = player.max_hp
                        msg = "Dr. Vex executed Emergency Medical Overhaul!"
                    else:
                        msg = "Dr. Vex is not on your crew!"
                        continue
                elif event.key == pygame.K_4:
                    if "Sprocket" in player.crew:
                        play_companion_cutscene(screen, "Sprocket", "Rerouting Auxiliary Plasma Cores!")
                        atk = player.weapons[player.equipped_weapon]["base_atk"] * 2
                        enemy_hp -= atk
                        msg = f"Sprocket's Overclock Strike dealt a massive {atk} damage!"
                    else:
                        msg = "Sprocket is not on your crew!"
                        continue

                if enemy_hp <= 0:
                    msg = f"Victory! {enemy_name} was defeated!"
                    pygame.display.flip()
                    pygame.time.delay(1600)
                    player.credits += 140
                    player.level += 1
                    return True

                e_dmg = random.randint(18, 30)
                player.hp -= e_dmg
                screen_flash = 5
                if player.hp <= 0:
                    msg = "Commander hull breached... Mission Failed."
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    return False


# ============================================================================
#                               VICTORY SPECIAL SCREEN
# ============================================================================
def show_ultimate_victory_screen(screen, player):
    waiting = True
    while waiting:
        clock.tick(FPS)
        screen.fill(BLACK)
        draw_starfield(screen)

        box = pygame.Rect(120, 80, WIDTH - 240, HEIGHT - 160)
        pygame.draw.rect(screen, PANEL_BG, box, border_radius=15)
        pygame.draw.rect(screen, GOLD, box, 4, border_radius=15)

        title = VICTORY_FONT.render("🌟 LEGENDARY SAVIOR OF THE VOID 🌟", True, GOLD)
        sub = BIG_FONT.render("THE UNIVERSE HAS BEEN SECURED", True, CYAN)

        p_stats = FONT.render(
            f"Commander {player.name} (Max Level {player.level})  |  Final Credits: {player.credits} ¢", True, WHITE)
        crew_stats = FONT.render(f"Elite Crew: {player.crew if player.crew else 'Solo Legend'}", True, WHITE)
        exit_msg = FONT.render("Press [ESC] or [ENTER] to exit the simulation.", True, GREEN)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, box.y + 50))
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, box.y + 120))
        screen.blit(p_stats, (WIDTH // 2 - p_stats.get_width() // 2, box.y + 210))
        screen.blit(crew_stats, (WIDTH // 2 - crew_stats.get_width() // 2, box.y + 250))
        screen.blit(exit_msg, (WIDTH // 2 - exit_msg.get_width() // 2, box.y + 340))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    pygame.quit()
                    sys.exit()


# ============================================================================
#                               MARKET SHOP SCREEN
# ============================================================================
def open_starbase_market(screen, player):
    in_market = True
    msg = "Welcome to Starbase 7 Trading Post."

    while in_market:
        clock.tick(FPS)
        screen.fill(SPACE_BLUE)
        draw_starfield(screen)

        box = pygame.Rect(100, 40, WIDTH - 200, HEIGHT - 80)
        pygame.draw.rect(screen, PANEL_BG, box, border_radius=12)
        pygame.draw.rect(screen, BLUE, box, 3, border_radius=12)

        title = TITLE_FONT.render("🛸 STARBASE 7 - SMUGGLER TRADING BAY", True, GOLD)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, box.y + 20))

        c_info = FONT.render(
            f"Available Credits: {player.credits} ¢  |  Crew: {player.crew}  |  Equipped: {player.equipped_weapon}",
            True, CYAN)
        screen.blit(c_info, (box.x + 40, box.y + 70))

        opt1 = FONT.render("[1] Recruit Dr. Vex (Medic Follower) - 70 Credits (+30 Max HP)", True, WHITE)
        opt2 = FONT.render("[2] Recruit Sprocket (Engineer Follower) - 85 Credits (+12 All ATK)", True, WHITE)
        opt3 = FONT.render("[3] Buy Nano-Medpac (+65 HP) - 25 Credits", True, WHITE)
        opt4 = FONT.render("[4] Buy Plasma Blade (ATK: 45) - 90 Credits", True, WHITE)
        opt5 = FONT.render("[5] Buy Quantum Disruptor Rifle (ATK: 65) - 130 Credits", True, WHITE)
        opt6 = FONT.render("[6] Buy Void Singularity Cannon (ATK: 95) - 220 Credits", True,
                           GOLD if player.in_post_game else DARK_GRAY)
        opt7 = FONT.render("[7] Return to Starship Bridge", True, RED)

        screen.blit(opt1, (box.x + 40, box.y + 125))
        screen.blit(opt2, (box.x + 40, box.y + 165))
        screen.blit(opt3, (box.x + 40, box.y + 205))
        screen.blit(opt4, (box.x + 40, box.y + 245))
        screen.blit(opt5, (box.x + 40, box.y + 285))
        screen.blit(opt6, (box.x + 40, box.y + 325))
        screen.blit(opt7, (box.x + 40, box.y + 390))

        msg_box = pygame.Rect(box.x + 40, box.y + 440, box.width - 80, 50)
        pygame.draw.rect(screen, DARK_GRAY, msg_box, border_radius=6)
        screen.blit(FONT.render(msg, True, GREEN), (msg_box.x + 15, msg_box.y + 15))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if "Dr. Vex" in player.crew:
                        msg = "Dr. Vex is already following your crew!"
                    elif player.credits >= 70:
                        player.credits -= 70
                        player.crew.append("Dr. Vex")
                        player.max_hp += 30
                        player.hp = player.max_hp
                        msg = "✨ Dr. Vex recruited as active follower & combat medic!"
                    else:
                        msg = "❌ Insufficient credits!"
                elif event.key == pygame.K_2:
                    if "Sprocket" in player.crew:
                        msg = "Sprocket is already following your crew!"
                    elif player.credits >= 85:
                        player.credits -= 85
                        player.crew.append("Sprocket")
                        for w in player.weapons.values():
                            w["base_atk"] += 12
                        msg = "✨ Sprocket recruited as active follower & combat engineer!"
                    else:
                        msg = "❌ Insufficient credits!"
                elif event.key == pygame.K_3:
                    if player.credits >= 25:
                        player.credits -= 25
                        player.inventory["Nano-Medpac"] += 1
                        msg = "📦 Purchased 1 Nano-Medpac."
                    else:
                        msg = "❌ Insufficient credits!"
                elif event.key == pygame.K_4:
                    if "Plasma Blade" in player.weapons:
                        player.equipped_weapon = "Plasma Blade"
                        msg = "⚔️ Equipped Plasma Blade!"
                    elif player.credits >= 90:
                        player.credits -= 90
                        bonus = 12 if "Sprocket" in player.crew else 0
                        player.weapons["Plasma Blade"] = {"base_atk": 45 + bonus, "desc": "Superheated melee blade."}
                        player.equipped_weapon = "Plasma Blade"
                        msg = "⚔️ Plasma Blade purchased & equipped!"
                    else:
                        msg = "❌ Insufficient credits!"
                elif event.key == pygame.K_5:
                    if "Quantum Rifle" in player.weapons:
                        player.equipped_weapon = "Quantum Rifle"
                        msg = "⚔️ Equipped Quantum Rifle!"
                    elif player.credits >= 130:
                        player.credits -= 130
                        bonus = 12 if "Sprocket" in player.crew else 0
                        player.weapons["Quantum Rifle"] = {"base_atk": 65 + bonus, "desc": "Dimensional rifle."}
                        player.equipped_weapon = "Quantum Rifle"
                        msg = "⚔️ Quantum Disruptor Rifle purchased & equipped!"
                    else:
                        msg = "❌ Insufficient credits!"
                elif event.key == pygame.K_6:
                    if not player.in_post_game:
                        msg = "🔒 Locked! Unlock the Void Dimension post-game first."
                    elif "Void Cannon" in player.weapons:
                        player.equipped_weapon = "Void Cannon"
                        msg = "⚔️ Equipped Void Singularity Cannon!"
                    elif player.credits >= 220:
                        player.credits -= 220
                        bonus = 12 if "Sprocket" in player.crew else 0
                        player.weapons["Void Cannon"] = {"base_atk": 95 + bonus,
                                                         "desc": "Warp-core singularity weapon."}
                        player.equipped_weapon = "Void Cannon"
                        msg = "⚔️ Legendary Void Singularity Cannon acquired!"
                    else:
                        msg = "❌ Insufficient credits!"
                elif event.key in (pygame.K_7, pygame.K_ESCAPE):
                    in_market = False


# ============================================================================
#                               MAIN GAME LOOP
# ============================================================================
def main():
    player = start_screen()
    running = True
    status_msg = f"Welcome, Commander {player.name}! Use [W, A, S, D] to navigate the expanded galaxy."

    while running:
        clock.tick(FPS)

        current_map = POST_GAME_MAP if player.in_post_game else MAIN_MAP

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.move(0, -1, current_map)
                elif event.key == pygame.K_s:
                    player.move(0, 1, current_map)
                elif event.key == pygame.K_a:
                    player.move(-1, 0, current_map)
                elif event.key == pygame.K_d:
                    player.move(1, 0, current_map)

        if player.ultimate_boss_defeated:
            show_ultimate_victory_screen(screen, player)
            break

        current_tile = current_map[player.y][player.x]

        if current_tile == "S":
            status_msg = "Starbase 7 docked! Press [E] to open Smuggler Market."
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                open_starbase_market(screen, player)

        elif current_tile in ("1", "A"):
            code_name = "CODE-7291" if not player.in_post_game else "VOID-KEY-1"
            enemy_title = "Zorblaxian Marauder" if not player.in_post_game else "Void Stalker Phantom"
            hp_pool = 110 if not player.in_post_game else 180

            if code_name not in player.vault_codes:
                won = trigger_combat(screen, player, enemy_title, hp_pool)
                if not won:
                    break
                player.vault_codes.append(code_name)
                status_msg = f"Sector Cleared! Acquired {code_name}"

        elif current_tile in ("2", "V"):
            code_name = "CODE-4085" if not player.in_post_game else "VOID-KEY-2"
            enemy_title = "Cyber-Derelict Drone" if not player.in_post_game else "Anomaly Behemoth"
            hp_pool = 140 if not player.in_post_game else 220

            if code_name not in player.vault_codes:
                won = trigger_combat(screen, player, enemy_title, hp_pool)
                if not won:
                    break
                player.vault_codes.append(code_name)
                status_msg = f"Sector Cleared! Acquired {code_name}"

        elif current_tile in ("3", "X"):
            code_name = "CODE-1934" if not player.in_post_game else "VOID-KEY-3"
            enemy_title = "Quantum Sanctum Guardian" if not player.in_post_game else "Nebula Archon"
            hp_pool = 160 if not player.in_post_game else 260

            if code_name not in player.vault_codes:
                won = trigger_combat(screen, player, enemy_title, hp_pool)
                if not won:
                    break
                player.vault_codes.append(code_name)
                status_msg = f"Sector Cleared! Acquired {code_name}"

        elif current_tile in ("4", "5"):
            bonus_type = "Credit Cache" if current_tile == "4" else "Energy Core Cache"
            if current_tile not in player.vault_codes:
                player.credits += 75
                player.energy = min(player.max_energy, player.energy + 40)
                player.vault_codes.append(current_tile)
                status_msg = f"📦 Discovered {bonus_type}! +75 Credits & +40 Energy."

        elif current_tile == "B":
            if len(player.vault_codes) >= 5 and not player.in_post_game:
                won = trigger_combat(screen, player, "DREADNOUGHT OMEGA AI", 350)
                if won:
                    loading_screen("ACTIVATING OMEGA VOID PORTAL...")
                    player.in_post_game = True
                    player.vault_codes.clear()
                    player.x, player.y = 2, 5
                    player.position_history = [(player.x, player.y)]
                    status_msg = "🌟 OMEGA DEFEATED! Welcome to the Omega Void Post-Game Dimension!"
                else:
                    break
            elif not player.in_post_game:
                status_msg = f"🔒 Vault Airlock Locked! Explore all sectors & caches first ({len(player.vault_codes)}/5 discovered)."

        elif current_tile == "Ω":
            if len(player.vault_codes) >= 4:
                won = trigger_combat(screen, player, "EMPYREAN VOID OVERLORD", 480)
                if won:
                    player.ultimate_boss_defeated = True
                else:
                    break
            else:
                status_msg = f"🔒 Void Singularity Sealed! Explore expanded void sectors first ({len(player.vault_codes)}/4)."

        # Render Map & Visuals
        screen.fill(SPACE_BLUE)
        draw_starfield(screen)

        for row in range(len(current_map)):
            for col in range(len(current_map[0])):
                tile = current_map[row][col]
                rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)

                if tile == "W":
                    pygame.draw.rect(screen, DARK_GRAY, rect)
                    pygame.draw.rect(screen, (50, 60, 90), rect, 1)
                elif tile == "S":
                    pygame.draw.rect(screen, BLUE, rect, border_radius=6)
                elif tile in ("1", "A"):
                    pygame.draw.rect(screen, GREEN, rect, border_radius=6)
                elif tile in ("2", "V"):
                    pygame.draw.rect(screen, PURPLE, rect, border_radius=6)
                elif tile in ("3", "X"):
                    pygame.draw.rect(screen, GOLD, rect, border_radius=6)
                elif tile in ("4", "5"):
                    pygame.draw.rect(screen, ORANGE, rect, border_radius=6)
                elif tile in ("B", "Ω"):
                    pygame.draw.rect(screen, RED if tile == "B" else VOID_PURPLE, rect, border_radius=6)
                else:
                    pygame.draw.rect(screen, (12, 16, 30), rect)
                    pygame.draw.rect(screen, (20, 26, 45), rect, 1)

        player.draw(screen, player.crew)

        # Bottom HUD Panel
        hud_rect = pygame.Rect(0, HEIGHT - 130, WIDTH, 130)
        pygame.draw.rect(screen, PANEL_BG, hud_rect)
        pygame.draw.rect(screen, CYAN, hud_rect, 2)

        dimension_label = "DIMENSION: OMEGA VOID (POST-GAME)" if player.in_post_game else "DIMENSION: PRIME GALAXY"
        stats_text = FONT.render(
            f"❤️ Hull: {player.hp}/{player.max_hp}  |  ⚡ Energy: {player.energy}/{player.max_energy}  |  💳 Credits: {player.credits}¢",
            True, WHITE)
        gear_text = FONT.render(
            f"🔫 Weapon: {player.equipped_weapon}  |  👥 Crew: {player.crew if player.crew else 'None'}  |  🔑 Exploration Progress: {len(player.vault_codes)} items",
            True, GOLD)
        msg_text = FONT.render(f"[{dimension_label}] STATUS: {status_msg}", True, CYAN)

        screen.blit(stats_text, (25, HEIGHT - 110))
        screen.blit(gear_text, (25, HEIGHT - 75))
        screen.blit(msg_text, (25, HEIGHT - 40))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
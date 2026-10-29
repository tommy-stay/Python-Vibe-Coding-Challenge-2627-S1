import random
import sys
import pygame

# Initialize Pygame
pygame.init()
pygame.font.init()

# Game Window Dimensions & Grid Config
WIDTH, HEIGHT = 900, 650
GRID_SIZE = 45
COLS = WIDTH // GRID_SIZE
ROWS = 11  # Grid rows for playfield, bottom is reserved for HUD

FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(
    "Starbound Odyssey: Intergalactic WASD Exploration"
)
clock = pygame.time.Clock()

# Fonts
FONT = pygame.font.SysFont("arial", 18)
BIG_FONT = pygame.font.SysFont("arial", 26, bold=True)
VICTORY_FONT = pygame.font.SysFont("arial", 36, bold=True)

# Color Palette (Sci-Fi Theme)
BLACK = (10, 10, 20)
WHITE = (255, 255, 255)
DARK_GRAY = (35, 35, 55)
LIGHT_GRAY = (180, 180, 200)
SPACE_BLUE = (15, 20, 40)
BLUE = (50, 150, 255)
CYAN = (0, 220, 220)
GREEN = (40, 220, 100)
PURPLE = (170, 60, 240)
GOLD = (255, 215, 0)
RED = (230, 50, 50)

# ============================================================================
#                               PLAYER CLASS
# ============================================================================


class Player:

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.hp = 150
    self.max_hp = 150
    self.energy = 80
    self.max_energy = 80
    self.credits = 120
    self.level = 1

    # Crew, Codes & Game State flags
    self.crew = []
    self.vault_codes = []
    self.inventory = {"Nano-Medpac": 3, "Energy Cell": 2}
    self.game_won = False

    # Weapons & Abilities
    self.weapons = {
        "Pulse Blaster": {
            "base_atk": 20,
            "desc": "Standard starfleet sidearm.",
        }
    }
    self.equipped_weapon = "Pulse Blaster"

  def move(self, dx, dy, world_map):
    if self.game_won:
      return  # Stop movement if game is won
    new_x = self.x + dx
    new_y = self.y + dy

    # Check bounds and walls ('W')
    if 0 <= new_x < COLS and 0 <= new_y < len(world_map):
      if world_map[new_y][new_x] != "W":
        self.x = new_x
        self.y = new_y

  def draw(self, surface):
    rect = pygame.Rect(
        self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE
    )
    pygame.draw.rect(surface, CYAN, rect, border_radius=8)
    pygame.draw.rect(surface, WHITE, rect, 2, border_radius=8)

    # Draw Starfleet Commander visor/eyes
    pygame.draw.circle(
        surface,
        BLACK,
        (self.x * GRID_SIZE + 14, self.y * GRID_SIZE + 16),
        4,
    )
    pygame.draw.circle(
        surface,
        BLACK,
        (self.x * GRID_SIZE + 31, self.y * GRID_SIZE + 16),
        4,
    )


# ============================================================================
#                               GALAXY MAP LAYOUT
# ============================================================================
GALAXY_MAP = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W...1........W.....W",
    "W...WWWWWW...W..2..W",
    "W........W...W.....W",
    "W..S.....W...W..WWWW",
    "W........W.........W",
    "WWWWWW...WWWWWW....W",
    "W.............W....W",
    "W..3..........W..B.W",
    "W.............W....W",
    "WWWWWWWWWWWWWWWWWWWW",
]

LOCATION_NAMES = {
    "S": "Starbase 7 (Market & Crew)",
    "1": "Planet Zorblax (Crystal Mines)",
    "2": "Cyber-Derelict Ship (Armory)",
    "3": "Quantum Sanctum (Elder Shrine)",
    "B": "Omega Dreadnought Vault",
}


# ============================================================================
#                            COMBAT & INTERACTION SUITE
# ============================================================================
def trigger_combat(screen, player, enemy_name, enemy_hp):
  combat_active = True
  msg = f"Hostile encounter with {enemy_name}!"
  enemy_max_hp = enemy_hp

  while combat_active:
    screen.fill(SPACE_BLUE)

    title = BIG_FONT.render(f"⚔️ BATTLE: {enemy_name.upper()}", True, RED)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

    p_info = FONT.render(
        f"Commander HP: {player.hp}/{player.max_hp}  |  Energy:"
        f" {player.energy}/{player.max_energy}",
        True,
        CYAN,
    )
    e_info = FONT.render(
        f"{enemy_name} HP: {max(0, enemy_hp)}/{enemy_max_hp}", True, RED
    )
    screen.blit(p_info, (100, 130))
    screen.blit(e_info, (520, 130))

    c1 = FONT.render("[1] Fire Weapon Attack", True, WHITE)
    c2 = FONT.render(
        "[2] Cast Shield Generator (-15 Energy, +40 HP)", True, GREEN
    )
    c3 = FONT.render(
        f"[3] Use Nano-Medpac Item ({player.inventory['Nano-Medpac']} left)",
        True,
        GOLD,
    )
    c4 = FONT.render("[4] Tactical Rest (+25 Energy)", True, LIGHT_GRAY)

    screen.blit(c1, (100, 220))
    screen.blit(c2, (100, 270))
    screen.blit(c3, (100, 320))
    screen.blit(c4, (100, 370))

    msg_box = pygame.Rect(80, 440, WIDTH - 160, 60)
    pygame.draw.rect(screen, DARK_GRAY, msg_box, border_radius=6)
    pygame.draw.rect(screen, CYAN, msg_box, 2, border_radius=6)
    msg_surf = FONT.render(msg, True, WHITE)
    screen.blit(msg_surf, (msg_box.x + 20, msg_box.y + 20))

    pygame.display.flip()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:
          atk = player.weapons[player.equipped_weapon]["base_atk"]
          dmg = random.randint(atk - 4, atk + 10)
          enemy_hp -= dmg
          msg = f"Fired {player.equipped_weapon} for {dmg} damage!"
        elif event.key == pygame.K_2:
          if player.energy >= 15:
            player.energy -= 15
            player.hp = min(player.max_hp, player.hp + 40)
            msg = "Shield Generator activated! Restored 40 HP."
          else:
            msg = "Not enough energy!"
            continue
        elif event.key == pygame.K_3:
          if player.inventory["Nano-Medpac"] > 0:
            player.inventory["Nano-Medpac"] -= 1
            player.hp = min(player.max_hp, player.hp + 60)
            msg = "Used Nano-Medpac! Restored 60 HP."
          else:
            msg = "No Nano-Medpacs left!"
            continue
        elif event.key == pygame.K_4:
          player.energy = min(player.max_energy, player.energy + 25)
          msg = "Rerouted power. Restored 25 Energy."

        # CHECK IF ENEMY / BOSS IS DEFEATED
        if enemy_hp <= 0:
          msg = f"🏆 Victory! {enemy_name} neutralized."
          screen.fill(SPACE_BLUE)
          screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))
          screen.blit(p_info, (100, 130))
          e_info_zero = FONT.render(
              f"{enemy_name} HP: 0/{enemy_max_hp}", True, RED
          )
          screen.blit(e_info_zero, (520, 130))
          pygame.draw.rect(screen, DARK_GRAY, msg_box, border_radius=6)
          pygame.draw.rect(screen, CYAN, msg_box, 2, border_radius=6)
          screen.blit(
              FONT.render(msg, True, GREEN), (msg_box.x + 20, msg_box.y + 20)
          )
          pygame.display.flip()

          pygame.time.delay(1500)
          player.credits += 75
          player.level += 1
          return True

        # Enemy Counter-Attack Turn
        e_dmg = random.randint(12, 22)
        player.hp -= e_dmg
        if player.hp <= 0:
          msg = "💀 Hull breached! You were defeated..."
          pygame.display.flip()
          pygame.time.delay(1800)
          return False


# ============================================================================
#                               VICTORY SPECIAL ROOM SCREEN
# ============================================================================
def show_victory_screen(screen, player):
  waiting = True
  while waiting:
    screen.fill(BLACK)

    # Draw decorative starlight background
    for i in range(50):
      sx = (i * 137) % WIDTH
      sy = (i * 91) % HEIGHT
      pygame.draw.circle(screen, WHITE, (sx, sy), 2)

    # Victory Box Frame
    box = pygame.Rect(100, 80, WIDTH - 200, HEIGHT - 160)
    pygame.draw.rect(screen, SPACE_BLUE, box, border_radius=12)
    pygame.draw.rect(screen, GOLD, box, 4, border_radius=12)

    title = VICTORY_FONT.render(
        "🌟 MISSION ACCOMPLISHED 🌟", True, GOLD
    )
    sub = BIG_FONT.render("THE OMEGA DREADNOUGHT IS DESTROYED", True, CYAN)

    p_stats = FONT.render(
        f"Commander: {player.name if hasattr(player, 'name') else 'Hero'}  | "
        f" Level Reached: {player.level}",
        True,
        WHITE,
    )
    credits_stats = FONT.render(
        f"Final Credits: {player.credits} ¢  |  Crew Members:"
        f" {player.crew if player.crew else 'Solo Explorer'}",
        True,
        WHITE,
    )
    exit_prompt = FONT.render(
        "Press [ESC] or close window to exit game.", True, GREEN
    )

    screen.blit(
        title, (WIDTH // 2 - title.get_width() // 2, box.y + 50)
    )
    screen.blit(
        sub, (WIDTH // 2 - sub.get_width() // 2, box.y + 110)
    )
    screen.blit(
        p_stats, (WIDTH // 2 - p_stats.get_width() // 2, box.y + 190)
    )
    screen.blit(
        credits_stats,
        (WIDTH // 2 - credits_stats.get_width() // 2, box.y + 230),
    )
    screen.blit(
        exit_prompt, (WIDTH // 2 - exit_prompt.get_width() // 2, box.y + 310)
    )

    pygame.display.flip()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
          pygame.quit()
          sys.exit()


# ============================================================================
#                               MARKET & HANGAR SCREEN
# ============================================================================
def open_starbase_market(screen, player):
  in_market = True
  msg = "Welcome to Starbase 7. Press keys to trade."

  while in_market:
    screen.fill(SPACE_BLUE)

    title = BIG_FONT.render(
        "🛸 STARBASE 7 - SMUGGLER MARKET & QUARTERS", True, GOLD
    )
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

    c_info = FONT.render(
        f"Your Credits: {player.credits} ¢  |  Crew: {player.crew}", True, CYAN
    )
    screen.blit(c_info, (100, 110))

    opt1 = FONT.render(
        "[1] Recruit Dr. Vex (Medic) - 70 Credits (Grants +30 Max HP)",
        True,
        WHITE,
    )
    opt2 = FONT.render(
        "[2] Buy Nano-Medpac (+60 HP) - 25 Credits", True, WHITE
    )
    opt3 = FONT.render(
        "[3] Buy Quantum Rifle (ATK: 50) - 100 Credits", True, WHITE
    )
    opt4 = FONT.render("[4] Exit Starbase Market", True, RED)

    screen.blit(opt1, (100, 180))
    screen.blit(opt2, (100, 230))
    screen.blit(opt3, (100, 280))
    screen.blit(opt4, (100, 350))

    msg_surf = FONT.render(msg, True, GREEN)
    screen.blit(msg_surf, (100, 440))

    pygame.display.flip()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:
          if "Dr. Vex" in player.crew:
            msg = "Dr. Vex is already on your crew!"
          elif player.credits >= 70:
            player.credits -= 70
            player.crew.append("Dr. Vex")
            player.max_hp += 30
            player.hp = player.max_hp
            msg = "✨ Dr. Vex joined your crew! Max HP increased."
          else:
            msg = "Not enough credits!"
        elif event.key == pygame.K_2:
          if player.credits >= 25:
            player.credits -= 25
            player.inventory["Nano-Medpac"] += 1
            msg = "Purchased 1 Nano-Medpac."
          else:
            msg = "Not enough credits!"
        elif event.key == pygame.K_3:
          if "Quantum Rifle" in player.weapons:
            msg = "You already own this weapon!"
          elif player.credits >= 100:
            player.credits -= 100
            player.weapons["Quantum Rifle"] = {
                "base_atk": 50,
                "desc": "Advanced dimensional blaster.",
            }
            player.equipped_weapon = "Quantum Rifle"
            msg = "⚔️ Purchased and equipped Quantum Rifle!"
          else:
            msg = "Not enough credits!"
        elif event.key == pygame.K_4 or event.key == pygame.K_ESCAPE:
          in_market = False


# ============================================================================
#                               MAIN GAME LOOP
# ============================================================================
def main():
  player = Player(2, 4)
  running = True
  status_msg = "Use [W, A, S, D] to pilot your starship across sectors."

  while running:
    clock.tick(FPS)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
          player.move(0, -1, GALAXY_MAP)
        elif event.key == pygame.K_s:
          player.move(0, 1, GALAXY_MAP)
        elif event.key == pygame.K_a:
          player.move(-1, 0, GALAXY_MAP)
        elif event.key == pygame.K_d:
          player.move(1, 0, GALAXY_MAP)

    # If the game is already won, trigger the special victory room screen
    if player.game_won:
      show_victory_screen(screen, player)
      break

    current_tile = GALAXY_MAP[player.y][player.x]

    if current_tile == "S":
      status_msg = "Starbase 7 detected! Press [E] to dock and trade."
      keys = pygame.key.get_pressed()
      if keys[pygame.K_e]:
        open_starbase_market(screen, player)

    elif current_tile == "1":
      if "CODE-7291" not in player.vault_codes:
        won = trigger_combat(screen, player, "Zorblaxian Marauder", 90)
        if not won:
          break
        player.vault_codes.append("CODE-7291")
        status_msg = (
            "Sector 1 Cleared! Acquired Vault Access Code: [CODE-7291]"
        )

    elif current_tile == "2":
      if "CODE-4085" not in player.vault_codes:
        won = trigger_combat(screen, player, "Cyber-Derelict Drone", 125)
        if not won:
          break
        player.vault_codes.append("CODE-4085")
        status_msg = (
            "Sector 2 Cleared! Acquired Vault Access Code: [CODE-4085]"
        )

    elif current_tile == "3":
      if "CODE-1934" not in player.vault_codes:
        won = trigger_combat(screen, player, "Quantum Sanctum Guardian", 145)
        if not won:
          break
        player.vault_codes.append("CODE-1934")
        status_msg = (
            "Sector 3 Cleared! Acquired Vault Access Code: [CODE-1934]"
        )

    elif current_tile == "B":
      if len(player.vault_codes) >= 3:
        won = trigger_combat(screen, player, "DREADNOUGHT OMEGA AI", 280)
        if won:
          player.game_won = True  # Set victory flag so it switches to the win room
        else:
          break
      else:
        status_msg = (
            f"🔒 Vault Airlock Locked! Codes found: {len(player.vault_codes)}/3."
            " Explore Sectors 1, 2, and 3 first!"
        )

    screen.fill(SPACE_BLUE)

    for row in range(len(GALAXY_MAP)):
      for col in range(COLS):
        tile = GALAXY_MAP[row][col]
        rect = pygame.Rect(
            col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE
        )

        if tile == "W":
          pygame.draw.rect(screen, DARK_GRAY, rect)
          pygame.draw.rect(screen, (60, 60, 90), rect, 1)
        elif tile == "S":
          pygame.draw.rect(screen, BLUE, rect, border_radius=6)
        elif tile == "1":
          pygame.draw.rect(screen, GREEN, rect, border_radius=6)
        elif tile == "2":
          pygame.draw.rect(screen, PURPLE, rect, border_radius=6)
        elif tile == "3":
          pygame.draw.rect(screen, GOLD, rect, border_radius=6)
        elif tile == "B":
          pygame.draw.rect(screen, RED, rect, border_radius=6)
        else:
          pygame.draw.rect(screen, (15, 20, 35), rect)
          pygame.draw.rect(screen, (25, 30, 50), rect, 1)

    player.draw(screen)

    hud_rect = pygame.Rect(0, HEIGHT - 150, WIDTH, 150)
    pygame.draw.rect(screen, (12, 16, 30), hud_rect)
    pygame.draw.rect(screen, CYAN, hud_rect, 2)

    stats_text = FONT.render(
        f"❤️ Hull HP: {player.hp}/{player.max_hp}  |  ⚡ Energy:"
        f" {player.energy}/{player.max_energy}  |  💳 Credits:"
        f" {player.credits}¢",
        True,
        WHITE,
    )
    gear_text = FONT.render(
        f"🔫 Weapon: {player.equipped_weapon}  |  👥 Crew:"
        f" {player.crew if player.crew else 'None'}  |  🔑 Vault Codes:"
        f" {len(player.vault_codes)}/3",
        True,
        GOLD,
    )
    msg_text = FONT.render(f"STATUS: {status_msg}", True, CYAN)

    screen.blit(stats_text, (20, HEIGHT - 130))
    screen.blit(gear_text, (20, HEIGHT - 95))
    screen.blit(msg_text, (20, HEIGHT - 55))

    pygame.display.flip()

  pygame.quit()
  sys.exit()


if __name__ == "__main__":
  main()
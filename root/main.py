import random
import sys
import time

# ============================================================================
#                               GAME DATA & HELPERS
# ============================================================================


def type_effect(text, delay=0.015):
    """Prints text with a typewriter effect for dramatic pacing."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def show_ascii_art(art_type):
    """Displays thematic ASCII artwork for major events."""
    art = {
        "title": r"""
  ❄️ 🧊 ❄️ 🧊 ❄️ 🧊 ❄️ 🧊 ❄️ 🧊 ❄️ 🧊 ❄️ 🧊 ❄️ 🧊 ❄️ 🧊 ❄️ 🧊 ❄️ 🧊 ❄️ 🧊 ❄️
  ______ _____  _____ ________  ___  ___ _____  _____   _____ _____ 
  |  ___|  _  ||  ___|_  /  ___| |  \/  |/  ___||  _  | /  ___/  __ \
  | |_  | | | || |__   / /\ `--. | .  . |\ `--. | | | | \ `--.| /  \/
  |  _| | | | ||  __| / /  `--. \| |\/| | `--. \| | | |  `--. \ |    
  | |   \ \_/ /| |___/ /__/ \__/ / |  | |/\__/ /\ \_/ / /\__/ / \__/\
  \_|    \___/ \____/\____/\____/\_|  |_/\____/  \___/  \____/ \____/
  ❄️ 🧊 ❄️ 🧊 ❄️ 🧊 ❄️ 🧊 ❄️ 🧊 ❄️ 🧊 ❄️ 🧊 ❄️ 🧊 ❄️ 🧊 ❄️ 🧊 ❄️ 🧊 ❄️ 🧊 ❄️
        """,
        "boss": r"""
                     .---.
                    /     \
                   | () () |
                   \  .-.  /
                  .-'`'-'`'-.
                 /  \     /  \
                /    |   |    \
               ;      ___      ;
               |     (___)     |
               |   ,       ,   |
               \  / \     / \  /
                '-'  '---'  '-'
             YETI KING - FROZEN EMPEROR
        """,
        "victory": r"""
     __   ______  _    _  _   _  _____ _____  _   _ !
     \ \ / / __ \| |  | || | | ||  ___/  ___|| | | |
      \ V /| |  | || |  | || | | || |__ \ `--. | | | |
       \ / | |  | || |  | || | | ||  __| `--. \| | | |
       | | | |__| || |__| || |_| || |___/\__/ /|_|_|_|
       \_/  \____/  \____/  \___/ \____/\____/ (_)(_)
        """,
    }
    print(art.get(art_type, ""))


# ============================================================================
#                               PLAYER CLASS
# ============================================================================


class Player:

    def __init__(self, name):
        self.name = name
        self.hp = 120
        self.max_hp = 120
        self.stamina = 50
        self.max_stamina = 50
        self.coins = 50
        self.xp = 0
        self.level = 1

        # Inventory
        self.inventory = {"Health Potions": 2, "Stamina Elixirs": 1}
        self.collectibles = []
        self.vault_codes = {}  # Format: {"Vault 1": "1234", ...}

        # Equipment & Stats
        self.weapons = {
            "Frost Dagger": {
                "base_atk": 15,
                "elem": "Ice",
                "desc": "Quick and agile ice blade.",
            }
        }
        self.equipped_weapon = "Frost Dagger"

        # Abilities (Name: {Cost, Damage, Healing, Type, Description})
        self.abilities = {
            "Ice Shard": {
                "cost": 10,
                "dmg": 25,
                "heal": 0,
                "elem": "Ice",
                "desc": "Fires a sharp cone of ice.",
            },
            "Frost Shield": {
                "cost": 15,
                "dmg": 0,
                "heal": 35,
                "elem": "Ice",
                "desc": "Surrounds user in ice, recovering HP.",
            },
        }

    def gain_xp(self, amount):
        self.xp += amount
        type_effect(f"\n🌟 Gained {amount} XP!")
        if self.xp >= self.level * 50:
            self.level += 1
            self.max_hp += 20
            self.max_stamina += 10
            self.hp = self.max_hp
            self.stamina = self.max_stamina
            type_effect(
                f"🎉 LEVEL UP! You reached Level {self.level}! HP and Stamina"
                " restored and increased!"
            )

    def show_status(self):
        print("\n" + "═" * 50)
        print(
            f"👤 PLAYER: {self.name} | Level {self.level} | XP:"
            f" {self.xp}/{self.level * 50}"
        )
        print(f"❤️ HP: {self.hp}/{self.max_hp}  | ⚡ Stamina: {self.stamina}/{self.max_stamina}")
        print(f"💰 Coins: {self.coins} gold")
        print(
            f"⚔️ Equipped Weapon: {self.equipped_weapon} (ATK:"
            f" {self.weapons[self.equipped_weapon]['base_atk']})"
        )
        print(f"🔑 Vault Codes Found: {len(self.vault_codes)}/3")
        print(f"🎒 Inventory: {list(self.inventory.keys())}")
        print(f"🏆 Collectibles: {self.collectibles}")
        print("═" * 50)


# ============================================================================
#                               ROOM SYSTEM
# ============================================================================


class GameWorld:

    def __init__(self, player):
        self.player = player

        # Room Status Flags
        self.cleared_minigame_cave = False
        self.cleared_forge_puzzle = False
        self.cleared_sanctum_riddle = False

    def merchant_shop(self):
        while True:
            print("\n" + "═" * 40)
            print("🏪 WANDERING FROST MERCHANT")
            print(f"Your Gold: {self.player.coins} coins")
            print("═" * 40)
            print(
                "1. Buy Health Potion (+40 HP) - 20 Coins\n2. Buy Stamina"
                " Elixir (+30 Stamina) - 15 Coins\n3. Buy [Glacier Breaker"
                " Hammer] (ATK: 45) - 80 Coins\n4. Buy [Aurora Beam Spell"
                " Scroll] - 60 Coins\n5. Exit Shop"
            )

            choice = input("\nSelect item (1-5): ").strip()

            if choice == "1":
                if self.player.coins >= 20:
                    self.player.coins -= 20
                    self.player.inventory["Health Potions"] = (
                        self.player.inventory.get("Health Potions", 0) + 1
                    )
                    type_effect("Bought 1 Health Potion!")
                else:
                    type_effect("Not enough coins!")
            elif choice == "2":
                if self.player.coins >= 15:
                    self.player.coins -= 15
                    self.player.inventory["Stamina Elixirs"] = (
                        self.player.inventory.get("Stamina Elixirs", 0) + 1
                    )
                    type_effect("Bought 1 Stamina Elixir!")
                else:
                    type_effect("Not enough coins!")
            elif choice == "3":
                if "Glacier Breaker Hammer" in self.player.weapons:
                    type_effect("You already own this weapon!")
                elif self.player.coins >= 80:
                    self.player.coins -= 80
                    self.player.weapons["Glacier Breaker Hammer"] = {
                        "base_atk": 45,
                        "elem": "Blunt Ice",
                        "desc": "Heavy hammer forged from ancient glacier ice.",
                    }
                    self.player.equipped_weapon = "Glacier Breaker Hammer"
                    type_effect(
                        "Equipped newly purchased Glacier Breaker Hammer!"
                    )
                else:
                    type_effect("Not enough coins!")
            elif choice == "4":
                if "Aurora Beam" in self.player.abilities:
                    type_effect("You already know this skill!")
                elif self.player.coins >= 60:
                    self.player.coins -= 60
                    self.player.abilities["Aurora Beam"] = {
                        "cost": 25,
                        "dmg": 55,
                        "heal": 0,
                        "elem": "Cosmic Ice",
                        "desc": "Radiant multi-colored freeze ray.",
                    }
                    type_effect("Learned the powerful Aurora Beam spell!")
                else:
                    type_effect("Not enough coins!")
            elif choice == "5":
                break

    def explore_ice_cave(self):
        print("\n❄️ AREA 1: ICE CAVE OF CRYSTALS")
        type_effect(
            "Glistening icicles line the cavern. You hear howling wind and"
            " growling beasts."
        )

        while True:
            print("\nWhat would you like to do?")
            print("1. Excavate Crystal Ore (Minigame)")
            print("2. Fight Frost Golem")
            print("3. Solve Crystal Beam Puzzle (Search for Code)")
            print("4. Return to Nexus")

            c = input("Choose (1-4): ").strip()

            if c == "1":
                type_effect("\n⛏️ MINIGAME: ICE PICK TIMING")
                type_effect(
                    "Press [ENTER] to strike the ore when the ticker hits"
                    " 'HOT'!"
                )

                score = 0
                for _ in range(3):
                    time.sleep(0.5)
                    print("\n[COLD] - [WARM] - [HOT!] - [WARM] - [COLD]")
                    user_input = input(
                        "Press ENTER now to mine! "
                    )  # Reaction check
                    result = random.choice(["HOT!", "WARM", "COLD"])
                    if result == "HOT!":
                        type_effect(
                            "🎯 PERFECT STRIKE! Uncovered Pure Diamond Ore!"
                        )
                        score += 30
                    else:
                        type_effect("🔨 Clang! Extracted plain ice shards.")
                        score += 10

                self.player.coins += score
                type_effect(f"Mining complete! Earned {score} Coins!")

            elif c == "2":
                golem = {
                    "name": "Frost Golem",
                    "hp": 90,
                    "max_hp": 90,
                    "atk": 18,
                    "xp": 40,
                    "coins": 35,
                }
                combat_engine(self.player, golem)

            elif c == "3":
                if "Vault 1 Code" in self.player.vault_codes:
                    type_effect("You already solved this puzzle!")
                else:
                    type_effect("\n🧩 PUZZLE: REFRACTIVE LIGHT ALIGNMENT")
                    type_effect(
                        "Align 3 prisms to redirect light into the door sensor."
                    )
                    p1 = input("Angle Prism 1 (45 / 90 / 180): ").strip()
                    p2 = input("Angle Prism 2 (45 / 90 / 180): ").strip()

                    if p1 == "90" and p2 == "45":
                        type_effect(
                            "✨ The beam reflects perfectly! A hidden panel"
                            " slides open."
                        )
                        type_effect("🔑 OBTAINED CODE 1: [8492]")
                        self.player.vault_codes["Vault 1"] = "8492"
                        self.player.collectibles.append("Crystal Prism")
                        self.player.gain_xp(30)
                    else:
                        type_effect("❌ The light missed! Try again.")

            elif c == "4":
                break

    def explore_forge(self):
        print("\n🔥 AREA 2: SUB-ZERO FROST FORGE")
        type_effect(
            "An abandoned ancient forge powered by magical blue flames."
        )

        while True:
            print("\nWhat would you like to do?")
            print("1. Craft / Upgrade Weapons")
            print("2. Battle Lava-Ice Drake")
            print("3. Unlock the Forge Vault Safe (Code Search)")
            print("4. Return to Nexus")

            c = input("Choose (1-4): ").strip()

            if c == "1":
                if "Glacial Greatsword" in self.player.weapons:
                    type_effect("Your weapons are already fully forged!")
                else:
                    if "Crystal Prism" in self.player.collectibles:
                        type_effect(
                            "🛠️ Combining Crystal Prism with your current"
                            " weapon..."
                        )
                        self.player.weapons["Glacial Greatsword"] = {
                            "base_atk": 38,
                            "elem": "Frostfire",
                            "desc": "A heavy blade capable of cleaving armor.",
                        }
                        self.player.equipped_weapon = "Glacial Greatsword"
                        type_effect(
                            "⚔️ NEW WEAPON CREATED & EQUIPPED: [Glacial"
                            " Greatsword]!"
                        )
                    else:
                        type_effect(
                            " You need a [Crystal Prism] from the Ice Cave to"
                            " forge!"
                        )

            elif c == "2":
                drake = {
                    "name": "Frostfire Drake",
                    "hp": 130,
                    "max_hp": 130,
                    "atk": 24,
                    "xp": 70,
                    "coins": 60,
                }
                combat_engine(self.player, drake)

            elif c == "3":
                if "Vault 2 Code" in self.player.vault_codes:
                    type_effect("You already unlocked the safe!")
                else:
                    type_effect("\n🔒 FORGE SAFE MEMORY PUZZLE")
                    type_effect(
                        "Memorize the color sequence glowing in the forge:"
                    )
                    seq = ["BLUE", "RED", "BLUE", "WHITE"]
                    type_effect("🔥 " + " - ".join(seq))
                    time.sleep(2)
                    print("\n" * 20)  # Clear screen effect

                    user_seq = (
                        input(
                            "Enter sequence separated by space (e.g. BLUE RED"
                            " BLUE WHITE): "
                        )
                        .strip()
                        .upper()
                        .split()
                    )

                    if user_seq == seq:
                        type_effect(
                            "🔓 Safe Unlocked! You recover the second code!"
                        )
                        type_effect("🔑 OBTAINED CODE 2: [3107]")
                        self.player.vault_codes["Vault 2"] = "3107"
                        self.player.collectibles.append("Ancient Ember")
                        self.player.gain_xp(40)
                    else:
                        type_effect("❌ Sequence incorrect! Safe locked.")

            elif c == "4":
                break

    def explore_sanctum(self):
        print("\n🏛️ AREA 3: THE ANCIENT SANCTUM OF WHISPERS")
        type_effect(
            "Ghostly spires and forgotten lore books floating in freezing"
            " wind."
        )

        while True:
            print("\nWhat would you like to do?")
            print("1. Decipher Forgotten Spellbook (Learn Ability)")
            print("2. Battle Phantom Sorcerer")
            print("3. Answer Sphinx Riddle (Code Search)")
            print("4. Return to Nexus")

            c = input("Choose (1-4): ").strip()

            if c == "1":
                if "Blizzard Tempest" in self.player.abilities:
                    type_effect("You already mastered all Sanctum spells!")
                else:
                    type_effect(
                        "📖 Deciphering glyphs... You learned [Blizzard"
                        " Tempest]!"
                    )
                    self.player.abilities["Blizzard Tempest"] = {
                        "cost": 30,
                        "dmg": 65,
                        "heal": 0,
                        "elem": "Ultimate Ice",
                        "desc": "Summons a devastating freezing storm.",
                    }

            elif c == "2":
                phantom = {
                    "name": "Phantom Sorcerer",
                    "hp": 110,
                    "max_hp": 110,
                    "atk": 22,
                    "xp": 60,
                    "coins": 50,
                }
                combat_engine(self.player, phantom)

            elif c == "3":
                if "Vault 3 Code" in self.player.vault_codes:
                    type_effect("The Sphinx already granted you the code!")
                else:
                    type_effect(
                        "\n🗿 SPHINX RIDDLE: 'I build up castles, tear down"
                        " mountains, make some men blind, help others to"
                        " see. What am I?'"
                    )
                    ans = input("Your answer: ").strip().lower()

                    if "sand" in ans or "time" in ans:
                        type_effect(
                            "✨ The Sphinx nods! 'Wisdom grants passage.'"
                        )
                        type_effect("🔑 OBTAINED CODE 3: [9521]")
                        self.player.vault_codes["Vault 3"] = "9521"
                        self.player.collectibles.append("Sanctum Seal")
                        self.player.gain_xp(50)
                    else:
                        type_effect(
                            "❌ 'Incorrect,' whispers the Sphinx. Try again."
                        )

            elif c == "4":
                break


# ============================================================================
#                               COMBAT ENGINE
# ============================================================================


def combat_engine(player, enemy):
    type_effect(f"\n⚔️ BATTLE START: {enemy['name']} approaches!")

    while enemy["hp"] > 0 and player.hp > 0:
        print("\n" + "─" * 40)
        print(
            f"👤 {player.name}: HP {player.hp}/{player.max_hp} | Stamina"
            f" {player.stamina}/{player.max_stamina}"
        )
        print(f"👾 {enemy['name']}: HP {enemy['hp']}/{enemy['max_hp']}")
        print("─" * 40)

        print("1. Weapon Attack")
        print("2. Cast Pokémon-Style Ability")
        print("3. Use Item")
        print("4. Rest (+20 Stamina)")

        choice = input("Action (1-4): ").strip()

        if choice == "1":
            # Weapon Attack
            atk_val = player.weapons[player.equipped_weapon]["base_atk"]
            dmg = random.randint(atk_val - 5, atk_val + 10)
            enemy["hp"] -= dmg
            type_effect(
                f"💥 You strike with {player.equipped_weapon} for {dmg}"
                " damage!"
            )

        elif choice == "2":
            # Ability Menu
            print("\n-- ABILITIES --")
            ab_keys = list(player.abilities.keys())
            for idx, k in enumerate(ab_keys, 1):
                data = player.abilities[k]
                print(
                    f"{idx}. {k} [Cost: {data['cost']} Stamina] ->"
                    f" {data['desc']}"
                )

            sel = input("Select Ability Number: ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(ab_keys):
                ab_name = ab_keys[int(sel) - 1]
                ab_data = player.abilities[ab_name]

                if player.stamina >= ab_data["cost"]:
                    player.stamina -= ab_data["cost"]

                    if ab_data["heal"] > 0:
                        player.hp = min(
                            player.max_hp, player.hp + ab_data["heal"]
                        )
                        type_effect(
                            f"✨ Cast {ab_name}! Restored {ab_data['heal']} HP!"
                        )
                    else:
                        dmg = ab_data["dmg"] + random.randint(5, 15)
                        enemy["hp"] -= dmg
                        type_effect(
                            f"⚡ Unleashed {ab_name}! Dealt {dmg}"
                            f" {ab_data['elem']} damage!"
                        )
                else:
                    type_effect("❌ Not enough Stamina!")
                    continue
            else:
                type_effect("Invalid selection!")
                continue

        elif choice == "3":
            # Items
            print("\n-- INVENTORY --")
            print(f"1. Health Potion ({player.inventory.get('Health Potions', 0)} left)")
            print(
                "2. Stamina Elixir"
                f" ({player.inventory.get('Stamina Elixirs', 0)} left)"
            )

            item_sel = input("Select item (1-2): ").strip()
            if item_sel == "1" and player.inventory.get("Health Potions", 0) > 0:
                player.inventory["Health Potions"] -= 1
                player.hp = min(player.max_hp, player.hp + 50)
                type_effect("🧪 Drank Health Potion! Restored 50 HP!")
            elif (
                item_sel == "2"
                and player.inventory.get("Stamina Elixirs", 0) > 0
            ):
                player.inventory["Stamina Elixirs"] -= 1
                player.stamina = min(player.max_stamina, player.stamina + 40)
                type_effect("🧪 Drank Stamina Elixir! Restored 40 Stamina!")
            else:
                type_effect("No potions remaining or invalid choice!")
                continue

        elif choice == "4":
            player.stamina = min(player.max_stamina, player.stamina + 20)
            type_effect("🧘 You took a breath and recovered 20 Stamina.")

        # Enemy Turn
        if enemy["hp"] > 0:
            e_dmg = random.randint(enemy["atk"] - 4, enemy["atk"] + 6)
            player.hp -= e_dmg
            type_effect(f"👹 {enemy['name']} counters for {e_dmg} damage!")

    if player.hp <= 0:
        type_effect("💀 You collapsed in battle...")
        return False
    else:
        type_effect(f"🏆 Defeated {enemy['name']}!")
        player.gain_xp(enemy["xp"])
        player.coins += enemy["coins"]
        type_effect(f"💰 Looted {enemy['coins']} coins!")
        return True


# ============================================================================
#                               FINAL BOSS BATTLE
# ============================================================================


def final_vault_door(player):
    show_ascii_art("boss")
    type_effect("\n🚪 THE GRAND VAULT DOOR TO THE YETI KING'S CHAMBER")
    type_effect("Three heavy steel keypads glow red.")

    req_codes = ["8492", "3107", "9521"]
    entered_codes = []

    for i in range(1, 4):
        code_input = input(f"Enter Vault Code #{i}: ").strip()
        entered_codes.append(code_input)

    if entered_codes == req_codes:
        type_effect(
            "\n🟢 CODES ACCEPTED! Steam vents release as the gigantic doors"
            " unlock!"
        )
        return start_yeti_king_boss(player)
    else:
        type_effect(
            "\n🔴 ACCESS DENIED! Invalid codes. Return and find all 3 codes in"
            " the rooms."
        )
        return False


def start_yeti_king_boss(player):
    type_effect("\n❄️ EMPEROR YETI KING DESCENDS FROM HIS THRONE!")
    boss = {
        "name": "Yeti King",
        "hp": 300,
        "max_hp": 300,
        "atk": 30,
        "phase": 1,
    }

    riddles = [
        (
            "I fly without wings, I cry without eyes. Whenever I lead, darkness"
            " flies. What am I?",
            "cloud",
        ),
        ("What gets wetter and wetter the more it dries?", "towel"),
        ("I have cities, but no houses. I have mountains, but no trees. What am I?", "map")
    ]

    while boss["hp"] > 0 and player.hp > 0:
        print("\n" + "🐉" * 25)
        print(f"👤 {player.name}: HP {player.hp}/{player.max_hp} | Stamina {player.stamina}/{player.max_stamina}")
        print(f"👑 YETI KING (PHASE {boss['phase']}): HP {boss['hp']}/{boss['max_hp']}")
        print("🐉" * 25)

        print("1. Weapon Attack")
        print("2. Cast Pokémon-Style Ability")
        print("3. Use Item")
        print("4. Outsmart with Riddle Solution (Massive Psychic Damage)")

        c = input("Action (1-4): ").strip()

        if c == "1":
            atk_val = player.weapons[player.equipped_weapon]["base_atk"]
            dmg = random.randint(atk_val, atk_val + 15)
            boss["hp"] -= dmg
            type_effect(f"💥 Strike landed for {dmg} damage!")

        elif c == "2":
            ab_keys = list(player.abilities.keys())
            for idx, k in enumerate(ab_keys, 1):
                data = player.abilities[k]
                print(f"{idx}. {k} [Cost: {data['cost']} Stamina]")

            sel = input("Select Ability: ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(ab_keys):
                ab_name = ab_keys[int(sel) - 1]
                ab_data = player.abilities[ab_name]

                if player.stamina >= ab_data["cost"]:
                    player.stamina -= ab_data["cost"]
                    if ab_data["heal"] > 0:
                        player.hp = min(
                            player.max_hp, player.hp + ab_data["heal"]
                        )
                        type_effect(f"✨ Restored {ab_data['heal']} HP!")
                    else:
                        dmg = ab_data["dmg"] + random.randint(10, 20)
                        boss["hp"] -= dmg
                        type_effect(
                            f"⚡ Unleashed {ab_name}! Dealt {dmg} elemental"
                            " damage!"
                        )
                else:
                    type_effect("Not enough Stamina!")
                    continue

        elif c == "3":
            if player.inventory.get("Health Potions", 0) > 0:
                player.inventory["Health Potions"] -= 1
                player.hp = min(player.max_hp, player.hp + 60)
                type_effect("🧪 Restored 60 HP!")
            else:
                type_effect("No Health Potions left!")
                continue

        elif c == "4":
            riddle, ans = random.choice(riddles)
            type_effect(f"\n🧠 YETI KING'S TRIAL: '{riddle}'")
            user_a = input("Your answer: ").strip().lower()

            if ans in user_a:
                type_effect(
                    "✨ CORRECT! The Yeti King is stunned by your genius and"
                    " takes 80 psychic damage!"
                )
                boss["hp"] -= 80
            else:
                type_effect("❌ WRONG! The Yeti King counters with a blast!")
                player.hp -= 25

        # Phase transition check
        if boss["hp"] <= 150 and boss["phase"] == 1:
            boss["phase"] = 2
            boss["atk"] += 10
            type_effect(
                "\n🔥 THE YETI KING ENRAGES! PHASE 2 BEGINS! ATTACK POWER"
                " INCREASED!"
            )

        # Boss Attack
        if boss["hp"] > 0:
            bdmg = random.randint(boss["atk"] - 5, boss["atk"] + 10)
            player.hp -= bdmg
            type_effect(f"❄️ Yeti King strikes with Avalanche for {bdmg} damage!")

    if player.hp <= 0:
        type_effect("\n☠️ The Blizzard overwhelms you... Game Over.")
        return False
    else:
        show_ascii_art("victory")
        type_effect(
            f"🎉 VICTORY! {player.name} HAS DEFEATED THE YETI KING AND SAVED THE"
            " TUNDRA!"
        )
        return True


# ============================================================================
#                               MAIN GAME LOOP
# ============================================================================


def main():
    show_ascii_art("title")
    print("Welcome to Blizzard Breach: Frozen Fortress Edition!")
    p_name = input("Enter your Hero's name: ").strip()
    if not p_name:
        p_name = "Hero"

    player = Player(p_name)
    world = GameWorld(player)

    while player.hp > 0:
        print("\n" + "🏰" * 20)
        print("📍 MAIN NEXUS HALL")
        print("1. Explore [Area 1: Ice Cave of Crystals]")
        print("2. Explore [Area 2: Sub-Zero Frost Forge]")
        print("3. Explore [Area 3: Ancient Sanctum of Whispers]")
        print("4. Visit Wandering Merchant")
        print("5. Check Character Stats & Inventory")
        print("6. OPEN THE FINAL VAULT DOOR (Requires 3 Codes)")
        print("7. Quit Game")

        c = input("\nWhere would you like to go? (1-7): ").strip()

        if c == "1":
            world.explore_ice_cave()
        elif c == "2":
            world.explore_forge()
        elif c == "3":
            world.explore_sanctum()
        elif c == "4":
            world.merchant_shop()
        elif c == "5":
            player.show_status()
        elif c == "6":
            won = final_vault_door(player)
            if won or player.hp <= 0:
                break
        elif c == "7":
            type_effect("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
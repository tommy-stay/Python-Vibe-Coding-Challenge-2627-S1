import random
import sys
import time

# ============================================================================
#                               GAME DATA & HELPERS
# ============================================================================


def type_effect(text, delay=0.012):
    """Prints text with a typewriter effect for dramatic cinematic pacing."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def show_ascii_art(art_type):
    """Displays thematic ASCII artwork for major game milestones."""
    art = {
        "title": r"""
  🚀 ✨ 🌌 ✨ 🚀 ✨ 🌌 ✨ 🚀 ✨ 🌌 ✨ 🚀 ✨ 🌌 ✨ 🚀 ✨ 🌌 ✨ 🚀 ✨ 🌌 ✨ 🚀
   _____ _____  ___  ______ ______  _____  _   _  _____  ______ 
  / ____|_   _|/ _ \ | ___ \| ___ \/  _  || | | ||  _  || ___ \
 / /     | | / /_\ \| |_/ /| |_/ /| | | || | | || | | || |_/ /
 \ \     | | |  _  || ___ \| ___ \| | | || | | || | | ||  _  / 
  \ \____| | | | | || |_/ /| |_/ /\ \_/ /\ \_/ /\ \_/ /| | \ \ 
   \_____|\_/ \_| |_/\____/ \____/  \___/  \___/  \___/ \_|  \_|
  🚀 ✨ 🌌 ✨ 🚀 ✨ 🌌 ✨ 🚀 ✨ 🌌 ✨ 🚀 ✨ 🌌 ✨ 🚀 ✨ 🌌 ✨ 🚀 ✨ 🌌 ✨ 🚀
        """,
        "boss": r"""
             /\
            /  \      [ DREADNOUGHT OMEGA AI ]
           / /\ \     Target Locked. Preparing Annihilation.
          | |  | |
          | |()()|
          \ \  / /
           '----'
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
        self.hp = 140
        self.max_hp = 140
        self.energy = 70
        self.max_energy = 70
        self.credits = 120
        self.xp = 0
        self.level = 1

        # Crew & Ship Upgrades
        self.crew = []
        self.ship_upgrades = {
            "Reinforced Hull Plating": False,
            "Hyperdrive Booster": False,
        }

        # Inventory & Vaults
        self.inventory = {"Nano-Medpacs": 3, "Energy Cells": 2}
        self.collectibles = []
        self.vault_codes = {}  # e.g., {"Sector 1": "7291"}

        # Weapons & Pokémon-style Abilities
        self.weapons = {
            "Pulse Blaster": {
                "base_atk": 18,
                "type": "Energy",
                "desc": "Standard-issue starfleet sidearm.",
            }
        }
        self.equipped_weapon = "Pulse Blaster"

        self.abilities = {
            "Plasma Beam": {
                "cost": 12,
                "dmg": 30,
                "heal": 0,
                "elem": "Plasma",
                "desc": "Fires a concentrated beam of superheated gas.",
            },
            "Shield Generator": {
                "cost": 15,
                "dmg": 0,
                "heal": 45,
                "elem": "Tech",
                "desc": "Rebuilds personal shields, restoring hull HP.",
            },
        }

    def gain_xp(self, amount):
        self.xp += amount
        type_effect(f"\n🌟 Gained {amount} Experience Points!")
        if self.xp >= self.level * 60:
            self.level += 1
            self.max_hp += 30
            self.max_energy += 20
            self.hp = self.max_hp
            self.energy = self.max_energy
            type_effect(
                f"🎉 COMMANDER RANK UP! You reached Level {self.level}! Max HP"
                " & Energy increased and fully restored!"
            )

    def show_status(self):
        print("\n" + "═" * 60)
        print(
            f"👨‍✈️ COMMANDER: {self.name} | Rank Level {self.level} | XP:"
            f" {self.xp}/{self.level * 60}"
        )
        print(
            f"❤️ Hull Integrity: {self.hp}/{self.max_hp}  | ⚡ Energy:"
            f" {self.energy}/{self.max_energy}"
        )
        print(f"💳 Galactic Credits: {self.credits} ¢")
        print(
            f"🔫 Equipped Weapon: {self.equipped_weapon} (ATK:"
            f" {self.weapons[self.equipped_weapon]['base_atk']})"
        )
        print(f"👥 Crew Recruited: {[c['name'] for c in self.crew]}")
        print(f"🛠️ Ship Upgrades: {list(self.ship_upgrades.keys())}")
        print(f"🔑 Vault Access Codes: {len(self.vault_codes)}/3")
        print(f"🎒 Inventory: {list(self.inventory.keys())}")
        print(f"🏆 Alien Relics: {self.collectibles}")
        print("═" * 60)


# ============================================================================
#                               GALACTIC WORLDS & ROOMS
# ============================================================================


class GalaxyWorld:

    def __init__(self, player):
        self.player = player

    def space_station_market(self):
        while True:
            print("\n" + "═" * 50)
            print("🛸 STARBASE 7 - SMUGGLER MARKET & CREW QUARTERS")
            print(f"Your Credits: {self.player.credits} ¢")
            print("═" * 50)
            print("1. Buy Nano-Medpac (+60 HP) - 25 Credits")
            print("2. Buy Energy Cell (+50 Energy) - 20 Credits")
            print(
                "3. Recruit Crew Member [Dr. Vex - Medic] - 80 Credits\n   (Perk:"
                " Grants +20 Max HP & automatic post-battle healing)"
            )
            print(
                "4. Recruit Crew Member [Sprocket - Engineer] - 90 Credits\n  "
                " (Perk: Boosts all weapon damage by +10)"
            )
            print(
                "5. Buy [Quantum Disruptor Rifle] (ATK: 55) - 120 Credits"
            )
            print("6. Talk to Crew / Visit Ship Hangar")
            print("7. Return to Starship Bridge")

            choice = input("\nSelect option (1-7): ").strip()

            if choice == "1":
                if self.player.credits >= 25:
                    self.player.credits -= 25
                    self.player.inventory["Nano-Medpacs"] = (
                        self.player.inventory.get("Nano-Medpacs", 0) + 1
                    )
                    type_effect("Bought 1 Nano-Medpac!")
                else:
                    type_effect("❌ Not enough credits!")
            elif choice == "2":
                if self.player.credits >= 20:
                    self.player.credits -= 20
                    self.player.inventory["Energy Cells"] = (
                        self.player.inventory.get("Energy Cells", 0) + 1
                    )
                    type_effect("Bought 1 Energy Cell!")
                else:
                    type_effect("❌ Not enough credits!")
            elif choice == "3":
                if any(c["name"] == "Dr. Vex" for c in self.player.crew):
                    type_effect("Dr. Vex is already on your crew!")
                elif self.player.credits >= 80:
                    self.player.credits -= 80
                    self.player.crew.append(
                        {
                            "name": "Dr. Vex",
                            "role": "Chief Medical Officer",
                            "perk": "Heal",
                        }
                    )
                    self.player.max_hp += 20
                    self.player.hp = self.player.max_hp
                    type_effect(
                        "✨ Dr. Vex joined your crew! Max HP permanently"
                        " increased by 20."
                    )
                else:
                    type_effect("❌ Not enough credits!")
            elif choice == "4":
                if any(c["name"] == "Sprocket" for c in self.player.crew):
                    type_effect("Sprocket is already on your crew!")
                elif self.player.credits >= 90:
                    self.player.credits -= 90
                    self.player.crew.append(
                        {
                            "name": "Sprocket",
                            "role": "Master Engineer",
                            "perk": "Damage",
                        }
                    )
                    for w in self.player.weapons.values():
                        w["base_atk"] += 10
                    type_effect(
                        "✨ Sprocket joined your crew! All weapon attacks"
                        " permanently boosted!"
                    )
                else:
                    type_effect("❌ Not enough credits!")
            elif choice == "5":
                if "Quantum Disruptor Rifle" in self.player.weapons:
                    type_effect("You already own this weapon!")
                elif self.player.credits >= 120:
                    self.player.credits -= 120
                    self.player.weapons["Quantum Disruptor Rifle"] = {
                        "base_atk": 55,
                        "type": "Quantum",
                        "desc": "Alien rifle that tears through dimensional armor.",
                    }
                    self.player.equipped_weapon = "Quantum Disruptor Rifle"
                    type_effect(
                        "⚔️ Equipped newly purchased Quantum Disruptor Rifle!"
                    )
                else:
                    type_effect("❌ Not enough credits!")
            elif choice == "6":
                self.ship_hangar_menu()
            elif choice == "7":
                break

    def ship_hangar_menu(self):
        while True:
            print("\n" + "═" * 40)
            print("🛠️ STARSHIP HANGAR & UPGRADE BAY")
            print("═" * 40)
            print(
                "1. Install Reinforced Hull Plating (Costs 75 Credits) - Grants"
                " +40 Max HP"
            )
            print(
                "2. Install Hyperdrive Booster (Costs 75 Credits) - Unlocks"
                " Special Tactical Maneuvers"
            )
            print("3. Back to Market")

            c = input("Choose (1-3): ").strip()
            if c == "1":
                if self.player.ship_upgrades["Reinforced Hull Plating"]:
                    type_effect("Hull Plating already installed!")
                elif self.player.credits >= 75:
                    self.player.credits -= 75
                    self.player.ship_upgrades[
                        "Reinforced Hull Plating"
                    ] = True
                    self.player.max_hp += 40
                    self.player.hp = self.player.max_hp
                    type_effect(
                        "🟢 Hull Plating Installed! Max HP permanently increased"
                        " to "
                        + str(self.player.max_hp)
                    )
                else:
                    type_effect("❌ Not enough credits!")
            elif c == "2":
                if self.player.ship_upgrades["Hyperdrive Booster"]:
                    type_effect("Hyperdrive Booster already installed!")
                elif self.player.credits >= 75:
                    self.player.credits -= 75
                    self.player.ship_upgrades["Hyperdrive Booster"] = True
                    type_effect(
                        "🟢 Hyperdrive Booster Installed! Your ship's evasion"
                        " is enhanced."
                    )
                else:
                    type_effect("❌ Not enough credits!")
            elif c == "3":
                break

    def explore_zorblax(self):
        print("\n🪐 SECTOR 1: PLANET ZORBLAX (CRYSTAL MINES)")
        type_effect(
            "Floating islands of violet crystals glow under a twin sun"
            " system."
        )

        while True:
            print("\nWhat would you like to do?")
            print("1. Mine Hyper-Crystals (Minigame Activity)")
            print("2. Fight Rogue Alien Marauder")
            print("3. Hack Holographic Terminal (Search for Vault Code 1)")
            print("4. Return to Starship Bridge")

            c = input("Choose (1-4): ").strip()

            if c == "1":
                type_effect("\n⛏️ MINIGAME: RESONANCE HARVESTING")
                type_effect(
                    "Timing the pulse crystal resonance core to maximize"
                    " output..."
                )

                score = 0
                for _ in range(3):
                    time.sleep(0.4)
                    print(
                        "\n[UNSTABLE] - [SYNCHRONIZING] - [OPTIMAL PULSE!] -"
                        " [OVERLOAD]"
                    )
                    input("Press ENTER to harvest crystal: ")
                    roll = random.choice(
                        ["OPTIMAL PULSE!", "SYNCHRONIZING", "UNSTABLE"]
                    )
                    if roll == "OPTIMAL PULSE!":
                        type_effect(
                            "🎯 PERFECT HARVEST! Extracted Pure Neutron Core!"
                        )
                        score += 40
                    else:
                        type_effect(
                            "⚡ Minor feedback surge! Extracted raw scrap"
                            " shards."
                        )
                        score += 20

                self.player.credits += score
                type_effect(
                    f"Harvest complete! Transferred {score} credits to your"
                    " account."
                )

            elif c == "2":
                alien = {
                    "name": "Zorblaxian Marauder",
                    "hp": 105,
                    "max_hp": 105,
                    "atk": 20,
                    "xp": 50,
                    "credits": 45,
                }
                combat_engine(self.player, alien)

            elif c == "3":
                if "Sector 1 Code" in self.player.vault_codes:
                    type_effect(
                        "You already extracted the code from this terminal."
                    )
                else:
                    type_effect("\n💻 HACKING CIPHER: ENTER FREQUENCY MATRIX")
                    ans = input(
                        "What is the square root of 81 multiplied by 10? "
                    ).strip()
                    if ans == "90":
                        type_effect(
                            "✨ Decryption Successful! Mainframe unlocks data"
                            " packet."
                        )
                        type_effect("🔑 OBTAINED CODE 1: [7291]")
                        self.player.vault_codes["Sector 1"] = "7291"
                        self.player.collectibles.append("Neutron Core Relic")
                        self.player.gain_xp(40)
                    else:
                        type_effect(
                            "❌ Decryption Failed! Security lock engaged."
                        )

            elif c == "4":
                break

    def explore_derelict(self):
        print("\n🛸 SECTOR 2: THE ABANDONED CYBER-DERELICT SHIP")
        type_effect(
            "A colossal ghost ship drifting silently through the asteroid"
            " belt."
        )

        while True:
            print("\nWhat would you like to do?")
            print("1. Scavenge Ship Armory (Weapon & Loot Check)")
            print("2. Fight Infected Cyborg Drone")
            print("3. Override Security Vault Safe (Search for Vault Code 2)")
            print("4. Return to Starship Bridge")

            c = input("Choose (1-4): ").strip()

            if c == "1":
                if "Plasma Blade" in self.player.weapons:
                    type_effect(
                        "You have already scavenged everything from this"
                        " armory."
                    )
                else:
                    type_effect(
                        "🛠️ Searching armory lockers... You discover an"
                        " advanced [Plasma Blade] weapon module!"
                    )
                    self.player.weapons["Plasma Blade"] = {
                        "base_atk": 48,
                        "type": "Energy Melee",
                        "desc": "Superheated plasma edge capable of slicing steel.",
                    }
                    self.player.equipped_weapon = "Plasma Blade"
                    self.player.collectibles.append("Starfleet Dogtags")
                    self.player.gain_xp(45)

            elif c == "2":
                drone = {
                    "name": "Infected Cyborg Drone",
                    "hp": 130,
                    "max_hp": 130,
                    "atk": 25,
                    "xp": 65,
                    "credits": 60,
                }
                combat_engine(self.player, drone)

            elif c == "3":
                if "Sector 2 Code" in self.player.vault_codes:
                    type_effect("The vault safe has already been bypassed.")
                else:
                    type_effect("\n🔐 VAULT SAFE MEMORY CIRCUIT")
                    type_effect(
                        "Memorize the flashing light sequence on the panel:"
                    )
                    seq = ["PURPLE", "CYAN", "PURPLE", "GOLD"]
                    type_effect("💡 " + " - ".join(seq))
                    time.sleep(2.5)
                    print("\n" * 25)

                    user_seq = (
                        input(
                            "Enter sequence separated by space (e.g. PURPLE CYAN"
                            " PURPLE GOLD): "
                        )
                        .strip()
                        .upper()
                        .split()
                    )
                    if user_seq == seq:
                        type_effect(
                            "🔓 Circuit bypassed! Safe door clicks open."
                        )
                        type_effect("🔑 OBTAINED CODE 2: [4085]")
                        self.player.vault_codes["Sector 2"] = "4085"
                        self.player.gain_xp(50)
                    else:
                        type_effect(
                            "❌ Incorrect sequence! Electric shock feedback."
                        )

            elif c == "4":
                break

    def explore_sanctum(self):
        print("\n🏛️ SECTOR 3: QUANTUM SANCTUM OF THE ELDERS")
        type_effect(
            "An ancient temple floating in deep space, glowing with stellar"
            " energy."
        )

        while True:
            print("\nWhat would you like to do?")
            print("1. Meditate at Elder Shrine (Unlock Ultimate Ability)")
            print("2. Fight Void Guardian Entity")
            print("3. Answer Celestial Oracle Riddle (Search for Vault Code 3)")
            print("4. Return to Starship Bridge")

            c = input("Choose (1-4): ").strip()

            if c == "1":
                if "Supernova Blast" in self.player.abilities:
                    type_effect(
                        "You have already mastered the ancient shrines."
                    )
                else:
                    type_effect(
                        "🌌 Cosmic energy floods your mind. You learned"
                        " [Supernova Blast]!"
                    )
                    self.player.abilities["Supernova Blast"] = {
                        "cost": 30,
                        "dmg": 75,
                        "heal": 0,
                        "elem": "Cosmic",
                        "desc": "Summons miniature star fire to incinerate foes.",
                    }
                    self.player.gain_xp(55)

            elif c == "2":
                guardian = {
                    "name": "Void Guardian",
                    "hp": 155,
                    "max_hp": 155,
                    "atk": 28,
                    "xp": 80,
                    "credits": 75,
                }
                combat_engine(self.player, guardian)

            elif c == "3":
                if "Sector 3 Code" in self.player.vault_codes:
                    type_effect("The Oracle has already granted you audience.")
                else:
                    type_effect(
                        "\n👁️ ORACLE RIDDLE: 'I have no beginning, middle, or"
                        " end, and all planets dance around me. What am I?'"
                    )
                    ans = input("Your answer: ").strip().lower()
                    if "orbit" in ans or "circle" in ans or "ring" in ans:
                        type_effect(
                            "✨ The Oracle beams with starlight! 'Your mind is"
                            " sharp, Traveler.'"
                        )
                        type_effect("🔑 OBTAINED CODE 3: [1934]")
                        self.player.vault_codes["Sector 3"] = "1934"
                        self.player.collectibles.append("Elder Starlight Orb")
                        self.player.gain_xp(65)
                    else:
                        type_effect(
                            "❌ 'Flawed logic,' echoes the Oracle. Try again."
                        )

            elif c == "4":
                break


# ============================================================================
#                               COMBAT ENGINE
# ============================================================================


def combat_engine(player, enemy):
    type_effect(
        f"\n⚠️ TACTICAL ALERT: Hostile encounter with {enemy['name']}!"
    )

    while enemy["hp"] > 0 and player.hp > 0:
        print("\n" + "─" * 45)
        print(
            f"👨‍✈️ {player.name}: HP {player.hp}/{player.max_hp} | Energy"
            f" {player.energy}/{player.max_energy}"
        )
        print(f"👾 {enemy['name']}: HP {enemy['hp']}/{enemy['max_hp']}")
        print("─" * 45)

        print("1. Standard Weapon Attack")
        print("2. Cast Pokémon-Style Combat Ability")
        print("3. Use Inventory Item")
        print("4. Tactical Rest (+30 Energy)")

        choice = input("Select combat action (1-4): ").strip()

        if choice == "1":
            atk_val = player.weapons[player.equipped_weapon]["base_atk"]
            dmg = random.randint(atk_val - 4, atk_val + 14)
            enemy["hp"] -= dmg
            type_effect(
                f"💥 Fired {player.equipped_weapon}! Dealt {dmg} damage to"
                f" {enemy['name']}."
            )

        elif choice == "2":
            print("\n-- STARFLEET ABILITIES --")
            ab_keys = list(player.abilities.keys())
            for idx, k in enumerate(ab_keys, 1):
                data = player.abilities[k]
                print(
                    f"{idx}. {k} [Energy Cost: {data['cost']}] ->"
                    f" {data['desc']}"
                )

            sel = input("Select ability number: ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(ab_keys):
                ab_name = ab_keys[int(sel) - 1]
                ab_data = player.abilities[ab_name]

                if player.energy >= ab_data["cost"]:
                    player.energy -= ab_data["cost"]
                    if ab_data["heal"] > 0:
                        player.hp = min(
                            player.max_hp, player.hp + ab_data["heal"]
                        )
                        type_effect(
                            f"🛡️ Activated {ab_name}! Restored"
                            f" {ab_data['heal']} hull HP."
                        )
                    else:
                        dmg = ab_data["dmg"] + random.randint(10, 20)
                        enemy["hp"] -= dmg
                        type_effect(
                            f"⚡ Unleashed {ab_name}! Dealt {dmg}"
                            f" {ab_data['elem']} damage!"
                        )
                else:
                    type_effect("❌ Insufficient energy!")
                    continue
            else:
                type_effect("Invalid choice!")
                continue

        elif choice == "3":
            print("\n-- INVENTORY --")
            print(
                "1. Nano-Medpac"
                f" ({player.inventory.get('Nano-Medpacs', 0)} left)"
            )
            print(
                "2. Energy Cell"
                f" ({player.inventory.get('Energy Cells', 0)} left)"
            )

            item_sel = input("Select item (1-2): ").strip()
            if (
                item_sel == "1"
                and player.inventory.get("Nano-Medpacs", 0) > 0
            ):
                player.inventory["Nano-Medpacs"] -= 1
                player.hp = min(player.max_hp, player.hp + 60)
                type_effect("🧪 Nano-Medpac applied! Restored 60 HP.")
            elif (
                item_sel == "2"
                and player.inventory.get("Energy Cells", 0) > 0
            ):
                player.inventory["Energy Cells"] -= 1
                player.energy = min(
                    player.max_energy, player.energy + 50
                )
                type_effect("🔋 Energy Cell plugged in! Restored 50 Energy.")
            else:
                type_effect("No items available or invalid selection!")
                continue

        elif choice == "4":
            player.energy = min(
                player.max_energy, player.energy + 30
            )
            type_effect("🧘 Rerouted auxiliary power. Restored 30 Energy.")

        # Enemy Turn
        if enemy["hp"] > 0:
            e_dmg = random.randint(enemy["atk"] - 4, enemy["atk"] + 8)
            player.hp -= e_dmg
            type_effect(
                f"👾 {enemy['name']} retaliates, hitting your shields for"
                f" {e_dmg} damage!"
            )

    if player.hp <= 0:
        type_effect(
            "\n💀 Your ship's hull has been breached... Mission Failed."
        )
        return False
    else:
        type_effect(f"🏆 Victory! {enemy['name']} neutralized.")
        player.gain_xp(enemy["xp"])
        player.credits += enemy["credits"]
        type_effect(f"💳 Salvaged {enemy['credits']} galactic credits!")
        if any(c["perk"] == "Heal" for c in player.crew):
            player.hp = min(player.max_hp, player.hp + 15)
            type_effect(
                "✨ Dr. Vex provided medical maintenance (+15 HP recovered)!"
            )
        return True


# ============================================================================
#                               FINAL BOSS BATTLE
# ============================================================================


def final_dreadnought_airlock(player):
    show_ascii_art("boss")
    type_effect(
        "\n🚪 YOU ARRIVE AT THE OMEGA DREADNOUGHT ANTECHAMBER."
    )
    type_effect(
        "Three biometric security locks flash crimson across the armored"
        " bulkhead."
    )

    req_codes = ["7291", "4085", "1934"]
    entered_codes = []

    for i in range(1, 4):
        c_input = input(f"Enter Vault Access Code #{i}: ").strip()
        entered_codes.append(c_input)

    if entered_codes == req_codes:
        type_effect(
            "\n🟢 ALL CODES ACCEPTED! Hydraulic blast doors hiss open..."
        )
        return start_dreadnought_boss(player)
    else:
        type_effect(
            "\n🔴 LOCKOUT ENGAGED! Invalid access codes. Explore sectors and"
            " find all 3 codes."
        )
        return False


def start_dreadnought_boss(player):
    type_effect(
        "\n⚡ THE SUPREME OVERLORD AI AND ITS DREADNOUGHT CORE ACTIVATE!"
    )
    boss = {
        "name": "Dreadnought Supreme AI",
        "hp": 380,
        "max_hp": 380,
        "atk": 32,
        "phase": 1,
    }

    boss_riddles = [
        (
            "I speak without a mouth and hear without ears. I have no body, but"
            " I come alive with wind. What am I?",
            "echo",
        ),
        (
            "I am full of holes, yet I still hold a massive amount of weight."
            " What am I?",
            "sponge",
        ),
        (
            "What can travel around the entire galaxy while staying right in"
            " the same spot?",
            "stamp",
        ),
    ]

    while boss["hp"] > 0 and player.hp > 0:
        print("\n" + "🚀" * 25)
        print(
            f"👨‍✈️ {player.name}: HP {player.hp}/{player.max_hp} | Energy"
            f" {player.energy}/{player.max_energy}"
        )
        print(
            f"👑 {boss['name']} (PHASE {boss['phase']}): HP"
            f" {boss['hp']}/{boss['max_hp']}"
        )
        print("🚀" * 25)

        print("1. Standard Weapon Attack")
        print("2. Cast Pokémon-Style Combat Ability")
        print("3. Use Inventory Item")
        print(
            "4. Overload AI Mainframe with Logic Riddle (Massive Psychic"
            " Damage)"
        )

        choice = input("Select final battle action (1-4): ").strip()

        if choice == "1":
            atk_val = player.weapons[player.equipped_weapon]["base_atk"]
            dmg = random.randint(atk_val, atk_val + 20)
            boss["hp"] -= dmg
            type_effect(
                f"💥 Direct hit with {player.equipped_weapon}! Dealt {dmg}"
                " damage."
            )

        elif choice == "2":
            ab_keys = list(player.abilities.keys())
            for idx, k in enumerate(ab_keys, 1):
                data = player.abilities[k]
                print(
                    f"{idx}. {k} [Energy Cost: {data['cost']}] ->"
                    f" {data['desc']}"
                )

            sel = input("Select ability number: ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(ab_keys):
                ab_name = ab_keys[int(sel) - 1]
                ab_data = player.abilities[ab_name]

                if player.energy >= ab_data["cost"]:
                    player.energy -= ab_data["cost"]
                    if ab_data["heal"] > 0:
                        player.hp = min(
                            player.max_hp, player.hp + ab_data["heal"]
                        )
                        type_effect(
                            f"🛡️ Activated {ab_name}! Restored"
                            f" {ab_data['heal']} HP."
                        )
                    else:
                        dmg = ab_data["dmg"] + random.randint(12, 22)
                        boss["hp"] -= dmg
                        type_effect(
                            f"⚡ Unleashed {ab_name}! Dealt {dmg}"
                            f" {ab_data['elem']} damage!"
                        )
                else:
                    type_effect("❌ Insufficient energy!")
                    continue
            else:
                type_effect("Invalid selection!")
                continue

        elif choice == "3":
            if player.inventory.get("Nano-Medpacs", 0) > 0:
                player.inventory["Nano-Medpacs"] -= 1
                player.hp = min(player.max_hp, player.hp + 70)
                type_effect("🧪 Nano-Medpac used! Restored 70 HP.")
            else:
                type_effect("No Nano-Medpacs remaining!")
                continue

        elif choice == "4":
            riddle, ans = random.choice(boss_riddles)
            type_effect(
                f"\n🧠 MAINFRAME SECURITY CHALLENGE: '{riddle}'"
            )
            user_ans = input("Your answer: ").strip().lower()

            if ans in user_ans:
                type_effect(
                    "✨ CORRECT LOGIC! The AI experiences a fatal logic loop,"
                    " taking 95 quantum damage!"
                )
                boss["hp"] -= 95
            else:
                type_effect(
                    "❌ ERROR! Firewall rejects your answer. AI counter-attacks"
                    " with laser fire!"
                )
                player.hp -= 25

        # Phase 2 Enrage Check
        if boss["hp"] <= 190 and boss["phase"] == 1:
            boss["phase"] = 2
            boss["atk"] += 12
            type_effect(
                "\n🚨 WARNING: DREADNOUGHT ENTERED OVERDRIVE PHASE 2! ATTACK"
                " POWER SURGED!"
            )

        # Boss Turn
        if boss["hp"] > 0:
            b_dmg = random.randint(boss["atk"] - 4, boss["atk"] + 10)
            player.hp -= b_dmg
            type_effect(
                f"🔥 Dreadnought fires Plasma Cannon for {b_dmg} damage!"
            )

    if player.hp <= 0:
        type_effect(
            "\n☠️ Your starship has been vaporized by the Dreadnought AI..."
            " Game Over."
        )
        return False
    else:
        show_ascii_art("victory")
        type_effect(
            f"\n🎉 VICTORY! {player.name} AND CREW HAVE DEFEATED THE DREADNOUGHT"
            " AI AND SAVED THE GALAXY!"
        )
        return True


# ============================================================================
#                               MAIN GAME LOOP
# ============================================================================


def main():
    show_ascii_art("title")
    print(
        "Welcome to Starbound Odyssey: The Vortex Chronicles (Intergalactic"
        " Edition)!"
    )
    p_name = input("Enter your Starfleet Commander name: ").strip()
    if not p_name:
        p_name = "Commander Rex"

    player = Player(p_name)
    galaxy = GalaxyWorld(player)

    while player.hp > 0:
        print("\n" + "🌌" * 22)
        print("📍 STARSHIP BRIDGE - COMMAND NEXUS")
        print(f"💳 Credits: {player.credits} ¢ | 👥 Crew: {len(player.crew)}")
        print(f"🔑 Vault Codes Found: {len(player.vault_codes)}/3")
        print("🌌" * 22)
        print("Where would you like to set coordinates?")
        print("1. Explore Sector 1: Planet Zorblax (Crystal Mines & Puzzles)")
        print(
            "2. Explore Sector 2: Abandoned Cyber-Derelict Ship (Armory & Safe)"
        )
        print(
            "3. Explore Sector 3: Quantum Sanctum of Elders (Shrine & Oracle)"
        )
        print("4. Visit Starbase 7 (Smuggler Market, Upgrades & Crew)")
        print("5. Inspect Commander Status & Inventory")
        print(
            "6. ENTER OMEGA DREADNOUGHT FINAL AIRLOCK (Requires all 3 Codes)"
        )
        print("7. Abandon Mission / Quit")

        choice = input("\nEnter navigation choice (1-7): ").strip()

        if choice == "1":
            galaxy.explore_zorblax()
        elif choice == "2":
            galaxy.explore_derelict()
        elif choice == "3":
            galaxy.explore_sanctum()
        elif choice == "4":
            galaxy.space_station_market()
        elif choice == "5":
            player.show_status()
        elif choice == "6":
            won = final_dreadnought_airlock(player)
            if won or player.hp <= 0:
                break
        elif choice == "7":
            type_effect(
                "Powering down hyperdrive... Thanks for playing Starbound"
                " Odyssey!"
            )
            break
        else:
            type_effect("Invalid coordinates entered. Choose 1-7.")


if __name__ == "__main__":
    main()
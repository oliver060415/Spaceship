from spaceship import Spaceship
import json
import random


class Encounter:
    # 2. Travel
    # 1. Map(not images only text for now)
    # 7. Shop system
    # 8. Leveling up system 
    def __init__(self, name: str, danger_level: int, ships: list[Spaceship]):
        self.name = name
        self.danger_level = danger_level
        self.ships = ships
        self.enemy_count = len(ships)

    def __repr__(self):
        return f"Encounter({self.name}, Danger: {self.danger_level}, Enemies: {self.enemy_count}, Ships: {self.ships})"

                                          
class Item:
    name: str
    price: float
    desc: str
    
    def __init__(self,name,desc,price):
        self.name = name
        self.price = price
        self.desc = desc

    def __str__(self):
        return f"{self.name}: {self.desc}. Costs {self.price}"
    
    def __add__(self):
        pass


class ShoppingEncounter(Encounter):

    def __init__(self, name, items):
        self.name = name
        self.danger_level = 0
        self.ships = list()
        self.items = items

    def __repr__(self):
        return f'{self.name}, {self.items}'

    def display_shop(self): 
        print(f"\n --- {self.name} Shop ---")
        for i, item in enumerate(self.items,start=1):
            print(f"{i}. {str(item)} " )
        print("-"*24)

    def buy(self, spaceship: Spaceship, item, amount):
            total_cost = item.price * amount
            if spaceship.money >= total_cost:
                spaceship.money -= total_cost
                spaceship.inventory[item.name] = spaceship.inventory.get(item.name, 0) + amount
                print(f"Hello {spaceship.name}, you just bought {amount} {item.name}(s) for {total_cost} credits!")
            else:
                print("Not enough money!")



                
    def sell(self, spaceship: Spaceship, item,
              amount):
        if item.name in spaceship.inventory and spaceship.inventory[item.name] >= amount:
            total_sell_price = (item.price // 2) * amount
            spaceship.money += total_sell_price
            spaceship.inventory[item.name] -= amount
            if spaceship.inventory[item.name] == 0:
                del spaceship.inventory[item.name]
                print(f"You sold {amount} {item.name}(s) for {total_sell_price} credits!")
            else:
                print("You don't have enough items to sell!")

    @staticmethod
    def select_action():
        while True: 
            action = input("Buy or Sell? (b/s): ").strip().lower()   

            if action == "b":
                return 'b'
            
            elif action == "s":
                return 's'
            
            else: 
                print("Invalid! Type 'b' to buy or 's' to sell.") 


    def select_from_shop(self):
        while True:
            try:
                choice = int(input("Enter item number to buy/sell (or 0 to exit): ").strip())
                item_index = choice - 1
                if item_index < 0 or item_index >= len(self.items):
                    print("Invalid item number!")
                    continue
            except ValueError:
                print("Invalid input! Please enter a number.")
                continue        

            return choice

    @staticmethod
    def select_from_ship():
        pass

    @staticmethod
    def ask_amount(item_name):
        while True:
            try:
                amount = int(input(f"How many {item_name}s? ").strip())
                if amount <= 0:
                    print("Invalid amount!")
                    continue
            except ValueError:
                print("Invalid input! Please enter a number.")
                continue
            return amount
    
    @staticmethod
    def display_sellable_items(self, spaceship):
        print("\n--- Your Inventory ---")

        if not spaceship.inventory:  # check if inventory is empty
            print("You have nothing to sell.")
            return

        for i, (item_name, amount) in enumerate(spaceship.inventory.items(), start=1):
            print(f"{i}. {item_name} (x{amount})")

        print("-" * 24)




    def trade_(self, spaceship: Spaceship):
        while True:
            self.display_shop()

            action = self.select_action()

            if action == "b":
                buy()
                
            elif action == "s":
                sell()

            else:
                raise RuntimeError
            #########
            try:
                choice = int(input("Enter item number to buy/sell (or 0 to exit): ").strip())
                if choice == 0:
                    return
                item_index = choice - 1
                if item_index < 0 or item_index >= len(self.items):
                    print("Invalid item number!")
                    continue
            except ValueError:
                print("Invalid input! Please enter a number.")
                continue
            ###########
            item = self.items[item_index]




        
def encounters_from_json(file_path: str) -> list[Encounter]:
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    encounters = []

    for encounter_data in data:
        if encounter_data.get("type") == "shop":
            items = []
            for it in encounter_data["items"]:
                items.append(Item(it["name"], it["desc"], it["price"]))

            encounters.append(ShoppingEncounter(encounter_data["name"], items))
        else:
            ships = []
            for ship_data in encounter_data.get("ships", []):
                ships.append(Spaceship(**ship_data))

            name = encounter_data.get("name", "Unnamed encounter")
            danger = encounter_data.get("danger_level", 1)
            encounters.append(Encounter(name, danger, ships))
            
    return encounters
        
class Map:
    available_encounters: list[Encounter]
    unlocked_area: list[tuple]

    def __init__(self, depth: int, max_width: int):
        self.available_encounters = encounters_from_json("encounters.json")
        self.map: list[list[Encounter]] = [] # list of lists of available encounters
        self.depth = depth
        self.max_width = max_width
        self.current_position = 0,0
        self.unlocked_area = list()
        for group in range(depth):
            encounters_per_group = random.randint(1, max_width)
            self.map.append(
                list(
                    random.choices(
                        self.available_encounters,
                        k=encounters_per_group
                    )
                )
            )

    def display(self):
        print("\n=== Space Encounter Map ===\n")
        
        for y, level in enumerate(self.map):
            spacing = " " * ((self.max_width - len(level)) * 4)
            encounter_str = spacing
            for x in range(self.max_width):
                if x < len(level):
                    if (x, y) == self.current_position:
                        encounter_str += f"[🚀] "  # Highlight current position with a spaceship emoji
                        self.unlocked_area.append(self.current_position)  # (x,y) into unlocked_area list
                    elif (x, y) in self.unlocked_area:
                        encounter_str += f"[✓] "  # Mark unlocked areas with a tick
                    else:
                        encounter = self.map[y][x]
                        if isinstance(encounter,ShoppingEncounter):
                            encounter_str += f"[💰] " # Marks Shops with a 💰
                        else:
                            encounter_str += f"[X] "  # Mark locked areas with an X
                else:
                    # to check whether it's a shopping encounter use:

                        

                    encounter_str += "    "  # Keep spacing aligned
            
            print(encounter_str)
            print()
        
        print("\n==========================\n")

    def navigate(self, direction):
        x, y = self.current_position

        if direction == "right":
            if x + 1 < len(self.map[y]):  # Ensure x doesnt exceed row length
                x += 1
            else:
                print("You can't move right!")
                return
        
        elif direction == "left":
            if x > 0:
                x -= 1
            else:
                print("You can't move left!")
                return

        elif direction == "down":
            if y + 1 < len(self.map) and x < len(self.map[y + 1]):
                y += 1
            else:
                print("You can't move down!")
                return

        else:
            print("Invalid direction! Use 'left', 'right', or 'down'.")
            return

        self.current_position = (x, y)
        if (x, y) not in self.unlocked_area:
            self.unlocked_area.append((x, y))  

        print(f"Moved {direction} ---- Now at {self.current_position}")

        self.display()

        return self.map[y][x] 


class Planet:
    levels: Map

    def __init__(self):
        pass


if __name__ == "__main__":
    game_map = Map(depth=5, max_width=3)
    game_map.display() 




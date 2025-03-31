import json
# import yaml
from typing import List

class Spaceship:
    # 5. Combat
    # 6. Upgrades
    # 3. Refueling


    def __init__(self, name, start_inventory=None, start_health=100, start_fuel_capacity=100, start_fuel=50,
                 start_max_health=100, start_damage_count=10, start_max_damage=100):
        self.name = name
        self.health = start_health
        self.inventory = start_inventory if start_inventory is not None else {}
        self.fuel_capacity = start_fuel_capacity
        self.fuel = start_fuel
        self.max_health = start_max_health
        self.damage_count = start_damage_count
        self.max_damage = start_max_damage
        self.money = 0

    def __repr__(self):
        return f"Spaceship({self.name}, Health: {self.health}, Fuel: {self.fuel})"

    def display_inventory(self):
        print(f"\nMoney: {self.money} credits")

        if not self.inventory:
            print("\nYour inventory is empty.")
            return
        
        print("\n===== Inventory =====")

        for i, (item, quantity) in enumerate(self.inventory.items(), start = 1 ):
            print(f"{i}. {item}: x{quantity}")

        print("=====================")

    def travel(self,map):
        fuel_needed = 100*map.current_position[1]
        if self.fuel >= fuel_needed:
            self.fuel -= fuel_needed
            map.navigate()
        else:
            raise RuntimeError("YOU LOSE (ran out of fuel ending)")
            
if __name__ == "__main__":
    pass
    # encounters = encounters_from_json("encounters.json")
    # for i in encounters:
        # print(i)
    
    # encounters_yaml = encounters_from_yaml("encounters.yaml")
    # for i in encounters_yaml:
    #     print(i)

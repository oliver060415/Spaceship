from spaceship import Spaceship
import game_map as gmap

def main():
    player_name = input("Please enter your name here: ")

    player = Spaceship(player_name)
    
    game_map = gmap.Map(5,3)
    game_map.display()

    while True:
        player.travel(game_map)

if __name__ == "__main__":
    main()
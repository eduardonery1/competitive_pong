from model import Model
from controller import ServerController, KeyboardController


if __name__ == "__main__":
    game = Model()
    
    keyboard = KeyboardController(game)
    keyboard.listen()

    server = ServerController(game)
    game.set_remote(server)


from model import Model
from controller import ServerController


if __name__ == "__main__":
    game = Model()
    websocket = ServerController(game)

    game.set_remote(websocket)
    websocket.listen()

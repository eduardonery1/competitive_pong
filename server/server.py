from user import User
from game import Game
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from json import dumps

app = FastAPI()
users = []
games = []


@app.websocket("/")
async def websocket_mirror(websocket: WebSocket):
    playing = False
    user = User(websocket, playing)
    users.append(user)
    await users[-1].websocket.accept()
    player_settings = {"y":0} 
    
    if len(users) % 2 == 1:
        player_settings["player"] = "left"
    else:
        player_settings["player"] = "right"

    print(dumps(player_settings))
    await users[-1].websocket.send_json(player_settings)
    
    game = Game(user, user)
    try:
        while True:
            response = await websocket.receive_json()
            print(response)
            await game.update(response)
    except WebSocketDisconnect:
        users.remove(user)



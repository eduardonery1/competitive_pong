from user import User
from game import Game
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, user: User):
        await user.websocket.accept()
        self.active_connections.append(user.websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, websocket: WebSocket, message: str):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

app = FastAPI()
manager = ConnectionManager()
games = []


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/")
async def websocket_mirror(websocket: WebSocket):
    user = User(websocket, True, 1)
    await manager.connect(user)
    print("Usuário conectado!")

    game = Game(user, user)
    try:
        while True:
            response = await websocket.receive_json()
            print(response)
            await game.update(response)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        game.close()


@app.websocket("/not")
async def websocket_endpoint(websocket: WebSocket):
    pos = len(manager.active_connections)
    playing = False
    user = User(websocket, playing, pos)
    await manager.connect(user)
    
    if pos > 0 and pos % 2 == 0:
        game = Game(user, manager.active_connections[pos-2])
        #Game handles inner variables
    try:
        while not user.playing:
            await manager.send_personal_message(websocket, "waiting...")
            pass

        while True:
            data = await websocket.receive_json()
            game.update(data) #update both players directily
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        game.close()

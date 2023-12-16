from user import User
from game import Game
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()
games = []

@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    
    pos = len(manager.active_connections)
    playing = False
    user = User(websocket, playing, pos)
    await manager.connect(user)
    
    if pos > 0 and pos % 2 == 0:
        game = Game(user, manager.active_connections[pos-2])
        #Game handles inner variables
    try:
        while not user.playing:
            pass

        while True:
            data = await websocket.receive_json()
            game.update(data) #update both players directily
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        game.close()

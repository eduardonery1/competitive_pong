from json import dumps


class Game:
    def __init__(self, user1, user2):
        self.user1 = user1
        self.user2 = user2
        self.user1.playing = True
        self.user2.playing = True

    async def update(self, data):
        if data["player"] == 'left':
            if self.user2 is not self.user1:
                await self.user2.websocket.send_json(data)
            else:
                data["player"] = 'right'
                await self.user1.websocket.send_json(data)
        elif data["player"] == 'right':
            await self.user1.websocket.send_json(data)

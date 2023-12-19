class Game:
    def __init__(self, user1, user2):
        self.user1 = user1
        self.user2 = user2
        self.user1.playing = True
        self.user2.playing = True

    async def update(data):
        await self.user1.send(data)
        await self.user2.send(data)

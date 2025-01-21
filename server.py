import random
import asyncio
import websockets
import json
from enum import Enum

class GameState(Enum):
    WAITING = "waiting"
    RUNNING = "running"
    FINISHED = "finished"

class GameServer:
    def _init_(self, min_players=2):
        self.clients = {}
        self.game_state = {
            "snakes": {},  # Will store all snake positions by client_id
            "food": []    # List of boosts (food) positions
        }
        self.current_state = GameState.WAITING
        self.min_players = min_players

    def spawn_boosts(self, count, world_size):
        return [
            {"x": random.randint(-world_size, world_size), "y": random.randint(-world_size, world_size)}
            for _ in range(count)
        ]
        
    async def broadcast_state(self):
        state_update = {
            "status": self.current_state.value,
            "game_state": self.game_state,
            "player_count": len(self.clients)
        }
        print(f"Broadcasting state: {state_update}")

        for client in list(self.clients.values()):
            try:
                await client.send(json.dumps(state_update))
            except websockets.ConnectionClosed:
                continue

    async def check_game_state(self):
        while True:
            if self.current_state == GameState.WAITING and len(self.clients) >= self.min_players:
                self.current_state = GameState.RUNNING
                print("Game state changed to RUNNING.")
                self.game_state['food'] = self.spawn_boosts(5, 100)  # spawn 5 boosts on the start
                await self.broadcast_state()

            if self.current_state == GameState.RUNNING and len(self.clients) < self.min_players:
                self.current_state = GameState.WAITING
                print("Game state changed to WAITING.")
                await self.broadcast_state()

            if self.current_state == GameState.RUNNING:
                # Periodically regenerate boosts (food) every 5 seconds
                self.game_state['food'] = self.spawn_boosts(5, 100)
                await self.broadcast_state()

            await asyncio.sleep(5)

    async def handle_client(self, websocket, path):
        client_id = str(id(websocket))
        self.clients[client_id] = websocket
        self.game_state["snakes"][client_id] = []  # Initialize empty snake for new client
        print(f"New client connected: {client_id}")

        try:
            # Send initial state to new client
            await websocket.send(json.dumps({
                "client_id": client_id,
                "status": self.current_state.value,
                "game_state": self.game_state,
                "player_count": len(self.clients)
            }))

            # Broadcast updated player count to all clients
            await self.broadcast_state()

            async for message in websocket:
                try:
                    if self.current_state == GameState.RUNNING:
                        data = json.loads(message)
                        self.game_state['snakes'][client_id] = data
                        # Broadcast immediately after receiving an update
                        await self.broadcast_state()
                except json.JSONDecodeError:
                    print(f"Invalid message from {client_id}: {message}")

        except websockets.ConnectionClosed:
            print(f"Client disconnected: {client_id}")
        finally:
            self.clients.pop(client_id, None)
            self.game_state["snakes"].pop(client_id, None)
            self.game_state["scores"].pop(client_id, None)
            
            if len(self.clients) < self.min_players:
                self.current_state = GameState.WAITING
                print("Not enough players, game state reset to WAITING.")
            
            await self.broadcast_state()

async def main():
    game_server = GameServer(min_players=2)
    
    async def handler(websocket, path):
        await game_server.handle_client(websocket, path)

    server = await websockets.serve(handler, "localhost", 8081)
    print("Server started at ws://localhost:8081")
    await asyncio.gather(
        server.wait_closed(), 
        game_server.check_game_state()
    )

if _name_ == "_main_":
    asyncio.run(main())
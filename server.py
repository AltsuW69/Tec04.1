import socket
import threading
import json
import time

# Server configuration
HOST = '0.0.0.0'
PORT = 5555
TICK_RATE = 30  # Updates per second

# Game state: keeps track of players and bullets
game_state = {"players": {}, "bullets": []}
clients = {}

def handle_client(client_socket, addr):
    """Handles incoming data and updates the game state for a specific client."""
    player_id = addr[1]  # Use client port as unique ID
    game_state["players"][player_id] = {"x": 150, "y": 100, "health": 100, "color": None, "bullets": []}
    print(f"Player {player_id} connected.")

    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            action = json.loads(data)

            # Update the player's game state
            if action["type"] == "update":
                game_state["players"][player_id].update(action["data"])
            elif action["type"] == "shoot":
                bullet = action["data"]
                bullet["player_id"] = player_id  # Attach bullet to player
                game_state["bullets"].append(bullet)
    except:
        print(f"Player {player_id} disconnected.")
    finally:
        # Clean up on disconnect
        del game_state["players"][player_id]
        del clients[player_id]
        client_socket.close()

def broadcast_game_state():
    """Sends the entire game state to all connected clients."""
    while True:
        state_json = json.dumps(game_state)
        for conn in clients.values():
            try:
                conn.sendall(state_json.encode('utf-8'))
            except:
                continue
        time.sleep(1 / TICK_RATE)

def start_server():
    """Main server loop: accepts connections and assigns threads."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server started on {HOST}:{PORT}")

    threading.Thread(target=broadcast_game_state, daemon=True).start()

    while True:
        client_socket, addr = server.accept()
        clients[addr[1]] = client_socket
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
import socket
import threading
import pickle  # For serializing game state
from typing import Dict

# Server Configuration
HOST = "127.0.0.1"  # Localhost for testing, or your public IP for remote connections
PORT = 5555

# Initialize Server Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Player Data Management
clients = []  # Track connected client sockets
player_states: Dict[int, dict] = {}  # Player state: {player_id: {state_data}}
next_player_id = 0  # Unique player ID counter


def handle_client(client_socket, player_id):
    global player_states

    # Initialize player state when connected
    player_states[player_id] = {
        "x": 100 + 50 * player_id,  # Stagger start positions
        "y": 500,
        "color": (255, 0, 0),  # Can dynamically assign colors
        "health": 100,
        "bullets": []  # Player bullets
    }

    try:
        while True:
            data = client_socket.recv(2048)  # Receive client data
            if not data:
                break

            action = pickle.loads(data)  # Deserialize client action

            # Update player state based on action
            if "move" in action:
                dx, dy = action["move"]
                player_states[player_id]["x"] += dx
                player_states[player_id]["y"] += dy

            if "shoot" in action:
                bullet = action["shoot"]
                player_states[player_id]["bullets"].append(bullet)

            broadcast_state()  # Sync state with all clients

    except Exception as e:
        print(f"Player {player_id} error: {e}")

    finally:
        # Remove disconnected player
        del player_states[player_id]
        clients.remove(client_socket)
        client_socket.close()
        broadcast_state()  # Notify other clients of player disconnect


def broadcast_state():
    """Broadcast current game state to all clients."""
    data = pickle.dumps(player_states)  # Serialize state
    for client in clients:
        try:
            client.sendall(data)
        except:
            clients.remove(client)
            client.close()


def accept_connections():
    """Handle new client connections."""
    global next_player_id

    print("Server running...")
    while True:
        client_socket, addr = server.accept()
        print(f"Player {next_player_id} connected from {addr}")
        clients.append(client_socket)

        # Start a new thread for the client
        threading.Thread(target=handle_client, args=(client_socket, next_player_id)).start()
        next_player_id += 1


if __name__ == "__main__":
    accept_connections()
# Socket XO 🎮

A real-time multiplayer XO (Tic-Tac-Toe) game built with Python using sockets.
Players connect to the server, take turns, and see the board update live in the terminal.

## 🚀 Features

- Multiplayer Tic-Tac-Toe (2 players)
- Real-time updates from server
- Turn-based gameplay
- Win/Lose/Draw score tracking
- Simple terminal interface

## 🛠️ Built With

- Python 3
- Socket Programming (TCP)
- Select (for handling multiple clients)

## 🏃‍♂️ Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/NaphatTor/XOgame.git
   ```

2. Start the server:
   ```bash
   python server.py
   ```

3. Open another terminal and run the client (do this twice for 2 players):
   ```bash
   python client.py
   ```

4. Enter moves as:
   ```bash
   row col
   ```

## 📁 Project Structure

```
SocketXO/
├── client.py      # Client-side: connects to server, sends moves, shows board
├── server.py      # Server-side: manages game logic, turns, scores
├── README.md      # Documentation
```

#ณภัทร โตรุ่งเรืองยศ 620965446
import os
import socket
import json
import time

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ENCODE_FORMAT = 'utf-8'

HOST = 'localhost'
PORT = 8080

def payloadByte(sender, receiver, functionName, data=None):
    payload_string = getPayload(sender, receiver, functionName, data)
    return bytes(payload_string, ENCODE_FORMAT)

def byteToJson(data_bytes):
    data = data_bytes.decode(ENCODE_FORMAT)
    return json.loads(data)

def getPayload(sender, receiver, functionName, data=None):
    payload = {
        'sender': sender,
        'receiver': receiver,
        'type': functionName,
        'data': data
    }
    return json.dumps(payload)

def getChoice(information, messageInput, limitChoice):
    while True:
        print(information)
        choice = input(messageInput)
        try:
            choice = int(choice)
            if 1 <= choice <= limitChoice:
                return choice
        except ValueError:
            pass
        print("Invalid choice. Please enter a number between 1 and", limitChoice)

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def testConnectToServer(client_tcp, SENDER_NAME):
    client_tcp.send(payloadByte(SENDER_NAME, 'server', 'test_server', {'example': 'test'}))
    client_tcp.recv(1024)  # รับค่าทดสอบเฉยๆ

import os

def startPlaying(client_tcp, SENDER_NAME):
    client_tcp.send(payloadByte(SENDER_NAME, "server", "play"))
    board = [[" " for _ in range(3)] for _ in range(3)]
    mark = None

    while True:
        try:
            data_bytes = client_tcp.recv(2048)
            data_json = byteToJson(data_bytes)
            msg = data_json.get("msg", "")

            if msg == "OK":
                print(f"{data_json.get('message')}")

            elif msg == "PLAY":
                board = data_json.get("board", board)
                task = data_json.get("task", None)
                mark = data_json.get("mark", mark)
                print_board(board)

                if task == "selectplace":
                    while True:
                        user_input = input("Enter row and column (0-2) separated by space : ")
                        try:
                            row, col = map(int, user_input.strip().split())
                            if 0 <= row <= 2 and 0 <= col <= 2 and board[row][col] == " ":
                                board[row][col] = mark
                                break
                            else:
                                print("Invalid move. Try again.")
                        except ValueError:
                            print("Please enter two numbers like '1 1'.")
                    client_tcp.send(payloadByte(SENDER_NAME, "server", "take_turn", {
                        "board": board,
                        "mark": mark
                    }))
                else:
                    print(f"{data_json.get('message', '')}")
            elif msg == "DONE_PLAY":
                if "board" in data_json:
                    board = data_json.get("board", board)
                    print("\n")
                    print_board(board)
                print(data_json.get("message"))
                break
            else:
                print("Unknown message. msg =", msg)
                print("Raw JSON:", data_json)

        except Exception as e:
            print(f"ERROR: {e}")
            break

def seeTheScore(client_tcp, SENDER_NAME):
    client_tcp.send(payloadByte(SENDER_NAME, 'server', 'check_score'))
    data_bytes = client_tcp.recv(2048)
    response = byteToJson(data_bytes)
    score_list = response.get("score", [])
    
    print("\n_____ Score Board _____")
    for line in score_list:
        print(line)
    print()

def main():
    client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_tcp.connect((HOST, PORT))
    
    SENDER_NAME = input("Enter your name: ")
    testConnectToServer(client_tcp, SENDER_NAME)
    
    while True:
        choice = getChoice(
            '_____ Welcome to XO game _____\n1. Play \n2. See the score\n3. Exit\n_____________________________________',
            'Enter your choice (1 or 2 or 3): ',
            3
        )
        if choice == 1:
            startPlaying(client_tcp, SENDER_NAME)
        elif choice == 2:
            seeTheScore(client_tcp, SENDER_NAME)
        elif choice == 3:
            print("Goodbye!")
            client_tcp.close()
            break

if __name__ == "__main__":
    main()
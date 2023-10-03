from socket import *

def smtp_server(port=1025):
    # Create a socket for the server to listen on
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('127.0.0.1', port))
    serverSocket.listen(1)

    print(f"SMTP server is listening on port {port}...")

    while True:
        # Establish the connection
        print("Waiting for a connection...")
        connectionSocket, addr = serverSocket.accept()
        print(f"Connection established from {addr}")

        # Send a 220 greeting to the client
        connectionSocket.send(b'220 Welcome to the SMTP server\r\n')

        while True:
            # Receive the client's command
            command = connectionSocket.recv(1024).decode()
            if not command:
                break
            print(f"Received command: {command}")

            # Process the command and send a response
            if command.startswith("HELO") or command.startswith("EHLO"):
                connectionSocket.send(b'250 Hello\r\n')

            elif command.startswith("MAIL FROM"):
                connectionSocket.send(b'250 OK\r\n')

            elif command.startswith("RCPT TO"):
                connectionSocket.send(b'250 OK\r\n')

            elif command.startswith("DATA"):
                connectionSocket.send(b'354 Start mail input; end with <CRLF>.<CRLF>\r\n')

                message_data = ""
                while True:
                    data_line = connectionSocket.recv(1024).decode()
                    message_data += data_line
                    if data_line.strip() == ".":
                        break
                print(f"Received message data:\n{message_data}")
                connectionSocket.send(b'250 Message accepted for delivery\r\n')
            elif command.startswith("QUIT"):
                connectionSocket.send(b'221 Bye\r\n')
                break
            else:
                connectionSocket.send(b'500 Error: command not recognized\r\n')

        # Close the connection
        connectionSocket.close()

if __name__ == '__main__':
    smtp_server(1025)
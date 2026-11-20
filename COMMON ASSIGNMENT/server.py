"""TCP + UDP multi-client server (Transport Layer demonstration)."""
import socket, threading, time, sys

HOST, TCP_PORT, UDP_PORT = "127.0.0.1", 5000, 5001

def log(msg): print(f"[SERVER {time.strftime('%H:%M:%S')}] {msg}", flush=True)

def handle_tcp_client(conn, addr):
    log(f"TCP connection ESTABLISHED with {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            text = data.decode()
            log(f"TCP received from {addr}: {text}")
            conn.sendall(f"ACK: {text}".encode())      # reliable delivery -> acknowledgment
    log(f"TCP connection CLOSED with {addr}")

def tcp_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, TCP_PORT)); s.listen(5)
    log(f"TCP server listening on {HOST}:{TCP_PORT}")
    while True:
        conn, addr = s.accept()                         # 3-way handshake completes here
        threading.Thread(target=handle_tcp_client, args=(conn, addr), daemon=True).start()

def udp_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, UDP_PORT))
    log(f"UDP server listening on {HOST}:{UDP_PORT}")
    while True:
        data, addr = s.recvfrom(1024)                   # no connection, each datagram independent
        text = data.decode()
        log(f"UDP datagram from {addr}: {text}")
        if not text.startswith("NOACK"):
            s.sendto(f"RECEIVED: {text}".encode(), addr)

if __name__ == "__main__":
    threading.Thread(target=tcp_server, daemon=True).start()
    threading.Thread(target=udp_server, daemon=True).start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        log("shutting down")

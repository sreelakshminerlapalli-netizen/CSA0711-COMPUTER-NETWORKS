"""TCP / UDP client. Usage: python client.py <client_id> <server_ip> <TCP|UDP> <message> [count]"""
import socket, sys, time

def tcp_send(cid, ip, port, msgs):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    t0 = time.perf_counter(); s.connect((ip, port)); hs = (time.perf_counter()-t0)*1000
    print(f"[{cid}] Connection Status: CONNECTED to {ip}:{port} (handshake {hs:.3f} ms)")
    times = []
    for m in msgs:
        t0 = time.perf_counter()
        s.sendall(f"{cid}: {m}".encode())
        reply = s.recv(1024).decode()
        dt = (time.perf_counter()-t0)*1000; times.append(dt)
        print(f"[{cid}] Sent: {m} | Received: {reply} | Time: {dt:.3f} ms | ACK: RECEIVED")
    s.close(); print(f"[{cid}] Connection Status: CLOSED")
    return times

def udp_send(cid, ip, port, msgs):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)
    times = []
    for m in msgs:
        t0 = time.perf_counter()
        s.sendto(f"{cid}: {m}".encode(), (ip, port))
        try:
            reply = s.recvfrom(1024)[0].decode()
            ack = "RECEIVED (application-level)"
        except socket.timeout:
            reply, ack = "-", "NO REPLY (packet may be lost)"
        dt = (time.perf_counter()-t0)*1000; times.append(dt)
        print(f"[{cid}] Sent: {m} | Received: {reply} | Time: {dt:.3f} ms | ACK: {ack}")
    s.close(); return times

if __name__ == "__main__":
    cid, ip, proto, msg = sys.argv[1:5]
    n = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    msgs = [f"{msg} #{i+1}" for i in range(n)]
    (tcp_send(cid, ip, 5000, msgs) if proto.upper() == "TCP" else udp_send(cid, ip, 5001, msgs))

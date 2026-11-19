import socket, time, statistics, json
ip="127.0.0.1"; N=500; msg=b"x"*100
s=socket.socket(); t0=time.perf_counter(); s.connect((ip,5000)); hs=(time.perf_counter()-t0)*1000
tt=[]
for i in range(N):
    t0=time.perf_counter(); s.sendall(msg); s.recv(1024); tt.append((time.perf_counter()-t0)*1000)
s.close()
u=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); u.settimeout(1); ut=[]; lost=0
for i in range(N):
    t0=time.perf_counter(); u.sendto(msg,(ip,5001))
    try: u.recvfrom(1024)
    except socket.timeout: lost+=1
    ut.append((time.perf_counter()-t0)*1000)
# no-ack udp throughput
t0=time.perf_counter()
for i in range(N): u.sendto(b"NOACK"+msg,(ip,5001))
ud=(time.perf_counter()-t0)*1000
r=dict(N=N,tcp_hs=hs,tcp_avg=statistics.mean(tt),tcp_min=min(tt),tcp_max=max(tt),udp_avg=statistics.mean(ut),udp_min=min(ut),udp_max=max(ut),udp_lost=lost,udp_noack_total=ud,tcp_total=sum(tt),udp_total=sum(ut),tcp=tt,udp=ut)
json.dump(r,open("bench.json","w"))
print({k:(round(v,4) if isinstance(v,float) else v) for k,v in r.items() if k not in("tcp","udp")})

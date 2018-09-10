from socket import *
import threading
import sys

# 定义命令行参数 scan.py <host> <start>-<end port>
host = sys.argv[1]
ports = sys.argv[2].split('-')

s_port = int(ports[0])
e_port = int(ports[1])

lock = threading.RLock()

res = []

def tcp_test(port):
    sock = socket()
    sock.settimeout(10)
    result = sock.connect_ex((target_ip, port))
    if result == 0:
        lock.acquire() # 打印时加锁防止数据变化
        print ("扫描到开放端口号:", port)
        res.append(port)
        lock.release() # 释放锁


if __name__=='__main__':

    target_ip = gethostbyname(host)
    print("扫描开始")
    for port in range(s_port, e_port+1):  # 注意要+1 不丢失最后一个port
        t = threading.Thread(target=tcp_test, args=(port,))  # 进程调用tcp_test函数，参数是port
        t.start()
    t.join()
    if not res:
        print("无开放端口")


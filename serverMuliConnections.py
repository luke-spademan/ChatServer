import socket
import threading

clients = []


class Client(threading.Thread):
    def __init__(self, c, i):
        threading.Thread.__init__(self)
        self.c = c
        self.i = i

    def GetMsg(self):
        while True:
            data = self.c.recv(1024).decode("utf-8")
            if not data:
                break
            else:
                print(data)
                counter = 0
                for client in clients:
                    if counter != self.i:
                        client.c.send(data.encode("utf-8"))
                    counter += 1

    def run(self):
        self.GetMsg()


class GetClient(threading.Thread):
    def __init__(self, s):
        threading.Thread.__init__(self)
        self.s = s

    def run(self):
        while True:
            self.s.listen(10)  # waits for connection from a client
            c, addr = self.s.accept()  # gets clients ip address
            cname = c.recv(1024).decode("utf-8")
            print("Connection from %s %s" % (cname, addr[0]))
            i = len(clients)
            clients.append(Client(c, i))
            clients[-1].start()


class SendMsg(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        while True:
            data = input()
            if data == "q":
                break
            else:
                data = "%s: %s" % (self.name, data)
                for c in clients:
                    c.c.send(data.encode("utf-8"))


def main():
    host = input("ip address: ")
    port = int(input("port: "))
    name = input("username: ")

    s = socket.socket()
    s.bind((host, port))

    print("Waiting for connections on %s:%s" % (host, str(port)))

    get_clients = GetClient(s)
    send_msg = SendMsg(name)

    get_clients.start()
    send_msg.start()

    get_clients.join()
    send_msg.join()
    for c in clients:
        c.c.close()

if __name__ == "__main__":
    main()

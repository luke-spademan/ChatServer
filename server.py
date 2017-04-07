import socket
import threading


class GetMsg(threading.Thread):
    def __init__(self, c):
        threading.Thread.__init__(self)
        self.c = c

    def run(self):
        while True:
            data = self.c.recv(1024).decode("utf-8")
            if not data:
                break
            else:
                print(data)


class SendMsg(threading.Thread):
    def __init__(self, c, name):
        threading.Thread.__init__(self)
        self.c = c
        self.name = name

    def run(self):
        while True:
            data = input()
            if data == "q":
                break
            else:
                data = "%s: %s" % (self.name, data)
                self.c.send(data.encode("utf-8"))


def main():
    host = input("ip address: ")
    port = int(input("port: "))
    name = input("username: ")

    s = socket.socket()
    s.bind((host, port))

    print("Waiting for connections on %s:%s" % (host, str(port)))
    s.listen(1)  # waits for connection from a client
    c, addr = s.accept()  # gets clients ip address
    cname = c.recv(1024).decode("utf-8")
    print("Connection from %s %s" % (cname, addr[0]))

    getMsg = GetMsg(c)
    sendMsg = SendMsg(c, name)
    getMsg.start()
    sendMsg.start()

    getMsg.join()
    sendMsg.join()
    c.close()
    print("Closed connection to " + str(addr))

if __name__ == "__main__":
    main()

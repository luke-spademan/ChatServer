import socket
import threading


class GetMsg(threading.Thread):
    def __init__(self, s):
        threading.Thread.__init__(self)
        self.s = s

    def run(self):
        while True:
            data = self.s.recv(1024).decode("utf-8")
            if not data:
                break
            else:
                print(data)


class SendMsg(threading.Thread):
    def __init__(self, s, name):
        threading.Thread.__init__(self)
        self.s = s
        self.name = name

    def run(self):
        while True:
            data = input()
            if data == "q":
                break
            else:
                data = "%s: %s" % (self.name, data)
                self.s.send(data.encode("utf-8"))


def main():
    host = input("ip address: ")
    port = int(input("port: "))
    name = input("username: ")
    s = socket.socket()
    s.connect((host, port))

    getMsg = GetMsg(s)
    sendMsg = SendMsg(s, name)
    getMsg.start()
    sendMsg.start()

    getMsg.join()
    sendMsg.join()
    s.close()
    s.close()

if __name__ == "__main__":
    main()

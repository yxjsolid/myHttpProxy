import socket
import threading

class httpRawProxyServer():
    def __init__(self, serverIp, serverPort, hostIp, hostPort):
        self.serverIp  = serverIp
        self.serverPort = serverPort
        self.hostIp = hostIp
        self.hostPort = hostPort
        self.serverSock = None
        self.serverRun()

    def serverRun(self):
        self.serverSock = socket.socket()
        self.serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSock.bind((self.serverIp , self.serverPort))
        self.serverSock.listen(1500)
        while True:
            conn, addr = self.serverSock.accept()
            self.newProxy(conn, addr)

    def newProxy(self, conn, addr):
        tsk = threading.Thread(target=self.doProxy, args=(conn, ))
        tsk.start()

    def clientRead(self, conn):
        conn.setblocking(1)
        rfile = conn.makefile('rb', -1)
        req = ""
        contentLen = 0
        while 1:
            buf = rfile.readline(-1)
            if not buf:
                break
            req += buf
            # print [buf]
            if "content-length" in buf.lower():
                contentLen = int(buf.strip().split(":")[-1])

            if buf == "\r\n":
                if contentLen == 0:
                    break
                else:
                    help(rfile)
                    buf = rfile.read(contentLen)
                    req += buf
                    break

        return req

    def toServer(self, buf):
        s1 = socket.socket()
        s1.connect((self.hostIp,self.hostPort))
        s1.sendall(buf.encode())

        resp = b''
        rfile = s1.makefile('rb', 65535)

        while 1:
            ddd = rfile.readline(65535)

            if not ddd:
                break
            resp += ddd

        return resp

    def doProxy(self, conn):
        req = self.clientRead(conn)
        resp = self.toServer(req)

        conn.sendall(resp)
        conn.close()

        pass


if __name__ == "__main__":

    myIp = "127.0.0.1"
    myPort = 80

    proxyToIp = "10.103.12.251"
    proxyToPort = 80

    srv = httpRawProxyServer(myIp, myPort, proxyToIp, proxyToPort)

    pass
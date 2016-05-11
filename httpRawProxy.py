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

    def httpRead(self, rfile):
        contentLen = 0
        req = ""
        while True:
            buf = rfile.readline(65535)
            if not buf:
                break
            req += buf
            if "content-length" in buf.lower():
                contentLen = int(buf.strip().split(":")[-1])

            if buf == "\r\n":
                if contentLen == 0:
                    break
                else:
                    buf = rfile.read(contentLen)
                    req += buf
                    break
        return req


    def clientRead(self, conn):
        conn.setblocking(1)
        rfile = conn.makefile('rb', 65535)
        return self.httpRead(rfile)

    def toServer(self, buf):
        s1 = socket.socket()
        s1.connect((self.hostIp,self.hostPort))
        s1.sendall(buf.encode())

        rfile = s1.makefile('rb', 65535)
        return self.httpRead(rfile)

    def doProxy(self, conn):
        req = self.clientRead(conn)
        # print req

        resp = self.toServer(req)
        # print resp

        conn.sendall(resp)
        conn.close()
        # print "done"

        pass


if __name__ == "__main__":

    myIp = "10.103.12.31"
    myPort = 80

    proxyToIp = "192.168.8.1"
    proxyToPort = 80

    srv = httpRawProxyServer(myIp, myPort, proxyToIp, proxyToPort)

    pass
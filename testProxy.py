import socket
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO
from SimpleHTTPServer import SimpleHTTPRequestHandler

class myHTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, rawData):
        self.rfile = StringIO(rawData)

        self.raw_requestline = self.rfile.readline()
        self.parse_request()

    def getData(self):
        key = 'Content-Length'

        if self.headers.has_key(key):
            len = self.headers[key]

            return self.rfile.read(int(len))

class mytestHTTPRequest(SimpleHTTPRequestHandler):
    def __init__(self, sock):
        self.client_address = "1.1.1.1"
        self.rfile = sock.makefile('rb', -1)
        self.wfile = sock.makefile('wb', 0)


def main():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 1024))
    s.listen(1500)
    while 1:
        print "before accept"
        conn, addr = s.accept()
        print "after accept"
        conn.setblocking(1)
        print(addr)
        headers = ''
        rfile = conn.makefile('rb', -1)
        # tt = mytestHTTPRequest(conn)
        while 1:
            ddd = rfile.readline(-1)

            # tt.handle_one_request()
            if "GET" in ddd:
                print ddd

            # buf = conn.recv(2048).decode('utf-8')
            # print [ddd]
            headers += ddd

            contentLen = 0
            if "content-length" in ddd.lower():
                contentLen = int(ddd.strip().split(":")[-1])


            if ddd == "\r\n":
                print "contentLen= ", contentLen
                if contentLen == 0:
                    print "break"
                    break
                else:
                    ddd = rfile.readline(contentLen)
                    print ddd



        # if len(buf) < 2048:
        #     break

        # rfile = StringIO(headers)

        # r = myHTTPRequest(headers)
        #
        #
        # print r.headers
        # print r.getData()

        # headers = headers.replace('10.103.12.31:1024', '192.168.8.1')\
        #                  .replace('keep-alive', 'close')\
        #                  .replace('gzip','')

        # headers = headers.replace('keep-alive', 'close')\
        #                  .replace('gzip','')

        print "xxxxxxxxx"
        s1 = socket.socket()
        s1.connect(('10.103.12.251', 80))
        s1.sendall(headers.encode())


        resp = b''
        rfile = s1.makefile('rb', 65535)
        # tt = mytestHTTPRequest(conn)

        while 1:
            ddd = rfile.readline(65535)



            if not ddd:
                break
            resp += ddd






        # print resp
        # print
        # print

        # resp = resp.replace(b'Content-Encoding: gzip\r\n', b'')\
        #            .replace(b'192.168.8.1', b'10.103.12.31:1024')

        # resp = resp.replace(b'Content-Encoding: gzip\r\n', b'')
        # print resp

        print('send to', addr)
        conn.sendall(resp)
        conn.close()
        print "done"


main()
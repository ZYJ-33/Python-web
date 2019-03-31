import socket
from utils import log
from utils import slog
from _thread import start_new_thread
from Router import Router_interface
from Router import error
from Request import Request


class Server(object):
    def __init__(self):
        self.sock = socket.socket()
        self.set_config()
        self.router_dict = {}
        with open('log.txt', 'w', encoding="utf-8") as f:
            pass

    def set_config(self):
        self.config = dict(
            port=3333,
            host="",
        )

    def rece_from(self, sock):
        buf_size = 1024
        mess = b""
        while True:
            try:
                buf = sock.recv(buf_size)
                mess += buf
                if len(buf) < 1024:
                    break
            except ConnectionResetError as e:
                log("in rece_from  ", e)

        return mess

    def get_response_from_request(self, request):
        self.router_dict.update(Router_interface.Router_dict)
        path = request.get_path()
        slog("client require path: ", path)
        response = self.router_dict.get(path, error)
        a = response(request)
        slog("the response of request is ", a)
        return a

    def handle_request(self, conn):
        req = self.rece_from(conn)
        req = req.decode("utf-8")
        log(req)
        #try:
        #except Exception as e:
         #   log(e)
        request = Request(req)
        if request is not None:
            response = self.get_response_from_request(request)
            slog(response)
            conn.send(response)
            conn.close()

    def run(self):
        self.sock.bind((self.config["host"], self.config["port"]))
        self.sock.listen(5)
        while True:
            conn, addr = self.sock.accept()
            start_new_thread(self.handle_request, (conn,))


if __name__ == "__main__":
    s = Server()
    s.run()

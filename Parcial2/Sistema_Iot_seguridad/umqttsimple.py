# umqttsimple.py - Cliente MQTT para MicroPython
import usocket as socket
import ustruct as struct


class MQTTException(Exception):
    pass


class MQTTClient:
    def __init__(self, client_id, server, port=0, user=None, password=None,
                 keepalive=0, ssl=None, ssl_params={}):
        if port == 0:
            port = 8883 if ssl else 1883
        self.client_id = client_id
        self.server = server
        self.port = port
        self.user = user
        self.pswd = password
        self.keepalive = keepalive
        self.ssl = ssl
        self.ssl_params = ssl_params
        self.sock = None
        self.cb = None

    # --- utilidades internas ---
    @staticmethod
    def _bytes(s):
        return s.encode("utf-8") if isinstance(s, str) else s

    def _str(self, s):
        b = self._bytes(s)
        return struct.pack("!H", len(b)) + b

    @staticmethod
    def _encode_len(n):
        out = bytearray()
        while True:
            byte = n % 128
            n //= 128
            if n > 0:
                byte |= 0x80
            out.append(byte)
            if n == 0:
                break
        return out

    def _recv_len(self):
        n = 0
        shift = 0
        while True:
            b = self.sock.read(1)[0]
            n |= (b & 0x7F) << shift
            if not (b & 0x80):
                return n
            shift += 7

    def set_callback(self, cb):
        self.cb = cb

    # --- API pública ---
    def connect(self, clean_session=True):
        sock = socket.socket()
        sock.settimeout(10)
        try:
            addr = socket.getaddrinfo(self.server, self.port)[0][-1]
            sock.connect(addr)
            if self.ssl:
                import ussl
                sock = ussl.wrap_socket(sock, **self.ssl_params)
            self.sock = sock

            flags = 0x02 if clean_session else 0x00
            if self.user is not None:
                flags |= 0xC0
            body = (self._str("MQTT") + bytes([0x04, flags]) +
                    struct.pack("!H", self.keepalive) + self._str(self.client_id))
            if self.user is not None:
                body += self._str(self.user) + self._str(self.pswd or "")

            self.sock.write(b"\x10" + self._encode_len(len(body)) + body)

            resp = self.sock.read(4)
            if resp is None or len(resp) < 4 or resp[0] != 0x20 or resp[1] != 0x02:
                raise MQTTException("Bad CONNACK")
            if resp[3] != 0:
                raise MQTTException("Connection refused, code {}".format(resp[3]))
            return resp[2] & 1
        except Exception:
            try:
                sock.close()
            except Exception:
                pass
            self.sock = None
            raise

    def disconnect(self):
        try:
            self.sock.write(b"\xe0\x00")
        except Exception:
            pass
        try:
            self.sock.close()
        except Exception:
            pass
        self.sock = None

    def ping(self):
        self.sock.write(b"\xc0\x00")

    def publish(self, topic, msg, retain=False, qos=0):
        t = self._bytes(topic)
        m = self._bytes(msg)
        pkt = bytearray([0x30 | (1 if retain else 0)])
        pkt += self._encode_len(2 + len(t) + len(m))
        pkt += struct.pack("!H", len(t)) + t + m
        self.sock.write(pkt)

    def subscribe(self, topic, qos=0):
        t = self._bytes(topic)
        pkt = bytearray(b"\x82")
        pkt += self._encode_len(2 + 2 + len(t) + 1)
        pkt += struct.pack("!H", 1)            # packet id
        pkt += struct.pack("!H", len(t)) + t
        pkt.append(qos)
        self.sock.write(pkt)
        while True:
            op = self.sock.read(1)
            if op is None:
                raise MQTTException("Timeout esperando SUBACK")
            if op == b"":
                raise MQTTException("Connection closed")
            if op == b"\x90":
                self.sock.read(3)
                return
            
            self._handle(op)

    def _handle(self, first):
        """Procesa un paquete cuyo primer byte ya fue leído."""
        if first == b"\xd0":                   
            self.sock.read(1)
            return None
        op = first[0]
        if (op & 0xF0) != 0x30:                
            return op
        self.sock.settimeout(5)                
        sz = self._recv_len()
        tl = self.sock.read(2)
        topic_len = (tl[0] << 8) | tl[1]
        topic = self.sock.read(topic_len).decode("utf-8")
        sz -= topic_len + 2
        if op & 0x06:                          
            self.sock.read(2)
            sz -= 2
        msg = self.sock.read(sz)
        if self.cb:
            self.cb(topic, msg)
        return None

    def wait_msg(self):
        res = self.sock.read(1)
        if res is None:
            return None
        if res == b"":
            raise MQTTException("Connection closed")
        return self._handle(res)

    def check_msg(self):
        """Revisa mensajes sin bloquear."""
        self.sock.setblocking(False)
        try:
            return self.wait_msg()
        finally:
            if self.sock:
                self.sock.settimeout(10)

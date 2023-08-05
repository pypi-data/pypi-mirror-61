'''
Developed by Abhijith Boppe - linkedin.com/in/abhijith-boppe/
'''
import socket
import ssl
import errno

from datetime import datetime
from select import select

fields_maxLength = 1024
data_maxLength = 65535

all_device_ids = []        # to check if device is already existing.
deviceid_length = 10       # fixed length of device id

class IOTSocket(object):
    def __init__(self, server, sock, address):  # each client socket handling
        self.server = server
        self.client = sock
        self.address = address
        self.usingssl = False
        self.sendq = []
        self.device_id = ''
        self.time_stamps = []
        self.last_called = ''
    
    def DeviceVerify(self, id_, key):  # use fileterrs or hash
        """
        connect to DB and verify if the device and key matches
        """
        return 1

    def handleMessage(self, id_, data):
        """
        manage your message here by overriding this method
        """
        pass

    def handleClose(self, error=''):
        """
        Called when a iotsocket server gets a Close frame from a client
        and also when error occurs
        """
        pass

    def chkTime(self, device_time, server_time):
        """
        Check if the time matches the server time and
        to make sure there are no reused data packet (replay attacks)
        """
        frmt = "%H.%M.%S.%f"
        time_drop_max = 3  # packet with time difference 3sec will not be accepted
        if(device_time in self.time_stamps):
            return False
        else:
            # block if more than 333 req are observed in time
            if(len(self.time_stamps) < 333):
                time = datetime.strptime(
                    server_time, frmt) - datetime.strptime(device_time, frmt)
                # to remove old time stamps (to reduce memory usage)
                if len(self.time_stamps) > 1:
                    stamps_time = datetime.strptime(
                        self.time_stamps[-1], frmt) - datetime.strptime(server_time, frmt)
                    if (stamps_time.seconds > time_drop_max):
                        self.time_stamps = []
                # check time difference
                if (time.seconds > time_drop_max):
                    return 0
                elif (time.seconds < time_drop_max):
                    self.time_stamps.append(device_time)
                    return 1
            else:
                raise Exception(
                    "ERROR: DOS attack more than 300 req from "+str(self.device_id))


    def verifyHeaders(self, headers, values, time_now):
        if(headers['IOT'] == '1.1'):
            if(self.chkTime(headers['TIME'], time_now)):  # check time
                if(self.device_id == '' and len(headers['DEVICE']) == deviceid_length and int(headers['DEVICE']) not in all_device_ids):
                    self.device_id = int(headers['DEVICE'])
                    # verify if device id and key are correct
                    if (self.DeviceVerify(self.device_id, headers['KEY'])):
                        all_device_ids.append(int(self.device_id))
                    else:
                        raise Exception(
                            "ERROR: Invalid Device key "+str(values)+' '+str(self.device_id))
                # close socket if device id is changed after 1st request
                if(int(headers['DEVICE']) != self.device_id):
                    raise Exception(
                        "ERROR: Invalid Device ID "+str(values)+' '+str(self.device_id))
                else:
                    return 1
            else:
                raise Exception(
                    "ERROR: Incorrect time stamp "+str(values)+' '+str(self.device_id))
        else:
            raise Exception(
                "ERROR: Incorrect IOT version detected "+str(values)+' '+str(self.device_id))

    def _handleData(self):
        time_now = str(datetime.now().time())           # 15:13:54.420103
        time_now = time_now.replace(':', '.')
        self.last_called = time_now
        try:  # 65535 max data (including headers)
            data = self.client.recv(data_maxLength)
        except Exception as n:
            data = b''
        data = data.decode()
        if not data:
            raise Exception("remote socket closed "+str(self.device_id))
        else:
            data = data.split('|#|')   # split data at delimeter
            del data[-1]
            # split headers and data
            for data in data:
                fields, data = data.split("\r\n\r\n", 1)
                fields, data = fields.strip() if len(
                    fields) < fields_maxLength else 0, data.strip() if len(data) < (data_maxLength-3000) else 0
                headers, values = {}, ''
                # separate each line with('\r\n')
                for field in fields.split('\r\n'):
                    # split each key,value with ':'
                    key, value = field.split(':')
                    headers[key] = value
                    values = values+value+' '
                    if len(headers) > 10:
                        break
                values = values.strip()
                if len(headers) != 5 or len(data) < 5:
                    raise Exception("ERROR: Headers issue " +
                                    str(values)+' '+str(self.device_id))
                elif(self.verifyHeaders(headers, values, time_now)):
                    self.handleMessage(self.device_id, data)

    def _sendBuffer(self, buff, send_all=False):
        # send data to client
        time_now = str(datetime.now().time())
        time_now = time_now.replace(':', '.')
        headers = '''
IOT:1.1
DATE:24/7/2019
TIME:{time_now}
DEVICE:{id_}
KEY:AJ
        

'''.format(time_now=time_now, id_=self.device_id).encode()
        buff = headers.replace(b'\n', b'\r\n')+buff.replace(b'|#|', b'') + b'|#|'
        size = len(buff)
        tosend = size
        already_sent = 0
        while tosend > 0:
            try:
                sent = self.client.send(buff[already_sent:])
                if sent == 0:
                    raise RuntimeError(
                        'ERROR: Socket connection broken while sending data to '+str(self.device_id))
                already_sent += sent
                tosend -= sent
            except socket.error as e:
                # if we have full buffers then wait for them to drain and try again
                if e.errno in [errno.EAGAIN, errno.EWOULDBLOCK]:
                    if send_all:
                        continue
                    return buff[already_sent:]
                else:
                    raise e
        return None


class IOTSocketServer(object):
    def __init__(self, host, port, read_from_function, IOTSocketclass, selectInterval=0.1):
        self.IOTSocketclass = IOTSocketclass
        if (host == ''):
            host = None
        if host is None:
            fam = socket.AF_INET6
        else:
            fam = 0
        hostInfo = socket.getaddrinfo(
            host, port, fam, socket.SOCK_STREAM, socket.IPPROTO_TCP, socket.AI_PASSIVE)
        self.serversocket = socket.socket(
            hostInfo[0][0], hostInfo[0][1], hostInfo[0][2])
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind(hostInfo[0][4])
        self.serversocket.listen(5)
        self.selectInterval = selectInterval
        self.connections = {}
        self.listeners = [self.serversocket]
        # open(read_from_function, 'r')
        self.read_from_function = read_from_function

    def _decorateSocket(self, sock):
        return sock

    def _constructIOTSocket(self, sock, address):
        return self.IOTSocketclass(self, sock, address)

    def close(self):
        self.serversocket.close()
        for _, conn in self.connections.items():
            conn.close()
            self._handleClose(conn)

    def _handleClose(self, client, error=''):
        if(client.device_id in all_device_ids):
            all_device_ids.remove(client.device_id)
        client.client.close()
        # only call handleClose when we have a successful iotsocket connection
        client.handleClose(error)

    def serveonce(self):
        # import pymysql
        frmt = "%H.%M.%S.%f"
        # 15:13:54.420103
        time_now = str(datetime.now().time())
        time_now = time_now.replace(':', '.')
        writers = []
        writers_send_data = {}
        # get actions of all requested clients
        f = self.read_from_function()                          # read data from pipe as list
        for clientID in f:
            try:
                # separate client id, data and send to client
                clientID, snd_data = clientID.split(' ', 1)
                writers_send_data[int(clientID)] = writers_send_data[int(
                    clientID)] + snd_data if (int(clientID)) in writers_send_data else snd_data
            except Exception as n:
                raise Exception(n,"Invalid data format")

        # iterate to all  file no's and check if any data is to be sent
        for fileno in self.listeners:
            if fileno == self.serversocket:
                continue
            client = self.connections[fileno]
            if client.last_called != '':
                time = datetime.strptime(
                    time_now, frmt) - datetime.strptime(client.last_called, frmt)
                # To remove Half-Open (Dropped) Connections
                if time.seconds > 90:   # if client did not send any data for 90 sec close the client
                    self._handleClose(client, 'ERROR: Removing half opened/Dropped connections'+ client.device_id)
                    del self.connections[fileno]
                    self.listeners.remove(fileno)
            # append client who has data to be sent for
            # if deviceid has data to send append to writers
            if client.device_id != '' and int(client.device_id) in writers_send_data:
                writers.append(fileno)
                client.sendq.append(writers_send_data[int(client.device_id)])

        rList, wList, xList = select(
            self.listeners, writers, self.listeners, self.selectInterval)

        # client who is ready to write for...
        for ready in wList:
            client = self.connections[ready]
            try:
                while client.sendq:                         # read data in deviceid sendq and send it to client
                    a_test = client.sendq
                    payload = client.sendq.pop(0)
                    client._sendBuffer(payload.encode())
            except Exception as n:
                self._handleClose(client, n)
                del self.connections[ready]
                self.listeners.remove(ready)

        for ready in rList:                                 # read available sockets in read list
            if ready == self.serversocket:
                sock = None
                try:
                    sock, address = self.serversocket.accept()      # accept the socket
                    newsock = self._decorateSocket(sock)
                    newsock.setblocking(0)
                    fileno = newsock.fileno()
                    self.connections[fileno] = self._constructIOTSocket(
                        newsock, address)
                    self.listeners.append(fileno)
                except Exception as n:
                    if sock is not None:
                        sock.close()
            else:  # read data if available
                if ready not in self.connections:
                    continue
                client = self.connections[ready]
                try:
                    client._handleData()  # handle each client data separately
                except Exception as n:
                    self._handleClose(client, n)
                    del self.connections[ready]
                    self.listeners.remove(ready)

        for failed in xList:
            if failed == self.serversocket:
                self.close()
                raise Exception('server socket failed')
            else:
                if failed not in self.connections:
                    continue
                client = self.connections[failed]
                self._handleClose(
                    client, 'Failed at xList(socket exception in select)')
                print(client)
                del self.connections[failed]
                self.listeners.remove(failed)

    def serveforever(self):
        while True:
            self.serveonce()


class IOTSocketServerSSL(IOTSocketServer):

    def __init__(self, host, port, read_from_function, IOTSocketclass, certfile=None,
                 keyfile=None, version=ssl.PROTOCOL_TLS_SERVER, selectInterval=0.1, ssl_context=None):

        IOTSocketServer.__init__(self, host, port, read_from_function,
                                 IOTSocketclass, selectInterval)

        if ssl_context is None:
            self.context = ssl.SSLContext(version)
            self.context.load_cert_chain(certfile, keyfile)
        else:
            self.context = ssl_context

    def close(self):
        super(IOTSocketServerSSL, self).close()

    def _decorateSocket(self, sock):
        sslsock = self.context.wrap_socket(sock, server_side=True)
        return sslsock

    def _constructIOTSocket(self, sock, address):
        s = self.IOTSocketclass(self, sock, address)
        s.usingssl = True
        return s

    def serveforever(self):
        super(IOTSocketServerSSL, self).serveforever()

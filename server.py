# -*- coding: utf-8 -*-

import asyncio


class ServerError(Exception):
    pass

class ServerSocketError(Exception):
    pass

class ServerProtocolError(Exception):
    pass


class EchoServerClientProtocol(asyncio.Protocol):
    metric_dict = {}

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connect successfully! Connection from {}'.format(peername))

        try:
            self.transport = transport
        except Exception as err:
            raise ServerSocketError('connection error. ', err)


    def data_receiver(self, data):

        message = data.decode()
        print('Data received: {!r}'.format(message))
        if message.find('put') != -1:
            try:
                message = message.split('\n')
                message = message[0].replace('put ', '')
                message = message.split(' ')
                if self.metric_dict.get(message[0]) is None:
                    self.metric_dict[message[0]] = [(int(message[2]), float(message[1]))]
                else:
                    self.metric_dict[message[0]].append((int(message[2]), float(message[1])))
                data = b'ok\n\n'
                self.transport.write(data)
            except:
                data = b"error\nwrong command\n\n"
                self.transport.write(data)

        elif message.find('get') != -1:
            try:
                message = message.split('\n')
                message = message[0].replace('get ', '')

                send_mes ='ok'
                if message == '*':
                    for key in self.metric_dict:
                        self.metric_dict[key] = set(self.metric_dict[key])
                        self.metric_dict[key] = sorted(self.metric_dict[key], key=lambda tmpstm: tmpstm[0])
                    for key in self.metric_dict:
                        for element in self.metric_dict[key]:
                            send_mes+= f'\n{key} {element[1]} {element[0]}'

                elif self.metric_dict.get(message)is not None:
                    self.metric_dict[message] = set(self.metric_dict[message])
                    self.metric_dict[message] = sorted(self.metric_dict[message], key=lambda tmpstm: tmpstm[0])
                    for element in self.metric_dict[message]:
                        send_mes += f"\n{message} {element[1]} {element[0]}"
                else:
                    data = b"ok\n\n"
                    self.transport.write(data)
                send_mes += '\n\n'
                send_mes = send_mes.encode()
                self.transport.write(send_mes)
            except:
                send_mes = b"error\nwrong command\n\n"
                self.transport.write(send_mes)

        else:
            send_mes = b"error\nwrong command\n\n"
            self.transport.write(send_mes)


def run_server(host='127.0.0.1', port=8888):
    try:
        eloop = asyncio.get_event_loop()
        server_generator = eloop.create_server(EchoServerClientProtocol, host, port)
        server = eloop.run_until_complete(server_generator)
    except Exception as err:
        raise server.ServerError('Server Error: ', err)

    print('Serving on {}'.format(server.sockets[0].getsockname()))

    try:
        eloop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    eloop.run_until_complete(server.wait_closed())
    eloop.close()


if __name__ == '__main__':
    run_server()

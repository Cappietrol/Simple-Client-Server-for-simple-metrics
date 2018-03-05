# -*- coding: utf-8 -*-
import socket
import time


class ClientError(Exception):
    """Общий класс исклечения клиента"""
    pass


class ClientSocketError(Exception):
    """Исключение, выбрасываемое клиентом при сетевой ошибке"""
    pass


class ClientProtocolError(Exception):
    """Исключение, выбрасываемое клиентом при ошибке протокола"""
    pass


class Client:

    def __init__(self, host_server, port_server, timeout=None):
        self.host_server = host_server
        self.port_server = port_server
        self.socket_connection = socket.socket()
        try:
            self.socket_connection.connect((self.host_server, self.port_server, timeout))
        except:
            raise ClientSocketError('Create connection error')

    def put(self, metric_name, metric_value, timestamp=None):
        """Метод для отправки метрик"""
        if type(metric_name) is not str:
            try:
                metric_name = str(metric_name)
            except:
                raise ClientError(f'Metric name incorrect. Metric name: {metric_name}')

        if type(metric_value) is not float:
            try:
                metric_value = float(metric_value)
            except:
                raise ClientError(f'Metric Value incorrect. Metric value: {metric_value}')

        timestamp = str(int(time.time())) if timestamp is not None else timestamp
        send_str = f"put {metric_name} {metric_value} {timestamp}\n"

        try:
            self.socket_connection.send(send_str.encode())
        except socket.error as err:
            raise ClientSocketError('Send data error', err)

        try:
            data_recv = (self.socket_connection.recv(1024))
            data_recv = data_recv.decode('utf-8')

            if data_recv.find('ok') == -1 or data_recv.find('error'):
                raise ClientProtocolError('Recived data include error')
            else:
                print('Send metric done')
                return None
        except Exception as err:
            raise ClientSocketError('Recive data error', err)

    def get(self, metric_name):
        """Метод для получения метрик"""
        try:
            metric_name = str(metric_name)
        except:
            raise ClientError(f'Metric name incorrect. Metric name: {metric_name}')

        send_str = f"get {metric_name}\n"
        send_str = send_str.encode()

        try:
            self.socket_connection.send(send_str)
        except Exception as err:
            raise ClientSocketError('Send data error', err)

        try:
            data_recv = (self.socket_connection.recv(1024))
            data_recv = data_recv.decode('utf-8')
            metric_dict = {}

            if data_recv.find('ok') == -1 or data_recv.find('error'):
                raise ClientError('Recived error data')
            elif data_recv.find(r"ok\n\n") != -1:
                return metric_dict
            else:
                tmp = data_recv.split(r'\n\n')
                tmp = tmp[0].split('\n')
                for element in tmp:
                    if element.find('ok') != -1 or element == '':
                        continue
                    else:
                        metrica = element.split(' ')
                        if metric_dict.get(metrica[0]) is None:
                            metric_dict[metrica[0]] = [(int(metrica[2]), float(metrica[1]))]
                        else:
                            metric_dict[metrica[0]].append((int(metrica[2]), float(metrica[1])))
                print(metric_dict)
                return metric_dict

        except Exception as err:
            raise ClientSocketError('Recive data error', err)

        pass
    
    def close(self):
        try:
            self.socket_connection.close()
        except:
            raise Exception

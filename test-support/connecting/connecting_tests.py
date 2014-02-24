import socket


def connecting_test_1():
    try:
        socket.create_connection(("localhost", 8080))
    except:
        pass


def connecting_test_2():
    try:
        socket.create_connection(("localhost", 8080))
    except:
        pass

    try:
        socket.create_connection(("127.0.0.1", 8000))
    except:
        pass

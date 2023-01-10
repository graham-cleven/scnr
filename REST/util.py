#! /usr/bin/env python3

import ipaddress
import traceback
import sys
import socket


def unix_socket(cmd):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect("/tmp/socket_test.s")
    client.send(bytes(str(cmd), "utf-8"))


def split_network(box):
    try:
        ips = list(ipaddress.ip_network(box).hosts())
        return ips

    except:
        # not a network
        return False


def asDict(obj):
    resp = []
    for z in obj:
        resp.append({c.name: getattr(z, c.name) for c in z.__table__.columns})
    return resp


def configure_logging():
    import logging

    logger = logging.basicConfig(
        filename="../agentless.log", encoding="utf-8", level=logging.debug
    )
    return logger


def format_exception(e):
    exception_list = traceback.format_stack()
    exception_list = exception_list[:-2]
    exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
    exception_list.extend(
        traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1])
    )

    exception_str = "Traceback (most recent call last):\n"
    exception_str += "".join(exception_list)
    # Removing the last \n
    exception_str = exception_str[:-1]

    return exception_str

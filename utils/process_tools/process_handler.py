# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : process_handler.py
"""
import psutil


def is_port_in_use(port) -> bool:
    """ 判断端口是否占用"""
    for proc in psutil.process_iter():
        for con in proc.connections():
            if con.status == 'LISTEN' and con.laddr.port == port:
                return True
    return False


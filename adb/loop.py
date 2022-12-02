# coding=UTF-8


def loop(*method, times):
    loop_time = 0
    while True:
        if loop_time > times:
            break
        loop_time = loop_time + 1
        method

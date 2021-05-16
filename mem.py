# coding=UTF-8
# 内存相关
import os


def meminfoSimple(package):
    # cmd = "adb  shell dumpsys meminfo " + package + " | grep -E 'Dalvik Heap|Activities|Private'"
    # os.system(cmd)
    meminfo(package, "Dalvik Heap|Activities|Private")


def meminfoAll(package):
    # cmd = "adb  shell dumpsys meminfo " + package + " | grep -E 'Dalvik Heap|Activities|Private'"
    # os.system(cmd)
    meminfo(package, "")


"""
adb  shell dumpsys meminfo 包名 的具体实现
打印包相关的内存信息
"""


def meminfo(pkg, grep):
    cmd = "adb  shell dumpsys meminfo "
    if pkg != "":
        cmd = cmd + pkg
    if grep != "":
        cmd = cmd + " | grep -E '" + grep + "'"
    print("cmd " + cmd)
    os.system(cmd)


def loop(times):
    loop_time = 0
    while True:
        if loop_time > times:
            print("loop end")
            break
        loop_time = loop_time + 1
        print("loop " + str(loop_time))
        meminfoSimple("com.baidu.haokan")


def test():
    # mem.meminfoAll("com.baidu.haokan")
    # mem.meminfoSimple("com.baidu.haokan")
    # adb  shell dumpsys meminfo 可以查看所有应用的内存情况，内存按照可见性、adj等排序，可以计算出当前应用的pss排行、oom adj排行，应用示范处于可见性等
    # mem.meminfoAll("")
    # adb  shell dumpsys meminfo  | grep -E 'Total|com.baidu.haokan'
    # mem.meminfo("", "Total|com.baidu.haokan")
    loop(5)

# coding=UTF-8
"""
adb shell dumpsys activity
activity 相关
"""
import os


def actTop(grep,notgrep):
    cmd = " adb shell dumpsys activity  top "
    if grep != "":
        cmd = cmd + " | grep -E '" + grep + "'"
    if notgrep != "":
        cmd = cmd + " | grep -v '" + notgrep + "'"
    print("cmd " + cmd)
    os.system(cmd)

def act(pkg, grep):
    cmd = " adb shell dumpsys activity  activities "
    if pkg != "":
        cmd = cmd + pkg
    if grep != "":
        cmd = cmd + " | grep -E '" + grep + "'"
    print("cmd " + cmd)
    os.system(cmd)


def test():
    print("test")
    """
    打印activity和Task相关
    """
    # act("com.baidu.haokan", 'com.baidu.haokan')
    # act("com.yy.mobile.union.haokan", 'com.yy.mobile.union.haokan')
    """
     # adb shell dumpsys activity top | grep -E 'ACTIVITY|Added Fragments|Active Fragments|id=|mContainer=' |  grep -v 'mParent'
     打印activity和fragment的层级关系
    """
    actTop("ACTIVITY|Added Fragments|Active Fragments|id=|mContainer=", "mParent")
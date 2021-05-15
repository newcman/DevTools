# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import wx

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')



    # 创建一个应用程序
    # 参数False表示标准输出和错误输出内容不会被重定向
    app = wx.App(False)
    # 创建一个窗口
    # 该窗口的父窗口是None，就是没有父窗口
    # wx.ID_ANY表示随机生成一个ID给该窗口
    # 第三个参数是窗口的标题
    frame = wx.Frame(None, wx.ID_ANY, u"第一个wxPython演示程序")
    frame.Show(True)  # 显示该窗口
    app.MainLoop()  # 应用程序消息处理

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

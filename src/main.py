import wx
from frontend import MainFrame  # Corrected import

def main():
    app = wx.App(False)
    frame = MainFrame()  # Corrected class name
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()
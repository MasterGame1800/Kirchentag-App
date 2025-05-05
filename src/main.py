import wx
from frontend import MainFrame  # Import the main GUI frame

def main():
    """
    Entry point for the application. Initializes the wxPython app and shows the main frame.
    """
    app = wx.App(False)  # Create a wxPython application instance
    frame = MainFrame()  # Instantiate the main GUI frame
    frame.Show()  # Display the frame
    app.MainLoop()  # Start the application's main event loop

if __name__ == "__main__":
    main()  # Run the main function if this script is executed directly
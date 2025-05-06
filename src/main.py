import wx
from main_frame import MainFrame  # Import the main GUI frame

def main():
    """
    Entry point for the application. Initializes the wxPython app and shows the main frame.
    """
    print("Initializing wxPython application...")
    app = wx.App()  # Create a wxPython application instance
    print("Creating MainFrame...")
    frame = MainFrame()  # Instantiate the main GUI frame
    print("Showing MainFrame...")
    frame.Show()  # Display the frame
    print("Starting main event loop...")
    app.MainLoop()  # Start the application's main event loop

if __name__ == "__main__":
    main()  # Run the main function if this script is executed directly
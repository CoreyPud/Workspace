# Website Monitor

This project provides a simple Tkinter-based GUI application that monitors specified web pages for given keywords at customizable intervals.

## Features
- Add multiple website monitors with individual keyword lists and check frequencies.
- Displays log output for keyword detections and errors.

## Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python website_monitor.py
   ```
3. Use the GUI to add websites, keywords (comma separated), and the interval in seconds.

## Notes
- The application fetches pages over HTTP using the `requests` library.
- Close the window to stop all monitoring threads.

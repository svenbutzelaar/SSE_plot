import os
import subprocess

def open_in_windows_browser(file_path):
    # Adjust the path as needed if it's different for your system
    windows_browser_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    subprocess.run([windows_browser_path, file_path])

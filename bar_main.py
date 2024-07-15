from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QUrl, pyqtSignal, QTimer, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from functions import dprint
import os
import re
import sys

# Main application window
class MainWindow(QMainWindow):
    url_changed_signal = pyqtSignal(str)  # Signal emitted when the URL changes

    def __init__(self):
        super().__init__()
        self.text = ""
        self.expected_url = ""
        self.current_url = ""
        self.is_gradient_page = False
        self.url_load_finished = False

        # Timer to periodically check the URL
        self.check_timer = QTimer(self)
        self.check_timer.timeout.connect(self.check_url)

        # Timer to hide the window after a certain time
        self.hide_timer = QTimer(self)
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide_window)

        self.setup_ui()

    # Set up the user interface
    def setup_ui(self):
        screen = QApplication.primaryScreen().availableGeometry()
        screen_width = screen.width()
        screen_height = screen.height()

        window_width = 400
        window_height = 50
        x = int((screen_width / 2) - (window_width / 2))
        y = screen_height - window_height - 15

        self.setGeometry(x, y, window_width, window_height)
        self.setWindowTitle("Window")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)

        self.webview = QWebEngineView(self)
        self.setCentralWidget(self.webview)

        self.setStyleSheet("""
            border-radius: 15px;
        """)

        self.webview.loadFinished.connect(self.on_load_finished)

    # Change the URL of the web view
    def change_url(self, url, text=""):
        self.text = text
        if url == "/web/bar_input.html":
            local_file_path = os.path.abspath("web/bar_input.html")
            full_url = QUrl.fromLocalFile(local_file_path)
        elif text:
            full_url = QUrl(f"{url}?text={text}")
        else:
            full_url = QUrl(url)
        self.expected_url = full_url.toString()
        self.url_load_finished = False
        self.webview.setUrl(full_url)

        # Hide the window while loading the new URL
        self.hide()
        QApplication.processEvents()

    # Called when the web view finishes loading
    def on_load_finished(self, ok):
        if ok:
            self.current_url = self.webview.url().toString()
            self.url_load_finished = True
            self.check_url()

    # Check the current URL and handle accordingly
    def check_url(self):
        if not self.url_load_finished:
            return

        current_url = self.webview.url().toString()
        dprint(current_url)

        if current_url.endswith("web/bar_input.html"):
            self.is_gradient_page = True
            self.show()
            self.activate_window()
            self.check_timer.start(100)
        elif "jarvistts" in current_url:
            self.handle_jarvistts_url()
        else:
            self.is_gradient_page = False
            match = re.search(r"text=([^&]*)", current_url)
            if match:
                text = match.group(1)
                self.url_changed_signal.emit(text)
                self.hide()
            else:
                self.url_changed_signal.emit("")
                self.hide()
            self.check_timer.stop()

    # Handle URLs containing 'jarvistts'
    def handle_jarvistts_url(self):
        match = re.search(r"text=([^&]*)", self.current_url)
        if match:
            text = match.group(1)
            total_time = self.calculate_typing_time(text)
            dprint(f"Total time for text window: {total_time} seconds")
            self.show()
            self.activate_window()
            self.hide_timer.start(int(total_time * 1000))  # Convert seconds to milliseconds
        else:
            dprint("No text found in  URL")

    # Calculate the time required for typing animation
    def calculate_typing_time(self, text):
        num_chars = len(text)
        typing_time_seconds = (num_chars * 50) / 1000.0
        typing_animation_time = 2.0
        fade_in_animation_time = 0.5
        total_time_seconds = typing_time_seconds + typing_animation_time + fade_in_animation_time
        return total_time_seconds

    # Hide the window
    def hide_window(self):
        self.hide()
        dprint("Window hidden")

    # Bring the window to the front and give it focus
    def activate_window(self):
        self.activateWindow()
        self.raise_()

# Helper class to manage URL setting and running the app
class URLSetter:
    def __init__(self):
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.main_window = MainWindow()

    def seturl(self, url, text="", url_change_callback=None):
        if callable(text) and url_change_callback is None:
            url_change_callback = text
            text = ""

        if url_change_callback:
            try:
                self.main_window.url_changed_signal.disconnect()
            except TypeError:
                pass
            self.main_window.url_changed_signal.connect(url_change_callback)

        self.main_window.change_url(url, text)

    def run(self):
        self.app.exec_()

url_setter = URLSetter()

def seturl(url, text="", url_change_callback=None):
    url_setter.seturl(url, text, url_change_callback)

def run_app():
    url_setter.run()

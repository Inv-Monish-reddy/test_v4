import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from app import app  # import your Flask app

def run_flask():
    app.run(host='127.0.0.1', port=5000, debug=False)

def start_desktop_app():
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    app_qt = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Animation Calculator")
    window.resize(1000, 700)

    browser = QWebEngineView()
    browser.setUrl(QUrl("http://127.0.0.1:5000"))
    window.setCentralWidget(browser)

    window.show()
    sys.exit(app_qt.exec_())

if __name__ == "__main__":
    start_desktop_app()

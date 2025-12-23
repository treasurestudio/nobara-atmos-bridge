import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QWidget, QTextEdit, QLabel, QFileDialog)
from PyQt6.QtCore import Qt, QTimer
from engine import AudioEngine

class NobaraAudioHub(QMainWindow):
    def __init__(self):
        super().__init__()
        self.engine = AudioEngine()
        
        # --- UNIVERSAL PATH LOGIC ---
        # This finds the current user's home (e.g., /home/john or /home/sarah)
        self.user_home = os.path.expanduser("~")
        
        # The dynamic path to your Ableton install
        self.daw_path = os.path.join(
            self.user_home, 
            ".wine/drive_c/ProgramData/Ableton/Live 12 Lite/Program/Ableton Live 12 Lite.exe"
        )
        
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Atmos Bridge Hub")
        self.setFixedSize(500, 400)
        
        layout = QVBoxLayout()
        
        self.label = QLabel("Nobara Atmos Bridge")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.label)

        # Status Display
        self.status_log = QTextEdit()
        self.status_log.setReadOnly(True)
        self.status_log.append("System Ready...")
        layout.addWidget(self.status_log)

        # Path Label (Shows the user where it's looking)
        self.path_label = QLabel(f"Target: {self.daw_path}")
        self.path_label.setWordWrap(True)
        self.path_label.setStyleSheet("font-size: 10px; color: gray;")
        layout.addWidget(self.path_label)

        # Launch Button
        self.btn_launch = QPushButton("Launch Ableton (Atmos Bridge)")
        self.btn_launch.clicked.connect(self.launch_daw)
        self.btn_launch.setStyleSheet("background-color: #2c3e50; color: white; padding: 10px;")
        layout.addWidget(self.btn_launch)

        # Exit Button
        self.btn_exit = QPushButton("Exit")
        self.btn_exit.clicked.connect(self.close)
        layout.addWidget(self.btn_exit)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def launch_daw(self):
        if os.path.exists(self.daw_path):
            self.status_log.append(f"Launching from: {self.daw_path}")
            # The engine handles the heavy lifting of Wine/Pipewire
            self.engine.start_bridge(self.daw_path)
        else:
            self.status_log.append("ERROR: Ableton not found at this path.")
            self.status_log.append("Please verify your Wine installation.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NobaraAudioHub()
    window.show()
    sys.exit(app.exec())

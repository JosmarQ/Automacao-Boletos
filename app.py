import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QHBoxLayout, QPushButton, QSlider, QVBoxLayout, QWidget

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Boleto Automatico')
        self.setGeometry(100, 100, 400, 250)

        # Create a media player
        self.media_player = QMediaPlayer()
        self.media_player.setVolume(50)  # Set the initial volume to 50%

        # Create a media player output
        self.media_output = QWidget(self)
        self.media_output.setStyleSheet("background-color: black;")

        # Create play button
        self.play_button = QPushButton(' ♪ ', self)
        self.play_button.setStyleSheet("background-color: black; color: #00FF00; border: 2px solid #00FF00;")
        self.play_button.clicked.connect(self.play_music)

        # Create volume slider
        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setStyleSheet("QSlider::groove:horizontal { background-color: #00FF00; } "
                                         "QSlider::handle:horizontal { background-color: #00FF00; border: 2px solid #000000; width: 15px; } "
                                         "QSlider::add-page:horizontal { background-color: #000000; } "
                                         "color: #00FF00;")
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)  # Set the initial volume to 50%
        self.volume_slider.valueChanged.connect(self.set_volume)

        # Create a vertical layout for the volume slider
        self.volume_layout = QVBoxLayout()
        self.volume_layout.addWidget(self.volume_slider)

        # Create a horizontal layout for the play button and volume layout
        self.controls_layout = QHBoxLayout()
        self.controls_layout.addWidget(self.play_button)
        self.controls_layout.addLayout(self.volume_layout)

        # Create a button for calling another program
        self.call_program_button = QPushButton('Call Another Program', self)
        self.call_program_button.setStyleSheet("background-color: black; color: #00FF00; border: 2px solid #00FF00;")
        self.call_program_button.clicked.connect(self.call_another_program)

        # Create a vertical layout for the controls and the additional button
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.controls_layout)
        self.main_layout.addWidget(self.call_program_button)

        # Set the layout of the media output widget
        self.media_output.setLayout(self.main_layout)

        # Set the central widget
        self.setCentralWidget(self.media_output)

    def play_music(self):
        music_content = QMediaContent(QUrl.fromLocalFile('Automacao-Boletos\music.mp3'))
        self.media_player.setMedia(music_content)
        self.media_player.play()

    def set_volume(self):
        volume = self.volume_slider.value()
        self.media_player.setVolume(volume)

    def call_another_program(self):
        # Add code here to call another program when the button is clicked
        pass  # Replace this with the actual code to call the program

def main():
    app = QApplication(sys.argv)
    player = App()
    player.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
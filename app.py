import sys
from PyQt5.QtCore import Qt, QUrl, QProcess, QThread, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QPushButton, QSlider, QVBoxLayout, QWidget, QTextEdit
from separar import separar_pdf
from main import Open_Browser, Load_Excel, Loop

class LoopThread(QThread):
    started_signal = pyqtSignal()
    finished_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        self.started_signal.emit()  # Emit a signal when the loop starts
        Loop()  # Run your loop function here
        self.finished_signal.emit()  # Emit a signal when the loop finishes

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Boleto Automatico')
        self.setGeometry(100, 100, 400, 550)

        self.media_player = QMediaPlayer()
        self.media_player.setVolume(50)

        self.media_output = QWidget(self)
        self.media_output.setStyleSheet("background-color: black;")

        self.play_button = QPushButton(' ♪ ', self)
        self.play_button.setStyleSheet("background-color: black; color: #00FF00; border: 2px solid #00FF00;")
        self.play_button.clicked.connect(self.play_music)

        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setStyleSheet("QSlider::groove:horizontal { background-color: #00FF00; } "
                                         "QSlider::handle:horizontal { background-color: #00FF00; border: 2px solid #000000; width: 15px; } "
                                         "QSlider::add-page:horizontal { background-color: #000000; } "
                                         "color: #00FF00;")
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.set_volume)

        self.controls_layout = QHBoxLayout()
        self.controls_layout.addWidget(self.play_button)
        self.controls_layout.addWidget(self.volume_slider)

        self.call_program_button = QPushButton('Open Chrome', self)
        self.call_program_button.setStyleSheet("background-color: black; color: #00FF00; border: 2px solid #00FF00;")
        self.call_program_button.clicked.connect(self.call_start)

        self.call_loop_button = QPushButton('Start Script', self)
        self.call_loop_button.setStyleSheet("background-color: black; color: #00FF00; border: 2px solid #00FF00;")
        self.call_loop_button.clicked.connect(self.call_loop)

        self.stop_loop_button = QPushButton('Stop Script', self)
        self.stop_loop_button.setStyleSheet("background-color: black; color: #FF0000; border: 2px solid #FF0000;")
        self.stop_loop_button.clicked.connect(self.stop_loop)

        self.progress_text = QTextEdit(self)
        self.progress_text.setReadOnly(True)
        self.progress_text.setStyleSheet("background-color: black; color: #00FF00; border: 2px solid #00FF00;")

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.controls_layout)
        self.main_layout.addWidget(self.call_program_button)
        self.main_layout.addWidget(self.call_loop_button)
        self.main_layout.addWidget(self.stop_loop_button)
        self.main_layout.addWidget(self.progress_text)

        self.media_output.setLayout(self.main_layout)
        self.setCentralWidget(self.media_output)

        self.loop_thread = None  # Initialize the LoopThread instance

    def play_music(self):
        music_content = QMediaContent(QUrl.fromLocalFile('music.mp3'))
        self.media_player.setMedia(music_content)
        self.media_player.play()
        self.progress_text.append('''\n
         #################################  
      ##################################  
    ###################################  
   #### \t      #####\t          ####
  ###   \t      #####\t          #####           
  #     \t      #####\t          #####           
  #     \t      #####\t            ####            
        \t      #### \t            ####            
        \t      #### \t            ####            
        \t      #### \t            ####            
        \t    ##### \t            #####            
        \t    ##### \t            #####            
        \t    ####  \t            #####            
        \t    ####  \t            #####            
        \t   #####  \t            #####            
        \t ######   \t            #####            
        \t#######   \t            #####        ##  
        \t#######   \t            ######       ##  
        \t#######   \t             ###########  
        \t#######   \t             ###########   
       \t#######    \t              #########    
       \t######     \t               ######
''')

    def set_volume(self):
        volume = self.volume_slider.value()
        self.media_player.setVolume(volume)

    def call_start(self):
        path = 'PlanilhaCondominos.xlsx'
        separar_pdf()
        self.progress_text.append('PDF recortado . . . . . . . . .  OK')
        Load_Excel(path)
        self.progress_text.append('Excel carregado . . . . . . . .  OK')
        Open_Browser()
        self.progress_text.append('Browser pronto . . . . . . . . . OK')

    def call_loop(self):
        if not self.loop_thread:
            self.loop_thread = LoopThread()
            self.loop_thread.started_signal.connect(self.loop_started)
            self.loop_thread.finished_signal.connect(self.program_finished)
            self.loop_thread.start()

    def loop_started(self):
        self.progress_text.append('Loop started.')

    def stop_loop(self):
        if self.loop_thread and self.loop_thread.isRunning():
            self.loop_thread.terminate()
            self.progress_text.append('Script stopped.')
            self.loop_thread = None

    def program_finished(self):
        self.progress_text.append('Script finished.')
        self.close()

def main():
    app = QApplication(sys.argv)
    player = App()
    player.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

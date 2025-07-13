import sys
import sounddevice as sd
import soundfile as sf
import numpy as np
import tempfile
import os
import whisper
import pyperclip
import keyboard
import configparser
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox
from PyQt6.QtCore import QTimer, QThread, pyqtSignal

class TranscribeThread(QThread):
    transcription_finished = pyqtSignal(str)
    transcription_error = pyqtSignal(str)

    def __init__(self, audio_path, model_name):
        super().__init__()
        self.audio_path = audio_path
        self.model_name = model_name

    def run(self):
        try:
            model = whisper.load_model(self.model_name)
            result = model.transcribe(self.audio_path)
            self.transcription_finished.emit(result["text"])
        except Exception as e:
            self.transcription_error.emit(str(e))

class AudioTranscriberApp(QWidget):
    def __init__(self):
        super().__init__()
        self.is_recording = False
        self.audio_data = []
        self.samplerate = 44100  # Taxa de amostragem
        self.channels = 1       # Mono
        self.recording_timer = QTimer(self)
        self.recording_timer.timeout.connect(self.update_recording_status)
        self.elapsed_time = 0
        self.temp_audio_file = None
        self.transcribe_thread = None
        self.hotkey_registered = None
        self.config = configparser.ConfigParser()
        self.config_file = 'config.ini'
        self.load_settings()
        self.initUI()
        self.register_hotkey()

    def load_settings(self):
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
            self.hotkey = self.config.get('Settings', 'hotkey', fallback='Ctrl+Shift+R')
            self.whisper_model = self.config.get('Settings', 'whisper_model', fallback='base')
        else:
            self.hotkey = 'Ctrl+Shift+R'
            self.whisper_model = 'base'

    def save_settings(self):
        self.config['Settings'] = {
            'hotkey': self.hotkey_input.text(),
            'whisper_model': self.whisper_model_combo.currentText()
        }
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def initUI(self):
        self.setWindowTitle("Gravador e Transcritor de Áudio")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Botão de Gravação
        self.record_button = QPushButton("Gravar Áudio")
        self.record_button.clicked.connect(self.toggle_recording)
        layout.addWidget(self.record_button)

        # Configuração de Atalho de Teclado
        layout.addWidget(QLabel("Atalho de Teclado:"))
        self.hotkey_input = QLineEdit(self.hotkey)
        self.hotkey_input.textChanged.connect(self.register_hotkey)
        self.hotkey_input.textChanged.connect(self.save_settings)
        layout.addWidget(self.hotkey_input)

        # Configuração do Modelo do Whisper
        layout.addWidget(QLabel("Modelo do Whisper:"))
        self.whisper_model_combo = QComboBox()
        self.whisper_model_combo.addItems(["tiny", "base", "small", "medium", "large"])
        self.whisper_model_combo.setCurrentText(self.whisper_model)
        self.whisper_model_combo.currentTextChanged.connect(self.save_settings)
        layout.addWidget(self.whisper_model_combo)

        # Status
        self.status_label = QLabel("Pronto para gravar...")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def register_hotkey(self):
        if self.hotkey_registered:
            keyboard.remove_hotkey(self.hotkey_registered)

        hotkey_sequence = self.hotkey_input.text()
        try:
            keyboard.add_hotkey(hotkey_sequence, self.toggle_recording)
            self.hotkey_registered = hotkey_sequence
            self.status_label.setText(f"Atalho \'{hotkey_sequence}\' registrado.")
        except Exception as e:
            self.status_label.setText(f"Erro ao registrar atalho: {e}")
            self.hotkey_registered = None

    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.is_recording = True
        self.audio_data = []
        self.elapsed_time = 0
        self.record_button.setText("Parar Gravação")
        self.status_label.setText("Gravando: 00:00")
        self.recording_timer.start(1000) # Atualiza a cada segundo

        def callback(indata, frames, time, status):
            if status:
                print(status)
            self.audio_data.append(indata.copy())

        self.stream = sd.InputStream(samplerate=self.samplerate, channels=self.channels, callback=callback)
        self.stream.start()

    def stop_recording(self):
        self.is_recording = False
        self.recording_timer.stop()
        self.record_button.setText("Gravar Áudio")
        self.status_label.setText("Processando áudio...")

        self.stream.stop()
        self.stream.close()

        if self.audio_data:
            recorded_audio = np.concatenate(self.audio_data, axis=0)
            # Salvar em um arquivo temporário
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
                self.temp_audio_file = tmpfile.name
                sf.write(self.temp_audio_file, recorded_audio, self.samplerate)
            self.status_label.setText(f"Áudio salvo em: {self.temp_audio_file}. Transcrevendo...")
            self.transcribe_audio(self.temp_audio_file)
        else:
            self.status_label.setText("Nenhum áudio gravado.")

    def update_recording_status(self):
        self.elapsed_time += 1
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        self.status_label.setText(f"Gravando: {minutes:02d}:{seconds:02d}")

    def transcribe_audio(self, audio_path):
        model_name = self.whisper_model_combo.currentText()
        self.transcribe_thread = TranscribeThread(audio_path, model_name)
        self.transcribe_thread.transcription_finished.connect(self.on_transcription_finished)
        self.transcribe_thread.transcription_error.connect(self.on_transcription_error)
        self.transcribe_thread.start()

    def on_transcription_finished(self, text):
        pyperclip.copy(text)
        self.status_label.setText("Transcrição copiada para a área de transferência!")
        if self.temp_audio_file and os.path.exists(self.temp_audio_file):
            os.remove(self.temp_audio_file)
            self.temp_audio_file = None

    def on_transcription_error(self, error_message):
        self.status_label.setText(f"Erro na transcrição: {error_message}")
        if self.temp_audio_file and os.path.exists(self.temp_audio_file):
            os.remove(self.temp_audio_file)
            self.temp_audio_file = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AudioTranscriberApp()
    ex.show()
    sys.exit(app.exec())


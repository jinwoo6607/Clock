import sys
import time
from PyQt5 import QtWidgets, QtCore

class ClockApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.alarm_time = None
        self.timer_running = False

    def initUI(self):
        """UI 초기화 및 구성"""
        self.setWindowTitle("Ultimate Clock App")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF;")

        # 현재 시간 라벨
        self.time_label = QtWidgets.QLabel("", self)
        self.time_label.setStyleSheet("font-size: 100px;")
        self.time_label.setAlignment(QtCore.Qt.AlignCenter)

        # 알람 입력 필드
        self.alarm_input = QtWidgets.QLineEdit(self)
        self.alarm_input.setPlaceholderText("Set Alarm (HH:MM)")
        self.alarm_input.setStyleSheet("font-size: 36px; padding: 15px;")

        # 알람 설정 버튼
        self.set_alarm_button = QtWidgets.QPushButton("Set Alarm", self)
        self.set_alarm_button.clicked.connect(self.set_alarm)
        self.set_alarm_button.setStyleSheet("font-size: 24px; background-color: #61DAFB; border: none; padding: 15px;")

        # 타이머 라벨
        self.timer_label = QtWidgets.QLabel("Timer: 0", self)
        self.timer_label.setStyleSheet("font-size: 48px;")
        self.timer_label.setAlignment(QtCore.Qt.AlignCenter)

        # 타이머 버튼들
        self.start_timer_button = QtWidgets.QPushButton("Start Timer", self)
        self.start_timer_button.clicked.connect(self.start_timer)
        self.start_timer_button.setStyleSheet("font-size: 24px; background-color: #4DAF7C; border: none; padding: 15px;")

        self.stop_timer_button = QtWidgets.QPushButton("Stop Timer", self)
        self.stop_timer_button.clicked.connect(self.stop_timer)
        self.stop_timer_button.setStyleSheet("font-size: 24px; background-color: #FF6F61; border: none; padding: 15px;")

        self.reset_timer_button = QtWidgets.QPushButton("Reset Timer", self)
        self.reset_timer_button.clicked.connect(self.reset_timer)
        self.reset_timer_button.setStyleSheet("font-size: 24px; background-color: #FF6F61; border: none; padding: 15px;")

        # 레이아웃 설정
        self.setup_layout()

        # 타이머 업데이트
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.stopwatch_time = 0
        self.stopwatch_timer = QtCore.QTimer(self)
        self.stopwatch_timer.timeout.connect(self.update_timer)

    def setup_layout(self):
        """레이아웃 구성"""
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.time_label)
        layout.addWidget(self.alarm_input)
        layout.addWidget(self.set_alarm_button)
        layout.addWidget(self.timer_label)
        layout.addWidget(self.start_timer_button)
        layout.addWidget(self.stop_timer_button)
        layout.addWidget(self.reset_timer_button)

        layout.setSpacing(20)  # 위젯 간 간격
        layout.setAlignment(QtCore.Qt.AlignCenter)  # 중앙 정렬

        self.setLayout(layout)

    def update_time(self):
        """현재 시간 업데이트"""
        current_time = time.strftime("%H:%M:%S")
        self.time_label.setText(current_time)

        # 알람 확인
        if self.alarm_time and time.strftime("%H:%M") == self.alarm_time:
            QtWidgets.QMessageBox.information(self, "Alarm", "Time's up!")
            self.alarm_time = None  # 알람 리셋

    def set_alarm(self):
        """알람 설정"""
        alarm_time_str = self.alarm_input.text()
        if self.validate_alarm_time(alarm_time_str):
            self.alarm_time = alarm_time_str
            QtWidgets.QMessageBox.information(self, "Alarm Set", f"Alarm set for {alarm_time_str}.")
        else:
            QtWidgets.QMessageBox.warning(self, "Invalid Time", "Please enter a valid time in HH:MM format.")

    def validate_alarm_time(self, alarm_time_str):
        """알람 시간 유효성 검사"""
        try:
            time.strptime(alarm_time_str, "%H:%M")
            return True
        except ValueError:
            return False

    def start_timer(self):
        """타이머 시작"""
        if not self.timer_running:
            self.timer_running = True
            self.stopwatch_time = 0
            self.stopwatch_timer.start(1000)

    def update_timer(self):
        """타이머 업데이트"""
        if self.timer_running:
            self.stopwatch_time += 1
            self.timer_label.setText(f"Timer: {self.stopwatch_time} seconds")

    def stop_timer(self):
        """타이머 정지"""
        self.timer_running = False
        self.stopwatch_timer.stop()

    def reset_timer(self):
        """타이머 리셋"""
        self.timer_running = False
        self.stopwatch_timer.stop()
        self.stopwatch_time = 0
        self.timer_label.setText("Timer: 0 seconds")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    clock_app = ClockApp()
    clock_app.show()
    sys.exit(app.exec_())

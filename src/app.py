import sys

from PySide6.QtCore import QStandardPaths, Slot
from PySide6.QtGui import QAction, QFont, QIcon, QIntValidator, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QStyle,
    QToolBar,
    QWidget,
)

from listening_to_spike.osc_control import run


class OSCSetup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._ip = "0.0.0.0"
        self._port = "5000"

        # (textbox) selected data path
        ip_tb = QLineEdit()
        ip_tb.setText(self._ip)
        ip_tb.setMaxLength(15)
        ip_tb.setFont(QFont("Arial", 12))
        ip_tb.textChanged.connect(self.change_ip)
        ip_label = QLabel("IP: ")

        port_tb = QLineEdit()
        port_tb.setText(self._port)
        port_tb.setMaxLength(5)
        port_tb.setValidator(QIntValidator())
        port_tb.setFont(QFont("Arial", 12))
        port_tb.textChanged.connect(self.change_port)
        port_label = QLabel("Port: ")

        layout = QGridLayout()
        layout.addWidget(ip_label, 0, 0)
        layout.addWidget(ip_tb, 0, 1)
        layout.addWidget(port_label, 1, 0)
        layout.addWidget(port_tb, 1, 1)
        self.setLayout(layout)

    def change_ip(self, text):
        self._ip = text

    def change_port(self, text):
        self._port = text


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Private Configuration
        self._data_path: str = None

        self.osc_widget = OSCSetup()
        self.initializeUI()

        # Window Configuration
        self.setWindowTitle("Spike Player")

    def initializeUI(self):
        # Toolbar
        tool_bar = QToolBar()
        tool_bar.setMovable(False)
        self.addToolBar(tool_bar)
        style = self.style()

        # (button) Open
        file_menu = self.menuBar().addMenu("&File")
        icon = QIcon.fromTheme("document-open")
        open_action = QAction(
            icon,
            "&Open...",
            self,
            shortcut=QKeySequence.Open,
            triggered=self.open,
        )
        file_menu.addAction(open_action)
        tool_bar.addAction(open_action)

        # (button) Play
        play_menu = self.menuBar().addMenu("&Play")
        icon = QIcon.fromTheme(
            "media-playback-start.png", style.standardIcon(QStyle.SP_MediaPlay)
        )
        self._play_action = tool_bar.addAction(icon, "Play")
        self._play_action.triggered.connect(self.play)
        play_menu.addAction(self._play_action)

        # (button) Stop
        icon = QIcon.fromTheme(
            "media-playback-stop.png", style.standardIcon(QStyle.SP_MediaStop)
        )
        self._stop_action = tool_bar.addAction(icon, "Stop")
        self._stop_action.triggered.connect(self._ensure_stopped)
        play_menu.addAction(self._stop_action)

        # (button) Exit
        icon = QIcon.fromTheme("application-exit")
        exit_action = QAction(
            icon, "E&xit", self, shortcut="Ctrl+Q", triggered=self.close
        )
        file_menu.addAction(exit_action)

        # (bar) About
        about_menu = self.menuBar().addMenu("&About")
        about_qt_act = QAction(
            "About &Qt", self, triggered=self.about
        )  # qApp.aboutQt)
        about_menu.addAction(about_qt_act)

        # (textbox) Datapath
        label = QLabel("Data Path: ")
        textbox = QLineEdit()
        textbox.setDisabled(True)
        textbox.setReadOnly(True)
        tool_bar.addWidget(label)
        tool_bar.addWidget(textbox)
        self.pathTextbox = textbox

        # External
        self.setCentralWidget(self.osc_widget)

    def closeEvent(self, event):
        event.accept()

    @Slot()
    def about(self):
        self._ensure_stopped()
        msgBox = QMessageBox()
        msgBox.setText(
            """
        Send spike signal through OSC protocol for the project Music-In-Vitro.
        """
        )
        if msgBox.exec() == QDialog.Accepted:
            pass

    @Slot()
    def open(self):
        self._ensure_stopped()
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.Directory)
        file_dialog.setOption(QFileDialog.ShowDirsOnly)

        # Set default starting location to be home directory
        default_location = QStandardPaths.writableLocation(
            QStandardPaths.HomeLocation
        )
        file_dialog.setDirectory(default_location)

        if file_dialog.exec() == QDialog.Accepted:
            url = file_dialog.selectedFiles()[0]
            self._data_path = url
            self.pathTextbox.setText(url)

    @Slot()
    def play(self):
        run(self._data_path)

    @Slot()
    def _ensure_stopped(self):
        print("stopped")
        pass

    @Slot()
    def _player_error(self, error, error_string):
        print(error_string, file=sys.stderr)
        self.show_status_message(error_string)

    def show_status_message(self, message):
        self.statusBar().showMessage(message, 5000)


def launch():
    app = QApplication(sys.argv)
    main_win = MainWindow()
    # available_geometry = main_win.screen().availableGeometry()
    main_win.setFixedWidth(713)
    main_win.setFixedHeight(120)
    main_win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    launch()

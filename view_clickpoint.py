import sys
import ctypes
from ctypes import wintypes

from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QPlainTextEdit
)
from PyQt5.QtCore import pyqtSignal, QObject

from pynput import mouse

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32


# ---------- 进程/窗口查找 ----------
def get_pids_by_name(process_name):
    TH32CS_SNAPPROCESS = 0x00000002

    class PROCESSENTRY32(ctypes.Structure):
        _fields_ = [
            ("dwSize", wintypes.DWORD),
            ("cntUsage", wintypes.DWORD),
            ("th32ProcessID", wintypes.DWORD),
            ("th32DefaultHeapID", ctypes.POINTER(ctypes.c_ulong)),
            ("th32ModuleID", wintypes.DWORD),
            ("cntThreads", wintypes.DWORD),
            ("th32ParentProcessID", wintypes.DWORD),
            ("pcPriClassBase", ctypes.c_long),
            ("dwFlags", wintypes.DWORD),
            ("szExeFile", ctypes.c_char * 260),
        ]

    snap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if snap == -1:
        return []

    entry = PROCESSENTRY32()
    entry.dwSize = ctypes.sizeof(PROCESSENTRY32)
    pids = []

    if kernel32.Process32First(snap, ctypes.byref(entry)):
        while True:
            name = entry.szExeFile.decode("utf-8", errors="ignore")
            if name.lower() == process_name.lower():
                pids.append(entry.th32ProcessID)
            if not kernel32.Process32Next(snap, ctypes.byref(entry)):
                break

    kernel32.CloseHandle(snap)
    return pids


def find_window_by_pid(pid):
    hwnds = []
    WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

    def callback(hwnd, lparam):
        wpid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(wpid))
        if wpid.value == pid and user32.IsWindowVisible(hwnd):
            hwnds.append(hwnd)
        return True

    user32.EnumWindows(WNDENUMPROC(callback), 0)
    return hwnds


# ---------- 信号辅助类（跨线程更新 UI） ----------
class SignalHelper(QObject):
    clicked = pyqtSignal(int, int)


# ---------- 主窗口 ----------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("鼠标坐标检测")
        self.resize(500, 400)

        self.hwnd = None
        self.listener = None

        self.btn = QPushButton("获取句柄")
        self.btn.clicked.connect(self.get_hwnd)

        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.btn)
        layout.addWidget(self.text)
        self.setLayout(layout)

        # 信号：从鼠标监听线程发到 UI 线程
        self.sig = SignalHelper()
        self.sig.clicked.connect(self.on_clicked)

    def get_hwnd(self):
        pids = get_pids_by_name("Probably Stolen.exe")
        if not pids:
            self.hwnd = None
            self.btn.setStyleSheet("background-color: red; color: white;")
            self.text.appendPlainText("未找到 Probably Stolen.exe 进程")
            return

        for pid in pids:
            hwnds = find_window_by_pid(pid)
            if hwnds:
                self.hwnd = hwnds[0]
                self.btn.setStyleSheet("background-color: green; color: white;")
                self.text.appendPlainText(f"已获取句柄: {self.hwnd} (PID={pid})")
                self.start_listener()
                return

        self.hwnd = None
        self.btn.setStyleSheet("background-color: red; color: white;")
        self.text.appendPlainText("找到进程但未找到可见窗口")

    def start_listener(self):
        if self.listener is not None:
            return
        self.listener = mouse.Listener(on_click=self.on_mouse_click)
        self.listener.daemon = True
        self.listener.start()

    def on_mouse_click(self, x, y, button, pressed):
        # 这个回调运行在监听线程，不能直接操作 UI，用信号转发
        if button == mouse.Button.left and pressed:
            self.sig.clicked.emit(x, y)

    def on_clicked(self, x, y):
        if not self.hwnd:
            return
        # 屏幕坐标 -> 窗口客户区坐标
        point = wintypes.POINT(x, y)
        user32.ScreenToClient(self.hwnd, ctypes.byref(point))
        self.text.appendPlainText(f"屏幕({x}, {y})  ->  窗口({point.x}, {point.y})")

    def closeEvent(self, event):
        if self.listener is not None:
            self.listener.stop()
            self.listener = None
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
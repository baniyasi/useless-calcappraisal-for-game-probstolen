import sys
import os,time,json
import shutil
import ctypes
from ctypes import wintypes
from pynput import keyboard

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox,
    QScrollArea, QFrame
)
from PyQt5.QtCore import QTimer,pyqtSignal, QObject,Qt

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
COUNTER_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "counters.json")

# ---------- Windows API 工具函数 ----------
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

    snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if snapshot == -1:
        return []

    entry = PROCESSENTRY32()
    entry.dwSize = ctypes.sizeof(PROCESSENTRY32)
    pids = []

    if kernel32.Process32First(snapshot, ctypes.byref(entry)):
        while True:
            name = entry.szExeFile.decode("utf-8", errors="ignore")
            if name.lower() == process_name.lower():
                pids.append(entry.th32ProcessID)
            if not kernel32.Process32Next(snapshot, ctypes.byref(entry)):
                break

    kernel32.CloseHandle(snapshot)
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


# ---------- 计数器 ----------
class Counter(QFrame):
    def __init__(self, index=1):
        super().__init__()
        self.value = 0
        self.setFrameShape(QFrame.StyledPanel)

        layout = QHBoxLayout(self)
        # 序号 label
        self.index_label = QLabel(str(index))
        self.index_label.setFixedWidth(30)
        self.index_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.index_label)
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("名称")
        self.name_edit.setFixedWidth(120)
        layout.addWidget(self.name_edit)

        self.btn_plus = QPushButton("+")
        self.btn_plus.setFixedWidth(40)
        self.btn_plus.clicked.connect(self.plus)
        layout.addWidget(self.btn_plus)

        self.value_label = QLabel("0")
        self.value_label.setFixedWidth(60)
        layout.addWidget(self.value_label)

        btn_minus = QPushButton("-")
        btn_minus.setFixedWidth(40)
        btn_minus.clicked.connect(self.minus)
        layout.addWidget(btn_minus)

        btn_reset = QPushButton("清零")
        btn_reset.setFixedWidth(60)
        btn_reset.clicked.connect(self.reset)
        layout.addWidget(btn_reset)

        layout.addStretch()
    def flash_plus(self, ms=2000):
        """加号按钮变绿 ms 毫秒后恢复"""
        self.btn_plus.setStyleSheet("background-color: green; color: white;")
        QTimer.singleShot(ms, lambda: self.btn_plus.setStyleSheet(""))
    
    def set_index(self, i):
        self.index_label.setText(str(i))
    def plus(self):
        self.value += 1
        self.value_label.setText(str(self.value))

    def minus(self):
        self.value -= 1
        self.value_label.setText(str(self.value))

    def reset(self):
        self.value = 0
        self.value_label.setText("0")
    def get_name(self):
        return self.name_edit.text()

    def set_name(self, name):
        self.name_edit.setText(name)

    def get_value(self):
        return self.value

    def set_value(self, v):
        self.value = v
        self.value_label.setText(str(v))

class CounterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("计数器")
        self.resize(400, 400)

        self.file_path = COUNTER_FILE

        layout = QVBoxLayout(self)

        # 按钮行
        btn_row = QHBoxLayout()

        btn_add = QPushButton("添加计数器")
        btn_add.clicked.connect(self.add_counter)
        btn_row.addWidget(btn_add)

        btn_clear = QPushButton("清空")
        btn_clear.clicked.connect(self.clear_all)
        btn_row.addWidget(btn_clear)

        btn_save = QPushButton("保存")
        btn_save.clicked.connect(self.save)
        btn_row.addWidget(btn_save)

        layout.addLayout(btn_row)

        # 滚动区域
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.addStretch()
        self.scroll.setWidget(self.container)
        layout.addWidget(self.scroll)
    def reindex(self):
        """按顺序给所有 Counter 重新编号，从 1 开始"""
        n = 0
        for i in range(self.container_layout.count()):
            w = self.container_layout.itemAt(i).widget()
            if isinstance(w, Counter):
                n += 1
                w.set_index(n)
    def add_counter(self):
        counter = Counter()
        self.container_layout.insertWidget(self.container_layout.count() - 1, counter)
        self.reindex()
    def clear_all(self):
        """删除容器里所有 Counter，保留最后的 stretch"""
        for i in reversed(range(self.container_layout.count())):
            item = self.container_layout.itemAt(i)
            w = item.widget()
            if isinstance(w, Counter):
                self.container_layout.takeAt(i)
                w.deleteLater()
        self.reindex()

    def save(self):
        """保存所有计数器的名称和值到 JSON 文件"""
        data = []
        for i in range(self.container_layout.count()):
            w = self.container_layout.itemAt(i).widget()
            if isinstance(w, Counter):
                data.append({"name": w.get_name(), "value": w.get_value()})
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存失败：\n{e}")

    def load(self):
        """从 JSON 文件还原所有计数器"""
        self.clear_all()
        if not os.path.isfile(self.file_path):
            return
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return
        for item in data:
            c = Counter()
            c.set_name(item.get("name", ""))
            c.set_value(item.get("value", 0))
            self.container_layout.insertWidget(self.container_layout.count() - 1, c)
        self.reindex()
    def increment_by_index(self, index):
        """把第 index 个 Counter 加一（index 从 1 开始）"""
        n = 0
        for i in range(self.container_layout.count()):
            w = self.container_layout.itemAt(i).widget()
            if isinstance(w, Counter):
                n += 1
                if n == index:
                    w.plus()
                    w.flash_plus()   # 加完再闪
                    return

class SignalHelper(QObject):
    hotkey = pyqtSignal()
    digit = pyqtSignal(int)
# ---------- 主窗口 ----------
class BackupRestore(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("存档恢复工具")
        self.resize(600, 280)
        self.counter_window = None
        self.hwnd = None

        self.path_edit = QLineEdit(
            rf"C:\Users\{os.getlogin()}\AppData\LocalLow\Questing Goose Studio\Probably Stolen"
        )
        self.backup_edit = QLineEdit("save_13bk.es3")
        self.target_edit = QLineEdit("save_13.es3")

        layout = QVBoxLayout()

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("路径："))
        row1.addWidget(self.path_edit)
        layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("备份文件名："))
        row2.addWidget(self.backup_edit)
        layout.addLayout(row2)

        row3 = QHBoxLayout()
        row3.addWidget(QLabel("被替换文件名："))
        row3.addWidget(self.target_edit)
        layout.addLayout(row3)

        self.btn = QPushButton("执行恢复")
        self.btn.clicked.connect(self.run)
        layout.addWidget(self.btn)

        self.btn_counter = QPushButton("开始统计")
        self.btn_counter.clicked.connect(self.open_counter)
        layout.addWidget(self.btn_counter)

        # 获取句柄按钮
        self.btn_hwnd = QPushButton("获取句柄")
        self.btn_hwnd.clicked.connect(self.get_hwnd)
        layout.addWidget(self.btn_hwnd)

        self.setLayout(layout)

        # 信号：从键盘监听线程发到 UI 线程
        self.sig_hotkey = SignalHelper()
        self.sig_hotkey.hotkey.connect(self.run)
        self.sig_hotkey.digit.connect(self._on_digit)

        # 启动键盘监听
        self.kb_listener = keyboard.Listener(on_press=self._on_key_press)
        self.kb_listener.daemon = True
        self.kb_listener.start()
    def _on_key_press(self, key):
        try:
            c = getattr(key, "char", None)
            if c == "q":
                self.sig_hotkey.hotkey.emit()
            elif c and c.isdigit() and "1" <= c <= "9":
                self.sig_hotkey.digit.emit(int(c))
        except Exception:
            pass
    def _on_digit(self, idx):
        # 只在计数器窗口存在且可见时响应
        if self.counter_window is not None and self.counter_window.isVisible():
            self.counter_window.increment_by_index(idx)
    def closeEvent(self, event):
        if getattr(self, "kb_listener", None) is not None:
            self.kb_listener.stop()
            self.kb_listener = None
        super().closeEvent(event)    
    # ----- 执行恢复 -----
    def run(self):
        folder = self.path_edit.text().strip()
        backup_name = self.backup_edit.text().strip()
        target_name = self.target_edit.text().strip()

        backup_path = os.path.join(folder, backup_name)
        target_path = os.path.join(folder, target_name)

        if not os.path.isdir(folder):
            QMessageBox.critical(self, "错误", f"路径不存在：\n{folder}")
            return

        if not os.path.isfile(backup_path):
            QMessageBox.critical(self, "错误", f"备份文件不存在：\n{backup_path}")
            return

        try:
            if os.path.isfile(target_path):
                os.remove(target_path)
            shutil.copy2(backup_path, target_path)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"操作失败：\n{e}")
            return

        # QMessageBox.information(
        #     self, "完成",
        #     f"已恢复：\n{target_name}\n← {backup_name}"
        # )

        # 如果已经获取到 hwnd，执行焦点 + ESC + 点击序列
        if self.hwnd: self.run_sequence(self.get_focus_sequence())
# ---------- 序列定义（只改这里） ----------

    def get_focus_sequence(self):
        """返回 [(延迟秒, 函数), ...]，延迟表示这一步之前等待的时间"""
        return [
            # (0.5, lambda: self.focus_window()),
            (0.5, lambda: self.right_click_at(392, 701)),
            (0.5, lambda: self.send_key(0x1B)),
            (0.5, lambda: self.send_key(0x1B)),
            (0.5, lambda: self.send_key(0x1B)),
            (0.5, lambda: self.click_at(823, 491)),
            (0.5, lambda: self.click_at(1013, 559)),
            (0.5, lambda: self.click_at(994, 234)),
            (5, lambda: self.click_at(1357, 77)),
            (0.5, lambda: self.click_at(1121, 248)),
            (1, lambda: self.double_click_at(760, 653)),
            (1, lambda: self.drag(614, 795, 590, 773)),
            (0.5, lambda: self.drag(590, 773, 392, 701)),
            (0.5, lambda: self.click_at(1121, 248)),
            (0.5, lambda: self.click_at(721, 524)),
            (0.5, lambda: self.click_at(1449, 762)),
            (0.5, lambda: self.click_at(796, 678)),
            (3, lambda: self.click_at(1357, 77)),
            (0.5, lambda: self.double_click_at(392, 701)),          
        ]
    # ---------- 通用动作 ----------

    def focus_window(self):
        SW_RESTORE = 9
        user32.ShowWindow(self.hwnd, SW_RESTORE)
        user32.SetForegroundWindow(self.hwnd)


    def send_key(self, vk):
        KEYEVENTF_KEYUP = 0x0002
        user32.keybd_event(vk, 0, 0, 0)
        user32.keybd_event(vk, 0, KEYEVENTF_KEYUP, 0)


    def click_at(self, x, y):
        point = wintypes.POINT(x, y)
        user32.ClientToScreen(self.hwnd, ctypes.byref(point))
        user32.SetCursorPos(point.x, point.y)
        user32.mouse_event(0x0002, 0, 0, 0, 0)   # 左键按下
        user32.mouse_event(0x0004, 0, 0, 0, 0)   # 左键抬起
    def right_click_at(self, x, y):
        point = wintypes.POINT(x, y)
        user32.ClientToScreen(self.hwnd, ctypes.byref(point))
        user32.SetCursorPos(point.x, point.y)
        user32.mouse_event(0x0008, 0, 0, 0, 0)   # 右键按下
        user32.mouse_event(0x0010, 0, 0, 0, 0)   # 右键抬起

    def double_click_at(self, x, y, interval=0.05):
        point = wintypes.POINT(x, y)
        user32.ClientToScreen(self.hwnd, ctypes.byref(point))
        user32.SetCursorPos(point.x, point.y)
        for _ in range(2):
            user32.mouse_event(0x0002, 0, 0, 0, 0)   # 左键按下
            user32.mouse_event(0x0004, 0, 0, 0, 0)   # 左键抬起
            time.sleep(interval)


    def drag(self, x1, y1, x2, y2, duration=0.5, steps=20):
        # 起点：客户区坐标 -> 屏幕坐标
        p1 = wintypes.POINT(x1, y1)
        user32.ClientToScreen(self.hwnd, ctypes.byref(p1))
        user32.SetCursorPos(p1.x, p1.y)
        user32.mouse_event(0x0002, 0, 0, 0, 0)   # 左键按下

        # 终点：客户区坐标 -> 屏幕坐标
        p2 = wintypes.POINT(x2, y2)
        user32.ClientToScreen(self.hwnd, ctypes.byref(p2))

        # 分步插值移动
        for i in range(1, steps + 1):
            xi = p1.x + (p2.x - p1.x) * i // steps
            yi = p1.y + (p2.y - p1.y) * i // steps
            user32.SetCursorPos(xi, yi)
            time.sleep(duration / steps)

        user32.mouse_event(0x0004, 0, 0, 0, 0)   # 左键抬起
    # ---------- 统一执行器（不用改） ----------

    def run_sequence(self, steps):
        if not steps:
            return
        delay, func = steps[0]
        QTimer.singleShot(int(delay * 1000), lambda: self._step(steps))

    def _step(self, steps):
        delay, func = steps[0]
        func()
        self.run_sequence(steps[1:])

    # ----- 获取句柄 -----
    def get_hwnd(self):
        pids = get_pids_by_name("Probably Stolen.exe")
        if not pids:
            self.hwnd = None
            self.btn_hwnd.setStyleSheet("background-color: red; color: white;")
            return

        for pid in pids:
            hwnds = find_window_by_pid(pid)
            if hwnds:
                self.hwnd = hwnds[0]
                self.btn_hwnd.setStyleSheet("background-color: green; color: white;")
                return

        self.hwnd = None
        self.btn_hwnd.setStyleSheet("background-color: red; color: white;")

    # ----- 开始统计 -----
    def open_counter(self):
        if self.counter_window is None:
            self.counter_window = CounterWindow()
            self.counter_window.load()
        self.counter_window.show()
        self.counter_window.raise_()
        self.counter_window.activateWindow()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = BackupRestore()
    w.show()
    sys.exit(app.exec_())
import sys
import os
import datetime
import regex as re
from pathlib import Path
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QMenu
from PyQt6.QtGui import QContextMenuEvent
from concurrent.futures import ThreadPoolExecutor

# 轉為exe 使用絕對路徑 解析img位置
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(520, 320)
        Form.setMinimumSize(QtCore.QSize(520, 320))
        Form.setMaximumSize(QtCore.QSize(520, 320))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(get_resource_path('img/LOGO.ico')), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet("background-color: #2e3440; color: #eceff4; font-family: 'Microsoft JhengHei UI'; font-size: 12pt;")

        # 列表選單樣式
        self.listWidget = QtWidgets.QListWidget(parent=Form)
        self.listWidget.setGeometry(QtCore.QRect(10, 20, 500, 200))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setStyleSheet("QScrollBar:vertical { border: none; background-color: #4c566a; width: 12px; margin: 0; } QScrollBar::handle:vertical { background-color: #88c0d0; min-height: 20px; border-radius: 5px; } QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { border: none; background: none; height: 0; } QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; } QScrollBar:horizontal { border: none; background-color: #4c566a; height: 12px; margin: 0; } QScrollBar::handle:horizontal { background-color: #88c0d0; min-width: 20px; border-radius: 5px; } QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { border: none; background: none; width: 0; } QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: none; }")

        # 進度條樣式
        self.progressBar = QtWidgets.QProgressBar(parent=Form)
        self.progressBar.setGeometry(QtCore.QRect(10, 230, 500, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.Direction.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setStyleSheet(
            "QProgressBar { border: 2px solid #4c566a; border-radius: 5px; text-align: center; }"
            "QProgressBar::chunk { background-color: #88c0d0; width: 20px; }")

        # 按鈕樣式
        button_style = ("QPushButton { background-color: #3b4252; border-radius: 8px; color: #eceff4; font-size: 16pt; }"
                        "QPushButton:hover { background-color: #5e81ac; }")

        self.pushButton = QtWidgets.QPushButton(parent=Form)
        self.pushButton.setGeometry(QtCore.QRect(10, 265, 70, 41))
        self.pushButton.setFont(QtGui.QFont("Microsoft JhengHei UI", 16))
        self.pushButton.setStyleSheet(button_style)
        self.pushButton.setText("📁")
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(parent=Form)
        self.pushButton_2.setGeometry(QtCore.QRect(100, 265, 70, 41))
        self.pushButton_2.setFont(QtGui.QFont("Microsoft JhengHei UI", 16))
        self.pushButton_2.setStyleSheet(button_style)
        self.pushButton_2.setText("❌")
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(parent=Form)
        self.pushButton_3.setGeometry(QtCore.QRect(190, 265, 320, 41))
        self.pushButton_3.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Weight.Bold))
        self.pushButton_3.setStyleSheet(button_style)
        self.pushButton_3.setText("執  行")
        self.pushButton_3.setObjectName("pushButton_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle("Remove Annotation")


class FileProcessor(QtCore.QObject):
    progressUpdated = QtCore.pyqtSignal(int)
    processingFinished = QtCore.pyqtSignal(int, int, str)  # 成功, 失敗, log

    def __init__(self):
        super().__init__()

    def remove_comments(self, content, pattern):
        return re.sub(pattern, '', content)

    def remove_blank_lines(self, content):
        return re.sub(r'^\s*\n', '', content, flags=re.MULTILINE)

    def process_file(self, file_path, log_file):
        try:
            file_extension = os.path.splitext(file_path)[1]
            if file_extension == '.py':
                comment_pattern = re.compile(r'\/\*[\s\S]*?\*\/|(?<!http:|https:)\/\/[^\n]*(?![\s\S]*http:|[\s\S]*https:)|<!--[\s\S]*?-->|(?<!http:|https:)\/\/[^\n]*|\#.*')
            else:
                comment_pattern = re.compile(r'\/\*[\s\S]*?\*\/|(?<!http:|https:)\/\/[^\n]*(?![\s\S]*http:|[\s\S]*https:)|<!--[\s\S]*?-->|(?<!http:|https:)\/\/[^\n]*')

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            content = self.remove_comments(content, comment_pattern)
            cleaned_content = self.remove_blank_lines(content)

            new_file_path = os.path.splitext(file_path)[0] + '_min' + os.path.splitext(file_path)[1]
            with open(new_file_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_content)

            return True
        except Exception as e:
            # 紀錄當前日期和時間
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 如果處理失敗，記錄到日誌文件
            with open(log_file, 'a', encoding='utf-8') as log:
                log.write(f"[{current_time}]\n檔案: {file_path}\n錯誤: {str(e)}\n\n")
            return False

    def process_files(self, file_paths):
        success_count = 0
        fail_count = 0
        log_file = "Error_Log.txt"

        # 檢查是否有選擇檔案
        if file_paths:

            for i, file_path in enumerate(file_paths):
                if self.process_file(file_path, log_file):
                    success_count += 1
                else:
                    fail_count += 1

                progress = int((i + 1) / len(file_paths) * 100)
                self.progressUpdated.emit(progress)

        self.processingFinished.emit(success_count, fail_count, log_file)


class MainWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.open_files)
        self.pushButton_2.clicked.connect(self.remove_selected_files)
        self.pushButton_3.clicked.connect(self.process_files)
        self.listWidget.setAcceptDrops(True)
        self.listWidget.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.DropOnly)

        self.listWidget.installEventFilter(self)  # 啟用事件過濾器

        self.file_processor = FileProcessor()
        self.file_processor.progressUpdated.connect(self.update_progress_bar)
        self.file_processor.processingFinished.connect(self.show_summary)

        # 文件處理線程
        self.thread_pool = ThreadPoolExecutor()

        # 右鍵菜單
        self.context_menu = QMenu(self)
        self.context_menu.addAction("開啟資料夾", self.open_folder)
        self.context_menu.addAction("刪除選擇", self.remove_selected_files)
        self.context_menu.addAction("清空全部", self.clear_all_files)
        self.context_menu.setStyleSheet(
            "QMenu { background-color: #3b4252; border: 1px solid #4c566a; }"
            "QMenu::item { padding: 5px 20px; }"
            "QMenu::item:selected { background-color: #5e81ac; }"
        )

    # 鍵盤觸發刪除
    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key.Key_Delete:
            self.remove_selected_files()
        super().keyPressEvent(event)

    # 覆蓋事件過濾器函數
    def eventFilter(self, source, event):
        if source == self.listWidget:
            if event.type() == QtCore.QEvent.Type.DragEnter:
                if event.mimeData().hasUrls():
                    event.acceptProposedAction()
                    return True
            elif event.type() == QtCore.QEvent.Type.Drop:
                for url in event.mimeData().urls():
                    file_path = url.toLocalFile()
                    if not self.is_duplicate(file_path):
                        self.listWidget.addItem(file_path)
                return True
        return super().eventFilter(source, event)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if not self.is_duplicate(file_path):
                self.listWidget.addItem(file_path)

    def open_files(self):
        file_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "選擇文件", "", "所有文件 (*)")
        for file_path in file_paths:
            if not self.is_duplicate(file_path):
                self.listWidget.addItem(file_path)

    def is_duplicate(self, file_path):
        for i in range(self.listWidget.count()):
            if self.listWidget.item(i).text() == file_path:
                return True
        return False

    def remove_selected_files(self):
        selected_items = self.listWidget.selectedItems()
        for item in selected_items:
            self.listWidget.takeItem(self.listWidget.row(item))

    def clear_all_files(self):
        self.listWidget.clear()

    def contextMenuEvent(self, event: QContextMenuEvent):
        self.context_menu.exec(event.globalPos())

    def update_progress_bar(self, value):
        self.progressBar.setValue(value)

    def show_summary(self, success_count, fail_count, log_file):
        self.progressBar.setValue(100)
        if fail_count > 0:
            message = f"完成: {success_count} 個，失敗: {fail_count} 個\n失敗的檔案已記錄在 {log_file}"
        else:
            message = f"完成: {success_count} 個，失敗: {fail_count} 個"
        QMessageBox.information(self, "處理結果", message)

    def process_files(self):
        if self.listWidget.count() == 0:
            QMessageBox.warning(self, "警告", "請選擇至少一個文件進行處理")
            return

        file_paths = [self.listWidget.item(i).text() for i in range(self.listWidget.count())]
        self.progressBar.setValue(0)

        # 單線程處裡
        self.thread_pool.submit(self.file_processor.process_files, file_paths)

    def open_folder(self):
        selected_items = self.listWidget.selectedItems()
        if selected_items:
            for item in selected_items:
                file_path = item.text()
                folder_path = os.path.dirname(file_path)
                folder_path = Path(folder_path)  # 使用 pathlib 處理路徑

                if not folder_path.exists() or not folder_path.is_dir():
                    QMessageBox.warning(self, "警告", f"資料夾不存在: {folder_path}")
                    continue

                try:
                    os.startfile(str(folder_path))
                except Exception as e:
                    # 顯示其他錯誤訊息
                    QMessageBox.critical(self, "錯誤", f"發生錯誤:\n{e}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())

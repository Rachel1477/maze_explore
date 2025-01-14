from PyQt5.QtWidgets import QTabWidget, QMainWindow, QDesktopWidget, QApplication
import sys
from ui_basic import Ui_basic
from ui_userDefine import Ui_userDefine

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(2500, 1500)
        self.center()
        self.setWindowTitle('Exploring a Maze')

        # 设置主窗口背景为淡蓝到淡米黄色渐变
        self.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #87CEEB, stop:1 #F5F5DC);
        """)

        # 创建 QTabWidget
        self.tabW = QTabWidget(parent=self)
        ui_userD = Ui_userDefine()
        ui_basic = Ui_basic()

        # 添加标签页
        self.tabW.addTab(ui_basic, "已有迷宫")
        self.tabW.addTab(ui_userD, "用户自定义")
        self.tabW.resize(2400, 1400)

        # 设置 QTabWidget 的样式
        self.tabW.setStyleSheet("""
            QTabWidget::pane {  /* 内容区域 */
                border: 1px solid #ccc;
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.9);  /* 90% 透明度 */
            }
            QTabBar::tab {  /* 标签页 */
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #E6E6FA, stop:1 #FFFACD);  /* 淡紫色到淡黄色渐变 */
                color: black;  /* 文字颜色为黑色 */
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                margin: 5px;
                font-weight: bold;  /* 加粗字体 */
            }
            QTabBar::tab:selected {  /* 选中的标签页 */
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ADD8E6, stop:1 #FFE4B5);  /* 淡蓝色到淡米黄色渐变 */
                color: white;  /* 文字颜色为白色 */
            }
            QLabel, QPushButton, QLineEdit, QTextEdit {  /* 其他控件 */
                color: black;  /* 文字颜色为黑色 */
                font-weight: bold;  /* 加粗字体 */
            }
        """)

        # 初始化 UI
        ui_basic.initUI()
        ui_userD.initUI()

        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

if __name__ == "__main__":
    app = QApplication([])
    ui = MainWindow()
    sys.exit(app.exec_())
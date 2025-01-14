from PyQt5.QtWidgets import QLabel, QComboBox, QPushButton, QMessageBox, QWidget, QGroupBox, QGridLayout,QTextEdit
from PyQt5.QtCore import QBasicTimer, QRect,QPoint,QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import (
    QTabWidget, QMainWindow, QDesktopWidget, QApplication, QPushButton, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QComboBox, QGraphicsRotation, QGraphicsEffect, QGraphicsDropShadowEffect
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, QPointF
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QStyle
class HoverButton(QPushButton):
    """自定义按钮，支持悬停时的偏移和投影效果"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(150, 50)  # 设置按钮大小
        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # 添加投影效果
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(10)  # 模糊半径
        self.shadow.setColor(QColor("#888888"))  # 使用 QColor 设置投影颜色
        self.shadow.setOffset(0, 0)  # 初始偏移量
        self.setGraphicsEffect(self.shadow)

        # 初始化动画
        self.animation = QPropertyAnimation(self.shadow, b"offset")
        self.animation.setDuration(200)  # 动画时长
        self.animation.setEasingCurve(QEasingCurve.OutQuad)  # 缓动曲线

    def enterEvent(self, event):
        """鼠标悬停时触发"""
        self.animation.setStartValue(QPoint(0, 0))  # 起始值
        self.animation.setEndValue(QPoint(5, 5))  # 结束值（偏移量）
        self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标离开时触发"""
        self.animation.setStartValue(QPoint(5, 5))  # 起始值
        self.animation.setEndValue(QPoint(0, 0))  # 结束值
        self.animation.start()
        super().leaveEvent(event)

class AnimatedComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # 设置默认样式
        self.setStyleSheet("""
            QComboBox {
                background-color: #F08080;  /* 背景颜色为品红色 */
                color: black;              /* 文字颜色为黑色 */
                border: 2px solid #555;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;         /* 字体加粗以增强锐度 */
            }
            QComboBox:hover {
                background-color: #ff77ff; /* 悬停时背景颜色稍浅 */
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #555;
                border-left-style: solid;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 10px;
                height: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: magenta; /* 下拉列表背景颜色 */
                color: black;              /* 下拉列表文字颜色 */
                selection-background-color: #ff77ff; /* 选中项背景颜色 */
            }
        """)

        # 添加锐度效果（阴影）
        self.shadow_effect = QGraphicsDropShadowEffect(self)
        self.shadow_effect.setBlurRadius(5)       # 阴影模糊半径
        self.shadow_effect.setColor(QColor(0, 0, 0, 150))  # 阴影颜色（黑色，半透明）
        self.shadow_effect.setOffset(3, 3)        # 阴影偏移量
        self.setGraphicsEffect(self.shadow_effect)

        # 初始化动画
        self.initAnimations()

    def initAnimations(self):
        # 倾斜动画
        self.tilt_animation = QPropertyAnimation(self, b"geometry")
        self.tilt_animation.setDuration(300)  # 动画持续时间
        self.tilt_animation.setEasingCurve(QEasingCurve.OutQuad)  # 缓动曲线

    def showPopup(self):
        # 显示下拉列表时触发动画
        start_rect = self.geometry()
        end_rect = QRect(
            start_rect.x() - 10,  # 向左偏移 10 像素
            start_rect.y(),
            start_rect.width(),
            start_rect.height()
        )
        self.tilt_animation.setStartValue(start_rect)
        self.tilt_animation.setEndValue(end_rect)
        self.tilt_animation.start()
        super().showPopup()

    def hidePopup(self):
        # 隐藏下拉列表时触发动画
        start_rect = self.geometry()
        end_rect = QRect(
            start_rect.x() + 10,  # 恢复原始位置
            start_rect.y(),
            start_rect.width(),
            start_rect.height()
        )
        self.tilt_animation.setStartValue(start_rect)
        self.tilt_animation.setEndValue(end_rect)
        self.tilt_animation.start()
        super().hidePopup()
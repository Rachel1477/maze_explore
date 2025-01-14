from PyQt5.QtWidgets import QLabel, QComboBox, QPushButton, QMessageBox, QWidget, QGroupBox, QGridLayout,QTextEdit
from PyQt5.QtCore import QBasicTimer, QRect,QPoint,QPropertyAnimation, QEasingCurve
from style import HoverButton,AnimatedComboBox
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFont
import numpy as np
from maze_map import Mazes
from maze import Maze
from train_qtable import QTableModel
import time
from BFS import bfs
from Dijkstra import dijkstra
from draw_ui import Draw_ui

class Ui_basic(QWidget):
    def __init__(self):
        super().__init__()
        self.model = None
        self.algorithm_choice =0
    def initUI(self):

        self.resize(2400, 1300)
        self.pic_list=['maze7_1', 'maze7_2', 'maze7_3', 'maze10_1', 'maze10_2', 'maze10_3' ]
        self.timer = QBasicTimer()

        widget1 = QWidget(parent=self)
        widget1.setGeometry(QRect(30, 50, 1400, 800))
        table_area = QGroupBox(parent=widget1) #图形显示区域
        table_area.setGeometry(QRect(widget1.x(), widget1.y(), widget1.width(), widget1.height()))
        self.Plot = Draw_ui(width=3, height=3, dpi=100)
        gridlayout1 = QGridLayout(table_area)  # 继承容器groupBox
        gridlayout1.addWidget(self.Plot, 0, 1)
        pic_choose_label = QLabel(self)
        pic_choose_label.move(table_area.x()+table_area.width()+300, table_area.y()+200)
        pic_choose_label.setText("选择迷宫：")

        self.text_edit = QTextEdit(self)
        self.text_edit.setPlainText("no path in this maze")
        self.text_edit.move(1700, 1000)  # 设置位置 (x, y)
        self.text_edit.resize(550, 55)  # 设置大小 (width, height)
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("color: red; font-size: 50px;")
        self.text_edit.hide()

        self.white_canvas = QWidget(self)
        self.white_canvas.setStyleSheet("background-color: white;")  # 设置背景为白色
        self.white_canvas.resize(600, 640)  # 设置画布大小
        self.white_canvas.move(190, 190)  # 设置画布位置

        self.pic_choose_combo = AnimatedComboBox(self)
        self.pic_choose_combo.move(pic_choose_label.geometry().x()+pic_choose_label.geometry().width()+300, pic_choose_label.geometry().y())
        self.pic_choose_combo.resize(150,self.pic_choose_combo.geometry().height())
        self.pic_choose_combo.addItems(self.pic_list)
        self.pic_choose_combo.currentIndexChanged.connect(self.pic_change)
        self.pic_change()

        middle_x = (pic_choose_label.geometry().x() + self.pic_choose_combo.geometry().x() + self.pic_choose_combo.geometry().width()) / 2

        self.playing_index = -1
        self.problem_solving = False

        self.solve_problem_button = HoverButton("训练（可跳过训练）",self)
        self.solve_problem_button.move(middle_x - self.solve_problem_button.width() / 2, self.pic_choose_combo.y()+self.pic_choose_combo.height()+200)
        self.solve_problem_button.pressed.connect(self.solve_button_pressed)

        self.solve_test = QLabel(parent=self)  # 解答过程中的信息显示
        self.solve_test.setText("正在训练。。。")
        self.solve_test.resize(600, self.solve_test.height())
        self.solve_test.setFont(QFont("Fixed",7))
        self.solve_test.move(middle_x - self.solve_test.geometry().width() / 2,
                             self.solve_problem_button.geometry().y() + self.solve_problem_button.geometry().height() + 20)
        self.solve_test.setHidden(True)

        speed_choose_label = QLabel(self)
        speed_choose_label.move(self.solve_test.x()+20, self.solve_test.geometry().y() + 40)
        speed_choose_label.setText("播放速度：")
        self.play_speed_combo = AnimatedComboBox(self)
        self.play_speed_combo.move(speed_choose_label.geometry().x() + speed_choose_label.geometry().width() + 30,
                                   speed_choose_label.geometry().y())
        self.play_speed_combo.addItems(["高速", "中速", "慢速"])

        play_button = HoverButton("解决", self)
        # play_button.setText("解决")
        play_button.move(middle_x - play_button.geometry().width() / 2,
                         self.play_speed_combo.geometry().y() + self.play_speed_combo.geometry().height() + 40)
        play_button.pressed.connect(self.play_button_pressed)

        self.algo_selector = AnimatedComboBox(self)
        self.algo_selector.move(table_area.x()+table_area.width()+600, table_area.y()+530)  # 调整下拉框位置
        self.algo_selector.addItems(["BFS算法", "Dijkstra算法", "强化学习"])
        self.algo_selector.setCurrentIndex(0)
        self.algo_selector.currentIndexChanged.connect(self.on_algorithm_selected)
        self.on_algorithm_selected()

    # def draw_to_clear(self):

    def on_algorithm_selected(self):
        self.model.my_maze.visited=[]
        self.pic_change()
        choice = self.algo_selector.currentText()
        if (choice == "BFS算法"):
            self.algorithm_choice=0
            self.white_canvas.show()
            self.model.my_maze.visited=bfs(Mazes[self.pic_choose_combo.currentText()])
            print("使用BFS")
        elif choice =="Dijkstra算法":
            self.algorithm_choice=1
            self.white_canvas.show()
            self.model.my_maze.visited=dijkstra(Mazes[self.pic_choose_combo.currentText()])
            print("使用Dijk")
        else:
            self.algorithm_choice=2
            self.white_canvas.hide()

        if self.algorithm_choice == 0 or self.algorithm_choice == 1:
            self.solve_problem_button.setHidden(True)
        elif self.algorithm_choice == 2:
            self.solve_problem_button.setHidden(False)





    def pic_change(self):
        self.timer.stop()
        self.text_edit.hide()
        current_text = self.pic_choose_combo.currentText()
        maze = Mazes[current_text]
        my_maze = Maze(maze_map=np.array(maze), period=2)


        self.model = QTableModel(my_maze)

        if self.algorithm_choice==0:
            self.model.my_maze.visited=bfs(Mazes[self.pic_choose_combo.currentText()])
        elif self.algorithm_choice==1:
            self.model.my_maze.visited=dijkstra(Mazes[self.pic_choose_combo.currentText()])
        elif self.algorithm_choice==2:
            self.model.play_game(self.model.my_maze.find_start(), 0)
        try:
            self.model.load_table('saved_qtable/'+current_text+'.npy')
        except:
            QMessageBox.information(self, "提示", "没找到Q表保存文件", QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)


        self.Plot.draw_root(self.model.my_maze, self.model.my_maze.find_start(), 1, 0, False,first=True)

        if self.algorithm_choice==2:
            self.Plot.draw_qtable(qtable_model=self.model, time_=self.model.my_maze.period-1 if self.model.my_maze.period!=0 else 0, fire_flag=True)

    def play_button_pressed(self):
        if self.model == None:
            QMessageBox.information(self, "提示", "请先选择迷宫", QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
            return
        if(self.algorithm_choice==2):
            self.model.play_game(self.model.my_maze.find_start(), 0)   #模拟策略的应用入口
        print(self.model.my_maze.visited)
        if self.model.my_maze.visited!=[] and self.algorithm_choice==2 and self.model.my_maze.visited[-1]!=self.model.my_maze.aim:
            self.model.my_maze.visited=[]
        if self.model.my_maze.visited==[]:
            self.text_edit.show()
        speed_text = self.play_speed_combo.currentText()
        self.playing_index = 0
        if speed_text == "高速":
            self.timer.start(150, self)
        elif speed_text == "中速":
            self.timer.start(1000, self)
        else:
            self.timer.start(3000, self)

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            period = self.model.my_maze.period
            if period != 0 and (self.playing_index % period) >= period / 2:
                fire_flag = True
            else:
                fire_flag = False

            if self.algorithm_choice==2:
                self.Plot.draw_qtable(self.model, self.playing_index % period if period != 0 else 0, fire_flag)
            self.Plot.draw_root(self.model.my_maze, self.model.my_maze.find_start(), self.playing_index, period, fire_flag)

            self.playing_index = self.playing_index + 1
            if self.playing_index >= len(self.model.my_maze.visited) + 2:
                # self.playing_index = len(self.model.my_maze.visited) + 3
                self.timer.stop()
                # print("up",self.playing_index)
            else:
                super(Ui_basic, self).timerEvent(event)

    def solve_button_pressed(self):
        if self.problem_solving:
            return
        if type(self.model)==type(None):
            QMessageBox.information(self, "提示", "请先选择迷宫", QMessageBox.Ok | QMessageBox.Close, QMessageBox.Close)
            return

        self.problem_solving = True
        self.playing_index = -1
        self.solve_test.setHidden(False)
        self.timer.stop()
        self.repaint()
        start_time = time.time()
        #path = "tangrams\\" + self.parent().pic_choose_combo.currentText() + ".png"
        self.model.train(output_line = self.solve_test, main_ui=self)

        end_time = time.time()

        QMessageBox.information(self, "提示", "完成训练，用时：%.3f s" % (end_time - start_time),
                                QMessageBox.Ok | QMessageBox.Close, QMessageBox.Close)

        if self.algorithm_choice==2:
            self.Plot.draw_qtable(qtable_model=self.model,time_=self.model.my_maze.period - 1 if self.model.my_maze.period != 0 else 0,fire_flag=True)
        self.problem_solving = False
        self.solve_test.setHidden(True)

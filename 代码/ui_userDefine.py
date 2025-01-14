from PyQt5.QtWidgets import QLabel, QComboBox, QPushButton, QMessageBox, QWidget, QGroupBox, QGridLayout, QPlainTextEdit, QSpinBox,QTextEdit
from PyQt5.QtCore import QBasicTimer, QRect
import numpy as np
from maze import Maze
from train_qtable import QTableModel
import time
from style import HoverButton,AnimatedComboBox
from draw_ui import Draw_ui
from BFS import bfs
from Dijkstra import dijkstra
class Ui_userDefine(QWidget):
    def __init__(self):
        super().__init__()
        self.model = None
        self.playing_index = -1
        self.problem_solving = False
        self.my_maze=[]
        self.rat=()
        self.aim=()
    def initUI(self):
        self.resize(1200, 700)

        self.timer = QBasicTimer()
        widget1 = QWidget(parent=self)
        widget1.setGeometry(QRect(30, 50, 800, 500))
        table_area = QGroupBox(parent=widget1) #图形显示区域
        table_area.setGeometry(QRect(widget1.x(), widget1.y(), widget1.width(), widget1.height()))

        self.Plot = Draw_ui(width=3, height=3, dpi=100)
        gridlayout1 = QGridLayout(table_area)  # 继承容器groupBox
        gridlayout1.addWidget(self.Plot, 0, 1)

        pic_choose_label = QLabel(self)
        pic_choose_label.move(table_area.x()+table_area.width()+30, table_area.y()+20)
        pic_choose_label.setText("输入迷宫：")
        pic_choose_label2 = QLabel(self)
        pic_choose_label2.move(pic_choose_label.geometry().x(), pic_choose_label.y()+pic_choose_label.height()+20)
        pic_choose_label2.setText("（1表示可通行，0表示墙, 2表示障碍, 3表示火，4表示出口，5表示金币）")

        self.maze_input = QPlainTextEdit(parent=self)
        self.maze_input.setGeometry(QRect(pic_choose_label2.x(), pic_choose_label2.y()+pic_choose_label2.height()+20, 300, 200))
        self.maze_input.setPlainText(
            '-1, 0, 1, 1, 1, 1, 1,\r\n1, 1, 1, 0, 0, 1, 0,\r\n0, 0, 0, 1, 1, 1, 0,\r\n1, 1, 1, 1, 0, 0, 1,\r\n1, 0, 0, 0, 1, 1, 1,\r\n1, 0, 1, 1, 1, 2, 2,\r\n1, 1, 1, 0, 1, 4, 1,'
        )

        period_label = QLabel(parent=self)
        period_label.setText('火焰周期:')
        period_label.move(self.maze_input.x(), self.maze_input.height()+self.maze_input.y()+10)

        self.text_edit = QTextEdit(self)
        self.text_edit.setPlainText("no path in this maze")
        self.text_edit.move(1700, 1000)  # 设置位置 (x, y)
        self.text_edit.resize(600, 60)  # 设置大小 (width, height)
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("color: red; font-size: 50px;")
        self.text_edit.hide()
        self.period_input = QSpinBox(parent=self)
        self.period_input.setValue(1)
        self.period_input.move(period_label.x()+period_label.width()+15, period_label.y())

        period_label2 = QLabel(parent=self)
        period_label2.setText('*2')
        period_label2.move(self.period_input.x()+self.period_input.width()-40, self.period_input.y())

        maze_input_button = HoverButton('确认输入',self)
        maze_input_button.move(self.period_input.x()-50, self.period_input.y()+self.period_input.height()+10)
        # maze_input_button.setText('确认输入')
        maze_input_button.pressed.connect(self.pic_change)
        middle_x = self.maze_input.geometry().x()+ self.maze_input.geometry().width()/2

        train_epoch_label = QLabel(parent=self)
        train_epoch_label.setText('训练次数上限:')
        train_epoch_label.move(self.maze_input.x(), maze_input_button.height() + maze_input_button.y() + 40)

        self.epoch_input = QSpinBox(parent=self)
        self.epoch_input.move(train_epoch_label.x() + train_epoch_label.width() + 15, train_epoch_label.y())
        self.epoch_input.setValue(30)

        train_epoch_label2 = QLabel(parent=self)
        train_epoch_label2.setText('*1000')
        train_epoch_label2.move(self.epoch_input.x() + self.epoch_input.width() - 40, self.epoch_input.y())

        self.solve_problem_button = HoverButton("训练",self)
        self.solve_problem_button.move(maze_input_button.x(), train_epoch_label.y()+train_epoch_label.height()+10)
        self.solve_problem_button.pressed.connect(self.solve_button_pressed)

        self.solve_test = QLabel(parent=self)  # 解答过程中的信息显示
        self.solve_test.setText("正在训练。。。")
        self.solve_test.resize(350, self.solve_test.height())
        self.solve_test.move(middle_x - self.solve_test.geometry().width() / 2,
                             self.solve_problem_button.y() + self.solve_problem_button.height() + 10)
        self.solve_test.setHidden(True)

        speed_choose_label = QLabel(self)
        speed_choose_label.move(train_epoch_label.x(), self.solve_test.y() + self.solve_test.height() + 10)
        speed_choose_label.setText("播放速度：")
        self.play_speed_combo = QComboBox(self)
        self.play_speed_combo.move(speed_choose_label.geometry().x() + speed_choose_label.geometry().width() + 30,
                                   speed_choose_label.geometry().y())
        self.play_speed_combo.addItems(["高速", "中速", "慢速"])

        self.algo_selector = AnimatedComboBox(self)
        self.algo_selector.move(table_area.x()+table_area.width()+600, table_area.y()+530)  # 调整下拉框位置
        self.algo_selector.addItems(["BFS算法", "Dijkstra算法", "强化学习"])
        self.algo_selector.setCurrentIndex(0)
        self.algo_selector.currentIndexChanged.connect(self.on_algorithm_selected)
        self.on_algorithm_selected()

        play_button = HoverButton("解决",self)
        play_button.move(speed_choose_label.x()+40,
                         self.play_speed_combo.geometry().y() + self.play_speed_combo.geometry().height() + 10)
        play_button.pressed.connect(self.play_button_pressed)



    def on_algorithm_selected(self):
        self.pic_change()
        choice = self.algo_selector.currentText()
        if (choice == "BFS算法"):
            self.algorithm_choice=0

            self.model.my_maze.visited=bfs(self.my_maze)
            print("使用BFS")
        elif choice =="Dijkstra算法":
            self.algorithm_choice=1

            self.model.my_maze.visited=dijkstra(self.my_maze)
            print("使用Dijk")
        else:
            self.algorithm_choice=2


        if self.algorithm_choice == 0 or self.algorithm_choice == 1:
            self.solve_problem_button.setHidden(True)
        elif self.algorithm_choice == 2:
            self.solve_problem_button.setHidden(False)
    def pic_change(self):
        self.timer.stop()
        current_text = self.maze_input.toPlainText()
        rows = current_text.split('\n')
        maze_map = []
        try:
            for row in rows:
                row_sp = row.split(',')
                row_list= []
                for c in row_sp:
                    c = c.strip()
                    if len(c)==0:
                        continue
                    else:
                        row_list.append(int(c))
                maze_map.append(row_list)
        except:
            QMessageBox.information(self, "提示", "无法解析输入", QMessageBox.Ok | QMessageBox.Close, QMessageBox.Close)
            return

        maze_len = len(maze_map[0])
        for i in range(1,len(maze_map)):
            if len(maze_map[i])!=maze_len:
                QMessageBox.information(self, "提示", "错误，每一行的列数应当相等", QMessageBox.Ok | QMessageBox.Close, QMessageBox.Close)
                return

        my_maze = Maze(maze_map=np.array(maze_map), period=self.period_input.value()*2)
        self.my_maze = my_maze.maze
        print(self.my_maze)
        self.model = QTableModel(my_maze)

        self.rat=self.model.my_maze.rat
        #self.model.play_game((0, 0), 0)
        self.Plot.draw_root(self.model.my_maze, self.rat, 1, 0, False)
        self.Plot.draw_qtable(qtable_model=self.model, time_=self.model.my_maze.period-1 if self.model.my_maze.period!=0 else 0, fire_flag=True)

    def play_button_pressed(self):
        if self.model == None:
            QMessageBox.information(self, "提示", "请先输入迷宫", QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
            return
        if (self.algorithm_choice == 2):
            self.model.play_game(self.model.my_maze.find_start(), 0)  # 模拟策略的应用入口
        print(self.model.my_maze.visited)
        if self.model.my_maze.visited != [] and self.algorithm_choice == 2 and self.model.my_maze.visited[
            -1] != self.model.my_maze.aim:
            self.model.my_maze.visited = []
        if self.model.my_maze.visited == []:
            self.text_edit.show()
        speed_text = self.play_speed_combo.currentText()
        self.playing_index = 0
        if speed_text == "高速":
            self.timer.start(150, self)
        elif speed_text == "中速":
            self.timer.start(500, self)
        else:
            self.timer.start(1500, self)

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            period = self.model.my_maze.period
            if period != 0 and (self.playing_index % period) >= period / 2:
                fire_flag = True
            else:
                fire_flag = False

            self.Plot.draw_qtable(self.model, self.playing_index % period if period != 0 else 0, fire_flag)
            self.Plot.draw_root(self.model.my_maze, (0,0), self.playing_index, period, fire_flag)

            self.playing_index = self.playing_index + 1

            if self.playing_index >= len(self.model.my_maze.visited) + 2:
                self.timer.stop()
                # print("up",self.playing_index)
        else:
            super(Ui_userDefine, self).timerEvent(event)

    def solve_button_pressed(self):
        if self.problem_solving:
            return
        if type(self.model)==type(None):
            QMessageBox.information(self, "提示", "请先输入迷宫", QMessageBox.Ok | QMessageBox.Close, QMessageBox.Close)
            return

        self.problem_solving = True
        self.playing_index = -1
        self.solve_test.setHidden(False)
        self.timer.stop()
        self.repaint()

        train_epoch = self.epoch_input.value()*1000
        start_time = time.time()
        #path = "tangrams\\" + self.parent().pic_choose_combo.currentText() + ".png"
        self.model.train(output_line = self.solve_test, main_ui=self, epoch_N=train_epoch)
        end_time = time.time()

        QMessageBox.information(self, "提示", "完成训练，用时：%.3f s" % (end_time - start_time),
                                QMessageBox.Ok | QMessageBox.Close, QMessageBox.Close)

        self.Plot.draw_qtable(qtable_model=self.model,
                              time_=self.model.my_maze.period - 1 if self.model.my_maze.period != 0 else 0,
                              fire_flag=True)
        self.problem_solving = False
        self.solve_test.setHidden(True)

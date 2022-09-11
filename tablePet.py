import os
import sys
import random
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui


class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()
        # 初始化窗口
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.repaint()
        # 导入一个宠物
        self.petImages, self.iconpath = self.loadPetImages()
        # 表示当前显示的图片(设置标签)
        self.image = QLabel(self)
        self.initPetAct()
        # 是否跟随鼠标
        self.is_follow_mouse = False
        # 宠物拖拽时避免鼠标直接跳到左上角
        self.mouse_drag_pos = self.pos()

        # 设置右键菜单
        self.image.setContextMenuPolicy(Qt.CustomContextMenu)
        self.image.customContextMenuRequested.connect(self.createRightMenu)

        # 设置退出选项
        quit_action = QAction('退出', self, triggered=self.quit)
        quit_action.setIcon(QIcon(self.iconpath))
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(quit_action)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(self.iconpath))
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()

        # 宠物重复动画所需一些变量
        self.is_run_action = False
        self.action_images = []
        self.action_pointer = 0
        self.action_max_len = 0

        # 宠物单次动画所需一些变量
        self.single_is_run_action = False
        self.single_action_images = []
        self.single_action_pointer = 0
        self.single_action_max_len = 0

        # 抓起动作定时器
        self.dragTimer = QTimer()
        self.dragTimer.timeout.connect(self.repeatDragUp)

        # 跳舞计时器
        self.danceTimer = QTimer()
        self.danceTimer.timeout.connect(self.danceAct)

        # 随机动作计时器
        self.randomTimer = QTimer()
        self.randomTimer.timeout.connect(self.randomAct)
        self.randomTimer.start(200)

        # 显示
        self.resize(128, 128)

        self.randomPosition()
        self.show()

    def randomAct(self):
        # self.repeatAct(self.petImages[random.choice(list(self.petImages.keys()))])
        self.repeatAct(self.petImages["lie"])
    '''创建右键菜单'''

    def createRightMenu(self):
        self.rightMenu = QMenu(self)
        self.actionA = QAction(QIcon('./img/cake.png'), u'生日快乐~', self)
        self.rightMenu.addAction(self.actionA)

        self.actionA.triggered.connect(self.birthday)

        self.rightMenu.popup(QCursor.pos())

    '''右键生日快乐按钮'''

    def birthday(self):
        # print("生日快乐！")
        self.danceTimer.start(200)
        self.randomTimer.stop()

    '''初始化动作'''

    def initPetAct(self):
        self.setImage(self.petImages['run'][0])

    '''跳舞动作'''

    def danceAct(self):
        isDance = self.singleAct(self.petImages["dance"])

        if not isDance:
            self.danceTimer.stop()
            self.randomTimer.start()
            # self.initPetAct()

    def repeatDragUp(self):
        self.repeatAct(self.petImages["dragUp"])

    def singleAct(self, images):
        if not self.single_is_run_action:
            self.single_is_run_action = True
            self.single_action_images = images
            self.single_action_pointer = 0
            self.single_action_max_len = len(self.single_action_images)

        if self.single_action_pointer == self.single_action_max_len:
            self.single_is_run_action = False
            self.single_action_pointer = 0
            self.single_action_max_len = 0
            return False

        self.setImage(self.single_action_images[self.single_action_pointer])
        self.single_action_pointer += 1

        return True

    def repeatAct(self, images):
        if not self.is_run_action:
            self.is_run_action = True
            self.action_images = images
            self.action_pointer = 0
            self.action_max_len = len(self.action_images)

        self.runFrame()

    '''完成动作每一帧'''

    def runFrame(self):
        if self.action_pointer == self.action_max_len:
            self.is_run_action = False
            self.action_pointer = 0
            self.action_max_len = 0

        # print("frame", self.action_pointer)
        self.setImage(self.action_images[self.action_pointer])
        self.action_pointer += 1

    '''导入所有桌面宠物照片'''

    def loadPetImages(self):
        petImages = {"dragUp": [], "run": [], "dance": [], "lie":[], "play":[], "jumpAround":[], }
        iconpath = "./img/icon.png"

        path = "./img/"
        dirList = os.listdir(path)  # ./img/下的所有文件夹名
        for name in dirList:
            if os.path.isfile(os.path.join(path, name)):
                dirList.remove(name)

        picNameDic = {}  # 文件夹内所有图片的名称集合
        for dirName in dirList:
            picNameDic[dirName] = os.listdir(path + dirName + "/")

        dirName = "Sylveon"

        # dragUp image
        petImages["dragUp"].append(
            self.loadImage(path + dirName + "/" + "shimeX.png"))
        petImages["dragUp"].append(
            self.loadImage(path + dirName + "/" + "shimeXa.png"))
        petImages["dragUp"].append(
            self.loadImage(path + dirName + "/" + "shimeXb.png"))

        # run image
        petImages["run"].append(
            self.loadImage(
                path + dirName + "/" + "shime1" + ".png"))
        for i in range(9):
            petImages["run"].append(
                self.loadImage(
                    path + dirName + "/" + "shime1" + chr(97 + i) + ".png"))

        # dance image
        for i in range(26, 30):
            petImages["dance"].append(
                self.loadImage(
                    path + dirName + "/" + "shime" + str(i) + ".png"))

        # lie image
        petImages["lie"].append(
            self.loadImage(
                path + dirName + "/" + "shime11" + ".png"))
        for i in range(3):
            petImages["lie"].append(
                self.loadImage(
                    path + dirName + "/" + "shime11" + chr(97 + i) + ".png"))

        # play image
        petImages["play"].append(
            self.loadImage(
                path + dirName + "/" + "shime30" + ".png"))
        for i in range(5):
            petImages["play"].append(
                self.loadImage(
                    path + dirName + "/" + "shime11" + chr(97 + i) + ".png"))

        # jumpAround image
        petImages["jumpAround"].append(
            self.loadImage(
                path + dirName + "/" + "shime31" + ".png"))
        for i in range(4):
            petImages["jumpAround"].append(
                self.loadImage(
                    path + dirName + "/" + "shime31" + chr(97 + i) + ".png"))

        petImages["jumpAround"].append(
            self.loadImage(
                path + dirName + "/" + "shime32" + ".png"))
        for i in range(5):
            petImages["jumpAround"].append(
                self.loadImage(
                    path + dirName + "/" + "shime32" + chr(97 + i) + ".png"))

        petImages["jumpAround"].append(
            self.loadImage(
                path + dirName + "/" + "shime33" + ".png"))
        for i in range(4):
            petImages["jumpAround"].append(
                self.loadImage(
                    path + dirName + "/" + "shime33" + chr(97 + i) + ".png"))

        return petImages, iconpath

    '''加载一张图片'''

    def loadImage(self, imagePath):
        image = QImage()
        image.load(imagePath)
        return image

    '''设置当前显示的图片'''

    def setImage(self, image):
        self.image.setPixmap(QPixmap.fromImage(image))

    '''鼠标左键按下时, 宠物将和鼠标位置绑定'''

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            self.dragTimer.start(200)
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    '''鼠标移动, 则宠物也移动'''

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
            event.accept()

    '''鼠标释放时, 取消绑定'''

    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.dragTimer.stop()
        # self.initPetAct()
        self.setCursor(QCursor(Qt.ArrowCursor))

    '''随机出现桌面位置'''

    def randomPosition(self):
        screen_geo = QDesktopWidget().screenGeometry()
        pet_geo = self.geometry()
        width = (screen_geo.width() - pet_geo.width()) * random.random()
        height = (screen_geo.height() - pet_geo.height()) * random.random()
        self.move(int(width), int(height))

    '''退出程序'''

    def quit(self):
        self.close()
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = DesktopPet()
    sys.exit(app.exec_())

# -*-codeing = utf-8 -*-
# @Time :2020/10/12 20:31
# @Author : baiweidou
# @File : 华容道main.py
# @Software :PyCharm
import sys
import os
import pygame
from collections import OrderedDict
from pygame.locals import *
import time
import random
from queue import PriorityQueue
FPS = 60                    #帧率
Shape = 3                   #游戏类型
cell_size = 200             #方格大小
cell_gap_size = 10          #方格间距
margin = 10                 #方格的边缘
padding = 10                #方格的填料
left_screen_size = 300      #左侧屏幕的大小
right_screen_size = 200      #右侧屏幕的大小

button_size = 100
button_start_size = 300

button1_x = 100
button1_y = 20
button2_x = 100
button2_y = 170
button3_x = 100
button3_y = 320
button4_x = 1000
button4_y = 50
button5_x = 1000
button5_y = 200
button_start_x = 410
button_start_y = 400


step_x = 50                 #步数框的x坐标
step_y = 500                #步数框的y坐标
step_size = 50              #步数框的大小

org_x =  50                    #原图片的x坐标
org_y =  430               #原图片的y坐标

screen_width = (cell_size + margin) * Shape + margin + left_screen_size + right_screen_size              #界面宽度
screen_height = (cell_size + margin) * Shape + margin                                     #界面高度

background_color = '#FFCC99'        #背景颜色

filelists = os.listdir(r'.\无框字符')
cname = []                  #所有字母
for file in filelists:
    cname.append(ord(file[0]))

def tuple_add(t1,t2):
#定义元组相加
    return(t1[0]+t2[0],t1[1]+t2[1])
class Logic:
    #定义游戏规则
    def __init__(self,shape = 3):
        self.board = []
        #初始序列
        self.final_list= []
        #最终序列
        self.before_auto_move = []
        #记录自动移动之前的编号
        self.before_auto_step = 0
        #记录自动移动之前的步数
        self.c = 65
        #字母ascii码
        self.shape = int(shape)
        #类型是3*3
        self.operations = []
        self.tiles = OrderedDict()
        #tiles用于存放坐标
        #{(0,0):3,
        # (0,1):5,
        #  ····}
        #使用OrderedDict会根据放入元素的先后顺序进行排序。所以输出的值是排好序的。而普通的字典不对元素排序
        self.neighbors = [
            [1,0],          #右
            [-1,0],         #左
            [0,1],          #上
            [0,-1],         #下
        ]
        #定义方向列表
        self.click_dict = {'x':{},'y':{}}
        #定义点击坐标字典
        self.step = 0
        #记录步数
        self.init_load()
        #初始化棋盘
    def get_final_board(self):
        #获取最终序列
        count = 45
        #1+2+···+9=45
        final_list = []
        for i in self.board:
            count -= i
        for i in range(1,10):
            final_list.append(i)
        final_list[count-1] = 0
        return final_list
    def init_load(self):
        self.board = random_first_list()
        self.c = random.choice(cname)
        self.final_list = self.get_final_board()
        self.step = 0
        count = 0
        for x in range(self.shape):
            for y in range(self.shape):
                mark = tuple([x,y])
                #mark是标记现在是哪个块
                #[0,0],[0,1],[0,2]
                #[1,0],[1,1],[1,2]
                #[2,0],[2,1],[2,2]
                self.tiles[mark] = self.board[count]
                #图片编号
                count += 1
        self.init_click_dict()
        #初始化点击转换坐标
    def init_click_dict(self):
        #初始化点击坐标转换下标的数据
        for row in range(self.shape):
            for column in range(self.shape):
                x = left_screen_size + margin * (column + 1) + column * cell_size
                x1 = x + cell_size
                click_x = tuple(range(x,x1))
                #横坐标点击范围为x到x1
                self.click_dict['x'][click_x] = column
                #字典中的字典，第c列的范围是
                y =  margin * (row + 1) + row * cell_size
                y1 = y + cell_size
                click_y = tuple(range(y,y1))
                #纵坐标点击范围为y到y1
                self.click_dict['y'][click_y] = row
    def move(self,mark):
        #移动数据
        for neighbor in self.neighbors:
            #遍历上下左右四个方向
            spot = tuple_add(mark,neighbor)
            #spot等于移动目标向四个方向移动后的坐标
            if spot in self.tiles and self.tiles[spot] == 0:
                #如果移动后在范围内，并且移动后的点数字为0，则交换数据
                self.tiles[spot],self.tiles[mark] = self.tiles[mark],self.tiles[spot]
                self.operations.append(neighbor)
                self.step += 1
                break
    def click_to_move(self,x,y):
        #点击移动
        x1 = None
        for k , v in self.click_dict['x'].items():#items是以元组方式返回键和值
            if x in k :
                #如果点击的x在九宫格范围内，则给x1附现在处于哪个行
                x1 = v
        if x1 is None:
            return

        y1 = None
        for k, v in self.click_dict['y'].items():
            if y in k:
                # 如果点击的y在九宫格范围内，则给y1附现在处于哪个列
                y1 = v
        if y1 is None:
            return
        self.move((y1,x1))
    def key_move(self,direction):
        #键盘移动
        i = list(self.tiles.values()).index(0)
        mark = list(self.tiles.keys())[i]
        (x,y) = tuple_add(mark,direction)
        if (x,y) not in self.tiles.keys():
            return
        self.move((x,y))
    def is_win(self):
        #游戏胜利判定
        if list(self.tiles.values()) == self.final_list:
            return True
        else:
            return False

def has_answer(board):
    count = 0
    for i in range(len(board)):
        if board[i] == 0:
            continue
        for j in range(i + 1, len(board)):
            if board[j] == 0:
                continue
            if board[i] > board[j]:
                count = count + 1
    if (count % 2 == 1):
        return 0
    return 1
def random_first_list():
    list = [i for i in range(1,10)]
    x = random.randint(0,8)
    list[x] = 0
    random.shuffle(list)
    while(not has_answer(list)):
        random.shuffle(list)
    return list
def goBackDistance(num):
    dist = 0
    row = 0
    col = 0
    for i in range(len(num)):
        if num[i] == 0:
            continue
        else:
            row = abs((num[i] - 1) // 3 - i // 3)  # 竖直距离之差
            col = abs((num[i] - 1) % 3 - i % 3)  # 水平距离之差
            dist = dist + row + col  # 当前位置到最终位置之差

    return dist
def search(board,final):
    operation = []
    begin = tuple(board)

    Queue = PriorityQueue()
    Queue.put([goBackDistance(begin), begin, begin.index(0), 0, operation])
    vis = {begin}

    while Queue.not_empty:
        prioritynum, board, pos, steps, operation = Queue.get()

        if board == final:
            for i in range(len(operation)):
                if operation[i] == -1:
                    operation[i] = 'a'
                elif operation[i] == 1:
                    operation[i] = 'd'
                elif operation[i] == 3:
                    operation[i] = 's'
                elif operation[i] == -3:
                    operation[i] = 'w'

            return operation

        pos = board.index(0)
        for i in (-1, 1, -3, 3):
            pos0 = pos + i
            row = abs(pos0 // 3 - pos // 3)  # 竖直距离之差
            col = abs(pos0 % 3 - pos % 3)  # 水平距离之差

            if row + col != 1:
                continue
            if pos0 < 0:
                continue
            if pos0 > 8:
                continue

            newboard = list(board)
            newboard[pos0], newboard[pos] = newboard[pos], newboard[pos0]
            visboard = tuple(newboard)
            if visboard not in vis:
                vis.add(visboard)
                tup1 = operation
                tup2 = [i]
                tup1 = tup1 + tup2
                Queue.put([steps + 1 + goBackDistance(newboard), newboard, pos0, steps + 1, tup1])
def auto_move(logic,screen,clock):
    logic.before_auto_move = list(logic.tiles.values())
    logic.before_auto_step = logic.step
    operations = search(list(logic.tiles.values()),logic.final_list)
    for c in operations:
        if c == 'w':
            direction = (-1,0)
        elif c == 's':
            direction = (1, 0)
        elif c == 'a':
            direction = (0,-1)
        elif c == 'd':
            direction = (0, 1)
        logic.key_move(direction)
        screen.fill(pygame.Color(background_color))
        load_img(logic, screen, path_org=r".\无框字符分块", path_icon=r".\icon")
        pygame.display.update()
        clock.tick(FPS)
        time.sleep(0.2)
def ret(logic):
    if logic.before_auto_move == []:
        return
    logic.step = logic.before_auto_step
    for i in range(logic.shape):
        for j in range(logic.shape):
            logic.tiles[(i,j)] = logic.before_auto_move[i*logic.shape+j]
def next_step(logic):
    if logic.final_list == list(logic.tiles.values()):
        return
    operations = search(list(logic.tiles.values()),logic.final_list)
    if operations[0] == 'w':
        logic.key_move((-1,0))
    elif operations[0] == 's':
        logic.key_move((1, 0))
    elif operations[0] == 'd':
        logic.key_move((0, 1))
    elif operations[0] == 'a':
        logic.key_move((0, -1))
def last_step(logic):
    if logic.step == 0:
        return
    i = list(logic.tiles.values()).index(0)
    x,y = list(logic.tiles.keys())[i]
    x1,y1 = tuple_add((x,y),logic.operations[-1])
    logic.tiles[(x,y)], logic.tiles[(x1,y1)] = logic.tiles[(x1,y1)], logic.tiles[(x,y)]
    del logic.operations[-1]
    logic.step -= 1
def init_game():
    #初始化游戏
    pygame.init()
    # 初始化游戏
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    #居中显示
    screen = pygame.display.set_mode((screen_width,screen_height))
    #初始化界面宽度长度，返回背景
    pygame.display.set_caption("图片华容道")
    #初始化标题
    return screen
def load_img(logic,screen,path_org,path_icon):
    #载入图片,包括按钮，原图，原图分块
    #path_org是原图分块所在路径
    #path_reset是按钮图片所在的路径
    surface = pygame.image.load(r'.\img\水墨1.jpg')
    screen.blit(surface, (0, 0))
    #载入背景

    #载入九宫格
    for r in range(logic.shape):
        for c in range(logic.shape):
            num = logic.tiles[(r,c)]
            x = left_screen_size + margin * (c + 1) + c * cell_size
            y = margin * (r + 1) + r * cell_size
            if num == 0:
                img = pygame.image.load(r'.\无框字符分块\0.jpg')
            else:
                img = pygame.image.load( path_org + r'\%s_%d.jpg'%(logic.c,num))
            screen.blit(img,(x,y))

    img_org = pygame.image.load(r'.\new\%s.jpg'%logic.c)
    #载入原图
    screen.blit(img_org,(org_x,org_y))

    reset_button = pygame.image.load(path_icon+r'\reset.png')
    #载入重置按钮
    screen.blit(reset_button, (button1_x, button1_y))

    ret_button = pygame.image.load(path_icon + r'\return_1.png')
    # 载入返回按钮
    screen.blit(ret_button, (button3_x, button3_y))

    right_button = pygame.image.load(path_icon + r'\left_1.png')
    # 载入下一步按钮
    screen.blit(right_button, (button4_x, button4_y))

    left_button = pygame.image.load(path_icon + r'\right_1.png')
    # 载入上一步按钮
    screen.blit(left_button, (button5_x, button5_y))

    start_button = pygame.image.load(path_icon+r'\start_1.png')
    #载入开始按钮
    screen.blit(start_button, (button2_x, button2_y))
# def load_step(logic,screen):
#     pygame.draw.rect(screen,(255,255,255),((step_x,step_y),(step_size*4,step_size)))
#     #pygame.draw.rect(Surface, color, Rect, width=0)
#     #在Surface上绘制矩形，第二个参数是线条（或填充）的颜色，第三个参数Rect的形式是((x, y), (width, height))，表示的是所绘制矩形的区域，其中第一个元组(x, y)表示的是该矩形左上角的坐标，第二个元组 (width, height)表示的是矩形的宽度和高度。
#     font = pygame.font.SysFont("华文宋体",18)
#     text = "步数为：%d"%logic.step
#     font_width, font_height = font.size(str(text))
#     screen.blit(font.render(str(text), True, (0, 0, 0)),(step_x+step_size*2.5-font_width,step_y+step_size/4))
def press(is_game_over,logic,screen,clock,count,counts):
    # 监控事件
    # is_game_over为判定是否结束游戏
    # count为自定义计时事件
    # counts为从哪开始计时
    for event in pygame.event.get():
        if event.type == count and not is_game_over:
            #计时事件
            counts += 1
            pygame.display.set_caption('图片华容道--{}s-----{}step'.format(counts,logic.step))

        if event.type == pygame.QUIT:
            #退出事件
            pygame.quit()
            sys.exit()
            #向sys借的exit()

        if event.type == pygame.MOUSEBUTTONUP:
            #松开鼠标事件
            if event.button == 1 and not is_game_over:
                x,y = event.pos
                #x,y为鼠标松开时的点的坐标
                if button1_x <x< button1_x +button_size and button1_y < y < button1_y + button_size:
                    #如果此时处于重置按钮位置，则重置
                    logic.init_load()
                    return 0
                elif button2_x < x < button2_x + button_size and button2_y < y < button2_y + button_size:
                    auto_move(logic,screen,clock=clock)

                elif button3_x < x < button3_x + button_size and button3_y < y < button3_y + button_size:
                    ret(logic)

                elif button4_x < x < button4_x + button_size and button4_y < y < button4_y + button_size:
                    last_step(logic)

                elif button5_x < x < button5_x + button_size and button5_y < y < button5_x + button_size:
                    next_step(logic)
                else:
                    #否则调用点击移动函数
                    logic.click_to_move(int(x),int(y))

        if event.type == pygame.KEYUP:
            #松开键盘事件
            #wasd和上下左右分别对应上下左右移动
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                direction = (-1, 0)
                logic.key_move(direction=direction)
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                direction = (0, -1)
                logic.key_move(direction=direction)
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                direction = (1, 0)
                logic.key_move(direction=direction)
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                direction = (0, 1)
                logic.key_move(direction=direction)
            elif event.key == 13:
                #如果按下为enter键，则重新开始
                return True
    if count:
        return counts
def game_win(screen,logic,clock):
    #游戏胜利后出现的画面
    font = pygame.font.SysFont('华文宋体',int(screen_height/4))
    text = "你赢了，按下enter键重新开始"
    font_width, font_height = font.size(str(text))
    while True:
        if press(True,logic,None,None):
            #判断游戏是否结束,如果按了enter键则返回True，则退出循环，重新开始，否则不断循环
            break

        screen.fill(pygame.Color(background_color))
        screen.blit(font.render(str(text),True,(0,0,0)),((screen_width - font_width)/2,(screen_height - font_height)/2))
        pygame.display.update()
        #画布更新
        clock.tick(FPS)
        #更新频率为FPS
def game_start_surface(screen,logic,clock):
    while True:
        img_surface = pygame.image.load(r'.\img\水墨1.jpg')
        screen.blit(img_surface,(0,0))
        img_title = pygame.image.load(r'.\img\图片华容道1.png')
        screen.blit(img_title, (0,0))
        img = pygame.image.load(r'.\img\开始游戏.png')
        screen.blit(img,(0,0))
        pygame.display.update()
        # 更新画布
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                x,y = event.pos
                if button_start_x < x < button_start_x+ button_start_size and button_start_y< y < button_start_y + button_start_size/4:
                    return
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
def main():
    screen = init_game()
    # 初始化界面
    clock = pygame.time.Clock()
    # 创建一个对象来跟踪时间（可以控制游戏循环频率）
    logic = Logic(Shape)
    # 创建游戏规则
    count = pygame.USEREVENT + 1
    # count为人为设定的用户事件，其键值在用户事件和pygame.NUMEVENTS之间
    pygame.time.set_timer(count, 1000)
    # set_timer(eventid, milliseconds) -> None
    # 在事件队列上重复创建事件,重复创建计数事件，每次创建事件要等1000ms
    seconds = 0
    game_start_surface(screen,logic,clock)
    while True:
        seconds = press(False, logic,screen,clock,count,seconds)
        # 初始化计时数据，监控程序
        load_img(logic, screen,path_org=r".\无框字符分块",path_icon= r".\icon")
        # 加载图片
        #load_step(logic,screen)
        pygame.display.update()
        # 更新画布
        clock.tick(FPS)
        # 设置更新频率为60hz
if __name__ == '__main__':
    while True:
        main()
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time      :2020/10/11 10:38
# @Author    :Roseman
# @File      :10.11.py
# @Software :PyCharm
import os
import base64
from PIL import Image
from PIL import ImageChops
import requests,json
import pprint
import operator
import math
from functools import reduce
import time
from queue import PriorityQueue

request_steps = -1
pic_num1 = 0
pic_num2 = 0
swap_num1 = 0
swap_num2 = 0
final = [0, 0, 0, 0, 0, 0, 0, 0, 0]
def get_api():
    r = requests.get('http://47.102.118.1:8089/api/problem?stuid=061800339')
    img = r.json()['img']
    step = r.json()['step']
    swap = r.json()['swap']
    uuid = r.json()['uuid']
    saveImg_base64('1.txt',img)
    return (step, swap, uuid)

def post_api(data):
    url_json = 'http://47.102.118.1:8089/api/answer'
    data1 = dict(data)
    headers = {"Content-Type":"application/json"}
    r_json = requests.post(url_json ,headers = headers,data = json.dumps(data1))
    print(r_json.text)

def saveImg_base64(path, img):
    with open(path, 'w') as f:
        f.write(img)

def cut_image(image):#图片剪切九宫格
    width, height = image.size
    item_width = int(width/3)
    box_list = []
    for i in range(0, 3):
        for j in range(0, 3):
            box = (j*item_width, i*item_width, (j+1)*item_width, (i+1)*item_width)
            box_list.append(box)
    image_list = [image.crop(box) for box in box_list]
    return image_list

def save_images(image_list):#图片保存
    index = 1
    for image in image_list:
        path = '%d.jpg'%index
        image.save(path)
        index += 1

def pic_decode():#图片base64解码并写入文件1.jpg
    with open('1.txt') as f:
        imgdata = base64.b64decode(f.read())
        file = open('10.jpg', 'wb')
        file.write(imgdata)
        file.close()

def Pic_Compare(path_one,path_two): #两张图片对比
    #打开两张图片
    imagea = Image.open(path_one)
    imageb = Image.open(path_two)
    #获取其直方图数据
    h1 = imagea.histogram()
    h2 = imageb.histogram()
    #返回两张图片相似度，result越低则相似度越高
    result = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
    return result

def Pics_Compare(num):  #九张分块图片和九张原图分块对比并编号
    #创建编号数组
    code_list = [0 for i in range(9)]
    #创建相似度二维数组
    sim = [[0 for i in range(9)] for j in range(9)]
    #计数，看一组图片中有多少块相似的
    count = 0

    #每张分块和原图片的九张分块对比
    for i in range(1, 10):
        path_one = '%d.jpg'%i
        #如果对比三次以上，还没有发现有两张图片相似，则跳出循环
        if i > 3 and count <= 1:
            break
        #每张分块和九张分块对比
        for j in range(1, 10):
            path_two = r'.\无框字符分块\%d_%d.jpg'%(num,j)
            sim[i-1][j-1] = int(Pic_Compare(path_one,path_two))
            if sim[i-1][j-1] == 0:
                count += 1
                #编号
                code_list[i-1] = j
    #如果相似的块大于4，就认为是同一组图片，返回确认值
    if count > 4:
        flag = 1
    else:
        flag = 0
    return (code_list,flag)

def blank_compare():#空白图像对比
    for i in range(1, 10):
        path_one = '%d.jpg' % i
        path_two = 'blank.jpg'
        sim = Pic_Compare(path_one, path_two)
        if sim == 0:
            print("图片%d是空白的" % i)
            return i

def All_compare():#全部图片对比，并确定编号
    #获取路径
    path_file = ".\无框字符"
    #获取路径内所有文件的名字
    filelists = os.listdir(path_file)

    #文件名列表，只需要文件的第一个字母的ASIIC码
    name = []
    #返回的编号
    code_list = []

    # 获取原字符的ASCII码
    for i in range(len(filelists)):
        name.append(ord(filelists[i][0]))
    #所有图片对比
    for c in name:
        num = c
        (code_list, flag) = Pics_Compare(num)
        if flag == 1:
            break
    return code_list, chr(num)


class Search:
    @staticmethod
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

    def search(self, board):
        operation = []
        begin = tuple(board)

        Queue = PriorityQueue()
        # 启发值，开始序列，空白图的位置，步数，交换图片1，交换图片2，操作过程
        Queue.put([self.goBackDistance(begin), begin, begin.index(0), 0, 0, 0, operation])
        vis = {begin}        # 遍历过的序列

        while Queue.not_empty:
            prioritynum, board, pos, steps, change_pos1, change_pos2, operation = Queue.get()
            # 优先级，序列，空白图位置，交换图片1，交换图片2，操作过程

            if board == final:  # 得到最终解时
                num1 = change_pos1
                num2 = change_pos2
                for i in range(len(operation)):
                    if operation[i] == -1:
                        operation[i] = 'a'
                    elif operation[i] == 1:
                        operation[i] = 'd'
                    elif operation[i] == 3:
                        operation[i] = 's'
                    elif operation[i] == -3:
                        operation[i] = 'w'

                return steps, operation, change_pos1, change_pos2

            if request_steps == steps: # 步数和指定步数相同时
                board = list(board)
                board[pic_num1 - 1], board[pic_num2 - 1] = board[pic_num2 - 1], board[pic_num1 - 1]  # 交换图片
                count = 0  # 统计逆序数个数的奇偶性
                for i in range(len(board)):
                    for j in range(i + 1, len(board)):
                        if board[j] == 0:
                            continue
                        if board[i] > board[j]:
                            count = count + 1

                if (count % 2) == 1:  # 奇数 — 无解
                    pos1, pos2 = self.quickExchange(board) # 寻找交换的最优情况
                    change_pos1 = pos1
                    change_pos2 = pos2
                    board[pos1], board[pos2] = board[pos2], board[pos1] # 交换情况

            pos = board.index(0)    # 更新空白图的位置
            for i in (-1, 1, -3, 3):  # 左右上下
                pos0 = pos + i
                row = abs(pos0 // 3 - pos // 3)  # 竖直距离之差
                col = abs(pos0 % 3 - pos % 3)    # 水平距离之差

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
                    vis.add(visboard)   # 加入遍历过的序列
                    tup1 = operation
                    tup2 = [i]
                    tup1 = tup1 + tup2
                    Queue.put([steps + 1 + self.goBackDistance(newboard), newboard, pos0, steps + 1, change_pos1, change_pos2, tup1])

    def quickExchange(self,board):
        min = 0xfffff
        dist = 0
        pic1 = 0
        pic2 = 0
        for i in range(len(board)):
            if board[i] == 0:
                continue
            for j in range(i+1, len(board)):
                if board[j] == 0:
                    continue
                board[i], board[j] = board[j], board[i]
                dist = self.goBackDistance(board)
                if dist < min:
                    min = dist
                    pic1 = i
                    pic2 = j

                board[i], board[j] = board[j], board[i]

        return pic1, pic2

def printProcess(board, process): # 输出解题过程
    print("初始状态")
    for i in range(0, 3):
        print(board[i * 3], board[i * 3 + 1], board[i * 3 + 2])
    print("--------------------------------------")
    pos = board.index(0)
    for step in range(len(process)):
        if step == request_steps:
            print("交换图片---此时状态")
            for i in range(0, 3):
                print(board[i * 3], board[i * 3 + 1], board[i * 3 + 2])
            print("---------------------------------------------")
            print(pic_num1, pic_num2)
            # 交换图片
            board[pic_num1 - 1], board[pic_num2 - 1] = board[pic_num2 - 1], board[pic_num1 - 1]  # 交换图片
            count1 = 0  # 统计逆序数个数的奇偶性
            for i in range(len(board)):
                for j in range(i + 1, len(board)):
                    if board[j] == 0:
                        continue
                    if board[i] > board[j]:
                        count1 = count1 + 1

            if (count1 % 2) == 1:  # 奇数 — 无解
                print("无解！----交换 第%d张 第%d张" % (swap_num1, swap_num2))
                board[swap_num1], board[swap_num2] = board[swap_num2], board[swap_num1]
                for i in range(0, 3):
                    print(board[i * 3], board[i * 3 + 1], board[i * 3 + 2])
                print("---------------------------------------------")

        if process[step] == 'w':
            num = -3
        elif process[step] == 'a':
            num = -1
        elif process[step] == 's':
            num = 3
        elif process[step] == 'd':
            num = 1
        tmp = pos + num
        board[pos], board[tmp] = board[tmp], board[pos]
        pos = tmp
        for i in range(0, 3):
            print(board[i * 3], board[i * 3 + 1], board[i * 3 + 2])
        print("---------------------------------------------")

if __name__ == '__main__':
    t = time.time()
    request_steps, swap, uuid = get_api()
    pic_num1 = swap[0]
    pic_num2 = swap[1]
    pic_decode()
    image = Image.open('10.jpg')
    image_list = cut_image(image)
    save_images(image_list)
    board, string = All_compare()
    count = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(board)):
        if (board[i] == 0):
            continue
        count[board[i] - 1] = 1

    for i in range(len(board)):
        if count[i] == 1:
            final[i] = i + 1
        else:
            final[i] = 0

    steps, process, swap_num1, swap_num2 = Search().search(board)

    swap_num1 = swap_num1 + 1
    swap_num2 = swap_num2 + 1
    strOperation = "".join(process)
    swapPic = []
    swapPic.append(swap_num1)
    swapPic.append(swap_num2)
    data1 = {"operations" : strOperation, "swap" : swapPic}
    data = {"uuid" : uuid, "answer" : data1 }
    post_api(data)
    print('步数: {}'.format(steps))
    print('时间: {}s'.format(time.time() - t))
    print('识别字母: {}'.format(string))
    print('操作过程: {}'.format(strOperation))
    print('初始状态: {}'.format(board))
    print('交换图片: %d %d' % (pic_num1, pic_num2))
    print('交换步数: {}'.format(request_steps))

    #printProcess(board, process)
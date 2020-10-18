# -*-codeing = utf-8 -*-
# @Time :2020/10/13 22:26
# @Author : baiweidou
# @File : post_获取题目.py
# @Software :PyCharm
import requests,json
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
def get_undo():
    r = requests.get('http://47.102.118.1:8089/api/team/problem/49')
    uuid = []
    for i in r.json():
        uuid.append(i['uuid'])
    print(uuid)
    with open('get_list_file.txt','w') as f:
        for i in uuid:
            f.write(i)
            f.write('\n')
def get_rank():
    r = requests.get('http://47.102.118.1:8089/api/rank')
    print(r.json())
def get_start(uuid):
    url_json = 'http://47.102.118.1:8089/api/challenge/start/'+uuid
    data = {
        "teamid": 49,
        "token": "4357e1a5-d93a-4fc4-8b3b-008d2c9dcfba"
    }
    headers = {"Content-Type":"application/json"}
    r_json = requests.post(url_json.strip(),headers = headers,data = json.dumps(data))
    img = r_json.json()['data']['img']
    step = r_json.json()['data']['step']
    swap = r_json.json()['data']['swap']
    uuid = r_json.json()['uuid']
    chance = r_json.json()['chanceleft']
    print("剩余机会为 %s"%chance)
    with open('1.txt','w') as f:
        f.write(img)
    return (step , swap , uuid )
def submit(data):
    url_json = 'http://47.102.118.1:8089/api/challenge/submit'
    headers = {"Content-Type": "application/json"}
    r_json = requests.post(url_json.strip(), headers=headers, data=json.dumps(data))
    print(r_json.json())
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
    for i in range(1,10):
        path_one = '%d.jpg'%i
        #如果对比三次以上，还没有发现有两张图片相似，则跳出循环
        if i > 3 and count <= 1:
            break
        #每张分块和九张分块对比
        for j in range(1,10):
            path_two = r'.\无框字符分块\%d_%d.jpg'%(num,j)
            sim[i-1][j-1] = int(Pic_Compare(path_one,path_two))
            if sim[i-1][j-1] == 0:
                count += 1
                #编号
                code_list[i-1] = j
    #如果想似的块大于4，就认为是同一组图片，返回确认值
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
        Queue.put([self.goBackDistance(begin), begin, begin.index(0), 0, 0, 0, operation])
        vis = {begin}

        while Queue.not_empty:
            prioritynum, board, pos, steps, change_pos1, change_pos2, operation = Queue.get()

            if board == final:
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

                return steps, operation,change_pos1,change_pos2

            if request_steps == steps:
                board = list(board)
                board[pic_num1 - 1], board[pic_num2 - 1] = board[pic_num2 - 1], board[pic_num1 - 1]  # 交换图片

                count = 0  # 统计逆序数个数的奇偶性
                for i in range(len(board)):
                    if board[i] == 0:
                        continue
                    for j in range(i + 1, len(board)):
                        if board[j] == 0:
                            continue
                        if board[i] > board[j]:
                            count = count + 1

                if (count % 2) == 1:  # 奇数 — 无解
                    pos1, pos2 = self.quickExchange(board)
                    change_pos1 = pos1
                    change_pos2 = pos2
                    board[pos1], board[pos2] = board[pos2], board[pos1]

            pos = board.index(0)
            for i in (-1, 1, -3, 3):
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
                    vis.add(visboard)
                    tup1 = operation
                    tup2 = [i]
                    tup1 = tup1 + tup2
                    Queue.put([steps + 1 + self.goBackDistance(newboard), newboard, pos0, steps + 1, change_pos1, change_pos2, tup1])

    def quickExchange(self, board):
        min = 0xfffff
        dist = 0
        pic1 = 0
        pic2 = 0
        for i in range(len(board)):
            if board[i] == 0:
                continue
            for j in range(i + 1, len(board)):
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

if __name__ == '__main__':
    get_undo()
    get_rank()
    with open('get_list_file.txt','r') as f:
        uuid = f.readline()
    request_steps, swap, return_uuid = get_start(uuid)
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

    data ={
        "uuid": return_uuid ,
        "teamid": 49,
        "token": "4357e1a5-d93a-4fc4-8b3b-008d2c9dcfba",
        "answer": {
            "operations": strOperation,
            "swap": swapPic
        }
    }
    submit(data)
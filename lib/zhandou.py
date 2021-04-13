import os, time, random
import numpy as nu
import cv2 as cv

"""
img = cv.imread('../images/fgo-02.png')
img_chongenng = cv.imread('../images/fgo-chongeng.jpg')
img_gongji = cv.imread('../images/fgo-gongji.png')

img_zhandou = cv.imread('../images/fgo-zhandou.png')

img_hong = cv.imread('../images/fgo-hong.png')
img_lv = cv.imread('../images/fgo-lv.png')
img_lan = cv.imread('../images/fgo-lan.png')
"""
"""===== 技能使用 ===== """
""" 创建一个战斗技能识别坐标 """
def master_skill(img_1,fgo_master_skill):
    res = cv.matchTemplate(img_1,fgo_master_skill, cv.TM_CCOEFF_NORMED)
    if (res >= 0.9).any():
        loc = nu.where(res >= 0.9)
        for i in zip(*loc[::-1]):
            return i


def skill(img_1, img_2):
    res = cv.matchTemplate(img_1, img_2, cv.TM_CCOEFF_NORMED)
    skill_contrast = 0.859
    pos = []

    """ res 内部的图像数组进项对比。 大于0.9 可以继续 """

    if (res >= skill_contrast).any():
        """ 使用 any() 函数输出布尔值 只要有一个符合的  """
        loc = nu.where(res >= skill_contrast)
        for i in zip(*loc[::-1]):
            pos.append(i)
    return pos


def Skill_object(fgo_opt,opt_id):
    """ 对技能确认选择   fgo_opt"""
    os.system('adb shell screencap /sdcard/02.png')
    os.system('adb pull /sdcard/02.png images/zhandou.png')
    fgo_zhandou = cv.imread('images/zhandou.png')
    res = cv.matchTemplate(fgo_zhandou, fgo_opt, cv.TM_CCOEFF_NORMED)
    if (res >= 0.8).any():
        print('进入技能选择 英灵阶段')
        if opt_id == 'role_1':
            print('选择 英灵 1')
            os.system(f'adb shell input tap {random.randint(600,730)} {random.randint(630,730)}')
        elif opt_id =='role_2':
            print('选择 英灵 2')
            os.system(f'adb shell input tap {random.randint(1050,1150)} {random.randint(630,730)}')
        else:
            print('选择 英灵 3')
            os.system(f'adb shell input tap {random.randint(1500, 1600)} {random.randint(630,730)}')
    else:
        print('没有匹配到选择界面')
# print(skill(img,img1))
def role(pos, role_id,opt_id):
    """ 角色 1 2 3 进项筛选返回坐标 """
    if role_id == 'role_1':
        loc = pre(700, 300, 930, 800, pos, opt_id)
        return loc
    elif role_id == 'role_2':
        loc = pre(1160, 770, 930, 800, pos, opt_id)
        return loc
    elif role_id == 'role_3':
        loc = pre(1640, 1250, 930, 800, pos, opt_id)
        return loc
    elif role_id == 'master':
        loc = pre(1940, 1550, 630, 400, pos, opt_id)
        return loc


""" ==================== """


def pre(x_1, x_2, y_1, y_2, pos,opi_id):
    """ 属于 role 内置判断函数 用于筛选坐标 """
    for i in pos:
        x = i[0]
        y = i[1]
        # if 700 > x > 300 and 930 > y > 800:
        if x_1 > x > x_2 and y_1 > y > y_2:
            loc = (x, y, opi_id)
            return loc


"""===== 指令牌 使用 ===== """


def attack(img_1, img_2):
    # 点开攻击
    res = cv.matchTemplate(img_1, img_2, cv.TM_CCOEFF_NORMED)
    attack_contrast = 0.7
    if (res >= attack_contrast).any():
        loc = nu.where(res >= attack_contrast)
        for i in zip(*loc[::-1]):
            return i  # 取第一个坐标即可


def attack_choose(img_zhandou, img_1, img_2, img_3):
    """
        分别是 三张 红卡 绿卡 蓝卡
        函数会自动分辨出五张卡牌的 x，y轴 进行返回
    """
    red = []
    green = []
    blue = []
    ran = [(295, 608, 1), (688, 973, 2), (1045, 1372, 3), (1148, 1769, 4), (1832, 2146, 5)]
    # lst = [('红卡', img_1, red), ('绿卡', img_2, green), ('蓝卡', img_3, blue)]
    lst_dict = {'红卡': [img_1, red], '绿卡': [img_2, green], '蓝卡': [img_3, blue]}
    for i in lst_dict:
        res = cv.matchTemplate(img_zhandou, lst_dict[i][0], cv.TM_CCOEFF_NORMED)
        contrast = 0.8
        if (res >= contrast).any():
            loc = nu.where(res >= contrast)
            for Ran in ran:
                for y in zip(*loc[::-1]):
                    if Ran[1] > y[0] > Ran[0] and 927 > y[1] > 757:
                        lst_dict[i][1].append(y)
                        break
    return red, green, blue


def attact_color(red, green, blue, role_id):
    """
    将attack_choose 返回的 结果 进行筛选
    目前是 优先选择红卡，其次绿卡，之后蓝卡
     """
    card = []
    for i in role_id:
        # 第一个角色宝具卡位置
        if i == 'role_1':
            x = (800, 300)
            card.append(x)
        elif i == 'role_2':
            x = (1150, 300)
            card.append(x)
        elif i == 'role_3':
            pass
    if len(card) == 3:
        return card

    if len(red) != 0:
        for i in red:
            i = i + ('红卡',)
            print(i)
            card.append(i)
            if len(card) == 3:
                return card
    if len(green) != 0:
        for i in green:
            i = i + ('绿卡',)
            print(i)
            card.append(i)
            if len(card) == 3:
                return card
    for i in blue:
        i = i + ('蓝卡',)
        print(i)
        card.append(i)
        if len(card) == 3:
            return card



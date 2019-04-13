import itchat
import os
import PIL.Image as Image
from os import listdir
import math
import sys

print("请输入查询模式：0-显示所有好友头像，但最终矩形头像集最后一行可能残缺；1-头像集为完整矩形，但好友可能不全，即在0模式下舍弃最后一行")
mode = input()
if mode not in ("0", "1"):
    print("请按照正确格式输入！")
    sys.exit(0)


# itchat.auto_login(enableCmdQR=True) # 这种登录时控制台生成登录二维码
itchat.login()  # 这种登录是生成二维码图片在本地目录

friends = itchat.get_friends(update=True)[0:]   # 核心：得到frieds列表集，内含很多信息

user = friends[0]["UserName"]

w = open(user+"_friends", 'a', encoding='utf-8', errors='ignore')  # 将friends列表存下来，看看内容
for i in friends:
    w.write(str(i))

print("授权微信用户为："+user)

os.mkdir(user)  # 创建文件夹用于装载所有好友头像

num = 0

for i in friends:
    img = itchat.get_head_img(userName=i["UserName"])
    fileImage = open(user + "/" + str(num) + ".jpg", 'wb')
    fileImage.write(img)
    fileImage.close()
    num += 1

pics = listdir(user)    # 得到user目录下的所有文件，即各个好友头像

numPic = len(pics)

print("所有好友头像数：" + str(numPic))

# eachsize = int(math.sqrt(float(640 * 640) / numPic))    # 先圈定每个正方形小头像的边长，如果嫌小可以加大
eachsize = int(math.sqrt(float(numPic * numPic) / numPic))
print("小正方形头像边长：" + str(eachsize))


numrow = int(numPic / eachsize)
print("一行小头像数：" + str(numrow))

if mode == "0":
    numcol = int(math.ceil(numPic * 1.0 / numrow))   # 向上取整
else:
    numcol = int(numPic / numrow)    # 向下取整
    print("舍弃好友数：" + str(numPic - numrow * numcol))

toImage = Image.new('RGB', (eachsize*numrow, eachsize*numcol))  # 先生成头像集模板


x = 0   # 小头像拼接时的左上角横坐标
y = 0   # 小头像拼接时的左上角纵坐标


for i in pics:
    try:
        #打开图片
        img = Image.open(user + "/" + i)
    except IOError:
        print("读取完成")
    else:
        #缩小图片
        img = img.resize((eachsize, eachsize), Image.ANTIALIAS)
        #拼接图片
        toImage.paste(img, (x * eachsize, y * eachsize))
        x += 1
        if x == numrow:
            x = 0
            y += 1


toImage.save(user + ".jpg")

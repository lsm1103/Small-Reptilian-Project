from PIL import Image
import time

im = Image.open('zp/psb.jpg')
# print('-'*100)

# print(im.getdata())  #获取所有通道的值 类似生成器的对象
# print('-'*100)
# print(list(im.getdata(0)))  #获取第一个通道的值, 转化为列表

# 取通道图片
# R, G, B = im.split()	#split()方法返回的是一个元祖，元祖中的元素则是分割后的单个通道的图片。
# R.save('zp/'+'{}.png'.format(time.time()))
# X = im.getchannel("R")	#getchannel()可以获取单个通道的图片：
# X.save('zp/'+'{}.png'.format(time.time()))
# X.show()


# 裁剪图片
# croped_im = im.crop((100, 100, 200, 200))

# # 复制图像
# copyed_im = im.copy()
# copyed_im.show()
# # 粘贴图像
# croped_im = im.crop((100, 100, 200, 200))	#左上右下
# im.paste(croped_im, (50, 0))
# im.show()

# 调整图像大小
# resized_im = im.resize((1000, 1200))
# resized_im.show()

# 或者使用thumbnail（）方法
# im = Image.open('zp/psb.jpg')
# #获得图像尺寸
# w, h = im.size  
# # 缩放到50%
# im.thumbnail((w//2, h//2))  
# #显示图片
# im.show()

# 逆时针旋转90度
# im.show()
# im.rotate(90).show()
# time.sleep

# im.rotate(180).show()
# time.sleep

# im.rotate(20, expand=True).show()
# time.sleep

# 灰度化-灰度公式： R=G=B = 处理前的 RX0.3 + GX0.59 + B*0.11
# im.convert('L').show()


# 二值化选阈值，迭代法
# 增强对比度
# img = im.point(lambda x: 1.2*x)
# # 获取尺寸
# w, h = img.size
# # 灰度
# img = img.convert('L')
# # 获取像素
# pixes = img.load()
# total = []

# for i in range(w):
#     for j in range(h):
#         total.append(pixes[i,j])
# # 计算平均值
# avg = sum(total)//len(total)
# img.show()
# # 二值化
# out = img.point(lambda x: 0 if x< avg else 255)
# out.show()

# 等同于👇
# img.point(lambda x: 0 if x< avg else 255).show()

# 3.降噪
def noise_reduction(img):
    w, h = img.size
    pixes = img.load()
    # 先处理4条边
    # 顶边
    for i in range(w):
        if pixes[i,0] == 0:
            if pixes[i, 1] == 255:
                pixes[i, 0] = 255
    # 底边
    for i in range(w):
        if pixes[i,h-1] == 0:
            if pixes[i, h-2] == 255:
                pixes[i, h-1] = 255

    # 左边
    for i in range(h):
        if pixes[0, i] == 0:
            if [1, i] == 255:
                pixes[0, i] = 255

    # 右边
    for i in range(h):
        if pixes[w-1, i] == 0:
            if [w-2, i] == 255:
                pixes[w-1, i] = 255

    # 处理其他的点
    for i in range(1, w-1):
        for j in range(1, h-1):
            if pixes[i, j] == 0:
                sum = pixes[i+1, j] + pixes[i, j+1] + pixes[i-1, j] + pixes[i, j-1] + pixes[i-1, j-1] + pixes[i+1, j-1] + pixes[i+1, j+1] + pixes[i-1, j+1]
                if sum // 255 > 4:
                    pixes[i, j] = 255

    return img

img = noise_reduction(im)
img.show()
# img.close()

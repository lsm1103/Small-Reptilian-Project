# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author:小民 2019/6/29 20:41

# pytesseract简单使用
# try:
#     from PIL import Image
# except ImportError:
#     import Image

# import pytesseract

# # 如果路径中没有Tesseract可执行文件，请包括以下内容：
# pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
# # Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

# # 简单图像到字符串
# print(pytesseract.image_to_string(Image.open('zp/psb.jpg')))

# # 法语文本图像到字符串
# print(pytesseract.image_to_string(Image.open('zp/test-european.jpg'), lang='fra'))


# 使用pytesseract进行字符型图片验证码获取
import pytesseract
from PIL import Image

class Captcha:
    def __init__(self, img=None):
        if img:
            self.open(img)
        else:
            self.img = img

    def open(self, img):
        self.img = Image.open(img)

    def convert_tow_value(self):
        # 增强对比度
        self.img = self.img.point(lambda x: 1.2 * x)
        # 获取尺寸
        w, h = self.img.size
        # 灰度
        self.img = self.img.convert('L')
        # 获取像素
        pixes = self.img.load()

        total = []

        for i in range(w):
            for j in range(h):
                total.append(pixes[i, j])
        # 计算平均值
        avg = sum(total) // len(total)

        # 二值化
        self.img = self.img.point(lambda x: 0 if x < avg - 10 else 255)

    def noise_reduction(self):
        w, h = self.img.size
        pixes = self.img.load()
        # 先处理4条边
        # 顶边
        for i in range(w):
            if pixes[i, 0] == 0:
                if pixes[i, 1] == 255:
                    pixes[i, 0] = 255
        # 底边
        for i in range(w):
            if pixes[i, h - 1] == 0:
                if pixes[i, h - 2] == 255:
                    pixes[i, h - 1] = 255

        # 左边
        for i in range(h):
            if pixes[0, i] == 0:
                if [1, i] == 255:
                    pixes[0, i] = 255

        # 右边
        for i in range(h):
            if pixes[w - 1, i] == 0:
                if [w - 2, i] == 255:
                    pixes[w - 1, i] = 255

        # 处理其他的点
        for i in range(1, w - 1):
            for j in range(1, h - 1):
                if pixes[i, j] == 0:
                    sum = pixes[i + 1, j] + pixes[i, j + 1] + pixes[i - 1, j] + pixes[i, j - 1] + pixes[i - 1, j - 1] + \
                          pixes[i + 1, j - 1] + pixes[i + 1, j + 1] + pixes[i - 1, j + 1]
                    if sum // 255 > 4:
                        pixes[i, j] = 255

    def image_to_string(self):
        self.convert_tow_value()
        self.noise_reduction()
        pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
        return pytesseract.image_to_string(self.img)


if __name__ == '__main__':

    captcha = Captcha('zp/check.jpg')
    res = captcha.image_to_string()
    print(res)
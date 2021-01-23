import matplotlib.pyplot as plt  # 数学绘图库
from jieba import * # 分词库
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator  # 词云库
from PIL import Image
import numpy as np
import re

#公用函数
def Replace(text,old,new): #替换列表的字符串
    for char in old:
        text = text.replace(char,new)
    return text
#词云生成
def zn_wordcloudGenerater(filePath, fontPath, imagePath, imageSavePath, zn_STOPWORDS, zn_CPfilePath,isImageColor):
    '''
    中文词云图生成器
    :param filePath: 本地文本文件路径
    :param fontPath: 字体文件路径
    :param imagePath: 本地图片(最好是白底)路径
    :param imageSavePath: 词云图保存路径
    :param zn_STOPWORDS: 中文停用词(List类型)
    :param isImageColor: 是否使用背景图片颜色作为词的颜色(bool值)
    '''
    # 使用上下文管理器with读取本地文本文件
    with open(filePath, 'r', encoding='utf-8') as f:
        # 1、读入txt文本数据
        text = f.read()
        # 2.使用jieba进行中文分词;cut_all参数表示分词模式,True为全局模式,False为精确模式,默认为False
   
        
        #print(result)
        #特殊符号和部分无意义的词,去噪
        sign = '''！~·@￥……*“”‘’\n?#0（）/;:,.<>=_[]]{}【】；："'「，」。-、？'''
        text = re.sub("[A-Za-z0-9]", "", text)
        text = Replace(text,sign,"")
        cut_text = lcut(text)
        result = '/'.join(cut_text)
        #print(result)
        #stopwords.add('是')
        counts = {}             #创建计数器 --- 字典类型
        #词频统计
        words = cut_text
        frequencies = {}
        with open(zn_CPfilePath,'w',encoding='utf-8') as wf2:
            for word in words:      #消除同意义的词和遍历计数
                if word == '小五' or word == '小五郎' or word == '五郎':
                    rword = '毛利'
                elif word == '柯' or word == '南':
                    rword = '柯南'
                elif word == '小' or word == '兰':
                    rword = '小兰'
                elif word == '目' or word == '暮' or word == '警官':
                     rword = '暮目'
                else:
                    rword = word
                counts[rword] = counts.get(rword,0) + 1
            # 3、设置中文停用词(可通过add方法添加所需中文词汇或标点符号)
            excludes = zn_STOPWORDS
            cexcludes = lcut_for_search("　你我事他和她在这也有什么的是就吧啊吗哦呢都了一个")
            excludes.extend(cexcludes)
            for word in excludes:   #除去意义不大的词语
                 print(word)
                 if counts.get(word) != None:
                    del(counts[word])
            items = list(counts.items()) #转换成列表形式
            items.sort(key = lambda x : x[1], reverse = True ) #按次数排序
            N=0
            if N==0:
               N=len(items)
            for i in range(N):     #依次输出
                word,count = items[i]
                print("{:<7}{:>6}".format(word,count))
                frequencies[word] =count
                wf2.write(word+' '+str(count)+'\n') 
        stopwords = set(zn_STOPWORDS)
        # 4.1、获取本地背景图片
        image = np.array(Image.open(imagePath))
        if isImageColor:
        # 4.2、获取背景图片颜色
            image_colors = ImageColorGenerator(image)
        # 5、创建WordCloud实例并自定义设置参数(如背景色,背景图片和停用词等)
        wc = WordCloud(font_path=fontPath, background_color='white', max_words=3000,
                       mask=image, stopwords=stopwords, random_state=42, max_font_size=45,repeat=False,relative_scaling=0.5)
        # 6、根据设置的参数，统计词频并生成词云图
        #wc.generate(result)
        wc.generate_from_frequencies(frequencies)   #根据词频生成词云

        # 7、将生成的词云图保存在本地
        plt.figure('词云图')  # 指定所绘图名称
        if isImageColor:
            plt.imshow(wc.recolor(color_func=image_colors))  # 以图片的形式显示词云,并依据背景色重置词的颜色
        else:
            plt.imshow(wc)
        plt.axis('off')      # 关闭图像坐标系
        plt.show()           # 在IDE中显示图片
        wc.to_file(imageSavePath)  # 按照背景图的宽高度保存词云图

def txt2set(zn_StopWordPath):
    '''
    读取本地中文停用词文本并转换为列表
    :param zn_StopWordPath: 中文停用词文本路径
    :return stopWordList: 一个装有中文停用词的列表
    '''
    with open(zn_StopWordPath, 'r', encoding='utf-8') as f:
        text = f.read()
        stopWordList = text.split('\n')
        cexcludes = lcut_for_search("　你我事他和她在这也有什么的是就吧啊吗哦呢都了一个")
        stopWordList.extend(cexcludes)
        return stopWordList

if __name__ == '__main__':    
    # 本地中文文本文件路径
    zn_filePath = 'd:\\raquel.txt'
     # 生成词频文件路径
    zn_CPfilePath = 'd:\\CP.txt'

    # 本地中文字体路径
    zn_fontPath = 'C:/Windows/Fonts/msyh.ttc'
    # 本地图片(最好是白底)路径
    imagePath = 'd:\\g.png'
    # 词云图保存路径
    imageSavePath = 'd:\\cwordcloud.png'
    # 中文停用词文本路径
    zn_StopWordPath = 'd:\\zn_STOPWORDS.txt'
    # 中文词云图生成器
    zn_StopWordsList = txt2set(zn_StopWordPath)
    zn_wordcloudGenerater(zn_filePath, zn_fontPath, imagePath, imageSavePath, zn_StopWordsList,zn_CPfilePath,False)
import os
import qrcode
import random
import time
import tkinter
from pystrich.ean13 import EAN13Encoder
import tkinter.filedialog
import tkinter.messagebox
from string import digits

#tkinter模块为python的标准图形界面接口，建立根窗口
root = tkinter.Tk()
#初始化数据
number = '1234567890'
letter = 'ABCDEFGHIJKLMNOBQRSTUVWXYZ1234567890'
allis = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()_+"
i = 0

randstr = []
fourth = []
fifth = []
randfir = ''
randsec = ''
randthr = ''
str_one = ''
strone = ''
strtwo = ''
nextcard = ''
userput = ''
nres_letter = ''

#创建文件夹
#若文件夹不存在则创建文件夹
def mkdir(path):
    isexists = os.path.exists(path)
    if not isexists:
        os.mkdir(path)

#读取文件夹内容并返回
def openfile(filename):
    f = open(filename)
    fllist = f.read()
    f.close()
    return fllist

#对输入数字、字母和位数的验证
#showstr为input函数提供动态输入提示文字，showorder提供验证方式，length提供要求输入数据的长度
#输入正确返回输入值 输入错误返回0并要求重新输入
def input_check(showstr,showorder,length):
    inputstr = input(showstr)
    if len(inputstr) != 0:
        #根据输入数据的要求，分成三种验证方式验证，1：数字，不限位数；2：字母；3：数字且有位数要求
        if showorder == 1:#验证方式
            if str.isdigit(inputstr):#验证是否为数字
                if inputstr == 0:
                    print("\033[1;31;40m 输入为零，请重新输入！！\033[0m")
                    return "0"
                else:
                    return inputstr
            else:
                print("\033[1;31;40m 输入错误，请重新输入！！\033[0m")
                return "0"
        if showorder == 2:
            if str.isalpha(inputstr):
                if len(inputstr) != length:
                    print("\033[1;31;40m必须输入相应个字母数，请重新输入！！\033[0m")
                    return "0"
                else:
                    return inputstr
            else:
                print("\033[1;31;40m 输入错误，请重新输入！！\033[0m")
                return "0"
        if showorder == 3:
            if str.isdigit(inputstr):
                if len(inputstr) != length:
                    print("\033[1;31;40m 必须输入相应个数字数，请重新输入！！\033[0m")
                    return "0"
                else:
                    return inputstr
            else:
                print("\033[1;31;40m 输入错误，请重新输入！！\033[0m")
                return "0"
    else:
        print("\033[1;31;40m 输入为空，请重新输入！！\033[0m")
        return "0"

#实现屏幕输出和文件输出编码信息，参数outfile设置输出的文件名称
#sstr 生成的防伪码,sfile 保存防伪码的文件,typeis 输出完成后是否通过信息框提示
# smsg 信息框显示的提示内容,datapath 保存防伪码的路径
def readinfo(sstr,sfile,typeis,smsg,datapath):
    mkdir(datapath)#创建文件夹
    datafile = datapath + "\\" + sfile
    file = open(datafile,'w')
    wrlist = sstr#将防伪码信息赋值给wrlist
    pdata = ""  # 清空变量pdata，pdata存储屏幕输出的防伪码信息
    wdata = ""  # 清空变量 wdata ， wdata 存储保存到文本文件的防伪码信息
    for i in range(len(wrlist)):  # 按条循环读取防伪码数据
        wdata = str(wrlist[i].replace('[', '')).replace(']', '')  # 去掉字符的中括号
        wdata = wdata.replace(''''','').replace(''''', '')  # 去掉字符的引号
        file.write(str(wdata))  # 写入保存防伪码的文件
        pdata = pdata + wdata  # 将单条防伪码存储到pdata 变量
    file.close()
    print("\033[1;31m" + pdata + "\033[0m")#输出生成的防伪码信息
    if typeis != "no":#显示信息提示框
        tkinter.messagebox.showinfo("提示",smsg + str(len(randstr)) + "\n 防伪码文件存放位置：" + datafile)
        root.withdraw()#关闭辅助窗口

#数据分析功能函数 scount为要生成的防伪码数量，typestr为数据分析字符（三位字母）
#ismessage在输出完成时是否显示提示信息 为no不显示  outfile设置输出的文件名称
def ffcode(scount,typestr,ismessage,outfile):
    randstr.clear()#清空保存批量注册码信息的变量randstr
    for j in range(int(scount)):#按数量生成含数据分析功能注册码
        strpro = typestr[0].upper()#取得三个字母中的第一个字母，并转为大写，区域分析码
        strtype = typestr[1].upper()# 取得三个字母中的第二个字母，并转为大写，颜色分析码
        strclass = typestr[2].upper()# 取得三个字母中的第三个字母，并转为大写，版本分析码
        randfir = random.sample(number,3)# 随机抽取防伪码中的三个位置，不分先后
        randsec = sorted(randfir)#对抽取的位置进行排序并存储给randsec变量，以便按顺序排列三个字母的位置
        letterone = ""#清空存储单条防伪码的变量letterone
        for i in range(9):#生成9位数字防伪码
            letterone = letterone + random.choice(number)
        #将三个字母按randsec变量中存储的位置值添加到数字防伪码中，并放到sim变量中
        sim = str(letterone[0:int(randsec[0])]) + strpro + str(
            letterone[int(randsec[0]):int(randsec[1])]) + strtype + str(
            letterone[int(randsec[1]):int(randsec[2])]) + strclass + str(
            letterone[int(randsec[2]):9]) + "\n"
        randstr.append(sim)#将组合生成的新防伪码添加到randstr变量
    readinfo(randstr,typestr + "scode" + str(outfile) + ".txt",ismessage,"生成含数据分析防伪码总计：","codepath")

#对系统主菜单的输入进行验证，判断输入是否合法
def input_validation(input):
    if str.isdigit(input):
        input = int(input)
        return input
    else:
        print("\033[1;31;40m       输入非法，请重新输入！！\033[0m")
        return 0


#系统主菜单
def mainMenu():
    print("""\033[1;35m
          ****************************************************************
                                企业编码生成系统
          ****************************************************************
              1.生成6位数字防伪编码 （213563型）
              2.生成9位系列产品数字防伪编码(879-335439型)
              3.生成25位混合产品序列号(B2R12-N7TE8-9IET2-FE35O-DW2K4型)
              4.生成含数据分析功能的防伪编码(5A61M0583D2)
              5.智能批量生成带数据分析功能的防伪码
              6.后续补加生成防伪码(5A61M0583D2)
              7.EAN-13条形码批量生成
              8.二维码批量输出          
              9.企业粉丝防伪码抽奖
              0.退出系统
          ================================================================
          说明：通过数字键选择菜单
          ================================================================
        \033[0m""")

#生成6位防伪码函数，参数outfile设置输出的文件名称
def number1(choice):
    incount = input_check("\033[1;32m     请输入您要生成验证码的数量:\33[0m", 1, 0)
    while int(incount) == 0:
        incount = input_check("\033[1;32m     请输入您要生成验证码的数量:\33[0m", 1, 0)
    randstr.clear()#清空保存批量注册码信息的变量randstr
    for j in range(int(incount)):#根据输入的验证码数量循环批量生成注册码
        randfir = ''#设置存储单条注册码的变量为空
        for i in range(6):#循环生成单条注册码 六位数字防伪码
            randfir = randfir + random.choice(number)#产生数字随机因子
        randfir = randfir + "\n"#在单条注册码后面添加转义换行字符“\n”，使验证码单条例显示
        randstr.append(randfir)#将单条注册码添加到保存批量验证码的变量randstr
    #调用函数 readinfo(),实现生成的防伪码屏幕输出和文件输出
    readinfo(randstr,"scode"+str(choice)+".txt","","已生成6位防伪码共计：","codepath")

#生成9位系列产品数字防伪编码函数：三位产品系列码+六位防伪码
def number2(choice):
    ordstart = input_check("\033[1;32m     请输入系列产品的数字起始号（3位）:\33[0m", 3, 3)
    while int(ordstart) == 0:
        ordstart = input_check("\033[1;32m     请输入系列产品的数字起始号（3位）:\33[0m", 3, 3)
    ordcount = input_check("\033[1;32m     请输入产品系列的数量:", 1, 0)
    #如果输入的产品系列数量小于1或者大于999.则要求重新输入
    while int(ordcount) < 1 or int(ordcount) > 999:
        ordcount = input_check("\033[1;32m     请输入产品系列的数量:", 1, 0)
    incount = input_check("\033[1;32m     请输入要生成的每个系列产品的防伪码数量:\33[0m", 1, 0)
    while int(incount) == 0:
        incount = input_check("\033[1;32m     请输入要生成的每个系列产品的防伪码数量:\33[0m", 1, 0)
    randstr.clear()#清空保存批量注册码信息的变量randstr
    for m in range(int(ordstart)):#分类产品编号
        for j in range(int(incount)):#产品防伪码编号
            randfir = ''
            for i in range(6):
                randfir = randfir + random.choice(number)#每次生成一个随机因子
            randstr.append(str(int(ordstart)+m)+randfir+"\n")#将生成的单条防伪码添加到防伪码列表
    #调用函数readinfo(),实现生成的防伪码屏幕输出和文件输出
    readinfo(randstr,"scode"+str(choice)+".txt","","已生成9位系列产品防伪码共计：","codepath")

#生成25位混合产品序列号函数（将6位拓展到25位）
def number3(choice):
    incount = input_check("\033[1;32m     请输入要生成的25位混合产品序列号数量:\33[0m", 1, 0)
    while int(incount) == 0:
        incount = input_check("\033[1;32m     请输入要生成的25位混合产品序列号数量:\33[0m", 1, 0)
    randstr.clear()#清空保存批量注册码信息的变量randstr
    for j in range(int(incount)):#按输入数量生成防伪码
        strone = ''#保存生成的单条防伪码，不带横线- ，循环时清空
        for i in range(25):
            strone = strone + random.choice(letter)#每次生成一个随机因子
            #将生成的防伪码每隔5位添加横线-
        strtwo = strone[:5] + "-" + strone[5:10] + "-" + strone[10:15] + "-" + strone[15:20]+\
                 "-" + strone[20:25] + "\n"
        randstr.append(strtwo)#将防伪码添加到列表
    readinfo(randstr,"scode" + str(choice) + ".txt", "", "已生成25位混合防伪序列码共计：","codepath")

#生成含有数据分析功能的防伪码函数(将三位数字换成三位字母)
def number4(choice):
    intype = input_check("\033[1;32m     请输入数据分析编号（3位字母）:\33[0m", 2, 3)
    while not str.isalpha(intype) or len(intype)!=3:
        intype = input_check("\033[1;32m     请输入数据分析编号（3位字母）:\33[0m", 2, 3)
    incount = input_check("\033[1;32m     请输入要生成的带数据分析功能的验证码数量:\33[0m", 1, 0)
    while int(incount) == 0:
        incount = input_check("\033[1;32m     请输入要生成的带数据分析功能的验证码数量:\33[0m", 1, 0)
    ffcode(incount,intype,"",choice)

#智能批量生成带数据分析功能的防伪码
def number5(choice):
    default_dir =r"mrsoft.mri"#设置默认打开的文件名称
    #打开文件选择对话框，指定打开的文件名称为‘mrsoft.mri’，拓展名为mri，可使用记事本和编辑器打开
    file_path = tkinter.filedialog.askopenfilename(
        filetypes = [("Text File","*.mri")],title = u"请选择自动防伪码智能批处理文件：",
        initialdir = (os.path.expanduser(default_dir)))
    codelist = openfile(file_path)#读取从文件选择对话框中的文件
    print("数据分析编号和防伪码数量为：",codelist)
    codelist = codelist.split("\n")#把读取的信息内容添加回车，以便列输出显示
    print("智能生成的数据分析防伪码为：",codelist)
    for item in codelist:#按读取的信息循环生成防伪码
        codea = item.split(",")[0]# 每一行信息中用 ","分割，","前面的信息存储防伪码标准信息
        codeb = item.split(",")[1]# 每一行信息中用 ","分割，","后面的信息存储防伪码生成的数量
        ffcode(codeb,codea,"no",choice) # 调用ffcode函数批量生成同一标识信息的防伪码

#  后续补加生成防伪码函数，防伪码格式为带数据分析功能注册码
def number6(choice):
    default_dir = r"./codepath/scode1.txt"#打开已经生成的防伪码文件
    #按默认的文件名称打开文件选择对话框，用于打开已经存在的防伪码文件
    file_path = tkinter.filedialog.askopenfilename(title=u"请选择已经生成的防伪码文件",
                                                   initialdir=(os.path.expanduser(default_dir)))
    codelist = openfile(file_path)#读取从文件选择对话框选中的文件
    codelist = codelist.split("\n")#把读取的信息内容添加回车，以便列输出显示
    codelist.remove("")
    strset = codelist[0]
    remove_digits = strset.maketrans("","",digits)#用maketrans方法创建删除数字的字符映射转换表
    res_letter = strset.translate(remove_digits)#根据字符映射转换表删除该条防伪码中的数字，获取字母标识信息
    nres_letter = list(res_letter)#把信息用列表变量nres—letter存储
    strpro = nres_letter[0]#从列表变量中取得第一个字母，即区域分析码
    strtype = nres_letter[1]#从列表变量中取得第二个字母，即色彩分析码
    strclass = nres_letter[2]#从列表变量中取得第三个字母，即版次分析码
    #去除信息中的括号和引号
    nres_letter = strpro.replace(''''','').replace(''''', '') + strtype.replace(
        ''''','').replace(''''', '') + strclass.replace(''''','').replace(''''', '')
    card = set(codelist)#将原有防伪码放到集合变量card中
    #利用tkinter的messagebox提示用户之前生成的防伪码数量
    tkinter.messagebox.showinfo("提示","之前的防伪码共计："+ str(len(card)))
    root.withdraw()#关闭提示信息框
    incount = input_check("请输入补充验证码生成的数量：",1,0)#让用户输入新补充生成的防伪码数量
    #最大值按输入生成数量的2倍数量生成新防伪码，防止新生成防伪码与原有防伪码重复造成新生成的防伪码数量不够
    for j in range(int(incount) * 2):
        randfir = random.sample(number,3)#随机生成三位不重复的数字
        randsec = sorted(randfir)#对产生的数字排序
        addcount = len(card)#记录集合中防伪码的总数量
        strone = ""#清空存储单条防伪码的变量strone
        for i in range(9):#生成9位数字防伪码
            strone = strone + random.choice(number)
        #将三个字母按randsec变量中存储的位置值添加到数字防伪码中，并放到sim变量
        sim = str(strone[0:int(randsec[0])]) + strpro + str(
            strone[int(randsec[0]):int(randsec[1])]) + strtype + str(
            strone[int(randsec[1]):int(randsec[2])]) + strclass + str(strone[int(randsec[2]):9]) + "\n"
        card.add(sim)#添加新生成的防伪码到集合
        #如果添加到集合，证明生成的防伪码与原有的防伪码没有产生重复
        if len(card) > addcount:
            randstr.append(sim)#添加新生成的防伪码到新防伪码列表
            addcount = len(card)#记录添加最新生成防伪码集合的防伪码数量
        if len(randstr) >= int(incount):#如果新防伪码列表中的防伪码数量达到输入的防伪码数量
            print(len(randstr))#输出已生成防伪码的数量
            break
    readinfo(randstr,nres_letter + "ncode" + str(choice) +".txt",nres_letter,"生成后补防伪码总计：","codeadd")

#条形码EAN13批量生成函数
def number7(choice):
    mainid = input_check("\033[1;32m     请输入EN13的国家代码（3位） :\33[0m", 3, 3)#输入三位国家代码
    compid = input_check("\033[1;32m     请输入EAN13的企业代码（4位）:\33[0m", 3, 4)#输入四位企业代码
    incount = input_check("\033[1;32m     请输入要生成的条形码数量:\33[0m", 1, 0)#输入要生成的条形码数量
    while int(incount) == 0:
        incount = input_check("\033[1;32m     请输入要生成的条形码数量:\33[0m", 1, 0)  # 输入要生成的条形码数量
    mkdir("barcode")#判断保存条形码的文件是否存在，若不存在则创建
    for j in range(int(incount)):#批量生成条形码
        strone = ''
        for i in range(5):#生成条形码的5位 3+4+5=12 还有一位是校验位
            strone = strone + str(random.choice(number))
        barcode = mainid + compid + strone#生成12位的条形码
        #计算条形码的校验位
        evensum = int(barcode[1]) + int(barcode[3]) + int(barcode[5]) + int(barcode[7]) +\
        int(barcode[9]) + int(barcode[11])
        oddsum = int(barcode[0]) + int(barcode[2]) + int(barcode[4]) + int(barcode[6]) +\
        int(barcode[8]) + int(barcode[10])
        checkbit = int((10-(evensum*3+oddsum)%10)%10)#计算校验位
        barcode = barcode + str(checkbit)#组成完整的13位EAN13条形码
        print(barcode)
        encoder = EAN13Encoder(barcode)#生成条形码
        encoder.save("barcode\\" + barcode + ".png")#保存条形码信息图片

#生成固定的12为二维码，也可根据需要修改为按输入位数进行生成
def number8(choice):
    #输入要生成的二维码数量
    incount = input_check("\033[1;32m     请输入要生成的12位数字二维码数量:\33[0m", 1, 0)
    while int(incount) == 0:
        incount = input_check("\033[1;32m     请输入要生成的12位数字二维码数量:\33[0m", 1, 0)
    mkdir("qrcode")#判断保存二维码的文件是否存在
    for j in range(int(incount)):
        strone = ''#清空存储单条二维码的变量
        for i in range(12):#生成12为二维码
            strone = strone + str(random.choice(number))
        encoder = qrcode.make(strone)#生成二维码文件
        encoder.save("qrcode\\" + strone + ".png")#保存二维码文件

#抽奖函数
def number9(choice):
    default_dir = r"lottery.ini"#设置默认打开文件为开发路径下的lottery.ini文件
    #选择包含用户抽奖信息票号的文件，拓展名为“*.ini”
    file_path = tkinter.filedialog.askopenfilename(filetypes=[("ini file","*.ini")],
        title=u"请选择抽奖号码的抽奖文件：",initialdir=(os.path.expanduser(default_dir)))
    codelist = openfile(file_path)#读取打开的抽奖文件
    codelist = codelist.split("\n")#通过换行转义符把抽奖信息分割成抽奖数列
    incount = input_check("\033[1;32m     请输入要生成的中奖数量:\33[0m", 1, 0)#要求用户输入中（抽奖）奖数量
    while int(incount) == 0 or len(codelist)<int(incount):
        incount = input_check("\033[1;32m     请输入要生成的中奖数量:\33[0m", 1, 0)  # 要求用户输入中（抽奖）奖数量
    strone = random.sample(codelist,int(incount))#根据输入的中（抽）数量进行抽奖

    print('\033[1;35m     抽奖信息名单发布：   \33[0m')
    for i in range(int(incount)):
        wdata = str(strone[i].replace('[','')).replace(']','')#循环将抽奖数列的引号和中括号去掉
        wdata = wdata.replace('''''.'').replace(''''','')#将抽奖数列的引号去掉
        print("\033[1;32m         " +  wdata  + "\33[0m")#输出中奖信息


def main():
    while 1:
        mainMenu()
        choice = input("\033[1;32m     请输入您要操作的菜单选项:\33[0m")
        choice = input_validation(choice)
        if choice == 0:
            break
        if choice == 1:
            number1(str(choice))
        if choice == 2:
            number2(str(choice))
        if choice == 3:
            number3(str(choice))
        if choice == 4:
            number4(str(choice))
        if choice == 5:
            number5(str(choice))
        if choice == 6:
            number6(str(choice))
        if choice == 7:
            number7(str(choice))
        if choice == 8:
            number8(str(choice))
        if choice == 9:
            number9(str(choice))

if __name__ == '__main__':
    main()

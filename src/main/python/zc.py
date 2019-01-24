#coding=utf-8

# TensorFlow and tf.keras
import tensorflow as tf
#from tensorflow import keras
import keras
# Helper libraries
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os

d1={'负':0,'平':1,'胜':2}
d2={0:'负',1:'平',2:'胜'}
days2={'一':1, '二':2, '三':3, '四':4, '五':5, '六':6, '日':7}
teams1={1:'比甲', 2:'墨超', 3:'英足总杯', 4:'解放者杯', 5:'俄罗斯杯', 6:'亚运男足', 7:'荷超杯', 8:'德超杯', 9:'中国杯', 10:'阿超杯', 11:'苏超', 12:'英甲', 13:'英联赛杯', 14:'葡萄牙杯', 15:'葡联赛杯', 16:'巴甲', 17:'国际赛', 18:'欧青预赛', 19:'美职足', 20:'意大利杯', 21:'英乙', 22:'墨超杯', 23:'瑞典杯', 24:'中北美冠', 25:'四强赛', 26:'世青赛', 27:'金杯赛', 28:'奥运男足', 29:'德乙', 30:'荷乙', 31:'欧国联', 32:'智利杯', 33:'韩足总杯', 34:'德国杯', 35:'公开赛杯', 36:'优胜者杯', 37:'杯赛', 38:'俱乐部赛', 39:'欧青赛', 40:'英超', 41:'荷兰杯', 42:'欧罗巴', 43:'日乙', 44:'挪超', 45:'亚运女足', 46:'比超杯', 47:'墨冠杯', 48:'世界杯', 49:'圣保罗锦', 50:'世预赛', 51:'非洲杯', 52:'荷甲', 53:'意甲', 54:'世俱杯', 55:'俱乐部杯', 56:'智利甲', 57:'瑞超', 58:'国王杯', 59:'亚冠', 60:'巴西杯', 61:'国冠杯', 62:'苏足总杯', 63:'女欧洲杯', 64:'联合会杯', 65:'意超杯', 66:'西甲', 67:'葡超', 68:'德甲', 69:'欧冠', 70:'韩职', 71:'阿根廷杯', 72:'挪威杯', 73:'澳杯', 74:'社区盾杯', 75:'葡超杯', 76:'英冠', 77:'法联赛杯', 78:'比利时杯', 79:'东南亚锦', 80:'阿甲', 81:'法国杯', 82:'日职', 83:'天皇杯', 84:'法超杯', 85:'亚青赛', 86:'智超杯', 87:'亚预赛', 88:'澳超', 89:'法甲', 90:'法乙', 91:'俄超', 92:'英锦标赛', 93:'苏联赛杯', 94:'墨西哥杯', 95:'日联赛杯', 96:'俄超杯', 97:'欧超杯', 98:'西超杯', 99:'挪超杯', 100:'日超杯', 101:'女四强赛', 102:'奥运女足'}
teams2={'比甲':1, '墨超':2, '英足总杯':3, '解放者杯':4, '俄罗斯杯':5, '亚运男足':6, '荷超杯':7, '德超杯':8, '中国杯':9, '阿超杯':10, '苏超':11, '英甲':12, '英联赛杯':13, '葡萄牙杯':14, '葡联赛杯':15, '巴甲':16, '国际赛':17, '欧青预赛':18, '美职足':19, '意大利杯':20, '英乙':21, '墨超杯':22, '瑞典杯':23, '中北美冠':24, '四强赛':25, '世青赛':26, '金杯赛':27, '奥运男足':28, '德乙':29, '荷乙':30, '欧国联':31, '智利杯':32, '韩足总杯':33, '德国杯':34, '公开赛杯':35, '优胜者杯':36, '杯赛':37, '俱乐部赛':38, '欧青赛':39, '英超':40, '荷兰杯':41, '欧罗巴':42, '日乙':43, '挪超':44, '亚运女足':45, '比超杯':46, '墨冠杯':47, '世界杯':48, '圣保罗锦':49, '世预赛':50, '非洲杯':51, '荷甲':52, '意甲':53, '世俱杯':54, '俱乐部杯':55, '智利甲':56, '瑞超':57, '国王杯':58, '亚冠':59, '巴西杯':60, '国冠杯':61, '苏足总杯':62, '女欧洲杯':63, '联合会杯':64, '意超杯':65, '西甲':66, '葡超':67, '德甲':68, '欧冠':69, '韩职':70, '阿根廷杯':71, '挪威杯':72, '澳杯':73, '社区盾杯':74, '葡超杯':75, '英冠':76, '法联赛杯':77, '比利时杯':78, '东南亚锦':79, '阿甲':80, '法国杯':81, '日职':82, '天皇杯':83, '法超杯':84, '亚青赛':85, '智超杯':86, '亚预赛':87, '澳超':88, '法甲':89, '法乙':90, '俄超':91, '英锦标赛':92, '苏联赛杯':93, '墨西哥杯':94, '日联赛杯':95, '俄超杯':96, '欧超杯':97, '西超杯':98, '挪超杯':99, '日超杯':100, '女四强赛':101, '奥运女足':102}

#name='毕尔巴鄂竞技'
#name='维戈塞尔塔'

#导入数据集
train_pl=[]
train_labels=[]
test_pl=[]
test_labels=[]
#file1=open('./zc/2017-01-01~2019-01-05_1.txt','r+')
file1=open('./og1.txt','r+')
for l in file1.readlines():
    #if l.split(',')[2]==name or l.split(',')[3]==name:
    #if (l.split(',')[2]=='利物浦' and l.split(',')[3]=='阿森纳') or (l.split(',')[2]=='阿森纳' and l.split(',')[3]=='利物浦'):
    pl=[float(x) for x in l.split(',')[4:7]]
    #pl.append(teams2[l.split(',')[1]])
    #pl.append(days2[l.split(',')[0][1]])
    pls2=[]
    for y in pl:
        pls=[]
        pls.append(y)
        pls2.append(pls)
    train_pl.append(pls2)
    lable=d1[l.split(',')[-1].replace('\n','')]
    train_labels.append(lable)
file1.close()
#file2=open('./zc/2017-01-01~2019-01-05_2.txt','r+')
file2=open('./og2.txt','r+')
for l in file2.readlines():
    #if l.split(',')[2]==name or l.split(',')[3]==name:
    #if (l.split(',')[2]=='利物浦' and l.split(',')[3]=='阿森纳') or (l.split(',')[2]=='阿森纳' and l.split(',')[3]=='利物浦'):
    #if l.split(',')[2]=='阿森纳' or l.split(',')[3]=='阿森纳':
    pl=[float(x) for x in l.split(',')[4:7]]
    #pl.append(teams2[l.split(',')[1]])
    #pl.append(days2[l.split(',')[0][1]])
    pls2=[]
    for y in pl:
        pls=[]
        pls.append(y)
        pls2.append(pls)
    test_pl.append(pls2)
    lable=d1[l.split(',')[-1].replace('\n','')]
    test_labels.append(lable)

file2.close()
train_pl=np.array(train_pl)
train_labels=np.array(train_labels)
test_pl=np.array(test_pl)
test_labels=np.array(test_labels)

print(train_pl.shape)
print(test_pl.shape)

#设置层
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(3,1)),         #第一层，将输入数据从二维数组(1*3)转换成一维数组(1*3=3)
    keras.layers.Dense(100, activation=tf.nn.relu),     #第一个密集层，3个神经元，采用relu方法
    keras.layers.Dense(3, activation=tf.nn.softmax)    #第二个密集层，3个神经元，采用softmax（判断各个概率）
])

model.compile(optimizer=tf.train.AdamOptimizer(), loss='sparse_categorical_crossentropy', metrics=['accuracy']) 

def test1(i,model1):
    predictions = model1.predict(test_pl)    #对测试集进行预测试
    print(predictions[i])
    #print(np.argmax(predictions[i]))
    print('预测：'+d2[np.argmax(predictions[i])])
    print('正确：'+d2[test_labels[i]])

c_pl=[[[2.25],[3.05],[2.80]]]
c_pl=np.array(c_pl)
print(c_pl)
def test2(model1):
    predictions = model1.predict(c_pl)    #对测试集进行预测试
    #print(predictions[0])
    print(np.argmax(predictions[0]))
    print('预测：'+d2[np.argmax(predictions[0])])

model.fit(train_pl, train_labels, epochs=15)
model.save_weights('my_checkpoint')    #手动保存权重

model.load_weights('my_checkpoint')
test1(18,model)
print(test_pl[18])

#model.load_weights('my_checkpoint_'+name)
#test2(model)

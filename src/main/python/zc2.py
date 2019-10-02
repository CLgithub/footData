#coding=utf-8

# 最基础的，利用keras，通过胜平负赔率预测胜平负结果，训练结果保存在my_checkpoint中

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
import cx_Oracle

d1={'胜':0,'平':1,'负':2}
d2={0:'胜',1:'平',2:'负'}
days2={'一':1, '二':2, '三':3, '四':4, '五':5, '六':6, '日':7}
user='user1'
pwd='123456'
dburl='localhost:1521/xe'
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'    #select userenv('language') from dual 先查询编码

def func1():
    getData() #导入数据库数据
    #应该加入k折验证，
    train_pl,train_labels,test_pl,test_labels = getDataForFile()
    print(train_pl.shape)
    print(train_pl[0])
    print(train_labels.shape)
    print(train_labels[0])
    model=setF()
    model=learn(model,train_pl,train_labels,test_pl,test_labels)
    #model.load_weights('my_checkpoint')

    #test1(test_pl,test_labels,1,model)

    c_pl=[[[1.22],[4.70],[8.00]]]
    c_pl=np.array(c_pl)
    test2(c_pl,model)

def getData():
    f1=open('./traindata.txt','w')
    f2=open('./testdata.txt','w')
    #导入数据集
    traindata=[]
    testdata=[]
    conn=cx_Oracle.connect(user, pwd, dburl)
    cursor = conn.cursor()
    cursor.prepare("select * from T_FOOTBALL_DATA_1 where odds1!=0 and odds2!=0 and odds3!=0 "+
            "and leagid=:leagid and vsdate>to_date('2016-06-01','yyyy-MM-dd') order by vsdate asc")
    r=cursor.execute(None, {'leagid':165})
    vss1=cursor.fetchmany(900)
    vss2=cursor.fetchall()
    for vs in vss1:
        for vsdata in vs:
            f1.write(str(vsdata)+',')
        f1.write('\n')
    for vs in vss2:
        for vsdata in vs:
            f2.write(str(vsdata)+',')
        f2.write('\n')
    f1.close()
    f2.close()
    cursor.close()
    conn.close()

def getDataForFile():
    train_pl=[]
    train_labels=[]
    test_pl=[]
    test_labels=[]
    f1=open('./traindata.txt','r+')
    for l in f1.readlines():
        pl=[float(x) for x in l.split(',')[8:11]]
        pls2=[]
        for y in pl:
            pls=[]
            pls.append(y)
            pls2.append(pls)
        train_pl.append(pls2)
        lable=d1[l.split(',')[-2]]
        train_labels.append(lable)
    f1.close()
    f2=open('./testdata.txt','r+')
    for l in f2.readlines():
        pl=[float(x) for x in l.split(',')[8:11]]
        pls2=[]
        for y in pl:
            pls=[]
            pls.append(y)
            pls2.append(pls)
        test_pl.append(pls2)
        lable=d1[l.split(',')[-2]]
        test_labels.append(lable)
    f2.close()

    train_pl=np.array(train_pl)
    train_labels=np.array(train_labels)
    test_pl=np.array(test_pl)
    test_labels=np.array(test_labels)
    #print(train_pl[0])
    #print(test_pl[0])
    return train_pl,train_labels,test_pl,test_labels

def setF():
    #设置层
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(3,1)),         #第一层，将输入数据从二维数组(1*3)转换成一维数组(1*3=3)
        keras.layers.Dense(12, activation=tf.nn.relu),     #第一个密集层，3个神经元，采用relu方法
        keras.layers.Dense(12, activation=tf.nn.relu),     #第一个密集层，3个神经元，采用relu方法
        keras.layers.Dense(3, activation=tf.nn.softmax)    #第二个密集层，3个神经元，采用softmax（判断各个概率）
    ])
    #model.compile(optimizer=tf.train.AdamOptimizer(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.compile(optimizer='rmsprop', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

def learn(model,train_pl,train_labels,test_pl,test_labels):
    model.fit(train_pl, train_labels, epochs=15, validation_data=(test_pl, test_labels))
    model.save_weights('my_checkpoint')    #手动保存权重
    return model

def test1(test_pl,test_labels,i,model1):
    predictions = model1.predict(test_pl)    #对测试集进行预测试
    print('赔率信息：'+str(test_pl[i]))
    print('胜平负概率分别：'+str(predictions[i]))
    print('预测：'+d2[np.argmax(predictions[i])])
    print('正确：'+d2[test_labels[i]])

def test2(pl,model1):
    predictions = model1.predict(pl)    #对测试集进行预测试
    print('赔率信息：'+str(pl))
    print('胜平负概率分别：'+str(predictions[0]))
    print('预测：'+d2[np.argmax(predictions[0])])


#model.load_weights('my_checkpoint_'+name)
#test2(model)
func1()

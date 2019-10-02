#coding=utf-8
# k折验证，胜平负赔率，获取胜平负概率
# TensorFlow and tf.keras
import tensorflow as tf
import keras
# Helper libraries
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os
import cx_Oracle
from keras import models
from keras import layers

d1={'胜':0,'平':1,'负':2}
d2={0:'胜',1:'平',2:'负'}

days2={'一':1, '二':2, '三':3, '四':4, '五':5, '六':6, '日':7}
user='user1'
pwd='123456'
dburl='localhost:1521/xe'
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'    #select userenv('language') from dual 先查询编码
num_epochs=20

def func1():
    # getData() #导入数据库数据
    #应该加入k折验证，
    train_pl,train_labels= getDataForFile()
    print(train_pl.shape)
    print(train_pl[0])
    print(train_labels.shape)
    print(train_labels[0])
    model=setF(train_pl)
    model,t_loss,t_acc,v_loss,v_acc=learn(model,train_pl,train_labels)
    # model.load_weights('my_checkpoint_pl-bf')
    # print(t_loss,t_acc,v_loss,v_acc)
    show2(t_loss,t_acc,v_loss,v_acc)

    #test1(test_pl,test_labels,1,model)

    # c_pl=[[2.92,3.23,1.97]]
    # c_pl=[[3.9,3.65,1.59]]  #诺维奇vs切尔西 6020
    # c_pl=[[1.23,4.6,7.75]]  #曼联vs水晶宫   6028
    # c_pl=[[3.3,3.3,1.92]]   #谢菲尔德vs莱切斯塔 6029
    # c_pl=[[1.98,3.2,2.93]]  #沃特福德vs西汉姆联 6030
    # c_pl=[[1.34,4.3,5.6]]   #利物浦vs阿森纳 7046
    # c_pl=[[166,123]]
    # c_pl=np.array(c_pl)
    # print(c_pl.shape)
    # test2(c_pl,model)
    '''
    '''

def getData():
    f1=open('./traindata.txt','w')
    #导入数据集
    traindata=[]
    testdata=[]
    conn=cx_Oracle.connect(user, pwd, dburl)
    cursor = conn.cursor()
    cursor.prepare("select * from T_FOOTBALL_DATA_1 where odds1!=0 and odds2!=0 and odds3!=0 "+
            "and leagid=:leagid and vsdate>to_date('2016-06-01','yyyy-MM-dd') order by vsdate asc")
    r=cursor.execute(None, {'leagid':165})
    vss1=cursor.fetchall()
    for vs in vss1:
        for vsdata in vs:
            f1.write(str(vsdata)+',')
        f1.write('\n')
    f1.close()
    cursor.close()
    conn.close()

def getDataForFile():
    train_pl=[]
    train_labels=[]
    f1=open('./traindata.txt','r+')
    for l in f1.readlines():
        sp=l.split(',')
        pl=[float(x) for x in sp[8:11]]
        #pl=[]
        #pl.append(sp[4])
        #pl.append(sp[6])
        train_pl.append(pl)

        lable=d1[l.split(',')[-2]]
        # if (sp[-4]+":"+sp[-3]) not in d3.keys():
        #     lable=28
        # else:
        #     lable=d3[sp[-4]+":"+sp[-3]]
        # #if(lable>=7):
        # #    lable=7
        train_labels.append(lable)
    f1.close()

    train_pl=np.array(train_pl)
    train_labels=np.array(train_labels)
    return train_pl,train_labels

def setF(train_pl):
    #设置层
    model = keras.Sequential()
    #model.add(layers.Flatten(input_shape=(train_pl.shape[1:])))
    model.add(layers.Dense(8, activation='relu', input_shape=(train_pl.shape[1:]) ))
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(12, activation='relu' ))
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(3, activation='softmax' ))

    # model.add(layers.Dense(6, activation='relu', input_shape=(train_pl.shape[1:]) ))
    # model.add(layers.Dropout(1))
    # model.add(layers.Dense(6, activation='relu' ))
    # model.add(layers.Dropout(1))
    # model.add(layers.Dense(3, activation='softmax' )) 

    # model = keras.Sequential([
    #     keras.layers.Flatten(input_shape=(3,)),         #第一层，将输入数据从二维数组(1*3)转换成一维数组(1*3=3)
    #     keras.layers.Dense(6, activation=tf.nn.relu),     #第一个密集层，3个神经元，采用relu方法
    #     keras.layers.Dense(3, activation=tf.nn.softmax)    #第二个密集层，3个神经元，采用softmax（判断各个概率）
    # ])

    #model.compile(optimizer=tf.train.AdamOptimizer(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.compile(
        loss='sparse_categorical_crossentropy', 
        optimizer='rmsprop', 
        metrics=['accuracy']
    )
    return model

def learn(model,train_data,train_labels):
    k=4
    num_val_samples=len(train_data) // k
    all_train_loss_histories=[]
    all_train_acc_histories=[]
    all_val_loss_histories=[]
    all_val_acc_histories=[]
    for i in range(k):
        print('processing fold #', i)
        index_a=i*num_val_samples
        index_b=(i+1)*num_val_samples
        val_data=train_data[index_a: index_b]   #截取第i个分区的数据,作为验证数据
        val_labels=train_labels[index_a:index_b]

        partial_train_data=np.concatenate(  #concatenate 串联
            [ train_data[:index_a], train_data[index_b:] ],
            axis=0
        )
        partial_train_labels=np.concatenate(
            [ train_labels[:index_a], train_labels[index_b:] ],
            axis=0
        )
        history=model.fit(
            partial_train_data,
            partial_train_labels,
            epochs=num_epochs,
            batch_size=10,
            validation_data=(val_data, val_labels),
            verbose=0
        )
        all_train_loss_histories.append(history.history['loss'])
        all_train_acc_histories.append(history.history['acc'])
        all_val_loss_histories.append(history.history['val_loss'])
        all_val_acc_histories.append(history.history['val_acc'])

    avg_train_loss_hist=[ np.mean([x[i] for x in all_train_loss_histories]) for i in range(num_epochs) ]
    avg_train_acc_hist=[ np.mean([x[i] for x in all_train_acc_histories]) for i in range(num_epochs) ]
    avg_val_loss_hist=[ np.mean([x[i] for x in all_val_loss_histories]) for i in range(num_epochs) ]
    avg_val_acc_hist=[ np.mean([x[i] for x in all_val_acc_histories]) for i in range(num_epochs) ]
    model.save_weights('my_checkpoint_zc3')    #手动保存权重
    return model,avg_train_loss_hist,avg_train_acc_hist,avg_val_loss_hist,avg_val_acc_hist

def show2(t_loss,t_acc,v_loss,v_acc):
    epochs=range(1, len(t_loss)+1)
    plt.figure(figsize=(10,5))

    plt.subplot(1,2,1)
    plt.plot(epochs, t_loss, 'b', label='t_loss')
    plt.plot(epochs, v_loss, 'r', label='v_loss')
    plt.ylim([0,2])
    plt.title('loss')
    plt.legend()

    plt.subplot(1,2,2)
    plt.plot(epochs, t_acc, 'b', label='t_acc')
    plt.plot(epochs, v_acc, 'r', label='v_acc')
    plt.ylim([0,1])
    plt.title('acc')
    plt.legend()
    plt.show()

def test1(test_pl,test_labels,i,model1):
    predictions = model1.predict(test_pl)    #对测试集进行预测试
    print('赔率信息：'+str(test_pl[i]))
    print('胜平负概率分别：'+str(predictions[i]))
    print('预测：'+d2[np.argmax(predictions[i])])
    print('正确：'+d2[test_labels[i]])

def test2(pl,model1):
    predictions = model1.predict(pl)    #对测试集进行预测试
    print('赔率信息：'+str(pl))
    print('概率分别：'+str(predictions[0]))
    print('预测：'+d2[np.argmax(predictions[0])])


#model.load_weights('my_checkpoint_'+name)
#test2(model)
func1()

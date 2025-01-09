import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
a = 1.3
b = 0.4
dataNum = 500
parsentage = 0.1
#比例データ y = ax [average x = 0.5]
dataX = np.random.normal(0.5,0.5,size=dataNum)
dataY = (a*dataX+np.random.normal(0,0.1,size=dataNum)+b)
for i in range(int(dataNum*parsentage)):
    dataY[np.random.choice(np.arange(0,dataY.shape[0]))] += np.random.normal(0,0.5)
    dataX[np.random.choice(np.arange(0,dataX.shape[0]))] += np.random.normal(0,0.5)

#fig,ax = plt.subplots(figsize=[10,10])
#ax.plot(dataX,dataY,lw = 0,marker='^',markersize = 2)
Data = np.array([dataX,dataY]).T # [[x_0,y_0],[x_1,y_1],[x_2,y_2],[x_3,y_3]...]

fig,ax = plt.subplots(figsize=[10,10])

Artist = []

def Ransac(Data,sampleNum,threshold):
    global ax,Artist
    resalt = [0,0,1e90,None]
    for i in range(100):

        DataCopy = Data.copy()
        SampleData = []
        for i in range(sampleNum):
            index = np.random.randint(DataCopy.shape[0])
            SampleData.append(DataCopy[index])
            DataCopy = np.delete(DataCopy,index,0)
        SampleData = np.array(SampleData)

        sampleAverage = [np.average(SampleData[:,0]),np.average(SampleData[:,1])]
        ExpA = np.sum((SampleData[:,0]-sampleAverage[0])*(SampleData[:,1]-sampleAverage[1]))/((SampleData[:,0]-sampleAverage[0])@(SampleData[:,0]-sampleAverage[0]))
        ExpB = sampleAverage[1] - ExpA*sampleAverage[0]

        a0 = ax.plot(SampleData[:,0],SampleData[:,1],lw=0,marker='o',markersize=5,c='r')
        a1 = ax.plot(np.array([0,1]),np.array([0,1])*ExpA+ExpB,c='b')

        Artist.append(a0+a1)

        ExpTrueData = DataCopy[abs(DataCopy[:,0]*ExpA+ExpB - DataCopy[:,1]) < threshold]
        Score = np.sqrt((ExpTrueData[:,0]*ExpA+ExpB - ExpTrueData[:,1])@(ExpTrueData[:,0]*ExpA+ExpB - ExpTrueData[:,1]))/ExpTrueData.shape[0]
        b0 = ax.plot(DataCopy[:,0],DataCopy[:,1],lw=0,marker='o',markersize=5,c='b')
        b1 = ax.plot(ExpTrueData[:,0],ExpTrueData[:,1],lw=0,marker='o',markersize=5,c='r')
        b2 = ax.plot(np.array([0,1]),np.array([0,1])*ExpA+ExpB,c='b')
        Artist.append(b0+b1+b2)
        if Score < resalt[2]:
            resalt = [ExpA,ExpB,Score,(b0+b1+b2).copy()]
    Artist.append(resalt[3])
    print(*resalt[:2])
    return

print(a,b)

Ransac(Data,7,0.1)

#最小二乗法
Average = [np.average(Data[:,0]),np.average(Data[:,1])]
ExpA = np.sum((Data[:,0]-Average[0])*(Data[:,1]-Average[1]))/((Data[:,0]-Average[0])@(Data[:,0]-Average[0]))
ExpB = Average[1] - ExpA*Average[0]

print(ExpA,ExpB)

#anim = ArtistAnimation(fig,Artist, interval=10, repeat=False)

# plt.show()
# plt.close()
import os
import csv
from preProcess import preProcess
from train import learn

#计算两列表的距离
def calDistance(list1,list2):
    dis=0
    for i in range(len(list1)):
        dis += abs(list1[i]-list2[i])
    return dis

#主函数
def main():
    all=learn(r'C:\Users\hp\Desktop\code\code\hard\train')
    str1=input("Please input path:")
    with open('result.csv','w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(('name','code'))
        for home,dir,files in os.walk(str1):
            for filename in files:
                info = preProcess(os.path.join(home, filename))
                answer=''
                for i in info:
                    vote=[]
                    #print(len(i))
                    distance=[]
                    for j in all:
                        distance.append(calDistance(j[0],i))
                    index=distance.index(min(distance))
                    vote.append([distance[index],all[index][1]])
                    distance[index]=1000
                    index=distance.index(min(distance))
                    vote.append([distance[index],all[index][1]])
                    distance[index]=1000
                    index=distance.index(min(distance))
                    vote.append([distance[index],all[index][1]])
                    distance[index]=1000
                    if(vote[0][1]==vote[1][1]):
                        answer+=str(vote[0][1])
                        continue
                    elif (vote[0][1]==vote[2][1]):
                        answer+=str(vote[0][1])
                        continue
                    elif (vote[1][1]==vote[2][1]):
                        answer+=str(vote[1][1])
                        continue
                    else:
                        answer+=str(vote[0][1])
                writer.writerow((filename,answer))
                

    




    '''
    template=train.learn(r'F:\AI Project\train')
    with open('result.csv','w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(('name','code'))
        for home,dir,files in os.walk(str1):
            for filename in files:
                numList=pictureProcess.imageProcess(os.path.join(home, filename))
                result=''
                for i in numList:
                    distance=[]
                    for j in template:
                        distance.append(calDistance(i,j))
                    result+=str(distance.index(min(distance)))
                writer.writerow((filename,result))
    '''    

if __name__ =="__main__":
    main()  

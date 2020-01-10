import train
import pictureProcess
import os
import csv

#计算两列表的距离
def calDistance(list1,list2):
    dis=0
    for i in range(len(list1)):
        dis += abs(list1[i]-list2[i])
    return dis

#主函数
def main():
    str1=input("Please input path:")
    template=train.learn(r'C:\Users\hp\Desktop\code\code\easy\train')
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
            

if __name__ =="__main__":
    main()  



        

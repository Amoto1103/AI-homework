import numpy as np
import cv2

def preProcess(path):
    #1是加载彩色图像，0是加载灰色图像
    im=cv2.imread(path,0)
    #二值化
    #im1=im
    #cv2.threshold(im, 200, 255, cv2.THRESH_BINARY_INV, im1)
    #中值滤波，效果不错，感觉滤的有点过
    #out=cv2.medianBlur(im,3,0)
    #去除边框
    height,weight=im.shape
    #print(weight,height)
    for i in range(height):
        for j in range(weight):
            if i < 1 or i > (height-2) or j < 1 or j >(weight-2):
                im[i,j]=255
    #先白色膨涨，有降噪效果，就是降得有点狠了
    kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
    dilation=cv2.dilate(im,kernel)
    #cv2.imshow("111",dilation)
    #再白色腐蚀，也没好看到哪里
    newkernel=cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
    eroded=cv2.erode(dilation,newkernel)
    #cv2.imshow("222",eroded)
    #二值化
    final=eroded
    cv2.threshold(eroded, 245, 255, cv2.THRESH_BINARY, final)
    #new=cv2.resize(final,(1320,500))
    #picList是一个25*60的矩阵
    picList=[]
    for i in range(height):
        hangList=[]
        for j in range(weight):          
            if(final[i,j]==0):
                #print(0,end='')
                hangList.append(0)
            else:
                #print(1,end='')
                hangList.append(1)     
        #print()
        picList.append(hangList)
    #print(len(picList))
    #print(len(picList[0]))
    #print(picList)
    #计算边框范围，0是黑色，1是白色,返回四个框框的坐标值
    zuobiao=findBorder(height,weight,picList)
    im1=final[zuobiao[0][0]:zuobiao[0][2]+1,zuobiao[0][1]:zuobiao[0][3]+1]
    im2=final[zuobiao[1][0]:zuobiao[1][2]+1,zuobiao[1][1]:zuobiao[1][3]+1]
    im3=final[zuobiao[2][0]:zuobiao[2][2]+1,zuobiao[2][1]:zuobiao[2][3]+1]
    im4=final[zuobiao[3][0]:zuobiao[3][2]+1,zuobiao[3][1]:zuobiao[3][3]+1]
    #cv2.imshow("333",final)

    '''
    image, contours, _ = cv2.findContours(im1, 2, 2)
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)  # 获取最小外接矩形的4个顶点
        box = np.int0(box)
        if 0 not in box.ravel():
            # 旋转角度
            theta = cv2.minAreaRect(cnt)[2]
            if abs(theta) <= 45:
                print('图片的旋转角度为%s.'%theta)
                angle = theta

    # 仿射变换,对图片旋转angle角度
    h, w = im1.shape
    center = (w//2, h//2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(im1, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    '''
    # 保存旋转后的图片
    newim1=rotateAndRegular(im1)
    newim2=rotateAndRegular(im2)
    newim3=rotateAndRegular(im3)
    newim4=rotateAndRegular(im4)
    he,we=newim1.shape
    list1=[]
    for i in range(he):
        for j in range(we):
            if newim1[i,j]==0:
                list1.append(0)
            else:
                list1.append(1)
    list2=[]
    for i in range(he):
        for j in range(we):
            if newim2[i,j]==0:
                list2.append(0)
            else:
                list2.append(1)
    list3=[]
    for i in range(he):
        for j in range(we):
            if newim3[i,j]==0:
                list3.append(0)
            else:
                list3.append(1)
    list4=[]
    for i in range(he):
        for j in range(we):
            if newim4[i,j]==0:
                list4.append(0)
            else:
                list4.append(1)
    all=[]
    all.append(list1)
    all.append(list2)
    all.append(list3)
    all.append(list4)
    return all
    #cv2.imwrite("11-"+path,newim1)
    #cv2.imwrite("22-"+path,newim2)
    #cv2.imwrite("33-"+path,newim3)
    #cv2.imwrite("44-"+path,newim4)
    #cv2.imshow("333",newim1)
    #cv2.waitKey(0)
    #cv2.imwrite("1-"+path,newim1)
    #cv2.imwrite("2-"+path,im2)
    #cv2.imwrite("3-"+path,im3)
    #cv2.imwrite("4-"+path,im4)
    '''
    cv2.imshow("333",newim1)
    image, contours, _ = cv2.findContours(newim1, cv2.RETR_EXTERNAL, 2)
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)  # 获取最小外接矩形的4个顶点
        box = np.int0(box)
        # 旋转角度
        theta = cv2.minAreaRect(cnt)[2]
        if abs(theta) <= 45:
            print('图片的旋转角度为%s.'%theta)
            angle = theta
        else:
            angle = theta+90
        print(box)
    # 仿射变换,对图片旋转angle角度
    h, w = newim1.shape
    center = (w//2, h//2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(newim1, M, (w, h), flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
    cv2.imshow("3",rotated)
    cv2.waitKey(0)
    '''


    '''
    #自动框选并不太好使,应该三个框框给我五个
    
    #ret, thresh = cv2.threshold(final ,245, 255, cv2.THRESH_BINARY_INV)
    image, contours, hier = cv2.findContours(final, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
    # find bounding box coordinates
        x,y,w,h = cv2.boundingRect(c)
        print(x,y,w,h)
        #cv2.rectangle(image, (x,y), (x+w, y+h), (0, 255, 0), 2)
        #rect = cv2.minAreaRect(c)
        #box = cv2.boxPoints(rect)
        #box = np.int0(box)
        #cv2.drawContours(image, [box], 0, (255,255,255), 1)
    #cv2.imshow("222",image)
    cv2.waitKey(0)
    '''

#框出每个数字的边界，横向竖向连接的数字从中间找到一列分割，斜向连接的会被分割
def findBorder(height,weight,numList): 
    #记录所有为零的坐标
    daBiao=[]
    for i in range(weight):
        lieBiao=[]
        for j in range(height):
            if(numList[j][i]==1):
                continue
            else:
                lieBiao.append((j,i))
        daBiao.append(lieBiao)
    #print(len(daBiao))
    #print(daBiao)
    #此时大表记录了所有0的坐标信息
    #判断和下一列有无粘连
    #扳机是在判断是否创建一个新列表
    banji=1

    singleSet=[]
    for i in range(len(daBiao)):
        #本列没有0
        if(len(daBiao[i])==0):
            banji=1
            continue
        else:
            if(banji):
                #print(i)
                newSet=[]
                banji=0               
            newSet.append(daBiao[i])
            #下一列没有0或者越界
            if (i+1)==weight  or (len(daBiao[i+1])==0):
                banji=1
                singleSet.append(newSet)
                continue
            #下一列有0
            else:
                exist=0
                for j in daBiao[i]:
                    for k in daBiao[i+1]:
                        #如果有粘连 
                        if(j[0]==k[0]):
                            exist=1
                if(exist):
                    continue
                else:
                    singleSet.append(newSet)
                    banji=1
    #进行字符连接的切割，不应该出现三个字符的连接
    newsingleSet=[]
    for everyList in singleSet:
        if(len(everyList)>17):
            same=[]
            for i in range(len(everyList)-1):
                calculate=0
                for dian1 in everyList[i]:
                    for dian2 in everyList[i+1]:
                        if(dian1[0]==dian2[0]):
                            calculate+=1
                same.append(calculate)
            #print(same)
            if (len(same)%2)==1 :
                initialindex=len(same)//2-1
                if(same[initialindex+1]<same[initialindex]):
                    if(same[initialindex+2]<same[initialindex+1]):
                        leastIndex=initialindex+2
                    else:
                        leastIndex=initialindex+1
                else:
                    if(same[initialindex+2]<same[initialindex]):
                        leastIndex=initialindex+2
                    else:
                        leastIndex=initialindex
                newsingleSet.append(everyList[0:leastIndex+1])
                newsingleSet.append(everyList[leastIndex+1:])
            else:
                initialindex=len(same)//2
                if(same[initialindex+1]<same[initialindex]):
                    initialindex+=1
                newsingleSet.append(everyList[0:initialindex+1])
                newsingleSet.append(everyList[initialindex+1:])
        else:
            newsingleSet.append(everyList)

    #提取每个区域的坐标
    zuobiao=[]
    for eachList in newsingleSet:
        minweight=eachList[0][0][1]
        minheight=50
        maxheight=0
        maxweight=eachList[-1][-1][1]
        #print(minweight,maxweight)
        for lie in eachList:
            for dian in lie:
                if (dian[0]>maxheight):
                    maxheight=dian[0]
                if (dian[0]<minheight):
                    minheight=dian[0]
        #print(minheight,maxheight)
        zuobiao.append((minheight,minweight,maxheight,maxweight))
    #print(zuobiao)
    #print(newsingleSet)
    #print(len(newsingleSet))
    #print(len(newsingleSet[0]))
    #print(len(newsingleSet[1]))
    #print(len(newsingleSet[2]))
    return zuobiao

def rotateAndRegular(im1):
    #黑白反转，貌似只能检测黑底白字的
    shu,heng=im1.shape
    for i in range(shu):
        for j in range(heng):
            im1[i,j]=255-im1[i,j]
    #以数字为中心拓宽边界，准备框出来
    #im11=cv2.resize(im1,(12,15),interpolation=cv2.INTER_CUBIC)
    newim1=cv2.copyMakeBorder(im1,7,7,7,7,cv2.BORDER_CONSTANT,value=(0,0,0))
    #取外边框
    contours, _ = cv2.findContours(newim1, cv2.RETR_EXTERNAL, 2)
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)  # 获取最小外接矩形的4个顶点
        box = np.int0(box)
        # 旋转角度选择
        theta = cv2.minAreaRect(cnt)[2]
        if abs(theta) <= 45:
            #print('图片的旋转角度为%s.'%theta)
            angle = theta
        else:
            #print('图片的旋转角度为%s.'%theta)            
            angle = theta+90
        #print(box)
    # 仿射变换,对图片旋转angle角度
    h, w = newim1.shape
    center = (w//2, h//2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(newim1, M, (w, h), flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
    middle=rotated
    cv2.threshold(rotated, 10, 255, cv2.THRESH_BINARY, middle)
    '''
    image, contours, _ = cv2.findContours(rotated, cv2.RETR_EXTERNAL, 2)
    for cnt in contours:
        theta = cv2.minAreaRect(cnt)[2]
        if(abs(theta)<5):
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)  # 获取最小外接矩形的4个顶点
            box = np.int0(box)
            print(box)
    '''
    final= cv2.resize(middle,(22,25),interpolation=cv2.INTER_NEAREST)
    return final

#preProcess('030.jpg')
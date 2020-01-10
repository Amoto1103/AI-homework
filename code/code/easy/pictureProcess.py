from PIL import Image
from PIL import ImageDraw

#获取最近的八个像素点位置
def getNeighbor(height,width,index):
    neighborIndex=[]
    if ((index+1) % width) != 0:
        neighborIndex.append(index+1)
    if (index % width) != 0:
        neighborIndex.append(index-1)
    if (index>(width-1)):
        neighborIndex.append(index-width)
    if index<(width*height-width):
        neighborIndex.append(index+width)
    if (((index+1) % width) != 0) and (index<(width*height-width)):
        neighborIndex.append(index+width+1)
    if (index % width != 0) and (index>(width-1)):
        neighborIndex.append(index-width-1)
    if (((index+1) % width) != 0) and index>(width-1):
        neighborIndex.append(index-width+1)
    if (index % width) != 0 and index<(width*height-width):
        neighborIndex.append(index+width-1)
    return neighborIndex


def imageProcess(path):
    im = Image.open(path)
    #转为灰度图
    im=im.convert("L")
    table=[]
    threshold=100
    for i in range(256):	
        if i < threshold:	
            table.append(0)	
        else:
            table.append(1)
    #转为二值图像
    im = im.point(table, '1')
    #降噪
    width, height = im.size	 
    lis = list(im.getdata())
    newlis=[]
    for shu in range(height):
        for heng in range(width):
            pixellist=[]
            indexlist=getNeighbor(height,width,shu*width+heng)
            for item in indexlist:
                pixellist.append(lis[item])
            #print(pixellist)
            #0是黑的 1是白的
            if (lis[shu*width+heng]==0) and (0 not in pixellist):
                newlis.append(1)
            else:
                newlis.append(lis[shu*width+heng])
            #print(newlis[-1],end='')
        #print

    newimage=Image.new('1',(60,18))
    draw=ImageDraw.Draw(newimage)
    for newshu in range(height):
        for newheng in range(width):
            draw.point((newheng,newshu),newlis[newshu*width+newheng])
    part1=newimage.crop((0,0,12,12))
    part2=newimage.crop((12,0,24,12))
    part3=newimage.crop((24,0,36,12))
    part4=newimage.crop((36,0,48,12))
    numList=[]
    numList.append(list(part1.getdata()))
    numList.append(list(part2.getdata()))
    numList.append(list(part3.getdata()))
    numList.append(list(part4.getdata()))
    return numList
    #part1.save("1-"+path)
    #part2.save("2-"+path)
    #part3.save("3-"+path)
    #part4.save("4-"+path)

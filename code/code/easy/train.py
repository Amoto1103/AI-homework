from PIL import Image
import os

def learn(path):
    fileList=[]
    for home,dir,files in os.walk(path):
        for filename in files:
            fileList.append(os.path.join(home, filename))
    #print(fileList)
    template=[]
    for item in fileList:
        im = Image.open(item)
        im = im.convert("L")
        table=[]
        threshold=100
        for i in range(256):	
            if i < threshold:	
                table.append(0)	
            else:
                table.append(1)
        #转为二值图像
        im = im.point(table, '1')
        template.append(list(im.getdata()))
    #print(template)
    return(template)



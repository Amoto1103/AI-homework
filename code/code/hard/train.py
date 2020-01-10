import cv2
import os

def learn(path):
    all=[]
    for home,dir,files in os.walk(path):    
        for filename in files:
            #print(fileList)       
            template=[]
            im = cv2.imread(os.path.join(home, filename),0)
            height,weight=im.shape
            for i in range(height):
                for j in range(weight):
                    if(im[i,j]<50):
                        template.append(0)
                    else:
                        template.append(1)
            #print(len(template))
            number=filename.split('-')[0]
            all.append([template,int(number)])

    return all
    #print(int(number)) 
    #print(template)
    #return(template)

#learn(r'F:\AI Project\train')
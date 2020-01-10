import os
import csv
import torch
from torch.autograd import Variable
import utils
import dataset
from preProcess import preprocess
from PIL import Image

import models.crnn as crnn

model_path = './data/crnn.pth'

with open('result.csv','w',newline='') as result:
    res = csv.writer(result)
    res.writerow(['name','code'])

model = crnn.CRNN(32, 1, 37, 256)
if torch.cuda.is_available():
    model = model.cuda()
print('loading pretrained model from %s' % model_path)
model.load_state_dict(torch.load(model_path))

alphabet = '012345678946066796176100049157000462'
converter = utils.strLabelConverter(alphabet)

transformer = dataset.resizeNormalize((100, 32))


path = input("Enter the path:")
for i in os.listdir(path):
    img_path = path+'/'+i
    image = preprocess(img_path)
    image = Image.open(img_path).convert('L')
    image = transformer(image)
    if torch.cuda.is_available():
        image = image.cuda()
    image = image.view(1, *image.size())
    image = Variable(image)

    model.eval()
    preds = model(image)

    _, preds = preds.max(2)
    preds = preds.transpose(1, 0).contiguous().view(-1)

    preds_size = Variable(torch.IntTensor([preds.size(0)]))
    sim_pred = converter.decode(preds.data, preds_size.data, raw=False)
    record = [i,sim_pred]
    with open('result.csv','a+',newline='') as result:
        res = csv.writer(result)
        res.writerow(record)

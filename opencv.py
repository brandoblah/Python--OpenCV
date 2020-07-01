import zipfile
import pytesseract
import cv2 as cv
import numpy as np
from zipfile import ZipFile
from PIL import Image, ImageDraw

images = {}  
file_list = []

# unzip the incoming files
def unzip(fzip):
    z = zipfile.ZipFile(fzip)
    for x in z.infolist():
        images[x.filename] = [Image.open(z.open(x.filename))]
        file_list.append(x.filename)

if __name__ == '__main__':
    unzip('readonly/images.zip')

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')


                    
# search by keyword
def search(keyword):
    
    for face in file_list:
        
        #display(images[face][0])
        img = images[face][0]
        images[face].append(pytesseract.image_to_string(img).replace('-\n', ''))    
        if keyword in images[face][1]:
            print('Results found in file ', face)
            try:
                faces = (face_cascade.detectMultiScale(np.array(img), 1.35,4)).tolist()
                images[face].append(faces)
                totalfaces = []      
                for x, y, w, h in images[face][2]:
                    totalfaces.append(img.crop((x, y, x+w, y+h)))
                            
                            
                contact_sheet = Image.new(img.mode, (550, 110 * int(np.ceil(len(totalfaces)/5))))
                x = 0
                y = 0
                
                # create thumbnails
                for j in totalfaces:
                    j.thumbnail((110, 100))
                    contact_sheet.paste(j, (x, y))
                    
                    if x + 110 == contact_sheet.width:
                        x = 0
                        y = y + 110
                    else:
                        x = x + 110
                    
                display(contact_sheet)
                            
            except:
                print('There were no faces in that file!')
    

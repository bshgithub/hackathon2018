
#imported libraries
from flask import Flask
from flask import request
import pytesseract


#imported files
import descriptor
import temperature
app = Flask(__name__)

#tasks = send image, read image, send temperature, play music.
#           0           1               2           3
current_rasp_image = None
current_rasp_temp = None
CURRENT_INSTRUCTION = -1
# 0 = describe
# 1 = read_image
# 2 = temperature
@app.route('/')
def index():
    return "prova"


@app.route('/putInfo',methods=['POST'])
def imageToServer():
    print (request.json)
#    image = request.args.get('image')
#    current_rasp_image = image
#    current_rasp_temp = request.args.get('temp')
    if request.headers['Content-Type'] == 'application/octet-stream':
        with open('./binary', 'wb') as f:
            f.write(request.data)
            f.close()
        return "Binary message written!"
    elif request.headers['Content-Type'] == 'text/plain':
        print(request.data)
        return "Text Message: " + request.data

    if CURRENT_INSTRUCTION==0:
        describeImage(image)
    elif CURRENT_INSTRUCTION==1:
        readImage(image)
    else :
        pass
    return 200

@app.route('/describeImage')
def describeImageRequest():
    CURRENT_INSTRUCTION = 0
    b = None
    with open('binary','rb') as f:
	b = f.read()
    current_rasp_image = b
    if current_rasp_image is None:
        pass
    else:
        sent = describeImage(current_rasp_image)
        #send to google
    return "ok"

@app.route('/readImage')
def readImageRequest():
    if current_rasp_image is None:
        pass
    else:
        sent = readImage(current_rasp_image)
        #send to google
    return "ok"

@app.route('/getTemperature')
def getTemperatureRequest():
    if current_rasp_temp is None:
        pass
    else:
        sent = temperature.create_sentence(current_rasp_temp)
        #send to google
    return "ok"

#python aux functions
def describeImage(img):
    sentence = descriptor.describe(img)
    return sentence

def readImage(img):
    sentence = pytesseract.image_to_string(img)
    return sentence

if __name__ == '__main__':
    app.run(debug=True, port=8092)

from flask import Flask, jsonify, request

from PIL import Image
import pytesseract
import cv2
import os
import base64

app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello():
    return jsonify({"about": "Hello World!"})


@app.route("/menuReader", methods=['POST'])
def decode_predictions():

    print(request.form.get('files'))

    imgdata = base64.b64decode(request.form['files'])

    filename = 'myimage.jpg'
    with open(filename, 'wb') as f:
        f.write(imgdata)

    image = cv2.imread("myimage.jpg")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cv2.imshow("Image", gray)

    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    text = pytesseract.image_to_string(Image.open(filename))

    text1=''.join(e for e in text if e.isalpha() or e==' ' or e=='\n')



    returnStringList = list(filter(None, text1.splitlines()))
    returnStringList = [s for s in returnStringList if s.strip()]

    os.remove(filename)
    with open('myfile.txt', "w") as file:
        file.write(str(returnStringList))

    print(jsonify(returnStringList))
    return jsonify(returnStringList)


if __name__ == '__main__':
    app.run(debug=True)
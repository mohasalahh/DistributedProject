import uuid
from flask import Flask, render_template, request

from models.zeromq_events import ZeroMQEvent
from rmq_helpers.rmq_sender import send_to_rmq

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        id = str(uuid.uuid4())
        fileName = file.filename.split(".")
        fileExt = fileName[len(fileName)-1]

        finalFileName = id+"."+fileExt
        img_path = '/Users/mohamedsalah/Documents/Mixes/DistributedProject/uploaded_imgs/' + finalFileName
        file.save(img_path)

        op_id = 1

        data = " ".join([id, img_path, str(op_id)])
        send_to_rmq(ZeroMQEvent.START_PROCESSING, data)
        return 'File uploaded successfully'

if __name__ == '__main__':
    app.run(debug=True)
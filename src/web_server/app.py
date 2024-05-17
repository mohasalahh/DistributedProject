
import uuid
from flask_socketio import SocketIO
from flask import Flask, redirect, render_template, request

from models.rmq_events import RMQEvent
from rmq_helpers.rmq_receiver import RMQEventReceiver
from rmq_helpers.rmq_sender import send_to_rmq

app = Flask(__name__)
socketio = SocketIO(app)

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
        send_to_rmq(RMQEvent.START_PROCESSING, data)

        return redirect("/track/"+id)


@app.route('/track/<string:process_id>')
def track_process(process_id: str):
    return render_template('track.html')

# Dictionary to store client rooms
client_rooms = {}

@socketio.on('track')
def handle_track(process_id):
    # Store client's room
    if process_id not in client_rooms:
        client_rooms[process_id] = []
    client_rooms[process_id].append(request.sid)

    print(f"Client with ID: {request.sid} is tracking process: {process_id}")

def didRecieveMessage(event: RMQEvent, data: str):
    dataSplit = data.split(" ")
    process_id = dataSplit[0]
    if event == RMQEvent.PROGRESS_UPDATE:
        done = int(dataSplit[1])
        size = int(dataSplit[2])

        progress = (done/size) * 100 # %
        emitUpdateOf(process_id, "progress_update", {'progress': progress})

    elif event == RMQEvent.PROCESSING_FAILED:
        # TODO: - Add reason
        emitUpdateOf(process_id, "process_failed", {'reason': "undefined"})
    elif event == RMQEvent.PROCESSING_DONE:
        # TODO: - Add Config
        emitUpdateOf(process_id, "process_done", {'downloadLink': "/Users/mohamedsalah/Documents/Mixes/DistributedProject/processed_imgs/"+process_id+".png"})


def emitUpdateOf(process_id, event, data):
    if process_id in client_rooms:
        for client_id in client_rooms[process_id]:
            socketio.emit('progress_update', data, room=client_id)

        

if __name__ == '__main__':
    rmqReceiver = RMQEventReceiver([RMQEvent.PROCESSING_DONE, RMQEvent.PROGRESS_UPDATE, RMQEvent.PROCESSING_FAILED], didRecieveMessage)
    rmqReceiver.start()
    socketio.run(app, port=3000)
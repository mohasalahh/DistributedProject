
import uuid
from flask_socketio import SocketIO
from flask import Flask, redirect, render_template, request, send_from_directory

from constants import PROCESSED_PATH, UPLOADED_PATH
from models.image_processing_task import ImageOperation
from models.rmq_events import RMQEvent
from redis_access.redis_access import ProcessState, get_from_redis, set_to_redis
from rmq_helpers.rmq_receiver import RMQEventReceiver
from rmq_helpers.rmq_sender import send_to_rmq

app = Flask(__name__)
socketio = SocketIO(app)

# Dictionary to store client rooms
client_rooms = {}

@app.route('/')
def index():
    """
    Render the main page of the web application.

    Returns:
        Rendered template for index.html.
    """
    return render_template('index.html')

@app.route('/uploaded_imgs/<path:filename>')
def uploaded_imgs_static(filename):
    """
    Serve uploaded images from the storage path defined in constants.

    Args:
        filename (str): The filename of the image to serve.

    Returns:
        File: The requested image file.
    """
    return send_from_directory(UPLOADED_PATH, filename)

@app.route('/processed_imgs/<path:filename>')
def processed_imgs_static(filename):
    """
    Serve processed images from the storage path defined in constants.

    Args:
        filename (str): The filename of the processed image to serve.

    Returns:
        File: The requested image file.
    """
    return send_from_directory(PROCESSED_PATH, filename)

@app.route('/upload', methods=['POST'])
def upload():
    """
    Handle file uploads and initiate image processing via RabbitMQ.

    Returns:
        Redirect: Redirects to the tracking page for the processes initiated by this upload.
    """
    if 'files' not in request.files:
        return 'No file part'
    files = request.files.getlist('files')
    if len(files) == 0 or files[0].filename == '':
        return 'No selected files'
    
    tracked_ids = []
    for file in files:
        id = str(uuid.uuid4())
        fileName = file.filename.split(".")
        fileExt = fileName[-1]
        finalFileName = f"{id}.{fileExt}"
        img_path = f"{UPLOADED_PATH}{finalFileName}"
        file.save(img_path)

        op_id = request.form.get('op_id')  # Get op_id from form data
        data = " ".join([id, img_path, str(op_id)])
        send_to_rmq(RMQEvent.START_PROCESSING, data)
        tracked_ids.append(id)
    
    return redirect(f"/track/{','.join(tracked_ids)}")


@app.route('/track/<string:process_id>')
def track_process(process_id: str):
    """
    Render the tracking page for an image processing task.

    Args:
        process_id (str): The unique identifier for the process to track.

    Returns:
        Rendered template for track.html.
    """
    return render_template('track.html')

@socketio.on('track')
def handle_track(processes_ids):
    """
    Websocket endpoint to handle tracking requests from clients for specific processes.

    Args:
        processes_ids (list): List of process IDs that the client wants to track.
    """
    for process_id in processes_ids:
        # Store client's room
        if process_id not in client_rooms:
            client_rooms[process_id] = []
        client_rooms[process_id].append(request.sid)
        
        current_state = get_from_redis(process_id)
        if current_state:
            print(current_state)
            current_state["id"] = process_id
            emitUpdateOf(process_id, "start_tracking", current_state)

        print(f"Client with ID: {request.sid} is tracking process: {process_id}")

def didRecieveMessage(event: RMQEvent, data: str):
    """
    Callback function for RabbitMQ events. Handles various types of messages to update process states.

    Args:
        event (RMQEvent): The type of event received.
        data (str): The data associated with the event.
    """
    dataSplit = data.split(" ")
    process_id = dataSplit[0]
    
    if event == RMQEvent.PROCESSING_STARTED:
        num_of_nodes = dataSplit[1]
        op_id = dataSplit[2]
        img_path_split = dataSplit[3].split("/")
        file_name = img_path_split[len(img_path_split)-1]
        set_to_redis(process_id, state=ProcessState.STARTED, num_of_nodes=num_of_nodes, operation=ImageOperation(int(op_id)), uploaded_file_name=file_name)

    elif event == RMQEvent.PROGRESS_UPDATE:
        current_state = get_from_redis(process_id)
        if current_state and (current_state['state'] == ProcessState.DONE or current_state['state'] == ProcessState.FAILED):
            return

        done = int(dataSplit[1])
        size = int(dataSplit[2])

        progress = (done/size) * 100 # %
        set_to_redis(process_id, state=ProcessState.PROGRESS, progress=progress, num_of_succeeded_nodes=1)

    elif event == RMQEvent.PROCESSING_FAILED:
        set_to_redis(process_id, state=ProcessState.FAILED)
    elif event == RMQEvent.PROCESSING_DONE:
        set_to_redis(process_id, state=ProcessState.DONE)
    print("aaaaaaaa")
    emitRMQEvent(event, data)

def emitRMQEvent(event: RMQEvent, data: str): 
    """
    Emit events based on RabbitMQ messages to update client-side state via websockets.

    Args:
        event (RMQEvent): The event type received from RMQ indicating the current state or action.
        data (str): The data string associated with the event, containing process details.

    Description:
        This function parses the event and data, and triggers corresponding websocket messages to update clients
        on the progress, start, completion, or failure of image processing tasks.
    """

    dataSplit = data.split(" ")
    process_id = dataSplit[0]

    if event == RMQEvent.PROCESSING_STARTED:
        num_of_nodes = dataSplit[1]
        emitUpdateOf(process_id, "process_started", {"id": process_id, 
                                                     "num_of_nodes": num_of_nodes})
    elif event == RMQEvent.PROGRESS_UPDATE:
        done = int(dataSplit[1])
        size = int(dataSplit[2])

        progress = (done/size) * 100 # %
        emitUpdateOf(process_id, "progress_update", {"id": process_id, 'progress': progress, "num_of_nodes": size, "num_of_succeeded_nodes": done})

    elif event == RMQEvent.PROCESSING_FAILED:
        # TODO: - Add reason
        emitUpdateOf(process_id, "process_failed", {"id": process_id, 'reason': "undefined"})
    elif event == RMQEvent.PROCESSING_DONE:
        # TODO: - Add Config
        emitUpdateOf(process_id, "process_done", {"id": process_id, 'download_link': PROCESSED_PATH+process_id+".png"})


def emitUpdateOf(process_id, event, data):
    """
    Emit real-time updates to specific clients tracking the process via their unique socket session IDs.

    Args:
        process_id (str): The unique identifier of the process being tracked.
        event (str): The name of the event to emit, describing the type of update.
        data (dict): A dictionary of data associated with the event to be passed to clients.

    Description:
        This function sends updates to all clients connected to a specific room (process_id).
        Each room corresponds to a process being tracked, and all clients in that room receive updates
        about the process via websocket emissions.
    """
    
    if process_id in client_rooms:
        for client_id in client_rooms[process_id]:
            socketio.emit(event, data, room=client_id)

        

if __name__ == '__main__':
    rmqReceiver = RMQEventReceiver([RMQEvent.PROCESSING_STARTED, RMQEvent.PROCESSING_DONE, RMQEvent.PROGRESS_UPDATE, RMQEvent.PROCESSING_FAILED], didRecieveMessage)
    rmqReceiver.start()
    socketio.run(app, port=3000)
from flask import Flask, request
import json
from rmq.rmq_sender import send_to_rmq
from models.events import Event

app = Flask(__name__)

@app.route('/add')
def add():
    ip = request.args.get('ip', '')  # 'name' is the query parameter
    
    if ip == '': return json.dumps({})

    with open('/home/ubuntu/nodefile', 'a+') as file:
        file.write(ip + " slots=16")
    with open('/home/ubuntu/host_num', 'r') as file:
        current_value = file.read().strip()
    with open('/home/ubuntu/host_num', 'w') as file:
        file.write(str(int(current_value) + 1))
    print(f"IP {ip} added to the file.")

    send_to_rmq(Event.ADD_NODE)

    return json.dumps({"success": True})

@app.route('/remove')
def remove():
    name = request.args.get('ip')  # 'name' is the query parameter
    return f'Hello, {name}!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080) # Running on http://0.0.0.0:8080
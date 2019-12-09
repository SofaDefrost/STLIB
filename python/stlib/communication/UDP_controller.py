''' Python controller to set a UDP communication between the SOFA scenes and a Simulink simulation.
Enables to read from and send data to Simulink.
'''

import socket
import Sofa
import numpy
import struct
import sys
from signal import signal, SIGINT

UDP_IP = "127.0.0.1"

class UDP(Sofa.PythonScriptController):

	def exit_gracefully(self, sig, frame):
		print('Closing UDP communication...')
		self.sock.close()
		sys.exit(0)

	def bwdInitGraph(self, node):
		self.node = node
		self.meca = self.node.robot.meca 	# first simple test, TODO : adapt to different cases 
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

		signal(SIGINT, self.exit_gracefully)

		self.UDP_port_in = 5005 	# simulink's UDP send remote IP port
		self.UDP_port_out = 5006 	# simulink's UDP receive local IP port
		self.sock.bind((UDP_IP, self.UDP_port_in))

	def onBeginAnimationStep(self,dt):
		# receive
		data, addr = self.sock.recvfrom(8192) # simulink's UDP buffer size is fixed at 8192 bytes and is not configurable.
		msg_in = struct.unpack('d', data)
		print "received message:", msg_in

		# send
		pos = numpy.matrix(self.meca.position[-1])
		msg_out = struct.pack('d', pos[0,0])
		self.sock.sendto(msg_out, (UDP_IP, self.UDP_port_out))
		print "sent message:", pos[0,0]
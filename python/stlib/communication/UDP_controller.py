''' Python controller to set a UDP communication between the SOFA scenes and a Simulink simulation.
Enables to read from and send data to Simulink.
'''

import socket
import Sofa
import numpy
import struct
import sys
from signal import signal, SIGINT

class UDP(Sofa.PythonScriptController):

	def exit_gracefully(self, sig, frame):
		Sofa.msg_info("Closing UDP communication...")
		self.sock.close()
		sys.exit(0)

	def bwdInitGraph(self, node):
		self.node = node
		self.meca = self.node.Beam.meca 	# first simple test, TODO : adapt to different cases 
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

		signal(SIGINT, self.exit_gracefully)

		self.UDP_IP = "127.0.0.1"
		self.UDP_port_in = 5005 	# simulink's UDP send remote IP port
		self.UDP_port_out = 5006 	# simulink's UDP receive local IP port
		self.sock.bind((self.UDP_IP, self.UDP_port_in))

	def onBeginAnimationStep(self,dt):
		# receive
		data, addr = self.sock.recvfrom(8192) # simulink's UDP buffer size is fixed at 8192 bytes and is not configurable.
		# msg_in = struct.unpack('d', data)	# works with simulink
		msg_in = struct.unpack('b', data)		# works with matlab
		Sofa.msg_info("received message:"+str(msg_in))

		# send
		pos = numpy.matrix(self.meca.position[0])
		# msg_out = struct.pack('d', pos[0,0])			# works with simulink
		msg_out = struct.pack('b', int(pos[0,0]))		# works with matlab
		self.sock.sendto(msg_out, (self.UDP_IP, self.UDP_port_out))
		Sofa.msg_info("sent message:"+str(pos[0,0]))


# Simple scene for example :

def createScene(rootNode):
                rootNode.findData('gravity').value="0 0 -9810"
                rootNode.findData('dt').value=0.01
                rootNode.createObject('RequiredPlugin', name='SoftRobots', pluginName='SoftRobots')
                rootNode.createObject('RequiredPlugin', name='SofaPython', pluginName='SofaPython')

                rootNode.createObject('FreeMotionMasterSolver')
                rootNode.createObject('GenericConstraintSolver',maxIterations=1000 ,tolerance=0.001)
                rootNode.createObject('PythonScriptController', filename='UDP_controller.py', classname='UDP')
               
                Beam = rootNode.createChild('Beam')
                Beam.createObject('EulerImplicitSolver', name="odesolver", rayleighStiffness=0.1, rayleighMass=0.1)
                Beam.createObject('ShewchukPCGLinearSolver', iterations=1, name="linearsolver", tolerance=1e-5, preconditioners="preconditioner", use_precond="true")
                Beam.createObject('RegularGridTopology', name="SoftBeam", nx=5, ny=2, nz=2, min="-0.050 -0.010 -0.0025", max="0.050 0.010 0.0025")     
                Beam.createObject('MechanicalObject', name="meca", template="Vec3d")
                Beam.createObject('UniformMass', totalmass=0.01)
                Beam.createObject('SparseLDLSolver', name="preconditioner")
                Beam.createObject('LinearSolverConstraintCorrection', solverName="preconditioner")
                Beam.createObject('HexahedronFEMForceField', youngModulus=3000, poissonRatio=0.2)
                Beam.createObject('BoxROI', name="boxFixed", box="0.0250 -0.015 -0.005 0.05 0.015 0.005", drawBoxes="true")
                Beam.createObject('FixedConstraint', indices="@boxFixed.indices")

                return rootNode
''' Python controller to set a UDP communication between the SOFA scenes and a Simulink simulation.
Enables to read from and send data to Simulink.
'''

import socket
import Sofa
import Sofa.Core
import numpy
import struct
import sys
from signal import signal, SIGINT

class UDP(Sofa.Core.Controller):

	def __init__(self, *args, **kwargs):
        Sofa.Core.Controller.__init__(self, *args, **kwargs)

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

	def onAnimateBeginEvent(self, event):
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
                rootNode.findData('gravity').value=[0., 0., -9810]
                rootNode.findData('dt').value=0.01
                rootNode.addObject('RequiredPlugin', name='SoftRobots')
                rootNode.addObject('RequiredPlugin', name='SofaPython3')

                rootNode.addObject('FreeMotionMasterSolver')
                rootNode.addObject('GenericConstraintSolver',maxIterations=1000 ,tolerance=0.001)
                rootNode.addObject(UDP)

                Beam = rootNode.addChild('Beam')
                Beam.addObject('EulerImplicitSolver', name="odesolver", rayleighStiffness=0.1, rayleighMass=0.1)
                Beam.addObject('ShewchukPCGLinearSolver', iterations=1, name="linearsolver", tolerance=1e-5, preconditioners="preconditioner", use_precond=True)
                Beam.addObject('RegularGridTopology', name="SoftBeam", nx=5, ny=2, nz=2, min=[-0.050, -0.010, -0.002], max=[0.050, 0.010, 0.0025])
                Beam.addObject('MechanicalObject', name="meca", template="Vec3")
                Beam.addObject('UniformMass', totalmass=0.01)
                Beam.addObject('SparseLDLSolver', name="preconditioner")
                Beam.addObject('LinearSolverConstraintCorrection', solverName="preconditioner")
                Beam.addObject('HexahedronFEMForceField', youngModulus=3000, poissonRatio=0.2)
                Beam.addObject('BoxROI', name="boxFixed", box=[0.0250, -0.015, -0.005, 0.05, 0.015, 0.005], drawBoxes=True)
                Beam.addObject('FixedConstraint', indices="@boxFixed.indices")

                return rootNode

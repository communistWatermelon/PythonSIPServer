import socket

def processError(msg, addr, utils, socks):
	print "Processing Error"
	# ignore errors

def processAck(msg, addr, utils, socks):
	print "Processing ACK"
	userAddress = lookupUser(msg, socks)
	sendACK(msg, userAddress, socks)

def processOK(msg, addr, utils, socks):
	print "Processing 200 OK"
	userAddress = lookupUser(msg, socks)
	sendOK(msg, userAddress, socks)
	
def processRegister(msg, addr, utils, socks):
	print "Processing REGISTER"
	socks[0].send(msg)

def processInfo(msg, addr, utils, socks):
	print "Processing INFO"

def processInvite(msg, addr, utils, socks):
	print "Processing INVITE"
	sendTrying(msg, addr, utils, socks)
	userAddress = lookupUser(msg, socks)
	if(userAddress != "NO USER"):
		sendInvite(msg, userAddress, socks)
		
def processRinging(msg, addr, utils, socks):
	print "Processing RINGING"
	userAddress = lookupUser(msg, socks)
	sendRinging(msg, userAddress, socks)

def processOptions(msg, addr, utils, socks):
	print "Processing OPTION"
	# don't do this
	
def processCancel(msg, addr, utils, socks):
	print "Processing CANCEL"
	# this sucks, ignore it

def processBye(msg, addr, utils, socks):
	print "Processing BYE"
	userAddress = lookupUser(msg, socks)
	sendRinging(msg, userAddress, socks)

def sendBye(msg, userAddress, socks):
	print "Send bye to ", userAddress
	clientAddress = (userAddress, 5060)
	print clientAddress
	socks[3].sendto(msg, clientAddress)
	
def sendACK(msg, userAddress, socks):
	print "Send ACK to ", userAddress
	clientAddress = (userAddress, 5060)
	socks[3].sendto(msg, clientAddress)
	
def sendOK(msg, userAddress, socks):
	print "Send OK to ", userAddress
	clientAddress = (userAddress, 5060)
	socks[3].sendto(msg, clientAddress)
	
def sendRinging(msg, userAddress, socks):
	print "Send ringing to ", userAddress
	clientAddress = (userAddress, 5060)
	socks[3].sendto(msg, clientAddress)
	
def sendTrying(msg, addr, utils, socks):
	utils.send_ok_msg(addr, socks[3], msg)

def sendInvite(msg, userAddress, socks):
	clientAddress = (userAddress, 5060)
	print clientAddress
	socks[3].sendto(msg, clientAddress)

def lookupUser(msg, socks):
	name = getToName(msg)
	socks[2] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socks[2].connect(("localhost", 5062))
	socks[2].send("LOOKUP " + name)
	address = socks[2].recv(1024)
	socks[2].close()
	if(address == ""):
		return "NO USER"
	return address

def getFromName(msg):
	nameStart 	= msg.find(";tag")
	nameEnd 	= msg.find("From: ")
	return msg[nameEnd:nameStart]

def getToName(msg):
	#print msg
	nameStart 	= msg.find("To: <sip:")
	nameEnd 	= msg.find("@", nameStart)
	name  		= msg[nameStart+9:nameEnd]
	return name
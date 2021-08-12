from socketserver import *
import socket
import sys
from ModbusServerTest import InputRegister

host = '178.154.241.46'
port = 502
addr = (host, port)
class MyTCPHendler (StreamRequestHandler):
    def handler(self):
        self.data = self.request.recv(1024)
        self.TransactioIdHi = self.data[0]
        self.TransactioIdLow = self.data[1]
        self.ProtocolId = self.data[2:3]
        self.length = self.data[4:5]
        self.untilID = self [6]


        print("Hi={0}\n, Low = {0}\n "
              "ProtId={0}\n"
              "length ={0}\n"
                "until id = {0}", self.TransactioIdHi, self.TransactioIdLow, self.ProtocolId,self.length,self.untilID)
        print('client send: '+str(self.data))
        self.request.sendall(b'Hello from server!')

def creeateResponce(TransactionIdHi, TransactionIdLo, ProtocolId, untilID, functionCode, RegisterData, QuantityOfReg ):
    quantityOfDataBytes = QuantityOfReg * 2
    length = 3 + quantityOfDataBytes
    data = (TransactionIdHi.to_bytes(1,"big"), TransactionIdLo.to_bytes(1,"big"), ProtocolId,
            bytes(length), untilID.to_bytes(1,"big"), functionCode.to_bytes(1,"big"),
            bytes(quantityOfDataBytes), RegisterData)
    #KK = bytes(data)

    bTransactionIdHi = TransactionIdHi.to_bytes(1,"big")
    print("Type Of TransactionIdHi = {0}\n Value ={1}".format(type(bTransactionIdHi), bTransactionIdHi))
    bTransactionIdLo = TransactionIdLo.to_bytes(1,"big")
    print("Type Of TransactionIdLo = {0}\n Value ={1}".format(type(bTransactionIdLo), bTransactionIdLo))
    bProtocolId = bytes(ProtocolId)
    print("Type Of ProtocolId= {0}\n Value ={1}".format(type(bProtocolId), bProtocolId))
    bUntilId = untilID.to_bytes(1,"big")
    print("Type Of UntilId = {0}\n Value ={1}".format(type(bUntilId), bUntilId))
    bFunctionCode = functionCode.to_bytes(1,"big")
    print("Type Of FunctionalCode = {0}\n Value ={1}".format(type(bFunctionCode), bFunctionCode))
    bLength = length.to_bytes(2,"big")
    print("Type Of Length = {0}\n Value ={1}".format(type(bLength), bLength))
    bQuantityOfDataBytes = quantityOfDataBytes.to_bytes(1,"big")
    print("Type Of QuantityOfDataBytes = {0}\n Value ={1}".format(type(bQuantityOfDataBytes), bQuantityOfDataBytes))
    bRegisterData_0 = RegisterData[0].to_bytes(1,"big")
    print("Type Of RegisterData = {0}\n Value ={1}".format(type(bRegisterData_0), bRegisterData_0))
    bRegisterData_1 = RegisterData[1].to_bytes(1, "big")
    print("Type Of RegisterData = {0}\n Value ={1}".format(type(bRegisterData_1), bRegisterData_1))
    bStringData = bTransactionIdHi+bTransactionIdLo+ProtocolId+bLength+bUntilId+bFunctionCode+bQuantityOfDataBytes+bRegisterData_0+bRegisterData_1
    #bStringData = bFunctionCode + bQuantityOfDataBytes + bRegisterData_0 + bRegisterData_1
    print(bStringData)
    """
    K = array.array("b")

    K.append(TransactionIdHi)

    K.append(TransactionIdLo)

    K.append(ProtocolId)

    K.append(length.to_bytes(2, "big"))
    K.append(untilID.to_bytes(1, "big"))
    K.append(functionCode.to_bytes(1, "big"))
    K.append(quantityOfDataBytes.to_bytes(2, "big"))
    K.append(RegisterData[0].to_bytes(1, "big"))
    K.append(RegisterData[1].to_bytes(1, "big"))
    """


    return bStringData



if __name__ =="__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', 502)
    print(sys.stderr, 'starting up on %s port %s' % server_address)
    objInputregister = InputRegister.InputRegister()
    objInputregister.addToRegister(0,1526,'Test')
    print(objInputregister.lInputRegisters[0][0])
    k = objInputregister.lInputRegisters[0][0]
    b = bytearray(k.to_bytes(2,"big"))
    print (b[0])
    print (b[1])
    sock.bind(server_address)
    sock.listen(1)
    while True:
        # Wait for a connection
        print (sys.stderr, 'waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print( sys.stderr, 'connection from', client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(16)
                print(sys.stderr, 'received "%s"' % data)
                TransactioIdHi = data[0]
                TransactioIdLow = data[1]
                ProtocolId = data[2:4]
                length = data[4:6]
                untilID = data[6]
                functionCode = data[7]
                Startingadress=data[8:10]
                QuantityOfReg = data [10:12]
                print("Hi={0}\n"
                      "Low = {1}\n"
                      "ProtId={2}\n"
                      "length = {3}\n"
                      "until id = {4}\n"
                      "functionalCode={5}\n"
                      "StartingAddress={6}\n"
                      "QantityofReg = {7}\n".format(TransactioIdHi.to_bytes(1,"big"), TransactioIdLow, int.from_bytes(ProtocolId,"big"),
                                              int.from_bytes(length,"big"),untilID, functionCode,
                                                    int.from_bytes(Startingadress,"big"),
                                                    int.from_bytes(QuantityOfReg,"big")))

                if data:
                    print  (sys.stderr, 'sending data back to the client')
                    sendData = creeateResponce(TransactionIdHi=TransactioIdHi,
                                               TransactionIdLo=TransactioIdLow,
                                               ProtocolId=ProtocolId,
                                               QuantityOfReg= int.from_bytes(QuantityOfReg,"big"),
                                               functionCode=functionCode,
                                               untilID=untilID,
                                               RegisterData=b)
                    print("Send data: {0}".format(sendData))
                    connection.sendall(bytes(sendData))
                else:
                    print (sys.stderr, 'no more data from', client_address)
                    break

        finally:
            # Clean up the connection
            #connection.close()
            print ("Wait....")
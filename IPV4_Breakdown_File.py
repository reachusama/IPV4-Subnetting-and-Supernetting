""""
This program takes input of IP Address, Validates it. Aferwards, it performs submitting and displays results.

Global Vars:
inputList -- Used to store IP Address 4 Octets
prefix -- hold the integer prefix

Functions Used:
takeInput -- This function takes inputs and valides it as well. Asks for input again if it was wrong.
getSubnetMask() -- This function returns the Subnet Mask for the IP Address
getNumberOfHost() -- This function returns the maximum possible Number of Hosts in an IP Address.
getNetworkId(subnetMask) -- This function returns the network ID.
getFirstAddress() -- This function returns the first IP Address after subnetting.
getLastAddress() -- This function returns the last IP Address after subnetting.
getBroadcastAddress() -- This function returns the broadcast Address after subnetting.
convertDigitToBinary(num) -- It is used as a helper func to convert a Decimal to Binary Number
getBinaryValue(num) -- It is used as a helper func to get a Binary Value against a place in an octet.
"""

inputList = list()
prefix = None


def convertDigitToBinary(num):
    l = ''
    while(num != 0):
        l = str(num % 2) + l
        num = num//2

    temp = ''
    while len(temp) + len(l) < 8:
        temp += '0'
    l = temp + l
    return l


def takeInput():

    ipAddress = input("Please enter an IPV4 Address & Prefix (#.#.#.#/MM): ")
    temp = ''
    exitCond = True
    global prefix
    global inputList
    while exitCond:
        for x in ipAddress:
            if x == ' ':
                break
            if x == '.' or x == '/':
                if int(temp) < 1 or int(temp) > 254:
                    break
                inputList.append(temp)
                temp = ''
            else:
                temp = temp + x
        prefix = int(temp)
        if len(inputList) != 4:
            print('- The Correct format is [0-255].[0-255].[0-255].[0-255]/[8-31] Mask')
            print('- Example: 192.168.42.1/24 (no spaces)\n')
            ipAddress = input("Please enter an IPV4 Address & Prefix (#.#.#.#/MM): ")
            inputList.clear()
            temp = ''
        else:
           exitCond = False


def getBinaryValue(num):
    if num == 0:
        return 255
    elif num == 1:
        return 254
    elif num == 2:
        return 252
    elif num == 3:
        return 248
    elif num == 4:
        return 240
    elif num == 5:
        return 224
    elif num == 6:
        return 192
    elif num == 7:
        return 128
    elif num == 8:
        return 0


def getSubnetMask():
    global prefix
    global inputList
    num = 32 - prefix
    subnetMask = [255,255,255,255]

    if num <= 8:
        subnetMask[3] = getBinaryValue(num)
    if num > 8 and num <= 16:
        subnetMask[2] = getBinaryValue(num-8)
        subnetMask[3] = 0
    if num > 16 and num <= 24:
        subnetMask[1] = getBinaryValue(num-16)
        subnetMask[2] = 0
        subnetMask[3] = 0
    if num > 24 and num <= 32:
        subnetMask[0] = getBinaryValue(num-24)
        subnetMask[1] = 0
        subnetMask[2] = 0
        subnetMask[3] = 0

    return subnetMask


def getNumberOfHost():
    global prefix
    return (2 ** (32-prefix)) -2


def getNetworkId(subnetMask):
    global inputList
    bit01 = int(inputList[0]) & int(subnetMask[0])
    bit02 = int(inputList[1]) & int(subnetMask[1])
    bit03 = int(inputList[2]) & int(subnetMask[2])
    bit04 = int(inputList[3]) & int(subnetMask[3])

    return str(bit01) + '.' + str(bit02) + '.' + str(bit03) + '.' + str(bit04)


def getFirstAddress():
    global inputList
    bit01 = int(inputList[0]) & int(subnetMask[0])
    bit02 = int(inputList[1]) & int(subnetMask[1])
    bit03 = int(inputList[2]) & int(subnetMask[2])
    bit04 = 1

    return str(bit01) + '.' + str(bit02) + '.' + str(bit03) + '.' + str(bit04)


def getLastAddress():
    global inputList
    global prefix
    numMax = 32 - prefix

    tempStr = ''
    for x in inputList:
        tempStr += convertDigitToBinary(int(x))

    _str = list(tempStr[::-1])
    for i in range(0,numMax):
        _str[i] = '1'

    _str[0] = '0'
    tempStr = "".join(_str)
    tempStr = tempStr[::-1]

    i = 0
    temp = ''
    newVar = ''
    for s in tempStr:
        if i == 8 or i == 16 or i == 24:
            newVar = newVar + str(int(temp,2)) + '.'
            temp = ''

        temp = temp + s
        i = i + 1

    newVar = newVar + str(int(temp,2))

    return newVar


def getBroadcastAddress():
    global inputList
    global prefix
    numMax = 32 - prefix

    tempStr = ''
    for x in inputList:
        tempStr += convertDigitToBinary(int(x))

    _str = list(tempStr[::-1])
    for i in range(0,numMax):
        _str[i] = '1'
    tempStr = "".join(_str)
    tempStr = tempStr[::-1]

    i = 0
    temp = ''
    newVar = ''
    for s in tempStr:
        if i == 8 or i == 16 or i == 24:
            newVar = newVar + str(int(temp,2)) + '.'
            temp = ''

        temp = temp + s
        i = i + 1

    newVar = newVar + str(int(temp,2))

    return newVar



takeInput()
ipAddress = str(inputList[0]) + '.' + str(inputList[1]) + '.' + str(inputList[2]) + '.' + str(inputList[3])
subnetMask = getSubnetMask()
subnetMaskStr = str(subnetMask[0]) + '.' + str(subnetMask[1]) + '.' + str(subnetMask[2]) + '.' + str(subnetMask[3])
print('\nFor the provided IP Address and Prefix')
print('The IP Address You Entered Was: ',ipAddress)
print('\nThe IP Belongs to the Network: ',getNetworkId(subnetMask))
print('--The Subnet Mask would be: ',subnetMaskStr)
print('\nThe Number of hosts allowed on Network: ',getNumberOfHost())
print('--The First Address Would be: ',getFirstAddress())
print('--The Last Address Would be: ',getLastAddress())
print('--The Network Broadcast Address Would be: ',getLastAddress())

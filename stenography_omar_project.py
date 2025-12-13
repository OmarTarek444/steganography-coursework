delimiter = "End of Message"

def main():
    while True:
        print("Stenography project")
        print("1: Encode")
        print("2: Decode")
        print("3: Exit")
        x= input("Please Enter your choice:")
        if x == "1":
            encode()
        elif x == "2":
            decode()
        elif x == "3":
            print("Bye Bye")
            break
        else:
            print("Invalid choice re-enter again")

def encode():
    print("Encode Mode")
    print("Enter Image path")
    imagepath = input()
    print("Enter where to save image after encoding")
    outputpath = input()
    if not outputpath.lower().endswith(".bmp"):
        outputpath += "encoded.bmp"
    print("1: Enter your secret Message")
    print("2: Enter path for text file")
    print("Choose which method you want to proceed with...")
    x = input()
    if x == "1":
        print("type the secret message")
        secretmsg = input()
    elif x == "2":
        print("Enter path for text file")
        path = input()
        file = open(path, "r", encoding="utf-8")
        secretmsg = file.read()
        file.close()
    else: 
        print("Invalid Choice")
        return
    msgbytes = list(secretmsg.encode("utf-8"))
    delimiterbytes = list(delimiter.encode("utf-8"))
    payloadbytes = msgbytes + delimiterbytes
    payloadbits = []
    for j in payloadbytes:
        for i in range(7, -1, -1):
            payloadbits.append((j >> i) & 1)
    f = open(imagepath, "rb")
    imagebytes = f.read()
    f.close()
    dataoffset = GetDataOffset(imagebytes)
    available = len(imagebytes) - dataoffset
    required = len(payloadbits)
    if required > available:
        print(" Not enough space")
        return
    encoded = bytearray(imagebytes)
    x = 0
    for j in range(dataoffset, len(encoded)):
        if x >= required:
            break
        else:
            encoded[j] = setlsb(encoded[j], payloadbits[x])
            x += 1
    
    file = open(outputpath,"wb")
    file.write(encoded)
    file.close()
    print("Message hidden in:", outputpath)

def decode():
    print("Decode Mode")
    print("Enter Path for Encoded image")
    encodedpath = input()
    file = open(encodedpath, "rb")
    imagebytes = file.read()
    file.close()
    dataoffset = GetDataOffset(imagebytes)
    delimiterbytes = list(delimiter.encode("utf-8"))
    delimiterbits = []
    for j in delimiterbytes:
        for i in range(7, -1, -1):
            delimiterbits.append((j >> i) & 1)
    delimiterlength = len(delimiterbits)
    extractedbits = []
    for i in range(dataoffset, len(imagebytes)):
        extractedbits.append(getlsb(imagebytes[i]))
        if len(extractedbits) >= delimiterlength:
            if extractedbits[-delimiterlength:] == delimiterbits:
                secretbits = extractedbits[:-delimiterlength]
                secretbytes = bittobyte(secretbits)
                encodedmsg = bytes(secretbytes).decode("utf-8", errors="ignore")
                print("Encoded message is:", encodedmsg)
                return
    print("No secret message found.")

def GetDataOffset(offset):
    return offset[10] + (offset[11] << 8) + (offset[12] << 16) + (offset[13] << 24)

def setlsb(byte, bit):
    return (byte & 0b11111110) | (bit & 1)

def getlsb(byte):
    return byte & 1

def bytetobit(bytelist):
    bits = []
    for j in bytelist:
        for i in range(7, -1, -1):
            bits.append((j >> i) & 1)
    return bits

def bittobyte(bitlist):
    if len(bitlist) % 8 != 0:
        raise ValueError("Bit list length must be a multiple of 8")
    output = []
    for i in range(0, len(bitlist), 8):
        b = 0
        for j in range(8):
            b = (b << 1) | (bitlist[i + j] & 1)
        output.append(b)
    return output
  
main()
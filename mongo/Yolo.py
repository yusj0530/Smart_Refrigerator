f = open("D:\\test\새파일.txt", 'r')

def newfile():
    f.close()
# newfile()

def writer():
    for i in range(1, 11):
        data = "%d번째 줄입니다.\n" % i
        f.write(data)
    f.close()
# writer()

def reader():
    while True:
        line = f.readline()
        if not line:
            break
        print(line, type(line))

    f.close()
# reader()

def readlines():
    while True:
        line = f.readlines()
        if not line:
            break
        print(line, type(line))
        name = line[1]
        print(name, type(name))


readlines()
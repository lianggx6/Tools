file = open("E:\\data_future_0810.txt", mode="rb")
num = 10
while num:
    data = file.read(1024)
    l = [hex(int(i)) for i in data]
    print(" ".join(l))
    num -= 1

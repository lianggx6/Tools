import gzip
file = gzip.open("E:\\temp_data_future_0830.txt.gz", mode="rb")
# num = 10
# while num:
data = file.read(1024)
l = [hex(int(i)) for i in data]
print(" ".join(l))
    # num -= 1

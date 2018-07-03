import sys
file =open("message.txt")
file_w = open("messageReplace.txt","a")
line = file.readline()
print(line)
flag = True
while (flag):
    try:
        nextline = file.__next__()
        flag = (nextline.strip()=="")
        print(flag)
    
        

    except:
        print('except')

print("over")
file_w.flush()
file_w.write("12312312")

file.close()
file_w.close()



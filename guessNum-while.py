num=10
print ("guess what i think")
answer=int(input())
while answer != num:
    if answer > num:
        print("%d 有点大啊" %answer)
    if answer  < num:
        print("%d 有点小啊" %answer)
    answer=int(input())

print ("BINGO,%d is right" %answer)

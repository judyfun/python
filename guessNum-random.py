from random import randint
a = randint(1,100)
flag=True
while flag:
    answer=int(input())
    if a==answer:
        print("BINGO")
    if a<answer:
        print("有点大")
    if a>answer:
        print("有点小")

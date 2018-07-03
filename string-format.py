import math
import re
import random
import time
import pickle
class Vehicle:
    def __init__(self,speed):
        self.speed = speed

    def drive(self,distance):
        print('need %f hours' %(distance / self.speed))

class Bike(Vehicle):
    pass

class Car(Vehicle):
    def __init__(self,speed,fuel):
        Vehicle.__init__(self,speed)
        self.fuel = fuel

    def drive(self,distance):
        Vehicle.drive(self,distance)
        print('nedd %f fuels ' %(distance * self.fuel))

b = Bike(15.0)
c = Car(80.0,0.012)
b.drive(100)
c.drive(100)

print("============")
def get_pos(n):
    return(n/2,n*2)

x,y = get_pos(20)
print (x)
print (y)

lon = get_pos(9)
print(lon[0])
print(lon[1])

print('----------')
print(math.pi)
print(math.e)
print(math.ceil(2.1))


print("============")
text = "Hi,I am Shirley Hilton. I am his wife."
m = re.findall(r"\S",text)
if m:
    print(m)
else:
    print ('not match')

print("=========")

a = random.choice([1,2,3,4])
print (a)

b = random.randrange(4,20,5)
print(b)

c = random.sample([1,2,3,4,5],2)
print(c)
d =[12,3,4,5]
e= random.shuffle(d)
print(d)

print("======+++++++++++++")
print(1)
time.sleep(10)
print(2)

test_data = ['Save me!', 123.456, True]



f = open('test.data', 'wb+')

pickle.dump(test_data, f)

f.close()

print("========")
f= open("test.data")
test_data=pickle.load(f)
print(test_data)





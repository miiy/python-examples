from threading import Timer

def hello():
    print('hello, world')

t = Timer(30.0, hello)
t.start()

print(1)

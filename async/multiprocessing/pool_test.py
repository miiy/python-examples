import random
import time
from multiprocessing import Pool

def f(x):
    rand = random.randint(1, 5)
    print(rand)
    time.sleep(rand)
    return x*x

if __name__ == "__main__":
    t1 = time.time()
    with Pool(5) as p:
        print(p.map(f, [1, 2, 3]))
    print(time.time() - t1)

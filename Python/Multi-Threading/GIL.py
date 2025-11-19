import threading
import time

def count(n):
    while n > 0:
        n -= 1

start = time.time()
t1 = threading.Thread(target=count, args=(10**7,))
t2 = threading.Thread(target=count, args=(10**7,))

t1.start()
t2.start()
t1.join()
t2.join()

print("Time taken with threads:", time.time() - start)

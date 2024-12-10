import threading
import random
import time
from collections import deque

NUM_BUFFERS = 5
BUFFER_SIZE = 100
NUM_WORKERS = 2

buffers = [deque() for _ in range(NUM_BUFFERS)]
buffer_locks = [threading.Lock() for _ in range(NUM_BUFFERS)]
buffer_not_empty = [threading.Condition(lock) for lock in buffer_locks]
buffer_not_full = [threading.Condition(lock) for lock in buffer_locks]
stop = False

def master_thread(thread_id):
    global stop
    while not stop:
        data = random.randint(0, 99)

        with buffer_not_full[thread_id]:
            buffer_not_full[thread_id].wait_for(lambda: len(buffers[thread_id]) < BUFFER_SIZE)
            buffers[thread_id].append(data)
            print(f"Master {thread_id} produced data {data}")
            buffer_not_empty[thread_id].notify()
        
        time.sleep(0.5)

def worker_thread():
    global stop

    while not stop:
        chosen_buffer = -1
        data = -1

        for i in range(NUM_BUFFERS):
            if buffer_locks[i].acquire(blocking=False):
                if buffers[i]:
                    chosen_buffer = i
                    data = buffers[i].pop()
                    buffer_locks[i].release()
                    break
                buffer_locks[i].release()
        
        if chosen_buffer != -1:
            print(f"Worker consumed data {data} from buffer {chosen_buffer}")
            with buffer_not_full[chosen_buffer]:
                buffer_not_full[chosen_buffer].notify()
        else:
            time.sleep(1)

if __name__ == "__main__":
    master_threads = []
    for i in range(NUM_BUFFERS):
        t = threading.Thread(target=master_thread, args=(i,))
        master_threads.append(t)
        t.start()

    worker_threads = []
    for i in range(NUM_WORKERS):
        t = threading.Thread(target=worker_thread)
        worker_threads.append(t)
        t.start()

    time.sleep(5)
    stop = True

    for t in master_threads:
        t.join()

    for t in worker_threads:
        t.join()
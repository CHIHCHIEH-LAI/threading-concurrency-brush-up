import threading
import random

SIZE = 10**8
NUM_THREADS = 8

found_index = -1
lock = threading.Lock()

def linear_search(arr, key, thread_id):
    global found_index

    chunk_size = SIZE // NUM_THREADS

    start = thread_id * chunk_size
    end = len(arr) if thread_id == NUM_THREADS - 1 else start + chunk_size

    for i in range(start, end):
        with lock:
            if found_index != -1:
                return
        
        if arr[i] == key:
            with lock:
                if found_index == -1:
                    found_index = i
            return

def main():
    arr = [random.randint(0, 99) for _ in range(SIZE)]

    threads = []
    key = random.randint(0, 99)

    for i in range(NUM_THREADS):
        thread = threading.Thread(target=linear_search, args=(arr, key, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    if found_index == -1:
        print("Element not found in the array.")
    else:
        print(f"Element found at index: {found_index}")


if __name__ == "__main__":
    main()
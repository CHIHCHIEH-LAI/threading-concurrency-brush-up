import threading
import random

SIZE = 10**8
NUM_THREADS = 4

found_indices = []
lock = threading.Lock()

def linear_search(arr, key, thread_id):
    global found_index

    chunk_size = SIZE // NUM_THREADS

    start = thread_id * chunk_size
    end = len(arr) if thread_id == NUM_THREADS - 1 else start + chunk_size

    for i in range(start, end):  
        if arr[i] == key:
            with lock:
                found_indices.append(i)

def main():
    arr = [random.randint(0, 9999) for _ in range(SIZE)]

    threads = []
    key = random.randint(0, 9999)

    for i in range(NUM_THREADS):
        thread = threading.Thread(target=linear_search, args=(arr, key, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    if not found_indices:
        print("Element not found in the array.")
    else:
        print(f"Element found at indices: {found_indices}")


if __name__ == "__main__":
    main()
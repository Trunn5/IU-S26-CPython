import os

def square(n):
    return n ** 2

def increment(shared_val, lock):
    for _ in range(1000):
        with lock:
            shared_val.value += 1

def worker_queue(q):
    message = q.get()
    print(f"PID {os.getpid()}: {message}")

def worker_receiver(conn):
    number = conn.recv()
    result = number ** 2
    conn.send(result)
    conn.close()

def register_process(shared_dict, name):
    pid = os.getpid()
    shared_dict[name] = (pid, f"Hello from {name}")

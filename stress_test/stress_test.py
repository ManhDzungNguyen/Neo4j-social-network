import subprocess
from multiprocessing import Process


def run_consumer(skip: int, limit: int):
    proc = subprocess.Popen(f"python  task.py -s {skip} -l {limit}", shell=True)
    # print(proc.pid)
    proc.communicate()


if __name__ == "__main__":
    execs = []

    no_process = 80
    total_nodes = 31996
    limit = 100
    skip = 0

    for i in range(no_process):
        ex = Process(target=run_consumer, args=(skip, limit))
        execs.append(ex)
        ex.start()
        skip = (skip+limit) % total_nodes
    print(f"no_process: {no_process}")

    for exe in execs:
        exe.join()

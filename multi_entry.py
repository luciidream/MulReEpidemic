import multiprocessing as mp
import subprocess as sp
import time


def run_single_entry(multi_entry_prefix):
    sp.call(['E:/Anoconda/python.exe', 'main.py', multi_entry_prefix])


if __name__ == '__main__':

    start = time.time()
    processes = []
    num_instances = 10

    for i in range(num_instances):
        print('Processing instance ', i)
        multi_entry_prefix = f'output_{i}'
        p = mp.Process(target=run_single_entry, args=(multi_entry_prefix,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    end = time.time()
    print('All processes done')
    print(f'Total time: {end - start}')

import pandas as pd
import time
from multiprocessing import Process, Queue
from concurrent.futures import ThreadPoolExecutor


def consumer(q, k):
    result = []
    while True:
        res = q.get()
        if res is None:
            break
        result.append(res)
    result = pd.DataFrame(result, columns=list('abc'))
    result.to_csv(f'{k}.csv', index=None, header=True)
    print(f'{k} finish')


def producer(q, num):
    time.sleep(1)
    q.put([num, num * 10, num * 100])


def main():
    result_q = {'a': Queue(10), 'b': Queue(10)}
    plist = []
    for k in result_q:
        p = Process(target=consumer, args=(result_q[k], k))
        plist.append(p)
        p.start()

    futures = []
    with ThreadPoolExecutor(50) as executor:
        for i in range(100):
            if i % 2:
                futures.append(executor.submit(producer, result_q['a'], i))
            else:
                futures.append(executor.submit(producer, result_q['b'], i))

        for f in futures:
            _ = f.result()

    for k in result_q:
        result_q[k].put(None)

    for p in plist:
        p.join()


if __name__ == '__main__':
    main()

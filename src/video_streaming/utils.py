from collections import deque

def pair(iterator, num=2):
    que = deque([], maxlen=num)
    for item in iterator:
        que.append(item)
        if len(que) < num: continue
        yield tuple(que)

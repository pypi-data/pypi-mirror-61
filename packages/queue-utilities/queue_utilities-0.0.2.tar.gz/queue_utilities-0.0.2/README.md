# queue-utilities

Let's make using Queues great again! Queue utilities and conveniences for those using sync libraries.

_Currently implements using threads and threading queues only, multiprocessing queues and process support will be implemented soon._

This utilities package contains the following classes:

1. **Pipe** - Pipe messages from one queue to another.
2. **Timer** - Threaded timer that emits time on internal or provided queue after given wait time period. Can be cancelled.
3. **Ticker** - Same as timer but emits time at regular intervals until stopped.
4. **Multiplex** - Many-to-One (fan-in) queue management helper.
5. **Multicast** - One-to-Many (fan-out) queue management helper.
6. **Select** - Like Multiplex but output payload contains message source queue to be used in dynamic message based switching. Inspired by Golangs select statements using channels.

**Note that this package is early stages of development.**

## Installation

```bash
python3 -m pip install queue-utilities
```

## Usage

### Pipe

```python
from queue_utilities import Pipe

original_q, output_q = _queue.Queue(), _queue.Queue()

p = Pipe(original_q, output_q)

# put an item into the original queue
original_q.put(1)

# get the message off the output queue
recv = output_q.get()
print(recv)  # 1

# don't forget to stop the pipe after you've finished.
p.stop()
```

### Timer

```python
from queue_utilities import Timer

# emit time after 5 seconds
five_seconds = Timer(5)
five_seconds.get()

# cancel a timer
to_cancel = Timer(60)
print(to_cancel._is_finished) # False
to_cancel.stop()
print(to_cancel._is_finished) # True

```

### Ticker

```python
from queue_utilities import Ticker

# print the time every 5 seconds 4 times
tick = Ticker(5)
for _ in range(4):
    print(f"The time is: {tick.get()}")

# cancel the ticker thread
tick.stop()

```

### Multiplex

```python
from queue_utilities import Multiplex

# TODO
```

### Multicast

```python
from queue_utilities import Multicast

# TODO
```

### Select

#### Timeout a function with Timer

```python
from threading import Thread
import time
from queue import Queue
from queue_utilities import Select, Timer


def do_something_slow(q: Queue) -> None:
    # do something slow
    time.sleep(3)
    q.put("Done")


output_q = Queue()
Thread(target=do_something_slow, args=(output_q,)).start()

timeout = Timer(2)

select = Select(output_q, timeout._output_q)

for (which_q, result) in select:
    if which_q is output_q:
        print("Received result", result)
    else:
        print("Function timed out!")
    break

select.stop()
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

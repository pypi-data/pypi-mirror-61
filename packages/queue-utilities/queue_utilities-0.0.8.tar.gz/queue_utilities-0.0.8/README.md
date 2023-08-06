# queue-utilities

Let's make using Queues great again! Queue utilities and conveniences for those using sync libraries.

_Currently implements using threads and threading queues as standard, multiprocessing queues can be used by passing in relevant multiprocessing.Queue arguments. Worker threads use threading.Thread not multiprocessing.Process by design, if you require running eg Select in an external process as a message broker I recommend spawning a Process and then using as is documented._

This utilities package contains the following classes:

1. **Pipe** - Pipe messages from one queue to another.
2. **Timer** - Threaded timer that emits time on internal or provided queue after given wait time period. Can be cancelled.
3. **Ticker** - Same as timer but emits time at regular intervals until stopped.
4. **Multiplex** - Many-to-One (fan-in) queue management helper.
5. **Multicast** - One-to-Many (fan-out) queue management helper.
6. **Select** - Like Multiplex but output payload contains message source queue to be used in dynamic message based switching. Inspired by Golangs select statements using channels.
7. **as_thread** - Decorator to run function in thread.
8. **attach_queue** - Decorator to attach input and output queues to function which will be run in a thread.

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
from queue import Queue

# create two queues and pass them into the Multiplex
queue_a, queue_b = Queue(), Queue()
multi_p = Multiplex(queue_a, queue_b)

# send messages to any of the queues
queue_a.put("a")
queue_b.put("b")

# read the messages
for _ in range(2):
    message = multi_p()  # or multi_p.get()
    print(f"I got a message! {message}")

# cleanup
multi_p.stop()

# if you try to read a message after stop
# it raises a MultiplexClosed exception
multi_p.get()

```

### Multicast

```python
from queue_utilities import Multicast
from queue import Queue

out_a, out_b = Queue(), Queue()

multicast = Multicast(out_a, out_b)

multicast.send("A message!")

for q in (out_a, out_b):
    print(q.get()) # prints "A message!" twice!

multicast.stop()
```

### Select

#### Use with context to build a cancellable thread

```python
from queue_utilities import Select
from queue import Queue
from threading import Thread

out_a, cancel_sig = Queue(), Queue()


def selector(*queues):
    with Select(*queues) as select:
        for which, message in select:
            if which is cancel_sig:
                # stop select on any message on queue b
                select.stop()
            else:
                print(f'Got a message {message}')


Thread(target=selector, args=(out_a, cancel_sig)).start()

out_a.put(1)
out_a.put(2)
out_a.put(3)
cancel_sig.put('Bye')
```

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

### as_thread

```python
from queue_utilities import as_thread
import time

@as_thread
def sleeper():
    time.sleep(5)
    print('Goodbye!')

sleeper()
print('Waiting...')
time.sleep(6)
print('Done!')

```

### attach_queue

```python
from queue_utilities import attach_queue
from queue import Queue

work_queue = Queue()
result_queue = Queue()

@attach_queue(work_queue, result_queue)
def squarer(input: int):
    return input**2

for i in range(10):
    work_queue.put(i)
    print(f'{i} squared is {result_queue.get()}')
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

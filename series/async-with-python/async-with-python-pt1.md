# Asynchronous Execution with Python (Pt. 1)

For a general overview of the advantages and concepts behind async patterns, check out:
- [Guide to Asyncio - Medium](https://medium.com/dev-bits/a-minimalistic-guide-for-understanding-asyncio-in-python-52c436c244ea)
- [JavaScript EventLoop - MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/EventLoop)
- [asyncio - PyDocs](https://docs.python.org/3.10/library/asyncio.html)

With Python’s `asyncio` library you can write **concurrent** code for **I/O-bound** strategies. This differs from the `multiprocessing` library which focuses on using threads for **CPU-bound** strategies.

The `asyncio` library along with the `async`/`await` keywords enable this by using a concept called the "**Event Loop**". This provides an abstract way to create and schedule asynchronous loops and functions. JavaScript, being used in front-end interaction in browsers, is also based around the event loop concept making it a perfect language to compare/examine this concept.

> Note: Some of the `asyncio` functions implemented in Python 3.7+ may be _`Deprecated`_ in Python 3.10+

## Synchronous Execution
---
Normally when programming in Python and most other _Procedural_ languages, programs are executed from top to bottom (even if the code is not structured as such; see language interpretation/compilers). This means that each statement is executed after the completion of the prior statement(s).

In example, say we have an `random_add` function that sums a `list` of random `int`s after a specified `delay` (in seconds):
```python
def random_add(delay: int) -> None:
	import time
	time.sleep(delay)
	# This retrieves a list of random ints
	n = random_number_list()
	print(f'Sum({n}) = {sum(n)}')
```
and we execute this function 3 times in succession:
```python
if __name__ == "__main__":
	random_add(5) # call1: Delayed 5s
	random_add(8) # call2: Delayed 8s
	random_add(2) # call3: Delayed 2s
```
the total timing would be near 15s. With each call completing one after the next as shown [below](#synchronous-timing).

Even though the `random_add` function is not performing any calculations during its delayed period, it still has resources allocated for that period. This is why the time consumption of normal synchronous programs can typically be described as the sum of all of its procedures.

### Synchronous Timing
call|start|finish|finish order
:---:|----:|----:|-----
1 |  0s |  5s | 1 
2 |  5s | 13s | 2
3 | 13s | 15s | 3

## Asynchronous Execution
---
We can reuse the prior `random_add` function and adapt it to execute asychronously:
```python
import asyncio
async def random_add(delay: int) -> None:
	asyncio.sleep(delay)
	# This retrieves a list of random ints
	n = random_number_list()
	print(f'Sum({n}) = {sum(n)}')
```
now to execute this function 3 times just as before:
```python
if __name__ == "__main__":
	await random_add(5)
	await random_add(8)
	await random_add(2)
```
Uh Oh! You should receive a `SyntaxError` similar to:
```pwsh
	await random_add(5)
	^^^^^^^^^^^^^^^^^^^
SyntaxError: 'await' outside function
```
This issue may have even been detected by the IDE you are using before running the Python script. This is because `await` can only be used in `async` scopes and the `main` thread is _synchronous_ without an event loop! To execute this code we must:  
1. Wrap this code in a `async` function:
	```python
	async def async_test():
		await random_add(5)
		await random_add(8)
		await random_add(2)
	```
2. Then utilize the `asyncio.run` function
	```python
	if __name__ == "__main__":
		asyncio.run(async_test())
	```

Now the code should run happily. However, the code is still taking the same amount of time to execute. Why is that? Doesn't `async` make it work in parallel?

The reason is that the `await` keyword means the parent function will _await_ a result before continuing to the next statement. Since the response is delayed it will wait for that period.

To execute the `random_add` function calls concurrently, we need to create `Task`s to execute them in. This can be done via `asyncio.create_task` individually:
```python
async def async_test_task():
	task1 = asyncio.create_task(random_add(5))
	task2 = asyncio.create_task(random_add(8))
	task3 = asyncio.create_task(random_add(2))
	await task1, await task2, await task3
```
or via `asyncio.gather` for lists of tasks:
```python
async def async_test_gather():
	await asyncio.gather(
		random_add(5),
		random_add(8),
		random_add(2)
	)
```

For the rest of this post we will be utilizing `asyncio.gather` for simplicity. There are certain scenarios (eg. variable task creation) that `asyncio.create_task` is applicable.

Now that the code has been adjusted you will observe that the total execution time is only limited by the slowest task! Also, the order each task completes differs (shown [below](#asynchronous-timing)).

### Asynchronous Timing
call|start|finish|finish order
:---:|----:|----:|-----
1 |  0s |  5s | 2 
2 | ~0s |  8s | 3
3 | ~0s |  2s | 1

This is just the start of the features that are provided by `async`/`await` and the `asyncio` library in Python. Be sure to read Part 2 of this overview once it is released.
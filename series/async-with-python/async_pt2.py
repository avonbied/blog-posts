import asyncio
from functools import wraps, partial
from time import time

def make_async(func):
	@wraps(func)
	async def async_func(*args, loop=None, executor = None, **kwargs):
		if loop is None:
			loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
		return await loop.run_in_executor(executor, partial(func, *args, **kwargs))
	return async_func


async def sleep_async(loop: asyncio.AbstractEventLoop, delay):
	await loop.run_in_executor(None, time.sleep, delay)

async def sleep_to_thread(delay):
	await asyncio.to_thread(time.sleep(delay))

async def no_wait():
	async def counter_loop():
		end = 100
		print(f'Let\'s count to {end}')
		for i in range(1, end):
			await asyncio.sleep(0.25)
			print(f'{i}')
	async def delayed_value():
		print('RETRIEVING VALUE')
		val = (1,'john', 'doe')
		await asyncio.sleep(5)
		print(f'RETRIEVED VALUE: {val}')
	t1 = asyncio.create_task(counter_loop())
	t2 = asyncio.create_task(delayed_value())
	await t2

if __name__ == '__main__':
	asyncio.run(no_wait())
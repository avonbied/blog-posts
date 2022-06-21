import asyncio, time, random

def gen_id():
	id = 1
	while id < 10:
		yield id
		id += 1
get_id = gen_id()

def get_inputs():
	return [random.randint(0, 50) for x in range(2)] 

# A co-routine
async def random_add(delay: int, is_sync: bool) -> None:
	i = next(get_id)
		# This represents a long-running blocking process
	if is_sync:
		time.sleep(delay)
	else:
		# This represents a long-running non-blocking process
		await asyncio.sleep(delay)
	n = get_inputs()
	print(f'#{i}a: sum({n}) = {sum(n)}')

async def async_radd(delay: int) -> None: await random_add(delay, False)
async def sync_radd(delay: int) -> None: await random_add(delay, True)

# Create a function to schedule co-routines on the event loop
# then print results and stop the loop
async def sync_test():
	await asyncio.gather(sync_radd(5), sync_radd(8), sync_radd(2))

async def mixed_test():
	t = set()
	t.add(asyncio.create_task(async_radd(5)))
	t.add(asyncio.create_task(sync_radd(8)))
	t.add(asyncio.create_task(async_radd(2)))
	[await e for e in t] 

async def async_test():
	await asyncio.gather(async_radd(5), async_radd(8), async_radd(2))

if __name__ == "__main__":
	# An event loop
	examples = [sync_test, mixed_test, async_test]
	for f in examples:
		print(f'START {f.__name__}')
		s = time.perf_counter()
		asyncio.run(f())
		elapsed = time.perf_counter() - s
		print(f'END {f.__name__} executed in {elapsed:0.2f} seconds.\n')

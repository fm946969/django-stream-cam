import asyncio
import time

run = True
i = 0
j = 0
async def loop():
    global run, i, j
    while run:
        print(f'{i = }')
        await asyncio.sleep(0.1)
        i += 1

async def loop2():
    global run, i, j
    for j in range(3):
        await asyncio.sleep(5)
        i = 0
        print(f'reset {i = }')
    run = False

async def loop3():
    global run, i, j
    while run:
        print(f'{j = }')
        await asyncio.sleep(0.033)
        j += 1

async def main():
    l1 = asyncio.create_task(loop())
    l2 = asyncio.create_task(loop2())
    l3 = asyncio.create_task(loop3())

    await l1
    await l2
    await l3

asyncio.run(main())
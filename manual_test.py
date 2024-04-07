from client.job_status import TimerClient
import asyncio

async def main():
    client = TimerClient()
    client.start_timer(10)
    task = asyncio.create_task(client.get_timer_status())
    print("Non-blocking code")
    await task

asyncio.run(main())

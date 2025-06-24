import asyncio
import logging
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from unigate.utils.exam_sync import sync_exam_results


def start_scheduler():
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(lambda: asyncio.run(sync_exam_results()), 'interval', weeks=2)
    scheduler.start()
    print(f"Scheduler started - exam sync will run every 2 weeks")
    print(f"Next run scheduled for: {job.next_run_time}")
    print(f"Current time: {datetime.now()}") 
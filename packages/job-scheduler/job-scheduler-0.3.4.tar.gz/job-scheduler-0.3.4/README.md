Scheduler
=======================

Simple scheduler module
----

### Installation

Only tested on Python 3.X

From source:

```sn
$ python setup.py install
```

For production:

```sn
$ pip install job-scheduler
```

### Usage

```python
from datetime import datetime
from datetime import timedelta
from haydn.scheduler import S
from haydn.event_emitter import EventEmitter
import logging

logging.basicConfig(level=logging.DEBUG)


class Example(EventEmitter):

    def __init__(self):
        self.schedule_manager = Scheduler(timer_interval=1)

    def main(self):
        schedule_time = ScheduleTime(start_datetime=datetime.utcnow() + timedelta(seconds=2), end_datetime=datetime.utcnow() + timedelta(seconds=100), repeat=ScheduleTime.REPEAT_SECOND, repeat_interval=5, repeat_limit=5)
        schedule = Schedule(schedule_time, self.do_something, task_params=[1], reference_id=1)

        self.schedule_manager.add_schedule(schedule)
        self.schedule_manager.start()

    def do_something(self, p1):
        print("doing task")
        print("task parameter: ", p1)


example = Example()
example.main()

```
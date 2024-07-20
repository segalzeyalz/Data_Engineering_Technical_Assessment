# Pipeline Design

## Objective
The objective of this assignment is to design and implement a data processing pipeline capable of
executing various data processing tasks on raw data.
This system will process the tasks, store the results in a database or data lake,
and provide telemetry and monitoring capabilities.

# Option 1:
For this task we should have a map between tasks running and the functions.

each Task model have a status (pending, running, completed, failed),
function name, start time and end time.

```python

class TaskStatus:
    PENDING = 'pending'
    RUNNING = 'running'
    SUCCESS = 'completed'
    FAILED = 'failed'

class Task:
    def __init__(self, id: str, name: str, func: callable, status: TaskStatus = TaskStatus.PENDING, result: Optional[Any] = None):
        self.id = id
        self.name = name
        self.func = func
        self.status = status
        self.result = result
        self.start_time = None
        self.end_time = None

    def run(self):
        try:
            self.status = TaskStatus.RUNNING
            self.start_time = datetime.now()
            self.result = self.func()
            self.status = TaskStatus.SUCCESS
        except Exception as e:
            self.status = TaskStatus.FAILED
            self.result = str(e)
        finally:
            self.end_time = datetime.now()
            self.save_to_db()

    def save_to_db(self):
        session = Session()
        task_record = TaskModel(
            id=self.id,
            name=self.name,
            status=self.status,
            result=self.result,
            start_time=self.start_time,
            end_time=self.end_time
        )
        session.add(task_record)
        session.commit()
        session.close()

    @staticmethod
    def get_task_by_id(task_id: str) -> 'TaskModel':
        session = Session()
        task_record = session.query(TaskModel).filter_by(id=task_id).first()
        session.close()
        return task_record

    def __repr__(self):
        return f"<Task(id={self.id}, name={self.name}, status={self.status}, result={self.result})>"

```

and there is a task runner:
```python
# Tasks is a dict of task and a callable function
Tasks = {
    "Task 1": task1,
    "Task 2": task2,
    "Task 3": task3,
}
for task in TaskModel.query.filter_by(status=TaskStatus.PENDING):
    task_func = Tasks[task.name]
    task_func.run()
```


SQL DB table will looks like:
```sql
CREATE TABLE tasks (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    status VARCHAR NOT NULL,
    result TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP
);
```

One task execute another task example:
```python
def task1():
    task2 = Task(id="2", name="Task 2", func=task2)
    return "Task 1 completed successfully!"
```

## Exectuion options

## Telemetry and Monitoring
Each task execution should be monitored, and its state and results should be stored. This allows for querying the execution status and results at any time.

```python
def example_task():
    return "Task completed successfully!"

task = Task(id="1", name="Example Task", func=example_task)
task.run()

print(task)

```


# Pipeline Design

## Objective
This assignment involves the design and development of a data pipeline
system that would be able to execute multiple data processing jobs over the raw data.
The system processes, stores results in a database and provides telemetry and monitoring capabilities.


## Stack Selection

### Chosen Stack: PostgreSQL

I selected PostgreSQL as primary database for this data processing pipeline due to its robust features and suitability for the requirements.

#### Reasons for Choosing PostgreSQL:

1. **Structured Data Support**: each task have start time, id, func etc and duration, simple to monitor it that way and to query it although the tradeoffs like multiple fields might be different from task to task

2. **Complex Query Capabilities**: PostgreSQL's powerful query engine enables efficient filtering, sorting, and aggregation of task data, which is crucial for monitoring and analysis, and will perform better that mongo for example.

3. **ACID Compliance**: Ensures data integrity and consistency, which is good for tracking task states and results accurately.

4. **Indexing Capabilities**: Allows for optimized querying on frequently accessed fields like status and timestamps, enhancing performance (these fields actually can be indexed in mongo too - which might be a great option here too).

5. **Scalability**: PostgreSQL can handle large volumes of data and concurrent connections, supporting the growth of pipeline.

6. **Integration with Monitoring Tools**: Easy integration with tools like Prometheus for metrics collection and visualization.

### Trade-offs and Alternatives

1. **MongoDB**: 
   - Pro: Offers flexibility for tasks with varying data structures due to its schema-less nature.
   - Con: May sacrifice some query performance and ACID compliance compared to PostgreSQL.

2. **ElasticSearch**: - actually can be additional DB for the results saving and than make search efficiently
   - Pro: Excels in full-text search and log analysis, which could be beneficial for complex log parsing or text-heavy task results.
   - Con: May introduce additional complexity in setup and maintenance.

How this is going to look like:
1. System Architecture Diagram
![System Architecture Diagram.png](System%20Architecture%20Diagram.png)


2. Data Flow Diagram:
![Data Flow Diagram.png](Data%20Flow%20Diagram.png)
3. Task on database:

![Task SQL.png](Task%20SQL.png)

4. Sequence Diagram:
![Sequence Diagram.png](Sequence%20Diagram.png)

For this task we should have a map between tasks running and the functions.

each Task model have a status (pending, running, completed, failed),
function name, start time and end time.

```python
# Metrics - we can use prometheus for this
REQUEST_TIME = Summary('task_processing_seconds', 'Time spent processing task')
TASK_COUNT = Counter('task_count', 'Number of tasks processed', ['status'])

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
            logging.info(f"Task {self.id} - {self.name} started.")
            self.result = self.func()
            self.status = TaskStatus.SUCCESS
        except Exception as e:
            self.status = TaskStatus.FAILED
            self.result = str(e)
            logging.error(f"Task {self.id} - {self.name} failed with error: {e}")
        finally:
            self.end_time = datetime.now()
            self.save_to_db()
            logging.info(f"Task {self.id} - {self.name} ended with status {self.status} and result: {self.result}")


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

### Exectuion options

We can run the tasks using CLI:
```bash
# List all tasks
python cli.py list_tasks
# Run a task
python cli.py run_task 1 "Task 1"
# Check task status
python cli.py task_status 1
```
This is implementing like this:
```python
@cli.command()
@click.argument('task_id')
@click.argument('task_name')
def run_task(task_id, task_name):
    """Run a task by ID and name."""
    task_func = Tasks.get(task_name)
    if not task_func:
        click.echo(f"Task {task_name} not found!")
        return
    
    task = Task(id=task_id, name=task_name, func=task_func)
    task.run()
    click.echo(f"Task {task_id} - {task_name} has been run. Status: {task.status}")

@cli.command()
@click.argument('task_id')
def task_status(task_id):
    """Check the status of a task by ID."""
    task = Task.get_task_by_id(task_id)
    if not task:
        click.echo(f"Task {task_id} not found!")
        return
    
    click.echo(f"Task {task_id} - {task.name} is {task.status}. Result: {task.result}")

@cli.command()
def list_tasks():
    """List all tasks."""
    tasks = Task.list_tasks()
    for task in tasks:
        click.echo(f"{task.id} - {task.name} - {task.status}")

if __name__ == '__main__':
    cli()
```

## Telemetry and Monitoring
Each task has it's logs - and easy to check the status of the task.

Each task execution should be monitored, and its state and results should be logged and stored. This allows for querying the execution status and results at any time. Additionally, metrics should be collected to provide insights into the performance and reliability of the system.

Each task has its logs and metrics, making it easy to check and monitor.

### Logging
- Detailed logs for each task execution, including start time, end time, duration, status, and errors, are stored in `task_log.log`.

### Metrics
- Task execution metrics are collected using Prometheus using the `prometheus_client` library (let''s assume have the ymls etc).
- Metrics include:
  - `task_processing_seconds`: Time spent processing each task.
  - `task_count`: Number of tasks processed, categorized by status.

### Logs
Detailed logs for each task execution, including start time, end time, duration, status, and errors, are stored in task_log.log.

### Example SQL Queries for Monitoring
```sql
# query all tasks
SELECT * FROM tasks;
# Query to get tasks by status
SELECT * FROM tasks WHERE status='completed';
#Query to get task details by ID:
SELECT * FROM tasks WHERE id='1';
#Query to get tasks executed within a specific time range:
SELECT * FROM tasks WHERE start_time BETWEEN '2024-01-01' AND '2024-12-31';

#Query to get the average execution time of tasks:
SELECT AVG(strftime('%s', end_time) - strftime('%s', start_time)) as avg_execution_time FROM tasks WHERE status = 'completed';
#Query to get the total number of tasks by status:
SELECT status, COUNT(*) as count FROM tasks GROUP BY status;
```
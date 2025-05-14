"""
Celery configuration for testing.
"""

from celery import Celery

# Create a test Celery app
app = Celery('tests')

# Configure the app for testing
app.conf.update(
    broker_url='memory://',
    result_backend='rpc',
    task_always_eager=True,  # Tasks will be executed locally instead of being sent to the queue
    task_eager_propagates=True,  # Propagate exceptions
    worker_hijack_root_logger=False,
    worker_log_color=False,
    task_time_limit=30,  # 30 seconds
    task_soft_time_limit=10,  # 10 seconds
    worker_max_tasks_per_child=1,
    worker_prefetch_multiplier=1,
)

# Import tasks to register them with the test app
import applications.tasks

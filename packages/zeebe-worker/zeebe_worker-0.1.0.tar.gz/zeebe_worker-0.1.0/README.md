# Zeebe Worker for Python

## Usage
### Install
`pip install zeebe-worker`

### Import
`from zeebe_worker import ZeebeWorker`

### Usage
```python
some_worker = ZeebeWorker(
    stub=zeebe_stub,
    type_='task-type',
    worker_name='worker-01',
    timeout=1 * 60*1000,
    request_timeout=5 * 60*1000,
    max_jobs_to_activate=1,
    target=handle_job)
some_worker.subscribe()

def handle_job(job):
    """Raise an Exception if the job should fail"""
    variables = json.loads(job.variables)
```

## Publish
- Bump version
- `python setup.py sdist`
- `twine upload dist/zeebe_worker-<version>.tar.gz -u <pypi-username> -p <pypi-password>`


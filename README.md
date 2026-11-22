# Reusable Python data engineering utilities

Small, dependency-free examples for data engineers and automation developers. All examples are original educational implementations with Python 3.10+.

## CSV quality profiler

Use a CSV file that has a header:

```bash
python python/csv_profiler.py path/to/orders.csv --keys order_id
```

The program emits a JSON report with total rows, blank-cell counts and percentages, and duplicate keys. Without `--keys`, duplicate detection considers all columns. It uses memory proportional to the number of distinct keys.

## Retry transient failures

```python
from python.retry import retry

result = retry(lambda: fetch_from_api(), attempts=3, base_delay=0.25)
```

The retry helper retries `TimeoutError` by default. Pass an explicit `retry_on` tuple for other known transient exceptions, rather than broadly retrying application errors. Operations should be idempotent before retrying.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Caveats

- CSV parser expects UTF-8/UTF-8-BOM, a single header line, and consistent columns.
- The profiler does not validate business rules, infer data types, or stream results to an external warehouse.
- Do not commit credentials or sensitive source data. Use test fixtures with synthetic information.

Contributions and bug reports welcome.

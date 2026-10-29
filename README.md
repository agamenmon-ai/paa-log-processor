# PAA Log Processor & JSON Exporter

A production-ready Python utility designed to handle low-level device log files, implement robust exception handling for file I/O operations, parse unstructured text streams, and export clean JSON reports.

## Key Features
- **Defensive File I/O:** Safely catches `FileNotFoundError` and `UnicodeDecodeError` during file ingestion.
- **Data Extraction:** Extracts endpoints, connection details, and specific operational states using string manipulation and exception guards.
- **JSON Serialization:** Exports structured analytical dictionaries into formatted JSON reports.

## Tech Stack
- Python 3.x
- Built-in modules: `json`, `pprint`

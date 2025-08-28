# Siple REST example

This is a simple project with fastApi REST

# Testing

```bash
curl -X POST "http://127.0.0.1:8000/upload-csv/" \
  -F "file=@data/data_test.csv;type=text/csv"
```
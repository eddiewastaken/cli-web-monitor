FROM python:3.9-alpine
# Or any preferred Python version.
ADD webserver.py .
RUN pip install fastapi
CMD ["python", "webserver.py", f'"powershell -c while (1) {Get-Date; sleep 1}"']
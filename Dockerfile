FROM python:3.14

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

#CMD ["fastmcp", "run", "main.py:mcp", "--transport=http", "--port=8000", "--host=0.0.0.0"]
CMD ["python", "main.py"]
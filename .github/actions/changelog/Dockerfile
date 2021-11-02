FROM python:3
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY main.py /main.py
CMD ["python", "/main.py"]

FROM python:3.10.12

ENV PYTHONUNBUFFERED=1

WORKDIR /bms

COPY re.txt .

RUN pip3 install -r re.txt

COPY . .

EXPOSE 8000

WORKDIR /bms/bms

CMD ["python3", "manage.py", "runserver"]
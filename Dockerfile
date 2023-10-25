FROM python:3

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

ENTRYPOINT [ "python", "enerbit/manage.py" ]

CMD ["runserver","0.0.0.0:8000" ]
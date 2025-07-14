FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src
COPY .env .
COPY wait-for-it.sh .

RUN chmod +x wait-for-it.sh

CMD ["./wait-for-it.sh", "appointment-db:5432", "--", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "4007", "--reload"]

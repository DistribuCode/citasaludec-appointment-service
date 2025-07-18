FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

COPY . .
#COPY .env .env   

RUN chmod +x wait-for-it.sh

EXPOSE 4007

CMD ["./wait-for-it.sh", "appointment-db:5432", "--", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "4007"]

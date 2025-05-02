FROM python:3.10-slim

WORKDIR /app

COPY sky_epg_grab.py .
COPY entrypoint.sh .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x entrypoint.sh

EXPOSE 8080

CMD ["./entrypoint.sh"]

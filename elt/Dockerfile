FROM python:3.8-slim

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY start.sh /app/start.sh
COPY elt_script.py .

RUN echo "0 3 * * * python /app/elt_script.py" | crontab

CMD ["python", "elt_script.py"]

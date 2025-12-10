FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
ENV FLASK_APP=app-v1.5.py
EXPOSE 5000
CMD ["python3", "-u", "app-v1.5.py"]
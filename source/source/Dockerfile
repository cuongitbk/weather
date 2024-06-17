FROM python:3.11
ENV PYTHONUNBUFFERED 1
RUN apt update -y
RUN apt-get install -y --no-install-recommends gettext && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
WORKDIR /src
ADD requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt
ADD . .

EXPOSE 8000
CMD ["gunicorn", "weather.wsgi",  "-b 0.0.0.0:8000",  "--worker-class=gthread",  "-w 3",  "--threads=3", "-t 300", "--max-requests=5000", "--max-requests-jitter=200", "--log-level=info"]
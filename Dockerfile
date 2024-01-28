FROM python:3.11

WORKDIR /app

# Miguels API key
#ENV OPENAI_API_KEY=

# Morningside API Key
ENV OPENAI_API_KEY=

# SendGrid API key
ENV SENDGRID_API_KEY=

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

ENTRYPOINT [ "python", "application.py" ]

# Goal is to migrate to Gunicorn but had issues with class instantiation and state across object instances.
#CMD ["gunicorn --bind :8500 app.application:server --log-level debug --preload --timeout 1800"]

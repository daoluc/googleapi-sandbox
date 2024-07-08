FROM python:3.12-slim@sha256:d5f16749562233aa4bd26538771d76bf0dfd0a0ea7ea8771985e267451397ae4

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

ENV PORT 8000

RUN pip install --no-cache-dir -r requirements.txt

# As an example here we're running the web service with one worker on uvicorn.
# CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT} --workers 1
CMD exec fastapi run main.py --port ${PORT}
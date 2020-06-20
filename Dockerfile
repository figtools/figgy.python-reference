FROM python:3.7-slim

WORKDIR /app
COPY src/requirements.txt /app
RUN pip install -r requirements.txt

RUN useradd -ms /bin/bash -d /tmp app_user && \
    chown -R app_user:app_user /app

COPY src/ /app

# Using root user to simplifying the demo across all different types of users with different configurations
# This enables us to write the generated figgy.json to the user's ./figgy/ directory
USER root

ENTRYPOINT ["python3"]
CMD ["app.py"]

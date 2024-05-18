FROM python:3.11
ENV PYTHUNBUFFERED=1
WORKDIR /app/

RUN pip install --upgrade pip
COPY ./requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/

RUN rm -rf /app/linuxVenv/ && \
    rm -rf /app/winVenv/

RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/start.sh
RUN chmod +x /app/runner.sh

ENTRYPOINT ["bash", "/app/runner.sh"]
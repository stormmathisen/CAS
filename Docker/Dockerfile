FROM python:3.10.12-alpine3.18
WORKDIR /usr/src/app
COPY ./server/requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt

RUN ["mkdir", "server"]
COPY ./server/ ./server
EXPOSE 5000
CMD ["python", "./server/server.py"]

FROM python:3.8-slim
WORKDIR /app 
COPY . /app 
RUN pip3 install -r requirements.txt 
EXPOSE 3000 
CMD python3 server.py
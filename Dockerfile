FROM python:3.8-slim

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

COPY check /opt/resource/check
COPY in /opt/resource/in
COPY webdav_res.py /opt/resource/webdav_res.py

RUN chmod +x /opt/resource/webdav_res.py

WORKDIR /opt/resource


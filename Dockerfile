FROM python:3.8.12
MAINTAINER sunyc<sunyuchen959@163.com>
ADD . /server
WORKDIR /server
VOLUME ["/var/data"]
RUN pip install --upgrade pip && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
CMD ["python", "app.py"]
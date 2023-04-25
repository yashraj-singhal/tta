FROM python:3.10
COPY . /ttc
WORKDIR /ttc/
RUN pip3 install -r ./requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]

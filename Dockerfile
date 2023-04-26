FROM python:3.10
COPY . /ttp
WORKDIR /ttp/
RUN pip3 install -r ./requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]

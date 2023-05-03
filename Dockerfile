FROM python:3.10
COPY . /tta
WORKDIR /tta/
RUN pip3 install -r ./requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]

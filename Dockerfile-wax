FROM python:3.9

ADD . /code 
RUN apt-get update
RUN pip install -r /code/requirements.txt

WORKDIR /code
ENV PYTHONPATH '/code/'

EXPOSE 8000

CMD ["python" , "/code/bpvalidate-exporter.py", "--network", "wax"]

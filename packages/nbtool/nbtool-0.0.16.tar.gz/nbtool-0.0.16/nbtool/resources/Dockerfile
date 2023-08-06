from nextbillionai/python:1.0-python3

ADD src/docker_requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

ADD src/*.py ./
ADD src/*.pyx ./
ADD src/*.ini ./

RUN python setup.py build_ext --inplace
CMD uwsgi uwsgi.ini


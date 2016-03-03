FROM python:3.5
ENV PYTHONBUFFERED 1

# PyBox2D and Swig 3.0
WORKDIR /tmp
RUN apt-get update && apt-get install -y build-essential python-dev swig3.0 python-pygame git
RUN ln -s /usr/bin/swig3.0 /usr/bin/swig
RUN git clone https://github.com/pybox2d/pybox2d
WORKDIR pybox2d
RUN python setup.py build
RUN python setup.py install
RUN apt-get autoremove -y
WORKDIR /

# Python packages
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/


FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requrirements.txt /app/requrirements.txt
RUN pip install -U pip setuptools wheel
RUN python -m pip install pyyaml
RUN pip install -r requrirements.txt
COPY . /app
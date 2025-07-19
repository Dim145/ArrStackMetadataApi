FROM python:3.12-alpine


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY . /code

ENV ROOT_DATA_PATH=/data
VOLUME ["/data"]

EXPOSE 80

CMD ["fastapi", "run", "main.py", "--port", "80"]
FROM python:3.8.10
COPY ./ /code
WORKDIR /code
RUN apt update

# poetry
RUN pip install -U pip &&  \
    pip install --no-cache poetry==1.6.1 &&  \
    poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-root

CMD python3 src/main.py

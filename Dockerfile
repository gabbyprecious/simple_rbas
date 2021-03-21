FROM python:3.9-buster

RUN mkdir /simple_rbas

RUN pip install -U pip

COPY ./requirements.txt ./simple_rbas/requirements.txt

RUN pip install --no-compile  -r /simple_rbas/requirements.txt

ENV PYTHONWARNINGS ignore
ENV PYTHONDONTWRITEBYTECODE=true
ENV PYTHONUNBUFFERED 1
ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.

COPY . /simple_rbas/

WORKDIR /simple_rbas

CMD ["gunicorn", "simple_rbas.wsgi"]
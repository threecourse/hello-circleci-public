FROM mcr.microsoft.com/dotnet/core/sdk:3.1

WORKDIR /tmp/work

RUN apt-get update && apt-get install -y python3.7 python3-pip
RUN ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

RUN pip install poetry
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && poetry install --no-interaction
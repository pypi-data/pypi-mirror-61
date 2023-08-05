FROM python:3.7.3-stretch

COPY requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install -qqy openssh-client \
  git python-dev default-libmysqlclient-dev ruby-dev rubygems build-essential cmake && \
  apt-get clean && \
  cd /opt && \
  curl -sLO https://github.com/dcoker/biscuit/releases/download/v0.1.3/biscuit-linux_amd64.tgz && \
  tar xzvf biscuit-linux_amd64.tgz && \
  mv biscuit /usr/bin/biscuit && \
  chmod +x /usr/bin/biscuit && \
  rm biscuit-linux_amd64.tgz && \
  groupadd -g 1000 app && \
  useradd -g 1000 -u 1000 --system app && \
  pip install -r /code/requirements.txt && \
  pip install pyinstaller setuptools wheel

USER app

WORKDIR /code

CMD ["/bin/bash"]

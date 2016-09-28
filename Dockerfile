FROM python:3.5
ENV PYTHONUNBUFFERED 1


RUN apt-get update && apt-get install -y \
    git \
    ca-certificates \
    curl \
&& update-ca-certificates && apt-get clean -y

# Install Nodejs
RUN curl -sL https://deb.nodesource.com/setup_4.x | bash && apt-get install -y --force-yes \
    nodejs \
&& apt-get clean -y

# Install Bower
RUN npm install bower -g && npm cache clean


RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

ADD . /code/

WORKDIR /code
ADD bower.json /code/
ADD .bowerrc /code/
RUN bower install --allow-root && bower cache clean --allow-root

ADD data/conf/secrets.json /code/data/conf/

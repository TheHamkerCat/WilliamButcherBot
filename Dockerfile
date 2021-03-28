FROM ubuntu:latest

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app
RUN apt-get -qq update
RUN DEBIAN_FRONTEND="noninteractive" apt-get -qq install python3 python3-pip software-properties-common

#Updating Libraries
RUN pip3 install -U pip
COPY requirements.txt .
RUN pip3 install --no-cache-dir -U -r requirements.txt

#Copying All Source
COPY . .

#Starting Bot
CMD ["python3", "-m", "wbb"]

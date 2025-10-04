FROM python:slim-bullseye
WORKDIR /wbb
RUN chmod 777 /wbb

RUN apt-get -qq update && apt-get -qq -y upgrade
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y git gcc build-essential
ENV PYTHONUNBUFFERED=1

# Copying All Source
COPY . .
RUN pip3 install -U pip setuptools wheel && pip3 install --no-cache-dir -U -r requirements.txt

# If u want to use /update feature, uncomment the following and edit
#RUN git config --global user.email "your_email"
#RUN git config --global user.name "git_username"

# Starting Bot
ENTRYPOINT ["python3", "-m", "wbb"]

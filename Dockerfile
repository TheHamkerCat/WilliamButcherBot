FROM python:3.9.5-buster

WORKDIR /wbb
RUN chmod 777 /wbb

RUN apt-get update -y

RUN apt-get install -y software-properties-common ffmpeg sudo bash wget curl neofetch git

# Updating Libraries
RUN pip3 install -U pip
COPY requirements.txt .
RUN pip3 install --no-cache-dir -U -r requirements.txt

# Copying All Source
COPY . .

# If u want to use /update feature , uncomment the following and edit it.
#RUN git config --global user.email "your_email"
#RUN git config --global user.name "git_username"        
 
#Starting Bot
CMD ["python3", "-m", "wbb"]

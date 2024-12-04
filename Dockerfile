FROM python:3.8
ADD . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN pip3 install numpy scikit-learn

COPY fonts ./fonts
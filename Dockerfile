FROM python:2.7

ADD duplicated.py /

ARG FOLDER_PATH
ENV ENV_FOLDER_PATH=$FOLDER_PATH
RUN mkdir $ENV_FOLDER_PATH
ADD resources/ $FOLDER_PATH
#RUN mkdir /tmp/test/
#ADD resources/ /tmp/test/
CMD [ "python", "duplicated.py" ]
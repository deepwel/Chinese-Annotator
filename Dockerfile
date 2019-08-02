FROM python:3.6.3-jessie

RUN mkdir /Chinese-Annotator
WORKDIR /Chinese-Annotator

ENV ALIYUN_PIP -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt $ALIYUN_PIP

COPY chi_annotator chi_annotator/
COPY config config/

RUN pip install -e /Chinese-Annotator/chi_annotator

EXPOSE 5000

CMD ["python3.6", "/Chinese-Annotator/scripts/run_webui.sh"]
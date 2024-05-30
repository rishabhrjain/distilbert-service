FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt ./
RUN python3 -m pip install -r requirements.txt --target ${LAMBDA_TASK_ROOT}

COPY ./ ${LAMBDA_TASK_ROOT}/

RUN export TRANSFORMERS_CACHE="/tmp"
RUN echo $TRANSFORMERS_CACHE

CMD [ "handler.handler" ]



FROM python:3.8-alpine
COPY ./requirements.txt /app/requirements
WORKDIR /app
ENTRYPOINT [ "python" ]
CMD [ "test.py" ] 
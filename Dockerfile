FROM python:3.6-alpine3.9

WORKDIR /bot

COPY . /bot

RUN apk update && pip install --upgrade -r requirements.txt

ENTRYPOINT ["python"]

CMD ["bot.py"]

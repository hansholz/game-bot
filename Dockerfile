FROM python:3.6-alpine3.9

COPY . ./

RUN apk update && pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python"]

CMD ["bot.py"]

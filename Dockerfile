FROM alpine

RUN apk add --no-cache python3 py3-pip

RUN adduser -D worker
USER worker

WORKDIR /home/worker
ENV PATH "$PATH:/home/worker/.local/bin"

RUN pip install --upgrade pip

COPY --chown=worker:worker requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY watch.py watch.py

# For prometheus metrics
EXPOSE 8000

ENTRYPOINT ["python3", "-u", "watch.py"]

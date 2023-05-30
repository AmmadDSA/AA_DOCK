FROM python:3
# remember to expose the port your app'll be exposed on.
EXPOSE 8080

RUN pip install -U pip
RUN mkdir /app

COPY requirements.txt app/requirements.txt
RUN pip install -r app/requirements.txt

# copy into a directory of its own (so it isn't in the toplevel dir)
COPY . ./app
WORKDIR /app

# run it!

streamlit run --server.port 8080 --server.enableCORS false aaemail.py
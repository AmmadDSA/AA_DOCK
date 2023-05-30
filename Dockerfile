FROM python:3
# remember to expose the port your app'll be exposed on.
EXPOSE 8501

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy into a directory of its own (so it isn't in the toplevel dir)
COPY . ./
WORKDIR /

# run it!

ENTRYPOINT ["streamlit", "run", "d:/MY Projects/Portfolio/aa_dock/app.py", "--server.port=8501", "--server.address=0.0.0.0"]

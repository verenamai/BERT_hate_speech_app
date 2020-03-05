FROM python:3.6
WORKDIR /app
COPY requirements.txt preprocess.py api.py /app/
RUN pip install -r ./requirements.txt
RUN python -m spacy download en
COPY models/ /app/models/
COPY static/ /app/static/
COPY templates/ /app/templates/
CMD ["python", "api.py"]~

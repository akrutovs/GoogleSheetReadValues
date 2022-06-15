FROM python
WORKDIR /code
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /code
CMD ["python", "db.py"]
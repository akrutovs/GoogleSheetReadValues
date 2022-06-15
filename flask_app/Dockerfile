FROM python
WORKDIR /flask
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY .. /flask
EXPOSE 9000
CMD ["python", "flask_app.py"]
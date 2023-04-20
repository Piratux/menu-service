FROM python:3.9
RUN pip install mysql-connector-python
RUN pip install CherryPy
RUN pip install Routes
RUN pip install simplejson
RUN pip install requests
EXPOSE 5000
COPY ./app .
CMD ["python", "main.py"]
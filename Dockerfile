FROM python:3.9
RUN pip install mysql-connector-python
RUN pip install pandas
RUN pip install CherryPy
EXPOSE 5000
COPY . .
CMD ["python", "main.py"]
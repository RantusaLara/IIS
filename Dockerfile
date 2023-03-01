FROM python:3.7
WORKDIR /Nal1
RUN python -m pip install --upgrade pip
RUN pip install numpy
RUN pip install pandas
RUN pip install --upgrade tensorflow
RUN pip install flask
RUN pip install scikit-learn
COPY . .
EXPOSE 5000
CMD ["python", "main.py"]
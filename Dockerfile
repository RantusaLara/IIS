FROM python:3.7
WORKDIR /Nal1
RUN python -m pip install --upgrade pip
RUN pip install pandas
RUN pip install flask
RUN pip install scikit-learn
RUN pip install pytest
RUN pip install fastapi
RUN pip install httpx
RUN pip install flask_cors
COPY . .
EXPOSE 5000
CMD ["python", "src/serve/server.py"]
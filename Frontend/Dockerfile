# Use the official Python image as the base image
FROM python:3.8

WORKDIR /frontend

COPY requirements.txt .

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "StreamlitTest.py"]
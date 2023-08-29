FROM python:3.8

WORKDIR /frontendTest

COPY requirements.txt .

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "testStreamlit.py"]
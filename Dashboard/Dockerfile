FROM python:3.11

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8050
CMD ["python3", "app.py", "--host=0.0.0.0", "--port=8050"]
# CMD ["uwsgi --ini app.ini"]

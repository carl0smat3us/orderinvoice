# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN apt install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 libffi-dev libjpeg-dev libopenjp2-7-dev
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY . .

# 
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0"]
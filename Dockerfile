# 
FROM python:3.10

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# Install Project dependencies
RUN pip install --root-user-action=ignore --no-cache-dir --upgrade -r /code/requirements.txt

# Install Weasyprint dependencies
RUN apt install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 libffi-dev libjpeg-dev libopenjp2-7-dev

# 
COPY . .

# 
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0"]
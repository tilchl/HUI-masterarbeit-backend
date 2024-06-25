# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app
# 
COPY ./app/conf /code/app/conf
COPY ./app/lib_build /code/app/lib_build
COPY ./app/lib_save /code/app/lib_save 
COPY ./app/lib_load /code/app/lib_load

# Change the working directory to /code/app
WORKDIR /code/app

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
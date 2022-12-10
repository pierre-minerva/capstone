#Use the python version used by the developer
FROM python:3.8.10
#Get the python requirements file
COPY requirements.txt .
#Set work directory to appropriate location
WORKDIR /capsite
#Add relevant files to the work directory
ADD . /capsite
#Install the python requirements
RUN pip3 install -r requirements.txt
#Expose the port used to run the web app
EXPOSE 8000
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
#Run the webapp
CMD ["python3", "capsite/manage.py", "runserver", "0.0.0.0:8000"]
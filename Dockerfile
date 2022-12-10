#Use the python version used by the developer
FROM python:3.8.10
#Get the python requirements file
COPY python-requirements.txt
#Set work directory to appropriate location
WORKDIR /capsite
#Add relevant files to the work directory
ADD . /capsite
#Install the python requirements
RUN pip3 install -r python-requirements.txt
#Expose the port used to run the web app
EXPOSE 8000
#Run the webapp
CMD ["python3", "capsite/manage.py", "runserver"]
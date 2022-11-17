FROM python:3.9

ADD requirements.txt .
# Install production dependencies.
RUN pip install --upgrade pip
RUN pip install -r requirements.txt




ADD price_model price_model
ADD configs configs

#ENV PORT 8080

#RUN python3 -m price_model.app
ENV PORT 8080
#
#CMD [ "python3", "-m" , "price_model.app"]
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 --max-requests-jitter 10 'price_model.app:app'
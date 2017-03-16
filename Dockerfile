FROM superphy/backend:working

COPY ./app /app

CMD ["/usr/bin/supervisord -c /app/supervisord-rq"]

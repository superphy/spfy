FROM superphy/backend:working

COPY ./app /app

RUN cat /app/supervisord-rq >> /etc/supervisor/conf.d/supervisord.conf

CMD /usr/bin/supervisord update

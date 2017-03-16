FROM superphy/backend:working

COPY ./app /app

RUN cat /app/supervisord-rq.conf >> /etc/supervisor/conf.d/supervisord.conf

RUN service supervisor stop && service supervisor start

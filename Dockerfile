FROM superphy/backend:working

COPY ./app /app

RUN cat /app/supervisord-rq.conf >> /etc/supervisor/conf.d/supervisord.conf

ENV PATH /opt/conda/envs/backend/bin:$PATH

RUN service supervisor stop && service supervisor start

FROM superphy/backend:working

COPY ./app /app

RUN cat /app/supervisord-rq.conf >> /etc/supervisor/conf.d/supervisord.conf

RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh

ENV PATH /opt/conda/bin:$PATH

ENV PATH /opt/conda/envs/backend/bin:$PATH

RUN service supervisor stop && service supervisor start

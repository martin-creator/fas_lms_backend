FROM grafana/grafana:6.7.1

COPY ./grafana.ini /etc/grafana/grafana.ini

COPY ./entrypoint.sh .

RUN rm -rf /var/lib/grafana/.init

# print that you ARE ABOUT TO RUN THE ENTRYPOINT
RUN echo "Running entrypoint.sh"

ENTRYPOINT ["sh", "./entrypoint.sh"]

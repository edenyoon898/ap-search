FROM docker.elastic.co/elasticsearch/elasticsearch:7.12.0

USER elasticsearch
RUN elasticsearch-plugin install analysis-nori \
  && echo "discovery.type: single-node" >> /usr/share/elasticsearch/config/elasticsearch.yml

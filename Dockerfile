FROM ubuntu:latest
MAINTAINER Group 12 Cloud
COPY murtazo.tgz /home/fenics

RUN cd /home/fenics
RUN tar xzvf murtazo.tgz
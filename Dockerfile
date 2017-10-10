FROM quay.io/fenicsproject/stable:latest
MAINTAINER Group 12 Cloud
COPY murtazo.tgz /home/fenics/

RUN tar xzvf /home/fenics/murtazo.tgz -C /home/fenics/ 
RUN tar xvf /home/fenics/murtazo/cloudnaca.tgz -C /home/fenics/murtazo/
RUN tar xvf /home/fenics/murtazo/navier_stokes_solver.tar -C /home/fenics/murtazo/

RUN cd /home/fenics/murtazo/navier_stokes_solver/src/ && ./compile_forms
RUN cd /home/fenics/murtazo/navier_stokes_solver/ && cmake .
RUN cd /home/fenics/murtazo/navier_stokes_solver/ && make -j 2
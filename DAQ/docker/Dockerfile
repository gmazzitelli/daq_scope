FROM jupyter/minimal-notebook

RUN pip install --no-cache-dir -U \
    numpy pyvisa pandas h5py gspread matplotlib pymemcache \
    git+https://github.com/SengerM/TeledyneLeCroyPy

USER root
RUN apt-get update
RUN apt-get install -y sshfs libfuse-dev

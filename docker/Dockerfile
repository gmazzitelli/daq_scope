FROM jupyter/minimal-notebook

RUN pip install --no-cache-dir -U \
    numpy pyvisa pyvisa_py pandas h5py gspread matplotlib pymemcache seaborn \
    git+https://github.com/SengerM/TeledyneLeCroyPy

USER root
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y wget lsb-release fuse
RUN wget  https://ecsft.cern.ch/dist/cvmfs/cvmfs-release/cvmfs-release-latest_all.deb
RUN dpkg -i cvmfs-release-latest_all.deb 
RUN rm -f cvmfs-release-latest_all.deb
RUN apt-get update
RUN apt-get install -y cvmfs cvmfs-server cvmfs-config-default
RUN apt-get autoremove -y && apt-get clean

RUN echo "user_allow_other" >> /etc/fuse.conf \
    && echo -e "\nCVMFS_HTTP_PROXY=DIRECT\n" >> /etc/cvmfs/default.conf

COPY mount_cvmfs.sh /mount_cvmfs.sh
RUN chmod +x /mount_cvmfs.sh
RUN echo "PS1='DAQ_SCOPE:\w> '" >> /home/jovyan/.bashrc 

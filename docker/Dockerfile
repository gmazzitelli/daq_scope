FROM jupyter/minimal-notebook

RUN pip install --no-cache-dir -U \
    numpy pyvisa pyvisa_py pandas h5py gspread matplotlib pymemcache seaborn boto3 \
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

COPY ./contents/common.infn.it.pub /etc/cvmfs/keys/infn.it/common.infn.it.pub
COPY ./contents/default.local /etc/cvmfs/default.local
COPY ./contents/infn.it.conf /etc/cvmfs/domain.d/infn.it.conf

COPY ./contents/startup.sh /opt/startup.sh

ENTRYPOINT ["/opt/startup.sh"]

RUN echo "PS1='DAQ_SCOPE:\w> '" >> /home/jovyan/.bashrc 

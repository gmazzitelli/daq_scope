daq contaner
```docker run -it -p 8888:8888 --name editor --user root -w /home/jovyan/work -v /Users/mazzitel/Google\ Drive/My\ Drive/DAQ:/home/jovyan/work gmazzitelli/daq:1.0```

```docker run -it -p 8888:8888 --name editor --user root -w /home/jovyan/work -v /Volumes/WC/:/home/jovyan/work/data -v /Users/mazzitel/Google\ Drive/My\ Drive/DAQ:/home/jovyan/work gmazzitelli/daq:1.0```


tips:

```docker build -t gmazzitelli/daq:1.0 .```
```docker login -u gmazzitelli```
```docker push gmazzitelli/daq:1.0```

### CYGNO/WC oscillocopio ###
ambiente per l'acquisizioni, gestione dei dati e analisi per l'iscipposcppi WaveSurfer
* l'ambiente e' definito da 4 docker: notebook, tunnel socket per l'intranet di CYGNO (o comunque configurabile), gestione del token per l'accesso allo storage S3 di CYGNO (o simili), CVMFS per software di analisi
* nel foleder DAQ, lo script daq.py permette acquisizione delle waveform dell'oscilloscopio LeCroy [WaveSurfer 4104HD](https://www.teledynelecroy.com/oscilloscope/oscilloscopemodel.aspx?modelid=11386) e tutti i modelli 4000
* lo script salva le waveform in h5 o pkl a scelta, in locale e con backup remoto.
  
```cd DAQ```
```./daq.py -h
Usage: daq.py -i -p

Options:
  -h, --help            show this help message and exit
  -i IP, --ip=IP        ip [192.168.140.211]
  -s, --socket          enable socket passthrough
  -d PATH, --path=PATH  destination path [/home/jovyan/work/data/generic/]
  -u, --upload          upload file in cloud?
  -f, --pkl             pkl format insted of h5?
  -v, --verbose         verbose output  
```
* di default c'e' il numero ip dei LNF, che implica che l'oscilloscopio sia collegato alla rete LNF. altrimenti si puo' accededere all'intranet di CYGNO con l'opsione -s
* se l'opsione -u e' abbilitata i dati sono caricati sullo storage S3 di CYGNO nel path analogo, il folder **/home/jovyan/work/data/** punta a un disco esterno per lo storage
* se vene attivata l'opsione uploeda i dati sono anche compressi
* le varie domande che vengono fatte sono archiviate un un gogglesheet 
* esempii:
  
```./day.py -i 192.168.140.211 -d /home/jovyan/work/data/generic/```

```./day.py -i 192.168.1.189 -s -d /home/jovyan/work/data/WC/```

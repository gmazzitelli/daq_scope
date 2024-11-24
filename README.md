### CYGNO/WC oscillocopio ###
ambient per l'acquisizioni, gestione dei dati e analisi per l'iscipposcppi WaveSurfer
* 
* script per acquisizione delle waveform dell'oscilloscopio LeCroy WaveSurfer 4104HD (https://www.teledynelecroy.com/oscilloscope/oscilloscopemodel.aspx?modelid=11386) e tutti i modelli 4000
* lo script salva le waveform in h5 o pkl 
DAQ_SCOPE:~/work> cd DAQ/
```cd DAQ```
```./daq.py -h
Usage: daq.py -i -p


Options:
  -h, --help            show this help message and exit
  -i IP, --ip=IP        ip [192.168.140.211]
  -s, --socket          enable socket passthrough
  -d PATH, --path=PATH  destination path [../data/generic/]
  -u, --upload          upload file in cloud?
  -f, --pkl             pkl format insted of h5?
  -v, --verbose         verbose output  
```
di default c'e' il numero ip dei LNF, che implica che l'oscilloscopio sia collegato alla rete LNF. 

```./day.py -i <192.168.140.211> -d <../data/generic/>

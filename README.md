script per acquisizione dei dati dell'oscilloscopio lecroy wave surfer
```./daq.py -h
Usage: daq.py -i -p

Options:
  -h, --help            show this help message and exit
  -i IP, --ip=IP        ip [192.168.140.211]
  -p PORT, --port=PORT  port [111]
  -d PATH, --path=PATH  destination path [../data/generic/]
  -u, --upload          upload file in cloud?
  -f, --pkl             pkl format insted of h5?
  -v, --verbose         verbose output```
  
```cd DAQ```
```./day.py -i <192.168.140.211> -d <../data/generic/>
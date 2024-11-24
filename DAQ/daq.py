#!/usr/bin/env python3
#
# G. Mazzitelli 2024
# WC DAQ
#
# accedere all'enviroment per MAC mazzitelli
# source daqenv/bin/activate
# python3 -m pip install xyx

import TeledyneLeCroyPy
from matplotlib import pyplot as plt
import requests
import numpy as np
import time
import pandas as pd
import h5py
import pickle
import json
import os
import pandas as pd
import gspread
from google.oauth2 import service_account
import json
import subprocess
import sys
import socks
import socket


def append_record_to_hdf5(filename, record_id, record_data):
    with h5py.File(filename, 'a') as hdf_file:
        group = hdf_file.create_group(str(record_id))
        for key, value in record_data.items():
            group.create_dataset(key, data=value)
            
def append_record_to_pickle(filename, record):
    # Read existing data from the pickle file
    try:
        with open(filename, 'rb') as file:
            existing_data = pickle.load(file)
    except FileNotFoundError:
        existing_data = []
    # Append the new record to the existing data
    existing_data.append(record)

    # Write the updated data back to the pickle file
    with open(filename, 'wb') as file:
        pickle.dump(existing_data, file)
        
from pymemcache.client.base import Client


def mc_get_str(ip, key):

    client = Client((ip, 11211))
    result = client.get(key)
    return result.decode("utf-8")


            
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def main(ip, enable_socket, path, enable_upload, enable_pkl, verbose):
    #
    # Configura il proxy SOCKS che apre una VPN con il router di CYGNO
    # "ssh-socks-proxy" e' il nomedel container, altrimenti dovresti usare localhost, 
    # anche la porta 1080 e' fissata dal docker.
    #
    if enable_socket:
        socks.set_default_proxy(socks.SOCKS5, "ssh-socks-proxy", 1080)
        socket.socket = socks.socksocket

    #############################################
    credentials = service_account.Credentials.from_service_account_file('../.ssh/.google_credentials.json')
    scope = ['https://spreadsheets.google.com/feeds']
    creds_scope = credentials.with_scopes(scope)
    client = gspread.authorize(creds_scope)
    sheet = client.open_by_key('1wtI7ybfk2HGaOFxNc5mXymqL0aU2aS8bSHa990xifeQ') # generic
    #sheet = client.open_by_key('1idBnsYG4pHdHZ2kDbq-S3PBUAf0ewFEzKXOtCTGDxyU') # WC
    log = sheet.worksheet("log")

    #
    # data saved in logbook
    # https://docs.google.com/spreadsheets/d/1idBnsYG4pHdHZ2kDbq-S3PBUAf0ewFEzKXOtCTGDxyU
    #


    start = time.time()
    if verbose: print('TCPIP0::{:s}::inst0::INSTR'.format(ip))
    while True:
        try:
            o = TeledyneLeCroyPy.LeCroyWaveRunner('TCPIP0::{:s}::inst0::INSTR'.format(ip)) 
            break
        except:
            pass
        end = time.time()
        if int(end-start)>=10:
            print("ERROR connection timeout")
            sys.exit(1)
        else:
            time.sleep(0.5)
            print("waiting for connection... "+str(int(end-start))+"/10 s", end="\r")

    print("Connected", o.idn) # Print e.g. LECROY,WAVERUNNER9254M,LCRY4751N40408,9.2.0

    # end to init connection

    EVENTS= 1000
    DSHOW = False
    CHANNELS = 4


    while True:
        try:
            input("\nPress Enter to start/continue, Ctr-C to exit")
            # reading logbook
            logdf=pd.DataFrame.from_dict(log.get_all_records())
            last_run = logdf.run.values[-1]
            run = last_run+1

            print ("\n-------> DAQ ready to acquire run number: {:05d}".format(run))
            user_input = input("Enter run description? (if any) ")
            if user_input:
                start_desc=user_input
            else:
                start_desc=''

            user_input = input("Number of channels: [{}] ".format(CHANNELS)).lower()
            if user_input:
                channels=int(user_input)
            else:
                channels=CHANNELS

            user_input = input("Number of events: [{}] ".format(EVENTS)).lower()
            if user_input:
                events=int(user_input)
            else:
                events=EVENTS

            if enable_pkl:
                filename = "run_{:05d}.pkl".format(run)
            else:
                filename = "run_{:05d}.h5".format(run)
            filepath = path+filename

            #########################
            start = time.time()
            dt = 0

            if os.path.exists(filepath):
                os.remove(filepath)
                print('File removed:', filepath)
            else:
                print('Writing on new file:', filepath)

            beam = mc_get_str(ip='192.168.198.164', key='BTFDATA_PADME')
            # updating startup condition
            start_date = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
            start_epoch = time.time()
            logdf = logdf._append({'run': run, 'start_desc': start_desc, 'start_date': start_date, 'start_epoch': start_epoch, 
                                   'filename': filename, 'beam': beam}, ignore_index=True)


            for event in range(events):
                dict2save = {}
                triggers = []
                try:
                    elapsed = time.time()-start
                    if event >0:
                        trate = elapsed/event
                    else:
                        trate = 0 
                    print('Triggers acquired: {:d}, elapsed {:.1f} s, Tr Hz: {:.1f}, storing time: {:.2f} s'.format(event,elapsed, trate, dt), end="\r")
                    o.wait_for_single_trigger() # Halt the execution until there is a trigger.
                    dt1 = time.time()
                    for channel in range(1, channels+1):
                        data = o.get_waveform(n_channel=channel)
                        if enable_pkl:
                            triggers.append(data)
                        else:
                            dict2save['H'+str(channel)]=json.dumps(data['wavedesc'], default=str)
                            dict2save['T'+str(channel)]=json.dumps(data['trigtime'])
                            dict2save['W'+str(channel)]=json.dumps(data['waveforms'], cls=NumpyEncoder)        
                        if DSHOW:
                            # show first waveform per 
                            x = data['waveforms'][0]['Time (s)']/1e-9
                            y = data['waveforms'][0]['Amplitude (V)']/1e-3
                            plt.plot(x,y, label="C"+str(n_channel))


                    if eanable_pkl:
                        append_record_to_pickle(filepath, triggers)
                    else:
                        dict2save['epoch']=data['wavedesc']['TRIGGER_TIME'].timestamp()
                        append_record_to_hdf5(filepath, event, dict2save)
                    if DSHOW:
                        t = data['wavedesc']['TRIGGER_TIME'].strftime('%m/%d/%Y %H:%M:%S')
                        plt.legend()
                        plt.title(t)
                        plt.xlabel('ns')
                        plt.ylabel('mV')
                        plt.show()
                    dt =  time.time() - dt1
                except KeyboardInterrupt:
                    print ("\nstopping DAQ...")
                    break
            print ("\n-------> DAQ acquisition of RUN {:05d} completed".format(run))
            print ("Upating metadata run info...")
            # updating ending condition
            end_date = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
            logdf.at[run, 'end_date']=end_date
            end_epoch = time.time()
            logdf.at[run, 'end_epoch']=end_epoch
            logdf.at[run, 'events']=event+1
            if enable_upload:
                print ("Uploding file on cloud in background...")
                subprocess.Popen(['./uploadFile.py', '-g', '-r', filepath], stdout=None, stderr=None, stdin=None)

            user_input = input("Enter closing remarks? (if any) ")
            if user_input:
                end_desc=user_input
            else:
                end_desc=''
            logdf.at[run, 'end_desc']=end_desc

            # updating logbook
            print ("Updating logbook...")
            log.update([logdf.columns.values.tolist()] + logdf.values.tolist())

            print("\n-------> RUN {:} ACQUIRED".format(filename))

        except KeyboardInterrupt:
            break
    print("\nDAQ STOP")
    
if __name__ == "__main__":
    from optparse import OptionParser
    #
    # deault parser value
    # 192.168.189.115 BTF
    # 192.168.201.7 CYGNO
    #
    IP         = 'spaip.lnf.infn.it'
    IP         = '192.168.140.211' # ip lnf
    PATH       = '../data/generic/'
    PORT       = 111

    parser = OptionParser(usage='usage: %prog -i -p\n')
    parser.add_option('-i','--ip', dest='ip', type='string', default=IP, help='ip [{:s}]'.format(IP))
    parser.add_option('-s','--socket', dest='socket', action="store_true", default=False, help='enable socket passthrough')
    parser.add_option('-d','--path', dest='path', type='string', default=PATH, help='destination path [{:s}]'.format(PATH))
    parser.add_option('-u','--upload', dest='upload', action="store_true", default=False, help='upload file in cloud?')
    parser.add_option('-f','--pkl', dest='pkl', action="store_true", default=False, help='pkl format insted of h5?')
    parser.add_option('-v','--verbose', dest='verbose', action="store_true", default=False, help='verbose output')
    (options, args) = parser.parse_args()
    if options.verbose: 
        print ("options", options)
        print ("args", args)
#     if len(args)<1:
#         parser.error("missing key/folder to beckup, example {:s}".format(KEY))
#         sys.exit(1)
     
    main(options.ip,  options.socket, options.path, options.upload, options.pkl, options.verbose)

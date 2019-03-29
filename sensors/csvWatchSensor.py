from os.path  import isfile,  join
from os import listdir
import os, eventlet
import time
from st2reactor.sensor.base import Sensor

class csvWatchSensor(Sensor):
    def __init__(self, sensor_service, config):
        super(csvWatchSensor, self).__init__(sensor_service=sensor_service, config=config)
        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)
        self._stop = False

        message = '__csvWatchSensor %s \n' % os.getcwd()
        self._logger.debug(message)

        if self.config['path']:
            self._path = self.config['path']
            if not os.path.isdir(self._path):
                # create the path and set permission
                os.mkdir(self._path)
                os.chmod(self._path, 0777)
        else:
            # the path is not specified in the config.yaml file.
            self._logger.debug('csvWatchSensor ERROR: path is missing from the config.yaml file.')

        if self.config['pollTime']:
            self.pollTime = int(self.config['pollTime'])
        else:
            self.pollTime = 30

        if self.config['triggerTime']:
            self.triggerTime = int(self.config['triggerTime'])
        else:
            self.triggerTime = 1


    def setup(self):
        pass

    def run(self):
        mypath = "/home/st2/addXmcDevices/"
        self._logger.debug('csvWatchSensor run...')

        while not self._stop:
            self._logger.debug('csvWatchSensor looping...')
            
            # scan the directory for csv files
            onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

            # filter on only csv files
            for f in onlyfiles:
                #if ".csv" in f:
                if f.endswith('csv'):
                    print("File is -> %s " % f)
                    #only trigger on files that have content
                    if os.path.getsize(mypath+f) > 0:
                        # get the files contents
                        with open (mypath+f, "r") as myfile:
                            data=myfile.readlines()
                        # Change the filename
                        os.rename(mypath+f, mypath+f+"processed")

                        # loop over each device
                        for line in data:
                            # "10.174.0.1", "mydevice1", "myProfile", "mySite"
                            # split the line 'line' on comma
                            if not line.startswith('#'):
                                d = line.split(',')
                                # dispatch the trigger and inject the data
                                self._logger.debug('csvWatchSensor dispatching trigger...')
                                #count = self.sensor_service.get_value('csvWatchSensor.count') or 0
                                payload = {'csvFile': str(f).strip(), 'deviceIpAddress': d[0].strip(), 'deviceName': d[1].strip(), 'profile': d[2].strip(), 'site': d[3].strip() }
                                self.sensor_service.dispatch(trigger='my_xmc.csvWatchSensor', payload=payload)
                                #self.sensor_service.set_value('csvWatchSensor.count', payload['count'])
                                # optional delay between triggers
                                eventlet.sleep(self.triggerTime)   
                    else:
                        print("Skipping %s file too small " %mypath+f)
            # optional delay between polls
            eventlet.sleep(self.pollTime)   

    def cleanup(self):
        self._stop = True

    # Methods required for programmable sensors.
    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

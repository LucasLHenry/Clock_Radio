from machine import Pin, I2C
from pin_lib import *
from settings_lib import RADIO_MAX_TRIES


class Radio:
    def __init__(self, NewFrequency, NewVolume, NewMute):
        # set the initial values of the radio
        self.Volume = 2
        self.Frequency = 101.9
        self.Mute = False
        self.MAX_TRIES = RADIO_MAX_TRIES # how many times it'll attempt communication before giving up
        # Update the values with the ones passed in the initialization code
        self.SetVolume(NewVolume)
        self.SetFrequency(NewFrequency)
        self.SetMute(NewMute)
        # Initialize I/O pins associated with the radio's I2C interface
        self.i2c_sda = Pin(RADIO_SDIO_PIN, pull=Pin.PULL_UP)
        self.i2c_scl = Pin(RADIO_SCLK_PIN, pull=Pin.PULL_UP)
        # I2C Device ID can be 0 or 1. It must match the wiring. 
        # The radio is connected to device number 1 of the I2C device
        self.i2c_device = 1 
        self.i2c_device_address = 0x10
        # Array used to configure the radio
        self.Settings = bytearray(8)

        self.radio_i2c = I2C(self.i2c_device, scl=self.i2c_scl, sda=self.i2c_sda, freq=200000)
        self.ProgramRadio()


    def SetVolume(self, NewVolume):
        # Convert the string into a integer
        try:
            NewVolume = int(NewVolume)
        except:
            return False
        # Validate the type and range check the volume
        if not isinstance(NewVolume, int):
            return False
        if (NewVolume < 0) or (NewVolume >= 16):
            return False
        self.Volume = NewVolume
        return True


    def SetFrequency(self, NewFrequency):
        # Convert the string into a floating point value
        try:
            NewFrequency = float(NewFrequency)   
        except:
            return False
        # validate the type and range check the frequency
        if not isinstance(NewFrequency, float ):
            return False 
 
        if (NewFrequency < 88.0) or (NewFrequency > 108.0):
            return False 

        self.Frequency = NewFrequency
        return True
        
        
    def SetMute(self, NewMute):
        try:
            self.Mute = bool(int(NewMute))
        except:
            return False
        return True


    # convert the frequency to 10 bit value for the radio chip
    def ComputeChannelSetting(self, Frequency):
        Frequency = int(Frequency * 10) - 870
        ByteCode = bytearray(2)
        # split the 10 bits into 2 bytes
        ByteCode[0] = (Frequency >> 2) & 0xFF
        ByteCode[1] = ((Frequency & 0x03) << 6) & 0xC0
        return ByteCode


    # Configure the settings array with the mute, frequency and volume settings
    def UpdateSettings(self):
        if (self.Mute):
            self.Settings[0] = 0x80
        else:
            self.Settings[0] = 0xC0

        self.Settings[1] = 0x09 
        self.Settings[2:3] = self.ComputeChannelSetting(self.Frequency)
        self.Settings[3] = self.Settings[3] | 0x10
        self.Settings[4] = 0x04
        self.Settings[5] = 0x00
        self.Settings[6] = 0x8F
        self.Settings[7] = 0x80 + self.Volume


    # Update the settings array and transmit it to the radio
    def ProgramRadio(self):
        self.UpdateSettings()
        # we were having trouble getting a connection, so the solution
        # was just to try a bunch of times. Can change MAX_TRIES as needed
        success = False
        counter = 0
        while not success and counter < self.MAX_TRIES:
            try:
                self.radio_i2c.writeto(self.i2c_device_address, self.Settings)
                success = True
            except:
                counter += 1
                continue
        if not success:
            print(f"failed to write after {counter} attempts")


    # Extract the settings from the radio registers
    def GetSettings(self):
        # Need to read the entire register space. This is allow access to the mute and volume settings
        # same issue of just trying a bunch of times until it works.
        success = False
        counter = 0
        while not success and counter < self.MAX_TRIES:
            try:
                self.RadioStatus = self.radio_i2c.readfrom(self.i2c_device_address, 256)
                success = True
            except:
                counter += 1
                continue
        if not success:
            print(f"failed to read after {counter} attempts")

        if ((self.RadioStatus[0xF0] & 0x40) != 0x00):
            MuteStatus = False
        else:
            MuteStatus = True
        VolumeStatus = self.RadioStatus[0xF7] & 0x0F
        # Convert the frequency 10 bit count into actual frequency in Mhz
        FrequencyStatus = ((self.RadioStatus[0x00] & 0x03) << 8) | (self.RadioStatus[0x01] & 0xFF)
        FrequencyStatus = (FrequencyStatus * 0.1) + 87.0

        if ((self.RadioStatus[0x00] & 0x04) != 0x00):
            StereoStatus = True
        else:
            StereoStatus = False
        return (MuteStatus, VolumeStatus, FrequencyStatus, StereoStatus)

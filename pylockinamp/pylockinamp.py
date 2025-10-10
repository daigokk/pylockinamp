import subprocess
import os
import time
import numpy as np


class pylockinamp:
    """
    Python wrapper for the LIA executable.

    This class provides an interface to communicate with the LIA binary via subprocess piping.
    It allows sending commands, receiving responses, and retrieving measurement data.

    References
    ----------
    LIA project: https://github.com/daigokk/LIA/
    """

    def __init__(self, option=''):
        """
        Initialize the LIA subprocess with optional command-line arguments.

        Parameters
        ----------
        option : str, optional
            Command-line argument passed to the LIA executable.
            Use 'nogui' to enable headless mode.
        """
        exe_path = os.path.join(os.path.dirname(__file__), 'bin', 'lia.exe')
        self.process = subprocess.Popen(
            f'{exe_path} pipe {option}',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            encoding='utf-8',
        )
        print(self._recieve())

    def __del__(self):
        """
        Destructor to safely terminate the LIA subprocess.

        Sends the 'end' command and kills the process after a short delay.
        """
        self._send('end')
        time.sleep(1)
        self.process.kill()

    def _send(self, cmd: str):
        """
        Send a command string to the LIA process.

        Parameters
        ----------
        cmd : str
            Command to send.
        """
        self.process.stdin.write(f'{cmd}\n')
        self.process.stdin.flush()

    def _recieve(self):
        """
        Receive a single line of response from the LIA process.

        Returns
        -------
        str
            Response string without trailing newline.
        """
        self.process.stdout.flush()
        return self.process.stdout.readline()[:-1]

    def _query(self, cmd):
        """
        Send a command and wait for the response.

        Parameters
        ----------
        cmd : str
            Command to send.

        Returns
        -------
        str
            Response from the LIA process.
        """
        self._send(cmd)
        return self._recieve()

    def get_help(self):
        """
        Print help information from the LIA process.

        Returns
        -------
        None
        """
        size = int(self._query('help:size?'))
        self._send('help?')
        for i in range(size):
            print(self._recieve())

    def get_idn(self):
        """
        Query the device identification string.

        Returns
        -------
        str
            Identification string.
        """
        return self._query('*idn?')

    def set_reset(self):
        """
        Send reset command to the device.

        Returns
        -------
        None
        """
        self._send('*rst')

    def get_lastError(self):
        """
        Retrieve the last error message from the device.

        Returns
        -------
        str
            Last error message.
        """
        return self._query('error?')

    def set_pause(self):
        """
        Pause the device operation.

        Returns
        -------
        None
        """
        self._send('pause')

    def set_run(self):
        """
        Resume or start the device operation.

        Returns
        -------
        None
        """
        self._send('run')

    def get_ch2state(self):
        """
        Check if channel 2 display is enabled.
        Returns
        -------
        bool
            True if channel 2 display is enabled, False otherwise.
        """
        ret = self._query(':chan2:disp?')
        if ret == 'on':
            return True
        else:
            return False

    def set_ch2state(self, state:bool):
        """
        Enable or disable the display of channel 2.

        Parameters
        ----------
        state : bool
            True to enable, False to disable.

        Returns
        -------
        None
        
        """
        if state:
            self._send(':chan2:disp on')
        else:
            self._send(':chan2:disp off')

    def get_raw(self):
        """
        Retrieve raw data from the device.

        Returns
        -------
        numpy.ndarray
            2D array of shape (N, 2) or (N, 3), where N is the number of samples.
        """
        dat = []
        size = int(self._query(':data:raw:size?'))
        self._send(':data:raw?')
        for i in range(size):
            dat.append(list(map(float, self._recieve().split(','))))
        return np.array(dat)

    def get_xy(self):
        """
        Retrieve XY data from the device.

        Returns
        -------
        list of float
            List of two or four float values [X0, Y0] or [X0, Y0, X1, Y1].
        """
        return list(map(float, self._query(':data:xy?').split(',')))

    def get_txy(self, sec=0):
        """
        Retrieve time-series XY data for a given duration.

        Parameters
        ----------
        sec : int, optional
            Duration in seconds to collect data. Default is 0.

        Returns
        -------
        numpy.ndarray
            2D array of shape (N, 3) or (N, 5), where N is the number of samples.
        """
        dat = []
        size = int(self._query(f':data:txy? {sec}'))
        for i in range(size):
            dat.append(list(map(float, self._recieve().split(','))))
        return np.array(dat)

    def get_fgFreq(self, ch=0):
        """
        Get the frequency of the function generator.

        Parameters
        ----------
        ch : int, optional
            Channel number. Default is 0. Then ch=0 corresponds to w1.

        Returns
        -------
        float
            Frequency value.
        """
        return float(self._query(f':w{ch+1}:freq?'))

    def set_fgFreq(self, freq, ch=0):
        """
        Set the frequency of the function generator.

        Parameters
        ----------
        freq : float
            Frequency value to set.
        ch : int, optional
            Channel number. Default is 0. Then ch=0 corresponds to w1.
        """
        self._send(f':w{ch+1}:freq {freq}\n')

    def get_fgAmp(self, ch=0):
        """
        Get the amplitude of the function generator.
        Parameters
        ----------
        ch : int, optional
            Channel number. Default is 0. Then ch=0 corresponds to w1.
        Returns
        -------
        float
            Amplitude value.
        """
        return float(self._query(f':w{ch+1}:amp?'))

    def set_fgAmp(self, amp, ch=0):
        """
        Set the amplitude of the function generator.

        Parameters
        ----------
        amp : float
            Amplitude value to set.
        ch : int, optional
            Channel number. Default is 0. Then ch=0 corresponds to w1.
        """
        self._send(f':w{ch+1}:amp {amp}\n')

    def get_fgPahse(self, ch=0):
        """
        Get the phase of the function generator.

        Parameters
        ----------
        ch : int, optional
            Channel number. Default is 0. Then ch=0 corresponds to w1.
        Returns
        -------
        float
            Phase value in degrees.
        """
        return float(self._query(f':w{ch+1}:phase?'))
    
    def set_fgPhase(self, phase, ch=0):
        """
        Set the phase of the function generator.

        Parameters
        ----------
        phase : float
            Phase value to set in degrees.
        ch : int, optional
            Channel number. Default is 0. Then ch=0 corresponds to w1.
        """
        self._send(f':w{ch+1}:phase {phase}\n')

    def get_offsetPhase(self, ch=0):
        """
        Get the offset phase for the channel.

        Parameters
        ----------
        ch : int, optional
            Channel number. Default is 0. Then ch=0 corresponds to ch1.

        Returns
        -------
        float
            Offset phase value in degrees.
        """
        return float(self._query(f':calc{ch+1}:offset:phase?'))

    def set_offsetPhase(self, phase, ch=0):
        """
        Set the offset phase for the channel.

        Parameters
        ----------
        phase : float
            Offset phase value to set in degrees.
        ch : int, optional
            Channel number. Default is 0. Then ch=0 corresponds to ch1.
        """
        self._send(f':calc{ch+1}:offset:phase {phase}\n')

    def _test(self):
        """
        Test function of all commands.

        Returns
        -------
        Charactor strings
        """
        print('Start test...')
        print(self.get_idn())
        print(self.get_help())
        previousW1Freq = self.get_fgFreq(0)
        previousW1Amp = self.get_fgAmp(0)
        previousW1Phase = self.get_fgPahse(0)
        previousW2Freq = self.get_fgFreq(1)
        previousW2Amp = self.get_fgAmp(1)
        previousW2Phase = self.get_fgPahse(1)
        previousCh1OffsetPhase = self.get_offsetPhase(0)
        previousCh2OffsetPhase = self.get_offsetPhase(0)
        previousCh2DispStatus = self.get_ch2state()
        print('previousW1Freq: ', previousW1Freq)
        print('previousW1Amp: ', previousW1Amp)
        print('previousW1Phase: ', previousW1Phase)
        print('previousW2Freq: ', previousW2Freq)
        print('previousW2Amp: ', previousW2Amp)
        print('previousW2Phase: ', previousW2Phase)
        print('previousCh1OffsetPhase: ', previousCh1OffsetPhase)
        print('previousCh2OffsetPhase: ', previousCh2OffsetPhase)
        print('previousCh2DispStatus: ', previousCh2DispStatus)

        self.set_reset()
        ret = self.get_lastError()
        if ret != 'No error.':
            raise ValueError(f'Device error detected. {ret}')
        w1freq = 12e3
        self.set_fgFreq(w1freq, 0)
        ret = self.get_lastError()
        if ret != 'No error.':
            raise ValueError(f'Device error detected. {ret}')
        ret = self.get_fgFreq(0)
        print('get freq: ', ret)
        if w1freq != ret:
            raise ValueError('Frequency setting failed.')
        w1amp = 0.5
        self.set_fgAmp(w1amp, 0)
        ret = self.get_fgAmp(0)
        print('get amp: ', ret)
        if w1amp != ret:
            raise ValueError('Amplitude setting failed.')
        self.set_ch2state(True)
        
        ch1offsetPhase = 30
        self.set_offsetPhase(ch1offsetPhase, 0)
        ret = self.get_offsetPhase(0)
        print('offset phase: ', ret)
        if ch1offsetPhase != ret:
            raise ValueError('Offset phase setting failed.')
        
        ret = self.get_xy()
        print('xy:', ret)
        if len(ret) != 4:
            raise ValueError('XY data size error.')
        self.set_pause()
        ret = self.get_lastError()
        if ret != 'No error.':
            raise ValueError(f'Device error detected. {ret}')
        ret = self.get_raw()
        if ret.shape != (5000, 3):
            raise ValueError('Raw data size error.')
        ret = self.get_txy(1)
        print('ret[0]', ret[0])
        if len(ret[0]) != 5:
            raise ValueError(f'Time-series XY data size error. {ret.shape[0]}')
        self.set_run()
        self.set_reset()
        self.set_fgFreq(previousW1Freq, 0)
        self.set_fgAmp(previousW1Amp, 0)
        self.set_fgPhase(previousW1Phase, 0)
        self.set_fgFreq(previousW2Freq, 1)
        self.set_fgAmp(previousW2Amp, 1)
        self.set_fgPhase(previousW2Phase, 1)
        self.set_offsetPhase(previousCh1OffsetPhase, 0)
        self.set_offsetPhase(previousCh2OffsetPhase, 1)
        self.set_ch2state(previousCh2DispStatus)
        print("Test finished.")

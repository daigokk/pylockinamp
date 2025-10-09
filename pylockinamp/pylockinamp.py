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

    def get_raw(self):
        """
        Retrieve raw data from the device.

        Returns
        -------
        numpy.ndarray
            2D array of float values.
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

    def get_fgFreq(self):
        """
        Get the frequency of the function generator 'W1'.

        Returns
        -------
        float
            Frequency value.
        """
        return float(self._query(':w1:freq?'))

    def set_fgFreq(self, freq):
        """
        Set the frequency of the function generator 'W1'.

        Parameters
        ----------
        freq : float
            Frequency value to set.
        """
        self._send(f':w1:freq {freq}\n')

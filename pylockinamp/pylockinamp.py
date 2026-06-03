import subprocess
import os
import time
import numpy as np


class Lia:
    """
    Python wrapper for the LIA executable.

    This class provides an interface to communicate with the LIA binary via subprocess piping.
    It allows sending commands, receiving responses, and retrieving measurement data.
    """

    def __init__(self, option=''):
        """
        Initialize the LIA subprocess with optional command-line arguments.
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
        """
        self._send('end')
        time.sleep(1)
        self.process.kill()

    def _send(self, cmd: str):
        """Send a command string to the LIA process."""
        self.process.stdin.write(f'{cmd}\n')
        self.process.stdin.flush()

    def _recieve(self):
        """Receive a single line of response from the LIA process."""
        self.process.stdout.flush()
        return self.process.stdout.readline()[:-1]

    def _query(self, cmd):
        """Send a command and wait for the response."""
        self._send(cmd)
        return self._recieve()

    # ============================================================
    # System & Basic Commands
    # ============================================================
    def get_help(self):
        """Print help information from the LIA process."""
        size = int(self._query('help size?'))
        self._send('help?')
        for _ in range(size):
            print(self._recieve())

    def get_idn(self):
        """Query the device identification string."""
        return self._query('*idn?')

    def set_reset(self):
        """Send reset command to the device."""
        self._send('*rst')

    def get_last_error(self):
        """Retrieve the last error message from the device."""
        return self._query('error?')

    def set_pause(self):
        """Pause the device operation."""
        self._send('pause')

    def set_run(self):
        """Resume or start the device operation."""
        self._send('run')

    # ============================================================
    # Display & Plot Settings
    # ============================================================
    def get_acfm_disp(self):
        """Check if ACFM window display is enabled."""
        return self._query('acfm:disp?') == 'on'

    def set_acfm_disp(self, state: bool):
        """Enable or disable ACFM window display."""
        self._send(f'acfm:disp {"on" if state else "off"}')

    def set_plot_xy_limit(self, limit: float):
        """Set XY window limit."""
        self._send(f'plot:xy:limit {limit}')

    def set_plot_raw_limit(self, limit: float):
        """Set raw window limit."""
        self._send(f'plot:raw:limit {limit}')

    # ============================================================
    # Channel Settings (chan[n])
    # ============================================================
    def get_chan_disp(self, ch=0):
        """Check if the channel display is enabled."""
        return self._query(f'chan{ch+1}:disp?') == 'on'

    def set_chan_disp(self, state: bool, ch=0):
        """Enable or disable the display of the channel."""
        self._send(f'chan{ch+1}:disp {"on" if state else "off"}')

    def get_chan_range(self, ch=0):
        """Get the range of the channel."""
        return float(self._query(f'chan{ch+1}:range?'))

    def set_chan_range(self, val: float, ch=0):
        """Set the range of the channel."""
        self._send(f'chan{ch+1}:range {val}')

    # ============================================================
    # Data Acquisition (data)
    # ============================================================
    def get_raw(self):
        """Retrieve raw data from the device."""
        dat = []
        size = int(self._query('data:raw:size?'))
        self._send('data:raw?')
        for _ in range(size):
            dat.append(list(map(float, self._recieve().split(','))))
        return np.array(dat)

    def save_raw(self, filename=""):
        """Save raw data to file."""
        cmd = f'data:raw:save {filename}'.strip()
        self._send(cmd)

    def get_fft(self):
        """Retrieve FFT data from the device."""
        dat = []
        size = int(self._query('data:fft:size?'))
        self._send('data:fft?')
        for _ in range(size):
            dat.append(list(map(float, self._recieve().split(','))))
        return np.array(dat)

    def save_fft(self, filename=""):
        """Save FFT data to file."""
        cmd = f'data:fft:save {filename}'.strip()
        self._send(cmd)

    def get_xy(self, n=1, waitsec=0.0):
        """Retrieve the latest XY data from the device."""
        xys = np.array(list(map(float, self._query(':data:xy?').split(','))))
        for i in range(n-1):
            time.sleep(waitsec)
            xys += np.array(list(map(float, self._query(':data:xy?').split(','))))
        return xys/n

    def get_txy(self, sec=0.0):
        """Retrieve time-series XY data for a given duration."""
        dat = []
        size = int(self._query(f'data:txy? {sec}'))
        for _ in range(size):
            dat.append(list(map(float, self._recieve().split(','))))
        return np.array(dat)

    # ============================================================
    # AWG Settings (w[n])
    # ============================================================
    def get_fg_freq(self, ch=0, arg=""):
        """Get the frequency of the AWG channel. arg can be 'min' or 'max'."""
        cmd = f'w{ch+1}:freq?' + (f' {arg}' if arg else '')
        return float(self._query(cmd))

    def set_fg_freq(self, freq: float, ch=0):
        """Set the frequency of the AWG channel."""
        self._send(f'w{ch+1}:freq {freq}')

    def get_fg_amp(self, ch=0, arg=""):
        """Get the amplitude of the AWG channel. arg can be 'min' or 'max'."""
        cmd = f'w{ch+1}:amp?' + (f' {arg}' if arg else '')
        return float(self._query(cmd))

    def set_fg_amp(self, amp: float, ch=0):
        """Set the amplitude of the AWG channel."""
        self._send(f'w{ch+1}:amp {amp}')

    def get_fg_phase(self, ch=0):
        """Get the phase of the AWG channel in degrees."""
        return float(self._query(f'w{ch+1}:phase?'))
    
    def set_fg_phase(self, phase: float, ch=0):
        """Set the phase of the AWG channel in degrees."""
        self._send(f'w{ch+1}:phase {phase}')

    def get_fg_func(self, ch=0):
        """Get the function type of the AWG channel ('sine', 'square', 'triangle')."""
        return self._query(f'w{ch+1}:func?')

    def set_fg_func(self, func_str: str, ch=0):
        """Set the function type of the AWG channel ('sine', 'square', 'triangle')."""
        self._send(f'w{ch+1}:func {func_str}')

    # ============================================================
    # Post Processing (post)
    # ============================================================
    def get_offset_phase(self, ch=0):
        """Get the calculation offset phase for the channel."""
        return float(self._query(f'post{ch+1}:offset:phase?'))

    def set_offset_phase(self, phase: float, ch=0):
        """Set the calculation offset phase for the channel."""
        self._send(f'post{ch+1}:offset:phase {phase}')

    def get_offset_state(self):
        """Check if the global auto-offset state is enabled."""
        return self._query('post:offset:state?') == 'on'

    def set_offset_state(self, state: bool):
        """Enable or disable the global offset state."""
        self._send(f'post:offset:state {"on" if state else "off"}')

    def set_offset_auto_once(self):
        """Perform one-time auto offset calibration."""
        self._send('post:offset:auto once')

    def get_hpf_freq(self):
        """Get the High-Pass Filter frequency."""
        return float(self._query('post:hpf:freq?'))

    def set_hpf_freq(self, freq: float):
        """Set the High-Pass Filter frequency (0 to 50 Hz)."""
        self._send(f'post:hpf:freq {freq}')

    def get_lpf_freq(self):
        """Get the Low-Pass Filter frequency."""
        return float(self._query('post:lpf:freq?'))

    def set_lpf_freq(self, freq: float):
        """Set the Low-Pass Filter frequency (1 to 100 Hz)."""
        self._send(f'post:lpf:freq {freq}')

    # ============================================================
    # Testing
    # ============================================================
    def _test(self):
        """Test function to verify commands."""
        print('Start test...')
        print(self.get_idn())
        self.get_help()
        
        # Save previous state
        previous_w1_freq = self.get_fg_freq(0)
        previous_w1_amp = self.get_fg_amp(0)
        previous_w1_phase = self.get_fg_phase(0)
        previous_w2_freq = self.get_fg_freq(1)
        previous_w2_amp = self.get_fg_amp(1)
        previous_w2_phase = self.get_fg_phase(1)
        previous_ch1_offset_phase = self.get_offset_phase(0)
        previous_ch2_offset_phase = self.get_offset_phase(1)
        previous_ch2_disp_status = self.get_chan_disp(1)
        
        print('previous w1 freq: ', previous_w1_freq)
        print('previous w1 amp: ', previous_w1_amp)
        print('previous w1 phase: ', previous_w1_phase)
        print('previous w2 freq: ', previous_w2_freq)
        print('previous w2 amp: ', previous_w2_amp)
        print('previous w2 phase: ', previous_w2_phase)
        print('previous ch1 offset phase: ', previous_ch1_offset_phase)
        print('previous ch2 offset phase: ', previous_ch2_offset_phase)
        print('previous ch2 disp status: ', previous_ch2_disp_status)

        self.set_reset()
        ret = self.get_last_error()
        if ret != 'No error.':
            raise ValueError(f'Device error detected. {ret}')
            
        w1freq = 12e3
        self.set_fg_freq(w1freq, 0)
        ret = self.get_last_error()
        if ret != 'No error.':
            raise ValueError(f'Device error detected. {ret}')
            
        ret = self.get_fg_freq(0)
        print('get freq: ', ret)
        if w1freq != ret:
            raise ValueError('Frequency setting failed.')
            
        w1amp = 0.5
        self.set_fg_amp(w1amp, 0)
        ret = self.get_fg_amp(0)
        print('get amp: ', ret)
        if w1amp != ret:
            raise ValueError('Amplitude setting failed.')
            
        self.set_chan_disp(True, 1) # CH2
        
        ch1offsetPhase = 30
        self.set_offset_phase(ch1offsetPhase, 0)
        ret = self.get_offset_phase(0)
        print('offset phase: ', ret)
        if ch1offsetPhase != ret:
            raise ValueError('Offset phase setting failed.')
        
        ret = self.get_xy()
        print('xy:', ret)
        if len(ret) < 2:
            raise ValueError('XY data size error.')
            
        self.set_pause()
        ret = self.get_last_error()
        if ret != 'No error.':
            raise ValueError(f'Device error detected. {ret}')
            
        ret = self.get_raw()
        if ret.shape[1] < 2:
            raise ValueError('Raw data size error.')
            
        ret = self.get_txy(1)
        print('ret[0]', ret[0])
        if len(ret[0]) < 3:
            raise ValueError(f'Time-series XY data size error. {ret.shape[0]}')
            
        self.set_run()
        self.set_reset()
        
        # Restore state
        self.set_fg_freq(previous_w1_freq, 0)
        self.set_fg_amp(previous_w1_amp, 0)
        self.set_fg_phase(previous_w1_phase, 0)
        self.set_fg_freq(previous_w2_freq, 1)
        self.set_fg_amp(previous_w2_amp, 1)
        self.set_fg_phase(previous_w2_phase, 1)
        self.set_offset_phase(previous_ch1_offset_phase, 0)
        self.set_offset_phase(previous_ch2_offset_phase, 1)
        self.set_chan_disp(previous_ch2_disp_status, 1)
        
        print("Test finished.")

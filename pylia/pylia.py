import subprocess
import os
import time
import numpy as np


class pylia:
  def __init__(self, option=''):
    exe_path = os.path.join(os.path.dirname(__file__), 'bin', 'lia.exe')
    self.process = subprocess.Popen(
        f'{exe_path} pipe {option}',
          stdin=subprocess.PIPE,
          stdout=subprocess.PIPE,
          encoding='utf-8',
    )
    print(self._recieve())
  def __del__(self):
    self._send('end')
    time.sleep(1)
    self.process.kill()
  def _send(self, cmd:str):
    self.process.stdin.write(f'{cmd}\n')
    self.process.stdin.flush()
  def _recieve(self, ):
    self.process.stdout.flush()
    return self.process.stdout.readline()[:-1]
  def _query(self, cmd):
    self._send(cmd)
    return self._recieve()
  def get_help(self):
    size = int(self._query('help:size?'))
    self._send('help?')
    for i in range(size):
      print(self._recieve())
    return
  def get_idn(self):
    return self._query('*idn?')
  def set_reset(self):
    self._send('*rst')
    return
  def set_pause(self):
    self._send('pause')
    return
  def set_run(self):
    self._send('run')
    return
  def get_raw(self):
    dat = []
    size = int(self._query(':data:raw:size?'))
    self._send(':data:raw?')
    for i in range(size):
      dat.append(list(map(float,self._recieve().split(','))))
    return np.array(dat)
  def get_xy(self):
    return list(map(float,self._query(':data:xy?').split(',')))
  def get_txy(self, sec=0):
    dat = []
    size = int(self._query(f':data:txy? {sec}'))
    for i in range(size):
      dat.append(list(map(float,self._recieve().split(','))))
    return np.array(dat)
  def get_fgFreq(self):
    return float(self._query(':w1:freq?'))
  def set_fgFreq(self, freq):
    self._send(f':w1:freq {freq}\n')

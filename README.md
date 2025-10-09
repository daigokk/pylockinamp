# pyliamp
    Python wrapper of LIA project: https://github.com/daigokk/LIA/
## Usage
1. Install Dependencies
    - [Digilent WaveForms SDK](https://digilent.com/reference/software/waveforms/waveforms-sdk/start)
1. Hardware Setup
    - Connect Analog Discovery 2 or 3 to your PC
    - Example wiring:
      - W1 → CH1+
      - GND → CH1−
1. pip install
    ```
    > pip install -U git+https://github.com/daigokk/pylia.git
    ```
1. Python
    ```Python
    import numpy as np
    import matplotlib.pyplot as plt
    import time
    import pylia
    
    def makeChart(dat:np.array):
      fig, ax = plt.subplots(1, 2, figsize=(3*2,3))
      ax[0].plot(dat[:,0], dat[:,1], label='$V_x$')
      ax[0].plot(dat[:,0], dat[:,2], label='$V_y$')
      ax[1].plot(dat[:,1], dat[:,2])
      ax[0].set_xlabel('Time (s)')
      ax[0].set_ylabel('$V$ (V)')
      ax[0].legend()
      ax[1].set_xlabel('$V_x$ (V)') 
      ax[1].set_ylabel('$V_y$ (V)')
      ax[1].set_aspect('equal', 'box')
      ax[0].grid()
      ax[1].grid()
      fig.tight_layout()
      fig.savefig('chart.svg')
    
    lia = pylia()
    time.sleep(5)
    makeChart(lia.get_txy()) # Save time series and XY(Lissajous) plots of X/Y components
    ```

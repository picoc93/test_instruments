#!/usr/bin/env python3

import funcgen.fy3224s as fg;
import time;

###############################################################################

funcGen = fg.Generator('COM10')
funcGen.debug_mode = True

print(funcGen.get_device_id())
funcGen.set_frequency(10000)
funcGen.set_amplitude(1)



#funcGen[1].set_frequency(5000)
#funcGen[1].set_amplitude(2.5)
#time.sleep(0.1)
#funcGen[1].set_offset(0)
#funcGen[1].set_waveform(fg.Waveform.triangle)
#funcGen[1].set_duty_cycle(50)

funcGen.close()

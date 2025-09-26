# Import necessary modules
import os.path

import numpy as np
from pylablib.devices import Andor
import pylablib as pll
from plotPL_function import plotPL_function

# Configure the library paths for Andor DLLs
pll.par["devices/dlls/andor_shamrock"] = "C:\\Program Files\\Andor SDK\\Shamrock64"
pll.par["devices/dlls/andor_sdk2"] = "C:\\Program Files\\Andor SDK"

def scanspectro_new(xdomain, ydomain,wl, pts,file_name):
    cam = Andor.AndorSDK2Camera(temperature=-80,fan_mode='full')
    cam.set_temperature(-80, enable_cooler=True)
    spec = Andor.ShamrockSpectrograph()

    cam.set_read_mode("fvb")
    cam.set_exposure(1) #integration time
    spec.set_wavelength(wl)  # set 600nm center wavelength
    spec.setup_pixels_from_camera(cam)  # setup camera sensor parameters (number and size of pixels) for wavelength calibration

    sweep_multi([posx, posy], [xdomain[0], ydomain[0]], [xdomain[1], ydomain[1]], [pts[0], pts[1]],
                out= instruments.FunctionWrap(getfunc=lambda: [spec.get_calibration(), np.median(np.stack([cam.snap()[0] for _ in range(3)]),axis=0)]), reset=True,
                filename=file_name, beforewait=0.2
                )

    #disable_piezos
    #spec.setup_pixels_from_camera(cam)  # setup camera sensor parameters (number and size of pixels) for wavelength calibration
    #wavelengths = spec.get_calibration()  # return array of wavelength corresponding to each pixel
    #cam.close()
    #spec.close()



xdomain = [-2500, 2500]
ydomain = [-2500, 2500]
wl = 520e-9;              # Center Wavelength in meters, del_lambda = 80 nm
xresol = 1000;
yresol = 1000;
xpoints=len(range(xdomain[0], xdomain[1], xresol))
ypoints=len(range(ydomain[0], ydomain[1], yresol))
pts = [xpoints, ypoints]
pts= [15,15] # <<<------- Edit here

folder="GaN_Si_16July"
if not os.path.exists(folder):
    os.makedirs(folder)

file_name=os.path.join(folder,'2GaNSi_5x5_0p01mW_0p3umres_0p5sec.txt')
# file_name='cosmic.txt' # laser power (in uW); center wavelength: WLN; alignment mark: FL; sample name/number
# Call the scanspectro function with the defined variables
scanspectro_new(xdomain, ydomain, wl, pts, file_name)

# Post-processing of results

coordinate_file_name=file_name[:-4]
serial_prefix = "name_not_found"
x, y, PL, PL_max_index,min_index, wl, all_pl, r_grid, c_grid = plotPL_function(coordinate_file_name, serial_prefix)



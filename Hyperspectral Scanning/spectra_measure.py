from pylablib.devices import Andor
import pylablib as pll
import matplotlib.pyplot as plt
pll.par["devices/dlls/andor_shamrock"] = "C:\Program Files\Andor SDK\Shamrock64"
pll.par["devices/dlls/andor_sdk2"] = "C:\Program Files\Andor SDK"


def spectra(wl):
    cam = Andor.AndorSDK2Camera(temperature=-80, fan_mode='full')
    cam.set_temperature(-80, enable_cooler=True)
    cam.set_read_mode("fvb")
    cam.set_exposure(0.5)
    # ////////////////
    spectrum = cam.snap()
    import numpy as np
    # spectra2=spectrum.sum(axis=0);
    # print("spectra2 size",spectra2.shape)

    spec = Andor.ShamrockSpectrograph()
    spec.set_wavelength(wl)  # set wl center wavelength
    spec.setup_pixels_from_camera(cam)  # setup camera sensor parameters (number and size of pixels) for wavelength calibration
    wavelengths = spec.get_calibration()
    w2=wavelengths.reshape(1,1024)/1e-9

    print("Center wavelength", spec.get_wavelength())
    print("CCD temperature", cam.get_temperature())
    print("exposure time",cam.get_exposure())

    # print(spectrum.shape)
    # print(wavelengths.shape)
    # print(w2.shape)
    # print(w2)

    plt.figure(figsize=(8, 6))
    plt.plot(w2[0], spectrum[0])
    # print("w2, spectrum, cam.get_detector_size,pizel size,data dimension, roi",w2.shape,spectrum.shape,cam.get_detector_size(),cam.get_pixel_size(),cam.get_data_dimensions(),cam.get_roi())
    plt.xlabel('Wavelength (nm)', size=16);
    plt.ylabel('Counts (a.u.)', size=16);

    # print(spectra2)
    # print(spectra2.shape)

    # plt.figure(figsize=(8, 6))
    # plt.plot(wavelengths / 1e-9, spectra2)
    # plt.xlabel('Wavelength (nm)', size=16);
    # plt.ylabel('Counts (a.u.)', size=16);


# Optical-Instruments-Automation

I have developed a solid-state quantum emitter that works at room temperature, with the goal of tackling the issues of decoherence and the need for low temperatures that current quantum emitters face. I have built the Confocal Microscopy, HBT, Hyperspectral mapping, Optical characterization setup from scractch. Now, my setup is highly optimized and can measure and analyze any solid-state defect, producing 99% pure quantum qubits. During the measurement and analysis, automation between the instruments are highly necessary for repetitive and accurate results. 

Confocal Scanning:

In the confocal scanning process, the nanopositioner is controlled through Python to move systematically across each predefined point on the sample. At each position, the focus of the objective lens is adjusted, and the emission is collected by an avalanche photodiode (APD). The APD records the photon counts, which are stored by the control code. After scanning the full area, a 2D color map of photon counts is generated, where bright spots correspond to regions with higher photon counts. These regions typically indicate defects that act as quantum emitters. This setup requires communication between the nanopositioner and the time-tagger to synchronize position with photon detection.
![alt text](https://github.com/fardin9191/Optical-Instruments-Automation/blob/main/Confocal%20Scanning/Confocal%20PL%20Mapping.png)

Hyperspectral Scanning:

The hyperspectral scanning procedure follows the same approach as the confocal scan, with the nanopositioner moving point by point across the sample. However, instead of recording only photon counts, a full emission spectrum is acquired at each point using a spectrometer. This allows both spatial and spectral information to be collected simultaneously, providing wavelength-resolved maps of the emission. In this configuration, the nanopositioner communicates directly with the spectrometer to save the spectral data at each scan point.
![alt text](https://github.com/fardin9191/Optical-Instruments-Automation/blob/main/Hyperspectral%20Scanning/PL%20Map.png)
![alt text](https://github.com/fardin9191/Optical-Instruments-Automation/blob/main/Hyperspectral%20Scanning/PL.png)

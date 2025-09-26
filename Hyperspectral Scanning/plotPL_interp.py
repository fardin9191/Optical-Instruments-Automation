def plotPL_interp(coordinate_file_name, serial_prefix, Nx=None, Ny=None):
    import math
    import numpy as np
    import matplotlib.pyplot as plt

    ########### Open main file #############################
    open_file = open(coordinate_file_name+".txt", "rb")
    strings = open_file.readlines()
    open_file.close()

    ######### Getting rid of headers and text log #########

    for i in range(len(strings[7])):
        if (strings[i][0:6] == b'#posx\t'):
            break;
    strings = strings[i+1:len(strings)]

    # Number of data points
    N = len(strings)

    # Initializing lists for coordinates
    x = [np.nan for i in range(N)]
    y = [np.nan for i in range(N)]

    # Initialize the photoluminescence list
    avg_pl_list = [np.nan for i in range(N)]

    ######### Get the co-ordinates #############
    for i in range(N):
        x[i], y[i], _, _ = [float(value) for value in strings[i].decode('utf-8').split('\t')]

    ################### Getting PL spectra for each point ###############

    for index in range(N):

        ###### Determining the suffix for the file name #####
        if index==0:
            padding = math.ceil(math.log(N, 10)) - 1
        else:
            padding = math.ceil(math.log(N, 10)) - math.ceil(math.log(index+1, 10))
        serial = str(0)*padding + str(index)

        ##################### Read file ####################
        file_name = coordinate_file_name + "_" + serial_prefix + "_" + serial + ".txt"

        open_file = open(file_name, "rb")
        strings = open_file.readlines()
        open_file.close()

        ############### Store and Calculate ################

        # Get rid of header
        strings = strings[2:len(strings)]

        M = len(strings)

        wl = [0 for i in range(M)]
        PL = [0 for i in range(M)]
        for i in range(M):
            wl[i], PL[i] = [float(value) for value in strings[i].decode('utf-8').split('\t')]

        # Taking the wavelength in units of nm
        wl = [i*1e9 for i in wl]

        # Integration
        int_ = 0
        for i in range(M-1):
            del_wl = wl[i+1]-wl[i]
            int_ = int_ + PL[i]*del_wl
        int_ = int_ + PL[M-1]*del_wl   #Last index
        int_ = int_ / (wl[-1] - wl[0])

        # Storing averaged PL
        avg_pl_list[index] = int_

    ##################### Formatting for 2D color plot ############################
    # Find unique x and y values to define the grid
    unique_x = np.unique(x)
    unique_y = np.unique(y)

    # Create a 2D grid to hold the PL values
    pl_grid = np.full((len(unique_y), len(unique_x)), np.nan)  # Initialize grid
    # clipped_pl_list = np.clip(avg_pl_list, 540, 570)
    # Fill the grid with PL values by mapping (x, y) to their respective indices
    for i in range(len(avg_pl_list)):
        x_idx = np.where(unique_x == x[i])[0][0]  # Column index
        y_idx = np.where(unique_y == y[i])[0][0]  # Row index
        pl_grid[y_idx, x_idx] = avg_pl_list[i]  # PL for corresponding grid cell

    ################## Create a grid of points to interpolate#####################
    from scipy.interpolate import griddata
    
    if Nx==None:
        Nx = len(unique_x)
    if Ny==None:
        Ny = len(unique_y)

    x_i = np.linspace(min(unique_x), max(unique_x), Nx)  # 100 points for x
    y_i = np.linspace(min(unique_y), max(unique_y), Ny)  # 100 points for y
    xi, yi = np.meshgrid(x_i, y_i)

    # Flatten the arrays
    points = np.array([(i, j) for j in unique_y for i in unique_x])
    values = pl_grid.flatten()

    # Interpolate PL onto the new grid (xi, yi)
    pl_interpole = griddata(points, values, (xi, yi), method='cubic')    

    # Create the 2D color plot
    plt.figure(figsize=(8, 6))
    plt.pcolormesh([i/1000 for i in xi], [i/1000 for i in yi], pl_interpole, shading='auto', cmap='inferno')
    plt.colorbar().set_label('Avg. Photoluminescence (a.u.)', fontsize=14)
    plt.xlabel('x ($\\mu$m)', size=14);
    plt.ylabel('y ($\\mu$m)', size=14);
    plt.title("Interpolated Spatial Map of Integrated Photoluminescence Intensity", fontsize=16);
    plt.show()

    # Return x,y coordinates, and average PL
    return x_i, y_i, pl_interpole,wl
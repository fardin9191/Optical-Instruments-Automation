def plotPL_function(coordinate_file_name, serial_prefix):
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
    serial_list=[]
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
        serial_list.append(serial)

        ##################### Read file ####################
        file_name = coordinate_file_name + "_" + serial_prefix + "_" + serial + ".txt"

        open_file = open(file_name, "rb")
        strings = open_file.readlines()
        open_file.close()

        ############### Store and Calculate ################

        # Get rid of header
        strings = strings[2:len(strings)]

        M = len(strings)

        if index == 0:
            all_pl = np.zeros((M, N))

        wl = [0 for i in range(M)]
        PL = [0 for i in range(M)]
        for i in range(M):
            wl[i], PL[i] = [float(value) for value in strings[i].decode('utf-8').split('\t')]

        all_pl[:, index] = PL


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

    # Fill the grid with PL values by mapping (x, y) to their respective indices (04.13.25 change it)
    # for i in range(len(avg_pl_list)):
    #     x_idx = np.where(unique_x == x[i])[0][0]  # Column index
    #     y_idx = np.where(unique_y == y[i])[0][0]  # Row index
    #     pl_grid[y_idx, x_idx] = avg_pl_list[i]  # PL for corresponding grid cell
    #
    #
    # # Create the 2D color plot
    # plt.figure(figsize=(8, 6))
    # plt.pcolormesh([i/1000 for i in unique_x], [i/1000 for i in unique_y], pl_grid, shading='auto', cmap='hot')
    # plt.colorbar().set_label('Avg. Photoluminescence (a.u.)', fontsize=16)
    # plt.xlabel('x ($\\mu$m)', size=14);
    # plt.ylabel('y ($\\mu$m)', size=14);
    # plt.title("Spatial Map of Integrated Photoluminescence Intensity", fontsize=16)
    # plt.show()
    # /////////////////////////////////////////////////////////////////////////////////////
    # Assuming avg_pl_list, unique_x, and unique_y are already defined

    # Clip the photoluminescence values between 456.4 and 457


    # Assuming avg_pl_list, unique_x, and unique_y are already defined
    # Replace these with your actual data variables


    # Clip the photoluminescence values between 456.4 and 457
     clipped_pl_list = np.clip(avg_pl_list, 520, 550)
    #


    # Reconstruct the PL grid with the clipped values
    pl_grid = np.zeros((len(unique_y), len(unique_x)))
    print("uniquex:","unique y:",unique_x,unique_y)
    for i in range(len(avg_pl_list)):
        x_idx = np.where(unique_x == x[i])[0][0]  # Column index
        y_idx = np.where(unique_y == y[i])[0][0]  # Row index
        pl_grid[y_idx, x_idx] = avg_pl_list[i]  # PL for corresponding grid cell

    # Create the 2D color plot with the updated color scale
    fig, ax_map = plt.subplots(figsize=(8, 6))
    cax = ax_map.pcolormesh([i / 1000 for i in unique_x], [i / 1000 for i in unique_y], pl_grid, shading='auto',
                            cmap='hot')
    fig.colorbar(cax, ax=ax_map, label='Avg. Photoluminescence (a.u.)')
    ax_map.set_xlabel('x ($\\mu$m)', size=14)
    ax_map.set_ylabel('y ($\\mu$m)', size=14)
    ax_map.set_title("Spatial Map of Integrated Photoluminescence Intensity", fontsize=16)

    # Create the spectrum plot figure
    fig_spectrum, ax_spectrum = plt.subplots(figsize=(8, 6))
    ax_spectrum.set_xlabel('Wavelength (nm)', size=14)
    ax_spectrum.set_ylabel('Counts (a.u.)', size=14)
    ax_spectrum.set_title('Photoluminescence Spectrum at targeted Point', size=15)

    # Example wavelength data and PL spectrum for each point (replace with your actual spectrum data)


    # Function to update the spectrum plot based on the cursor's position
    def update_spectrum(event):
        if event.inaxes != ax_map:
            return  # Only respond to events inside the map

        # Snap cursor position to the nearest x and y grid points
        target_x_index = np.argmin(
            np.abs(unique_x - round(event.xdata, 4)))  # Round cursor position to nearest grid point
        target_y_index = np.argmin(
            np.abs(unique_y - round(event.ydata, 4)))  # Round cursor position to nearest grid point

        # Find the corresponding 1D index in the flattened grid
        one_d_index = np.ravel_multi_index((target_y_index, target_x_index), pl_grid.shape, order='F')

        # Update the spectrum plot
        ax_spectrum.clear()  # Clear the previous plot
        ax_spectrum.plot(wl, all_pl[:, one_d_index])
        ax_spectrum.set_xlabel('Wavelength (nm)', size=14)
        ax_spectrum.set_ylabel('Counts (a.u.)', size=14)
        ax_spectrum.set_title(
            f'Photoluminescence Spectrum at ({unique_x[target_x_index]:.2f}, {unique_y[target_y_index]:.2f}) µm',
            size=15)
        fig_spectrum.canvas.draw()  # Redraw the figure with the updated spectrum

    # Redraw the figure with the updated spectrum

    # Redraw the figure with the updated spectrum

    # Connect the hover event to update the spectrum
    fig.canvas.mpl_connect('motion_notify_event', update_spectrum)

    # Show the PL map and spectrum plots
    plt.show()

    #///////////////////////////////////////////////////////////////////////////////
    max_index = np.unravel_index(np.argmax(pl_grid), pl_grid.shape)

    x_max = unique_x[max_index[1]]
    y_max = unique_y[max_index[0]]


    row_index = max_index[0]
    col_index = max_index[1]

    print("Maximum PL Intensity at:", f"(x: {x_max}, y: {y_max})")
    r=col_index+1
    c=row_index+1
    print("Grid location in 2D map:", f"({r},{c})")

    PL_max_ind= avg_pl_list.index(max(avg_pl_list))
    PL_min_ind= avg_pl_list.index(min(avg_pl_list))


    # plt.figure(figsize=(8, 6))
    # plt.plot(wl, all_pl[:, PL_max_ind])
    # plt.xlabel('Wavelength (nm)', size=16);
    # plt.ylabel('Counts (a.u.)', size=16);
    #
    # plt.show()

    max_serial=serial_list[PL_max_ind]
    min_serial=serial_list[PL_min_ind]

    print(max_serial,min_serial)
    # Return x,y coordinates, and average PL
    return unique_x, unique_y, pl_grid,PL_max_ind, PL_min_ind, wl, all_pl, r, c

import matplotlib.pyplot as plt
import numpy as np

# make sure the image file is in the same directory as your Python file.


def construct_file_name(lat, lon):
    """ Takes the latitude and longitude as signed integers and
    constructs the appropriate file name for the TIF file. """
    lat_str = "n" + str(abs(lat)).zfill(2) if lat >= 0 else "s" + str(abs(lat)).zfill(2)
    lon_str = "w" + str(abs(lon)).zfill(3) if lon < 0 else "e" + str(abs(lon)).zfill(3)
    filename = f"USGS_NED_1_{lat_str}{lon_str}_IMG.tif"
    return filename


def load_trim_image(lat, lon):
    """ Takes the latitude and longitude as signed integers and
    loads the appropriate file. It then trims off the boundary
    of six pixels on all four sides. """
    file_name = construct_file_name(lat, lon)
    image = plt.imread(file_name)
    image = image[6:-6, 6:-6]
    return image



def stitch_four(lat, lon):
    nw_image = load_trim_image(lat, lon)
    ne_image = load_trim_image(lat, lon + 1)
    sw_image = load_trim_image(lat - 1, lon)
    se_image = load_trim_image(lat - 1, lon + 1)
    top_row = np.concatenate((nw_image, ne_image), axis=1)
    bottom_row = np.concatenate((sw_image, se_image), axis=1)
    image = np.concatenate((top_row, bottom_row), axis=0)
    return image


def get_row(lat, lon_min, num_tiles):
    """ Takes the latitude, minimum longitude, and number of tiles and
    returns an image that combines tiles along a row of different
    longitudes. """
    tiles = []
    for i in range(num_tiles):
        lon = lon_min + i
        images = load_trim_image(lat, lon)
        tiles.append(images)
    image = np.concatenate(tiles, axis=1)
    return image


def get_tile_grid(lat_max, lon_min, num_lat, num_lon):
    """ Takes the northwest coordinate (maximum latitude, minimum longitude)
    and the number of tiles in each dimension (num_lat, num_lon) and
    constructs the image containing the entire range. """
    rows = []
    for i in range(num_lat):
        lat = lat_max - i
        row = get_row(lat, lon_min, num_lon)
        rows.append(row)
    image = np.concatenate(rows, axis=0)

    return image


def get_northwest(lat, lon):
    """ Get the integer coordinates of the northwest corner of the tile
    that contains this decimal (lat, lon) coordinate. """

    # Find the northwest corner of the containing tile by rounding down to the nearest integer degree
    nw_lat = int(np.ceil(lat))
    nw_lon = int(np.floor(lon))

    return nw_lat, nw_lon



def get_tile_grid_decimal(northwest, southeast):
    """ Construct the tiled grid of TIF images that contains these
    northwest and southeast decimal coordinates. Each corner
    is a tuple, (lat, lon). """
    nw_lat, nw_lon = get_northwest(northwest[0], northwest[1])
    se_lat, se_lon = get_northwest(southeast[0], southeast[1])
    num_lat = nw_lat - se_lat + 1
    num_lon = se_lon - nw_lon + 1
    image = get_tile_grid(nw_lat, nw_lon, num_lat, num_lon)
    return image

nw = (37.2, -82.7)
se = (36.6, -82.5)
im = get_tile_grid_decimal(nw, se)
print(im.shape)
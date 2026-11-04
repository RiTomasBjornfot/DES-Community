"""040_VIZ_020-Drawing-Images-On-Base-Map: see the accompanying Markdown guide."""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parent)
from example_output import display, save_plots

if __name__ == "__main__":
    # Step 2
    import openeo
    import io
    import numpy as np

    from shapely.geometry import shape, Polygon

    import rasterio
    from rasterio.plot import show
    import matplotlib.pyplot as plt

    from pyproj import Transformer

    import cartopy.crs as ccrs
    import cartopy.io.img_tiles as cimgt

    from config import user,passwd,eo_service_url
    from demo_helpers import show_result
    from demo_regions import s2
     
    plt.rcParams['figure.figsize'] = [20, 10]

    # Step 3
    # Connect to OpenEO
    conn = openeo.connect(eo_service_url)
    display(
    conn.authenticate_basic(username=user, password=passwd)
    )
    #conn.authenticate_oidc()

    # Step 5
    (lat, lon) = (65.61440779660053, 22.10106269154247)

    # Step 6
    # Create a transformer from EPSG:4326 to EPSG:3006
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3006", always_xy=True)
    # Transform the polygon coordinates
    x, y = transformer.transform(lon, lat)

    # Create a bounding box with size half_size * 2 in meters.
    half_size = 500

    # Adjust bounds
    east = x + half_size
    west = x - half_size
    north = y + half_size
    south = y - half_size

    # Step 7
    # Define padded bounding box in correct CRS
    bbox = {
        'east': east,
        'south': south,
        'west': west,
        'north': north,
        'crs':"EPSG:3006"
    }
    display(
    bbox
    )

    # Step 8
    # Download S2MSI2A data
    cube = conn.load_collection(
        s2.s2_msi_l2a,
        bands=["b04","b03","b02"], #RGB channels
        spatial_extent=bbox,
        temporal_extent=["2020-06-08", "2020-06-09"],
    )
    cube = cube.reduce_dimension(dimension="t", reducer="first")
    res = cube.download()

    # Step 9
    # Read the result
    filelike = io.BytesIO(res)
    raster_data = rasterio.open(filelike)
    display(
    raster_data.read(1) 
    )

    # Step 10
    # Read the result
    filelike = io.BytesIO(res)
    raster_data = rasterio.open(filelike)

    # Split the data into color channels
    red = raster_data.read(1)   # Red channel
    green = raster_data.read(2) # Green channel
    blue = raster_data.read(3)  # Blue channel

    # Determine the actual range of the data
    max_value = np.max([red.max(), green.max(), blue.max()])

    # Scale the data to 0-1 range based on the actual max value (needed for plt.imshow)
    red_scaled = red / max_value
    green_scaled = green / max_value
    blue_scaled = blue / max_value

    # Stack the scaled bands to form an RGB image
    rgb_scaled = np.dstack((red_scaled, green_scaled, blue_scaled))

    # Step 11
    # Define the Coordinate Reference System (CRS)
    # EPSG:3006 is used for the Swedish national coordinate system (SWEREF99 TM)
    crs = 3006

    # Set the extent of the map based on the bounding box coordinates
    # The extent is defined as (west, east, south, north) in the CRS defined above
    extent = (west, east, south, north)

    # Create a Cartopy map projection using the specified CRS
    ax = plt.axes(projection=ccrs.epsg(crs))

    # Set the geographical extent of the map view using the bounding box defined earlier
    # This ensures that the map is centered around the region of interest
    ax.set_extent(extent, crs=ccrs.epsg(crs))


    # Choose base map
    request = cimgt.GoogleTiles()
    #request = cimgt.OSM()

    ax.add_image(request, 15, alpha=.5)
    display(
    ax.imshow(rgb_scaled, extent=extent, transform=ccrs.epsg(crs))
    )
    save_plots()

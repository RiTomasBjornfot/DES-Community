"""session2_loading_and_visualizing: see the accompanying Markdown guide."""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parent)
from example_output import display, save_plots

if __name__ == "__main__":
    # Step 3
    import openeo

    # Connect and authenticate
    connection = openeo.connect('https://openeo.digitalearth.se')
    connection.authenticate_basic(username='testuser', password='secretpassword')
    display(
    print('Connected successfully.')
    )

    # Step 5
    import io
    import xarray as xr
    import numpy as np
    import matplotlib.pyplot as plt

    # Step 7
    # Inspect the DES Sentinel-2 Level 2 collection
    info = connection.describe_collection('des_s2_msi_l2a')
    print('Collection title:', info.get('title'))
    print('Temporal extent :', info.get('extent', {}).get('temporal'))

    # List available bands
    summaries = info.get('summaries', {})
    bands = summaries.get('eo:bands', [])
    print('\nAvailable bands:')
    for b in bands:
        print(f"  {b.get('name', '?'):6s}  {b.get('description', '')}")

    # Step 10
    # Area of interest: Karlstad city centre and surroundings
    aoi = {
        'west':  13.460930954751282,
        'east':  13.585449709728213,
        'south': 59.36327761288911,
        'north': 59.40107161575003,
        'crs':   'EPSG:4326',
    }

    # We will load a cloud-free autumn scene
    timespan = ['2026-06-01', '2026-07-01']

    # Cloud cover threshold (optional)
    max_cloud_cover = 20

    print('Area of interest:', aoi)
    display(
    print('Time range      :', timespan)
    )

    # Step 12
    datacube = connection.load_collection(
        collection_id='des_s2_msi_l2a',
        spatial_extent=aoi,
        temporal_extent=timespan,
        bands=['B02', 'B03', 'B04', 'B08'],
        properties = {'eo:cloud_cover': lambda x: x <= max_cloud_cover},
    )

    display(
    print('Datacube defined. Use .download() to retrieve the data.')
    )

    # Step 14
    # Pick the first available scene using the reduction method (we will look at dimension reduction in detail in Session 4) 
    image = datacube.reduce_dimension(dimension='t', reducer='first')

    # Downloading the image as GeoTIFF
    image_tif = image.download(format='GTiff')

    # Load into xarray
    da = xr.open_dataarray(io.BytesIO(image_tif), engine='rasterio')
    da = da.assign_coords(band=['B02', 'B03', 'B04', 'B08'])

    # Step 16
    print(da)
    # print(da.values)

    # Rescaling reflectance values to [0, 1]
    da = (da.astype(np.float32) / 10_000).clip(0, 1)

    # Step 18
    # Select red band
    red = da.sel(band='B04')

    # Vizualize 
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    red.plot.imshow(ax=ax, cmap='gray', vmin=0, vmax=0.4, add_colorbar=False)
    ax.set_aspect('equal')
    ax.set_title('Sentinel-2 Red Band (B04)')
    plt.tight_layout()
    display(
    plt.show()
    )

    # Step 20
    # Create true color visualization
    rgb = da.sel(band=['B04', 'B03', 'B02'])

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    rgb.plot.imshow(rgb='band', vmin=0, vmax=0.4, ax=ax)
    ax.set_aspect('equal')
    ax.set_title('Sentinel-2 True Color (B04, B03, B02)')
    plt.tight_layout()
    display(
    plt.show()
    )

    # Step 22
    # Create false color visualization
    rgb = da.sel(band=['B08', 'B04', 'B03'])

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    rgb.plot.imshow(rgb='band', vmin=0, vmax=0.4, ax=ax)
    ax.set_aspect('equal')
    ax.set_title('Sentinel-2 False Color (B08, B04, B03)')
    plt.tight_layout()
    display(
    plt.show()
    )
    save_plots()

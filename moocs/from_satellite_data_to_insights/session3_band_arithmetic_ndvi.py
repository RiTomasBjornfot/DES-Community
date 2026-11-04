"""session3_band_arithmetic_ndvi: see the accompanying Markdown guide."""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parent)
from example_output import display, save_plots

if __name__ == "__main__":
    # Step 3
    import openeo
    import io
    import numpy as np
    import xarray as xr
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    import rasterio
    import rasterio.plot

    # Connect to Digital Earth Sweden
    connection = openeo.connect('https://openeo.digitalearth.se')
    connection.authenticate_basic(username='testuser', password='secretpassword')

    # Area of interest: Karlstad, Sweden
    aoi = {
        'west':  13.460930954751282,
        'east':  13.585449709728213,
        'south': 59.36327761288911,
        'north': 59.40107161575003,
        'crs':   'EPSG:4326',
    }
    timespan = ['2026-06-01', '2026-07-01']

    # Load Sentinel-2 datacube with Red and NIR bands
    datacube = connection.load_collection(
        collection_id='des_s2_msi_l2a',
        spatial_extent=aoi,
        temporal_extent=timespan,
        bands=['B02', 'B03', 'B04', 'B08'],
        properties = {'eo:cloud_cover': lambda x: x <= 20},
    )
    image = datacube.reduce_dimension(dimension='t', reducer='first')

    display(
    print('Connected and datacube defined.')
    )

    # Step 5
    image = datacube.reduce_dimension(dimension='t', reducer='first')

    # Downloading the image as GeoTIFF
    image_tif = image.download(format='GTiff')

    # Load into xarray
    da = xr.open_dataarray(io.BytesIO(image_tif), engine='rasterio')
    da = da.assign_coords(band=['B02', 'B03', 'B04', 'B08'])
    da = (da.astype(np.float32) / 10_000).clip(0, 1)

    # True color visualization
    rgb = da.sel(band=['B04', 'B03', 'B02'])
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    rgb.plot.imshow(rgb='band', vmin=0, vmax=0.4, ax=ax)
    ax.set_aspect('equal')
    ax.set_title('Sentinel-2 True Color (B04, B03, B02)')
    plt.tight_layout()
    display(
    plt.show()
    )

    # Step 9
    # Extract individual bands from the datacube
    red = image.band('B04')  # Red (665 nm)
    nir = image.band('B08')  # Near-infrared (842 nm)

    # Compute NDVI using the standard formula
    # Note: these operations are translated to backend processes, not computed locally
    ndvi = (nir - red) / (nir + red)

    # Download the result as a GeoTIFF
    ndvi_tif = ndvi.download(format='GTiff')
    display(
    print('NDVI downloaded successfully.')
    )

    # Step 11
    ndvi_da = xr.open_dataarray(io.BytesIO(ndvi_tif), engine='rasterio')
    ndvi_da = ndvi_da.squeeze()  # Drop any singleton band dimension

    # Formatting the colorbar to look 'nicer'
    cbar_kwargs={'shrink': 0.6, 'aspect': 20, 'pad': 0.02, 'label': 'NDVI'}

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ndvi_da.plot.imshow(ax=ax, cmap='RdYlGn', cbar_kwargs=cbar_kwargs, vmin=-1, vmax=1)
    ax.set_aspect('equal')
    ax.set_title('NDVI')
    display(
    plt.show()
    )

    # Step 13
    # Compute NDVI using the built-in openEO method
    ndvi_datacube = datacube.ndvi(nir='B08', red='B04')
    ndvi = ndvi_datacube.reduce_dimension(dimension='t', reducer='first')

    # Download and display
    ndvi_tif = ndvi.download(format='GTiff')
    ndvi_da = xr.open_dataarray(io.BytesIO(ndvi_tif), engine='rasterio')
    ndvi_da = ndvi_da.squeeze()  # Drop any singleton band dimension

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ndvi_da.plot.imshow(ax=ax, cmap='RdYlGn', cbar_kwargs=cbar_kwargs, vmin=-1, vmax=1)
    ax.set_aspect('equal')
    ax.set_title('NDVI')
    display(
    plt.show()
    )
    save_plots()

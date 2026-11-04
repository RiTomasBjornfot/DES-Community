"""session4_temporal_reduction: see the accompanying Markdown guide."""
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

    # Connect to Digital Earth Sweden
    connection = openeo.connect('https://openeo.digitalearth.se')
    connection.authenticate_basic(username='testuser', password='secretpassword')

    display(
    print('Connected to Digital Earth Sweden.')
    )

    # Step 6
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
    display(
    print('Multi-temporal datacube defined.')
    )

    # Step 9
    # Reduce the time dimension by selecting the first image in the series
    first_image = datacube.reduce_dimension(dimension='t', reducer='first')
    first_tif = first_image.download(format='GTiff')

    # Load into xarray
    da = xr.open_dataarray(io.BytesIO(first_tif), engine='rasterio')
    da = da.assign_coords(band=['B02', 'B03', 'B04', 'B08'])
    da = (da.astype(np.float32) / 10_000).clip(0, 1)

    # True color visualization
    rgb = da.sel(band=['B04', 'B03', 'B02'])
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    rgb.plot.imshow(rgb='band', vmin=0, vmax=0.4, ax=ax)
    ax.set_aspect('equal')
    ax.set_title('First Sentinel-2 Scene (B04, B03, B02)')
    plt.tight_layout()
    display(
    plt.show()
    )

    # Step 11
    # Reduce the time dimension by computing the per-pixel mean
    mean_image = datacube.reduce_dimension(dimension='t', reducer='mean')
    mean_tif = mean_image.download(format='GTiff')

    # Load into xarray
    da = xr.open_dataarray(io.BytesIO(mean_tif), engine='rasterio')
    da = da.assign_coords(band=['B02', 'B03', 'B04', 'B08'])
    da = (da.astype(np.float32) / 10_000).clip(0, 1)

    # True color visualization
    rgb = da.sel(band=['B04', 'B03', 'B02'])
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    rgb.plot.imshow(rgb='band', vmin=0, vmax=0.4, ax=ax)
    ax.set_aspect('equal')
    ax.set_title('Mean Sentinel-2 Composite (B04, B03, B02)')
    plt.tight_layout()
    display(
    plt.show()
    )

    # Step 13
    # Reduce the time dimension using the median (more robust than mean for cloud removal)
    median_image = datacube.reduce_dimension(dimension='t', reducer='median')
    median_tif = median_image.download(format='GTiff')

    # Load into xarray
    da = xr.open_dataarray(io.BytesIO(median_tif), engine='rasterio')
    da = da.assign_coords(band=['B02', 'B03', 'B04', 'B08'])
    da = (da.astype(np.float32) / 10_000).clip(0, 1)

    # True color visualization
    rgb = da.sel(band=['B04', 'B03', 'B02'])
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    rgb.plot.imshow(rgb='band', vmin=0, vmax=0.4, ax=ax)
    ax.set_aspect('equal')
    ax.set_title('Median Sentinel-2 Composite (B04, B03, B02)')
    plt.tight_layout()
    display(
    plt.show()
    )

    # Step 15
    # Compute NDVI for every scene in the datacube (as learned in Session 3)
    ndvi_datacube = datacube.ndvi(nir='B08', red='B04')

    # Maximum NDVI over the period (proxy for maximum vegetation greenness)
    max_ndvi_image = ndvi_datacube.reduce_dimension(dimension='t', reducer='max')
    max_ndvi_tif = max_ndvi_image.download(format='GTiff')

    # Load into xarray
    max_ndvi_da = xr.open_dataarray(io.BytesIO(max_ndvi_tif), engine='rasterio').squeeze()

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    cbar_kwargs = {'shrink': 0.6, 'aspect': 20, 'pad': 0.02, 'label': 'NDVI'}
    max_ndvi_da.plot.imshow(ax=ax, cmap='RdYlGn', cbar_kwargs=cbar_kwargs, vmin=-1, vmax=1)
    ax.set_aspect('equal')
    ax.set_title('Max NDVI — Karlstad, June 2026 (Peak Greenness)')
    plt.tight_layout()
    display(
    plt.show()
    )
    save_plots()

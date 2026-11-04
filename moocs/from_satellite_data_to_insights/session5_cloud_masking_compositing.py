"""session5_cloud_masking_compositing: see the accompanying Markdown guide."""
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

    # Area of interest: Karlstad, Sweden
    aoi = {
        'west':  13.460930954751282,
        'east':  13.585449709728213,
        'south': 59.36327761288911,
        'north': 59.40107161575003,
        'crs':   'EPSG:4326',
    }

    # We use a one-month window to ensure multiple scenes are available
    timespan = ['2026-06-01', '2026-07-01']
    max_cloud_cover = 20  # Scene-level pre-filter: drop scenes with > 20% cloud cover

    display(
    print('Connected to Digital Earth Sweden.')
    )

    # Step 6
    # Load a single scene from the time range (may contain clouds)
    datacube = connection.load_collection(
        collection_id='des_s2_msi_l2a',
        spatial_extent=aoi,
        temporal_extent=timespan,
        bands=['B02', 'B03', 'B04', 'B08'],
        properties={'eo:cloud_cover': lambda x: x <= max_cloud_cover},
    )

    # Take the first available scene
    image = datacube.reduce_dimension(dimension='t', reducer='first')
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

    # Step 8
    # Load the QAI band for the same area, time range, and scene-level filter
    qai_datacube = connection.load_collection(
        collection_id='des_s2_msi_l2a',
        spatial_extent=aoi,
        temporal_extent=timespan,
        bands=['QAI'],
        properties={'eo:cloud_cover': lambda x: x <= max_cloud_cover},
    )
        
    qai_image = qai_datacube.reduce_dimension(dimension='t', reducer='first')

    # Visualize the QAI layer for the Sentinel-2 scene
    qai_image_tif = qai_image.download(format='GTiff')
    da = xr.open_dataarray(io.BytesIO(qai_image_tif), engine='rasterio')
    da = da.assign_coords(band=['QAI'])
    quality_bits = da.sel(band='QAI')

    # Vizualize 
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    quality_bits.plot.imshow(ax=ax, cmap='gray', add_colorbar=False)
    ax.set_aspect('equal')
    ax.set_title('Quality Assurance Information (QAI)')
    plt.tight_layout()
    display(
    plt.show()
    )

    # Step 10
    def create_cloud_mask(qai_band):
        # Bits 1 and 2 are cloud state bits -> shift bits one bit to the right
        shifted = qai_band.process('bitwise_right_shift', x=qai_band, y=1)
        # Isolate the two bits using a bit mask (binary 11 is 3)
        cloud_state = shifted.process('bitwise_and', x=shifted, y=3)
        # Create a cloud mask for confident, opaque clouds (integer value 2)
        cloud_mask = cloud_state == 2
        return cloud_mask

    cloud_mask = create_cloud_mask(qai_image.band('QAI'))

    # Visualize the QAI layer for the Sentinel-2 scene
    cloud_mask_tif = cloud_mask.download(format='GTiff')
    da = xr.open_dataarray(io.BytesIO(cloud_mask_tif), engine='rasterio')
    da = da.assign_coords(band=['QAI'])
    qai = da.sel(band='QAI')

    # Vizualize 
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    qai.plot.imshow(ax=ax, cmap='gray', add_colorbar=False)
    ax.set_aspect('equal')
    ax.set_title('QAI-Based Cloud Mask')
    display(
    plt.show()
    )

    # Step 12
    # Resample QAI (20 m) to match the RGB datacube (10 m)
    cloud_mask_resampled = cloud_mask.resample_cube_spatial(image)

    # Apply the mask: masked pixels become NaN / NoData
    masked_image = image.mask(cloud_mask_resampled)

    masked_image_tif = masked_image.download(format='GTiff')

    # Load into xarray
    da = xr.open_dataarray(io.BytesIO(masked_image_tif), engine='rasterio')
    da = da.assign_coords(band=['B02', 'B03', 'B04', 'B08'])
    da = (da.astype(np.float32) / 10_000).clip(0, 1)

    # True color visualization
    rgb = da.sel(band=['B04', 'B03', 'B02'])
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    rgb.plot.imshow(rgb='band', vmin=0, vmax=0.4, ax=ax)
    ax.set_aspect('equal')
    ax.set_title('Sentinel-2 True Color (B04, B03, B02) with Masked Clouds')
    plt.tight_layout()
    display(
    plt.show()
    )

    # Step 14
    cloud_mask_datacube = qai_datacube.band('QAI').apply(lambda x: create_cloud_mask(x))

    # Resample QAI (20 m) to match the RGB datacube (10 m)
    cloud_mask_datacube_resampled = cloud_mask_datacube.resample_cube_spatial(datacube)

    # Apply the mask: masked pixels become NaN / NoData
    datacube_masked = datacube.mask(cloud_mask_datacube_resampled)

    composite = datacube_masked.reduce_dimension(dimension='t', reducer='median')

    # Download and display the cloud-free composite
    composite_tif = composite.download(format='GTiff')

    # Load into xarray
    da = xr.open_dataarray(io.BytesIO(composite_tif), engine='rasterio')
    da = da.assign_coords(band=['B02', 'B03', 'B04', 'B08'])

    # True color visualization
    rgb = da.sel(band=['B04', 'B03', 'B02'])
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    rgb.plot.imshow(rgb='band', vmin=0, vmax=4_000, ax=ax)
    ax.set_aspect('equal')
    ax.set_title('Cloud-Free Sentinel-2 True Color Composite (B04, B03, B02)')
    plt.tight_layout()
    display(
    plt.show()
    )

    # Step 16
    # Computing NDVI for each scene in the datacube, as learned in Session 3
    ndvi_datacube = datacube_masked.ndvi(nir='B08', red='B04')

    # Performing additional masking of low-quality (subzero and saturation) pixels
    # The procedure is identical to cloud masking, but different bit information is isolated
    def extract_bit(band, bit_position):
        shifted = band.process('bitwise_right_shift', x=band, y=bit_position)
        return shifted.process('bitwise_and', x=shifted, y=1)

    def create_quality_mask(qai_band):
        subzero_mask = extract_bit(qai_band, 8) == 1
        saturation_mask = extract_bit(qai_band, 9) == 1
        
        quality_mask = subzero_mask.process('or', x=subzero_mask, y=saturation_mask)
        
        return quality_mask

    # Apply the quality mask to the NDVI datacube
    quality_mask_datacube = qai_datacube.band('QAI').apply(lambda x: create_quality_mask(x))
    quality_mask_datacube_resampled = quality_mask_datacube.resample_cube_spatial(ndvi_datacube)
    ndvi_datacube = ndvi_datacube.mask(quality_mask_datacube_resampled)

    # Compute NDVI across high-quality observations
    ndvi_composite = ndvi_datacube.reduce_dimension(dimension='t', reducer='mean')

    # Download and display the NDVI product
    ndvi_tif = ndvi_composite.download(format='GTiff')
    ndvi_da = xr.open_dataarray(io.BytesIO(ndvi_tif), engine='rasterio')
    ndvi_da = ndvi_da.squeeze()  # Drop any singleton band dimension

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    cbar_kwargs={'shrink': 0.6, 'aspect': 20, 'pad': 0.02, 'label': 'NDVI'}
    ndvi_da.plot.imshow(ax=ax, cmap='RdYlGn', cbar_kwargs=cbar_kwargs, vmin=-1, vmax=1)
    ax.set_aspect('equal')
    ax.set_title('Mean NDVI Product')
    display(
    plt.show()
    )
    save_plots()

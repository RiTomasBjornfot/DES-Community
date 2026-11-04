"""session1_welcome_to_des: see the accompanying Markdown guide."""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parent)
from example_output import display, save_plots

if __name__ == "__main__":
    # Step 4
    import openeo
    import io
    import numpy as np
    import xarray as xr
    import matplotlib.pyplot as plt

    connection = openeo.connect('https://openeo.digitalearth.se')
    connection.authenticate_basic(username='testuser', password='secretpassword')

    aoi = {
        'west':  16.328473091125044,
        'east':  16.499276161193396,
        'south': 61.32281205270308,
        'north': 61.38375204609653,
        'crs':   'EPSG:4326',
    }

    image = connection.load_collection(
        collection_id='des_s2_msi_l2a',
        spatial_extent=aoi,
        temporal_extent=['2026-05-31', '2026-06-02'],
        bands=['B02', 'B03', 'B04', 'B08'],
    ).reduce_dimension(dimension='t', reducer='first')

    image_tif = image.download(format='GTiff')

    # Load into xarray
    da = xr.open_dataarray(io.BytesIO(image_tif), engine='rasterio')
    da = da.assign_coords(band=['B02', 'B03', 'B04', 'B08'])

    # Rescale data
    da = (da.astype(np.float32) / 10_000).clip(0, 1)

    # Create different visualizations
    true_color = da.sel(band=['B04', 'B03', 'B02'])
    false_color = da.sel(band=['B08', 'B04', 'B03'])

    fig, axs = plt.subplots(1, 2, figsize=(12, 10), sharey=True)
    true_color.plot.imshow(rgb='band', vmin=0, vmax=0.4, ax=axs[0])
    false_color.plot.imshow(rgb='band', vmin=0, vmax=0.4, ax=axs[1])
    axs[0].set_aspect('equal')
    axs[1].set_aspect('equal')
    axs[0].set_title('Sentinel-2 True Color (B04, B03, B02)')
    axs[1].set_title('Sentinel-2 False Color (B08, B04, B03)')
    axs[0].set_xlabel('Easting')
    axs[0].set_ylabel('Northing')
    axs[1].set_xlabel('Easting')
    axs[1].set_ylabel('')
    plt.tight_layout()
    display(
    plt.show()
    )

    # Step 8
    # Install the openEO Python client (run once)
    # Install from the terminal: python -m pip install openeo

    # Step 10
    import openeo

    # Connect to the Digital Earth Sweden openEO backend
    connection = openeo.connect('https://openeo.digitalearth.se')

    # Authenticate with basic credentials
    connection.authenticate_basic(username='testuser', password='secretpassword')

    display(
    print('Connected to:', connection.describe_account())
    )

    # Step 12
    # List all available collection IDs on Digital Earth Sweden
    collection_ids = connection.list_collection_ids()
    print('Collections:')
    for cid in collection_ids:
        print(' -', cid)

    # Step 13
    # Inspect the metadata for the Sentinel-2 Level-2A collection
    s2_info = connection.describe_collection('s2_msi_l2a')

    print('Title      :', s2_info.get('title', 'N/A'))
    print('Description:', s2_info.get('description', 'N/A')[:200], '...')
    print('Spatial ext:', s2_info.get('extent', {}).get('spatial', 'N/A'))
    display(
    print('Temporal ext:', s2_info.get('extent', {}).get('temporal', 'N/A'))
    )

    # Step 15
    # List all available processes on the DES backend
    processes = connection.list_processes()
    process_names = [p['id'] for p in processes]
    print(f'Total processes available: {len(process_names)}')
    print('\nA selection of processes:')
    selected = ['ndvi', 'mask', 'reduce_dimension', 'load_collection', 'save_result']
    for name in selected:
        if name in process_names:
            print(f'  ✓ {name}')
        else:
            print(f'  ✗ {name} (not found)')
    save_plots()

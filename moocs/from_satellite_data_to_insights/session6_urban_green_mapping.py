"""session6_urban_green_mapping: see the accompanying Markdown guide."""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parent)
from example_output import display, save_plots

if __name__ == "__main__":
    # Step 3
    import io
    import numpy as np
    import xarray as xr
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    import openeo

    # Connect to Digital Earth Sweden
    connection = openeo.connect('https://openeo.digitalearth.se')
    connection.authenticate_basic(username='testuser', password='secretpassword')

    # Training area: Karlstad, Sweden (same area used in Session 5)
    aoi_karlstad = {
        'west':  13.460930954751282,
        'east':  13.585449709728213,
        'south': 59.36327761288911,
        'north': 59.40107161575003,
        'crs':   'EPSG:4326',
    }
    timespan_karlstad = ['2026-06-01', '2026-07-01']
    max_cloud_cover = 20  # Scene-level pre-filter: drop scenes with > 20% cloud cover

    display(
    print('Connected to Digital Earth Sweden.')
    )

    # Step 5
    def create_cloud_mask(qai_band):
        # Bits 1 and 2 are cloud state bits -> shift bits one bit to the right
        shifted = qai_band.process('bitwise_right_shift', x=qai_band, y=1)
        # Isolate the two bits using a bit mask (binary 11 is 3)
        cloud_state = shifted.process('bitwise_and', x=shifted, y=3)
        # Confident, opaque cloud (integer value 2)
        return cloud_state == 2

    def extract_bit(band, bit_position):
        shifted = band.process('bitwise_right_shift', x=band, y=bit_position)
        return shifted.process('bitwise_and', x=shifted, y=1)

    def create_quality_mask(qai_band):
        subzero_mask = extract_bit(qai_band, 8) == 1
        saturation_mask = extract_bit(qai_band, 9) == 1
        return subzero_mask.process('or', x=subzero_mask, y=saturation_mask)

    def build_analysis_ready_datacubes(aoi, timespan, max_cloud_cover=20):
        # Reproduces the Session 5 pipeline: cloud-masked composite + quality-masked NDVI composite
        bands = connection.load_collection(
            collection_id='des_s2_msi_l2a',
            spatial_extent=aoi,
            temporal_extent=timespan,
            bands=['B02', 'B03', 'B04', 'B08'],
            properties={'eo:cloud_cover': lambda x: x <= max_cloud_cover},
        )
        qai = connection.load_collection(
            collection_id='des_s2_msi_l2a',
            spatial_extent=aoi,
            temporal_extent=timespan,
            bands=['QAI'],
            properties={'eo:cloud_cover': lambda x: x <= max_cloud_cover},
        )

        # Cloud mask -> cloud-free spectral composite (median)
        cloud_mask = qai.band('QAI').apply(lambda x: create_cloud_mask(x))
        cloud_mask = cloud_mask.resample_cube_spatial(bands)
        bands_masked = bands.mask(cloud_mask)
        composite = bands_masked.reduce_dimension(dimension='t', reducer='median')

        # Quality mask -> cloud-free NDVI composite (mean)
        ndvi = bands_masked.ndvi(nir='B08', red='B04')
        quality_mask = qai.band('QAI').apply(lambda x: create_quality_mask(x))
        quality_mask = quality_mask.resample_cube_spatial(ndvi)
        ndvi = ndvi.mask(quality_mask)
        ndvi_composite = ndvi.reduce_dimension(dimension='t', reducer='mean')

        return composite, ndvi_composite

    # Step 7
    composite, ndvi_composite = build_analysis_ready_datacubes(
        aoi_karlstad, timespan_karlstad, max_cloud_cover
    )

    # Visualize the true-color composite
    composite_tif = composite.download(format='GTiff')
    da = xr.open_dataarray(io.BytesIO(composite_tif), engine='rasterio')
    da = da.assign_coords(band=['B02', 'B03', 'B04', 'B08'])
    rgb = da.sel(band=['B04', 'B03', 'B02'])

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    rgb.plot.imshow(rgb='band', vmin=0, vmax=4_000, ax=ax)
    ax.set_aspect('equal')
    ax.set_title('Cloud-Free Composite — Karlstad (Training Area)')
    plt.tight_layout()
    display(
    plt.show()
    )

    # Step 8
    ndvi_tif = ndvi_composite.download(format='GTiff')
    ndvi_da = xr.open_dataarray(io.BytesIO(ndvi_tif), engine='rasterio')
    ndvi_da = ndvi_da.squeeze()

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    cbar_kwargs = {'shrink': 0.6, 'aspect': 20, 'pad': 0.02, 'label': 'NDVI'}
    ndvi_da.plot.imshow(ax=ax, cmap='RdYlGn', cbar_kwargs=cbar_kwargs, vmin=-1, vmax=1)
    ax.set_aspect('equal')
    ax.set_title('Cloud-Free NDVI Composite — Karlstad')
    display(
    plt.show()
    )

    # Step 10
    ndvi_threshold = 0.3
    urban_green_mask = ndvi_composite > ndvi_threshold

    # Visualize the label mask
    mask_tif = urban_green_mask.download(format='GTiff')
    mask_da = xr.open_dataarray(io.BytesIO(mask_tif), engine='rasterio').squeeze()

    cmap = ListedColormap(['lightgrey', 'forestgreen'])
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    mask_da.plot.imshow(ax=ax, cmap=cmap, add_colorbar=False)
    ax.set_aspect('equal')
    ax.set_title(f'NDVI-Based Urban Green Labels (threshold = {ndvi_threshold})')
    plt.tight_layout()
    display(
    plt.show()
    )

    # Step 12
    # Reuse the GTiff bytes already downloaded for visualization (band order: B02, B03, B04, B08)
    composite_da = xr.open_dataarray(io.BytesIO(composite_tif), engine='rasterio')
    composite_da = composite_da.assign_coords(band=['B02', 'B03', 'B04', 'B08'])

    # Reuse the GTiff bytes already downloaded for the label mask visualization
    labels_da = xr.open_dataarray(io.BytesIO(mask_tif), engine='rasterio').squeeze()

    print('Feature cube shape:', composite_da.shape)
    display(
    print('Label  cube shape :', labels_da.shape)
    )

    # Step 14
    bands_np = composite_da.values  # shape: (4, H, W)
    mask_np = labels_da.values      # shape: (H, W)

    H, W = mask_np.shape

    # (4, H, W) -> (H*W, 4): each row is a pixel, each column is a spectral band
    X = bands_np.reshape(4, -1).T
    # (H, W) -> (H*W,)
    y = mask_np.flatten()

    # Step 16
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    display(
    print(f'Training pixels: {len(X_train):,}  |  Test pixels: {len(X_test):,}')
    )

    # Step 18
    from sklearn.ensemble import RandomForestClassifier

    rf = RandomForestClassifier(
        n_estimators=100,          # Number of trees in the ensemble
        max_depth=10,               # Maximum depth of each tree
        class_weight='balanced',    # Correct for class imbalance
        n_jobs=-1,                  # Parallelize training across all CPU cores
        random_state=42,            # Seed for reproducibility
    )
    rf.fit(X_train, y_train)
    display(
    print('Training complete.')
    )

    # Step 20
    from sklearn.metrics import classification_report, confusion_matrix
    import seaborn as sns

    y_pred = rf.predict(X_test)

    print(classification_report(y_test, y_pred, target_names=['Non-green', 'Urban green']))

    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(4, 3))
    sns.heatmap(
        cm, annot=True, fmt='d', cmap='Blues',
        xticklabels=['Non-green', 'Urban green'],
        yticklabels=['Non-green', 'Urban green'],
        ax=ax,
    )
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    ax.set_title('Confusion Matrix — Test Set')
    plt.tight_layout()
    display(
    plt.show()
    )

    # Step 22
    aoi_stockholm = {
        'west':  18.025636,
        'east':  18.107674,
        'south': 59.301681,
        'north': 59.322233,
        'crs':   'EPSG:4326',
    }
    timespan_stockholm = ['2026-06-01', '2026-07-01']

    composite_stockholm, _ = build_analysis_ready_datacubes(
        aoi_stockholm, timespan_stockholm, max_cloud_cover
    )

    # Visualize the true-color composite over the new area
    composite_stockholm_tif = composite_stockholm.download(format='GTiff')
    da = xr.open_dataarray(io.BytesIO(composite_stockholm_tif), engine='rasterio')
    da = da.assign_coords(band=['B02', 'B03', 'B04', 'B08'])
    rgb = da.sel(band=['B04', 'B03', 'B02'])

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    rgb.plot.imshow(rgb='band', vmin=0, vmax=4_000, ax=ax)
    ax.set_aspect('equal')
    ax.set_title('Cloud-Free Composite — Södermalm, Stockholm (Inference Area)')
    plt.tight_layout()
    display(
    plt.show()
    )

    # Step 24
    # Reuse the GTiff bytes already downloaded for the Stockholm true-color preview
    X_stockholm_bands = xr.open_dataarray(
        io.BytesIO(composite_stockholm_tif), engine='rasterio'
    ).values  # shape: (4, H, W)
    H_new, W_new = X_stockholm_bands.shape[1], X_stockholm_bands.shape[2]
    X_stockholm = X_stockholm_bands.reshape(4, -1).T

    # Predict with the already-trained Random Forest — no re-training needed
    y_pred_stockholm = rf.predict(X_stockholm).reshape(H_new, W_new)

    # Visualize true color and predicted urban green map side by side
    cmap = ListedColormap(['lightgrey', 'forestgreen'])
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    rgb.plot.imshow(rgb='band', vmin=0, vmax=4_000, ax=axes[0], add_labels=False)
    axes[0].set_title('True Color — Södermalm')
    axes[0].set_aspect('equal')

    axes[1].imshow(y_pred_stockholm, cmap=cmap, interpolation='none')
    axes[1].set_title('Predicted Urban Green — Södermalm')
    axes[1].axis('off')

    plt.tight_layout()
    display(
    plt.show()
    )
    save_plots()

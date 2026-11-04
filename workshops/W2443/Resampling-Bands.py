"""Resampling-Bands: see the accompanying Markdown guide."""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parent)
from example_output import display, save_plots

if __name__ == "__main__":
    # Step 2
    from config import eo_service_url,user,passwd
    from demo_regions import  s2

    # Step 4
    import openeo
    import xarray as xr
    import matplotlib.pyplot as plt

    # Connect to OpenEO
    #conn = openeo.connect(eo_service_url)
    conn = openeo.connect("https://openeo.digitalearth.se")

    # Authenticate (replace with your credentials or use OAuth if available)
    conn.authenticate_basic(username=user, password=passwd)

    # Define the collection and bands to load
    collection = s2.s2_msi_l2a
    band_10m = "b04"  # Red band, 10m resolution
    band_20m = "b11"  # SWIR band, 20m resolution

    # Define a bounding box for the area of interest
    bbox = {
              "west": 13.460930954751282,
              "east": 13.585449709728213,
              "south": 59.36327761288911,
              "north": 59.40107161575003
            }
    timespan=["2024-06-12", "2024-06-13"]
    # Load the data for both bands
    datacube_10m = conn.load_collection(collection, bands=[band_10m], temporal_extent=timespan, spatial_extent=bbox)
    datacube_20m = conn.load_collection(collection, bands=[band_20m], temporal_extent=timespan, spatial_extent=bbox)

    # Step 6
    # Resample the 20m datacube to 10m resolution
    resampled_10m = datacube_10m.resample_cube_spatial(target=datacube_20m, method='bilinear')

    # Step 9
    # Merge the datacubes into a single multi-band cube
    multi_band_cube = datacube_20m.merge_cubes(resampled_10m)

    display(
    multi_band_cube
    )

    # Step 10
    # This is typically a too big job for execute or download
    job = multi_band_cube.create_job(out_format='netcdf',title="Combine bands of different resolution")

    # Step 11
    display(
    display(job)
    )

    # Step 12
    display(
    job.start_and_wait()
    )

    # Step 13
    display(
    job.logs()
    )

    # Step 14
    display(
    job.get_results()
    )

    # Step 15
    results = job.get_results()

    # Step 16
    display(
    results.download_files()
    )

    # Step 17
    ds = xr.open_dataset("summary.nc")
    display(
    ds
    )

    # Step 18
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

    ds['b11'].plot(ax=axes[0], cmap='cividis',add_colorbar=False)
    axes[0].set_title('B11')

    ds['b04'].plot(ax=axes[1], cmap='cividis',add_colorbar=False)
    axes[1].set_title('B04')

    plt.tight_layout()
    display(
    plt.show()
    )

    # Step 20
    display(
    job.delete()
    )
    save_plots()

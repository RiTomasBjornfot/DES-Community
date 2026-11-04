"""loading-data: see the accompanying Markdown guide."""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parent)
from example_output import display, save_plots

if __name__ == "__main__":
    # Step 3
    # Import some commonly used python packages
    import openeo
    from matplotlib import pyplot as plt
    plt.rcParams['figure.figsize'] = [20, 10]

    # Import some convenience modules made for this tutorial
    from config import user,passwd,eo_service_url # This module contains some guide specifics
    from demo_helpers import show_result # We have written some helper functions here
    from demo_regions import s2, s3 # We have defined a few regions of interest to de-clutter the code

    # Step 4
    # 1. We always need to connect to the back-end
    connection = openeo.connect(eo_service_url)
     
    print(eo_service_url)
    print(user)

    display(
    connection.authenticate_basic(username=user, password=passwd)
    )

    # Step 6
    display(
    connection.list_collection_ids()
    )

    # Step 7
    display(
    connection.list_collections()
    )

    # Step 10
    datacube=connection.load_collection(collection_id=s2.s2_msi_l2a,
                             spatial_extent=s2.bbox.karlstad_mini_land,
                             temporal_extent=s2.timespans.one_image,
                            bands=['b04'],
                            )
    display(
    datacube
    )

    # Step 12
    connection.list_file_formats # Browsable description
    display(
    connection.list_output_formats() # Textual representation
    )

    # Step 14
    # 2. download the result
    s2_image_data2 = datacube.download(format="gtiff")

    # Step 15
    # 3. Use our tutorial helper function to view the data!
    display(
    show_result(s2_image_data2, colormap="Reds")
    )

    # Step 17
    import xarray as xr
    import io

    # Downloading the result as a NetCDF file (in memory)
    s2_netcdf_data = datacube.download(format="NetCDF")

    # Load the NetCDF data into an xarray.Dataset directly from memory
    dataset = xr.open_dataset(io.BytesIO(s2_netcdf_data))

    # If you prefer working with a DataArray, you can convert the Dataset to a DataArray
    data_array = dataset.to_array()

    # Inspect the DataArray structure
    display(
    print(data_array)
    )
    save_plots()

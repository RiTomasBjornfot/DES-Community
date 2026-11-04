"""Introduction: see the accompanying Markdown guide."""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parent)
from example_output import display, save_plots

if __name__ == "__main__":
    # Step 2
    # Import some commonly used python packages
    import openeo
    from matplotlib import pyplot as plt
    plt.rcParams['figure.figsize'] = [20, 10]

    # Import some convenience modules made for this tutorial
    from config import user,passwd,eo_service_url # This module contains some guide specifics
    from demo_helpers import show_result # We have written some helper functions here
    from demo_regions import s2, s3 # We have defined a few regions of interest to de-clutter the code

    # Step 3
    # Connect to DES OpenEO backend
    connection = openeo.connect(eo_service_url)

    # connection.authenticate_basic(username=user, password=passwd)

    # Connect with RISE authorized credentials
    display(
    connection.authenticate_oidc() 
    )

    # Step 5
    # To list all collection ids provided by the back-end
    display(
    connection.list_collection_ids()
    )

    # Step 6
    # To get the complete metadata of a particular collection
    display(
    connection.describe_collection('s2_msi_l2a')
    )

    # Step 7
    # To list the basic metadata of all collections
    display(
    connection.list_collections()
    )

    # Step 9
    datacube=connection.load_collection(collection_id=s2.s2_msi_l2a,
                             spatial_extent=s2.bbox.karlstad_mini_land,
                             temporal_extent=s2.timespans.one_image,
                            bands=['b04'],
                            )
    display(
    datacube
    )

    # Step 10
    # Download the data as Gtiff
    s2_image_data2 = datacube.download(format="gtiff")

    # Step 11
    # Use our tutorial helper function to view the data!
    display(
    show_result(s2_image_data2, colormap="Reds")
    )

    # Step 13
    # Explore list of processes

    display(
    connection.list_processes()
    )

    # Step 15
    # Loading the data
    cube=connection.load_collection(s2.s2_msi_l2a,
                             spatial_extent=s2.bbox.karlstad_mini_land,
                             temporal_extent=s2.timespans.one_image,
                             bands=['b04','b08'])
    # Building and Executing the NDVI Process
    res =cube.ndvi(nir="b08",red="b04").download(format="gtiff")
    # Visulizing the result
    _ = show_result(res,is_ndvi=True)
    save_plots()

"""operators: see the accompanying Markdown guide."""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parent)
from example_output import display, save_plots

if __name__ == "__main__":
    # Step 2
    import openeo
    import config
    from demo_regions import s2
    from demo_helpers import show_result
        
    conn = openeo.connect(config.eo_service_url)
    display(
    conn.authenticate_basic(username=config.user, password=config.passwd)
    )

    # Step 4
    display(
    conn.list_processes()
    )

    # Step 6
    # B. Load Some Sample Data 
    s2_datacube=conn.load_collection(collection_id=s2.s2_msi_l2a,
                             spatial_extent=s2.bbox.karlstad_mini_land,
                             temporal_extent=s2.timespans.one_image,
                             bands=['b08','b04'],
                                    )
    # Verify that we have a process graph with just one node, load_collection
    display(
    s2_datacube.flat_graph()
    )

    # Step 8
    red = s2_datacube.band('b04')
    display(
    display(red) # a graphical way to view the process graph. 
    )

    # Step 9
    # Then we pick out the nir band from the data cube
    nir = s2_datacube.band('b08')
    display(
    display(nir.flat_graph()) # Shows the same as above but as a JSON representation.
    )

    # Step 12
    # Perform band math to calculate NDVI using the defined variables (that corresponds to the process trees above)
    ndvi = (nir - red) / (nir + red)
    display(ndvi.flat_graph())
    display(
    ndvi
    )

    # Step 15
    # This is the same ndvi calculation as before, but without creating the intermediate process trees
    long_ndvi = (s2_datacube.band('b08') - s2_datacube.band('b04')) / (s2_datacube.band('b08') + s2_datacube.band('b04'))
    display(long_ndvi.flat_graph())
    display(
    long_ndvi
    )

    # Step 18
    # Download the NDVI result
    ndvi_image_data = ndvi.download(format="gtiff")
    display(
    show_result(ndvi_image_data,is_ndvi=True)
    )
    save_plots()

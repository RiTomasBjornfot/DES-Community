"""reductions: see the accompanying Markdown guide."""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parent)
from example_output import display, save_plots

if __name__ == "__main__":
    # Step 2
    import openeo
    import numpy as np
    from config import user,passwd,eo_service_url
    from demo_regions import s2
    from demo_helpers import show_result, show_zipped_results, plot_pixel_stats

    # Step 3
    connection = openeo.connect(eo_service_url)
    display(
    connection.authenticate_basic(username=user, password=passwd)
    )

    # Step 4
    s2_datacube=connection.load_collection(collection_id=s2.s2_msi_l2a,
                             spatial_extent=s2.bbox.karlstad_mini_land,
                             temporal_extent=s2.timespans.two_images,
                            bands=['b04', 'b03', 'b02'],
                            )
    # - 'b04' (Red): The red band, with a central wavelength of 665 nm, commonly used in vegetation analysis.
    # - 'b03' (Green): The green band, with a central wavelength of 560 nm, useful for monitoring plant health.
    # - 'b02' (Blue): The blue band, with a central wavelength of 490 nm, often used in water body and atmospheric analysis.

    # Step 5
    # Show information
    print(s2_datacube.flat_graph())
    s2_image_data = s2_datacube.download(format="gtiff")
    original_images = show_result(s2_image_data, 'Reds')
    display(
    print("Shape of downloaded datacube (time,bands,x,y)",original_images.shape)
    )

    # Step 9
    display(
    s2.timespans.two_images
    )

    # Step 11
    reduced_cube_over_time = s2_datacube.reduce_dimension(dimension="t", reducer="first")

    # Show information
    #print(reduced_cube_over_time.flat_graph())
    s2_image_data_reduced = reduced_cube_over_time.download(format="gtiff")

    # Step 12
    results_time_reduce=show_result(s2_image_data_reduced, colormap="Greys_r")

    # Step 14
    display(
    print("We expect a single raster/time but multible bands to look at, (time,bands,x,y):", results_time_reduce.shape)
    )

    # Step 16
    display(
    connection.list_processes()
    )

    # Step 19
    reduced_cube_over_bands = s2_datacube.reduce_dimension(dimension="bands", reducer="mean")

    # Show information
    print(reduced_cube_over_bands.flat_graph())
    # reduced_cube_over_bands.metadata
    s2_image_data_reduced = reduced_cube_over_bands.download(format="gtiff")
    results_bands_reduce = show_result(s2_image_data_reduced, "Greys_r")

    # Step 21
    display(
    print(f"We expect multiple rasters/ time steps but only one band in (band,time,x,y):{results_bands_reduce.shape}") 
    )

    # Step 23
    time = 0 
    band = 0
    pixel_x = 0
    pixel_y = 0
    print("Shape of results_time_reduce (time,bands,x.y):",results_time_reduce.shape)
    display(
    np.mean([results_time_reduce[time][band     ][pixel_x,pixel_y], 
             results_time_reduce[time][band + 1 ][pixel_x,pixel_y], 
             results_time_reduce[time][band + 2][pixel_x,pixel_y]])
    )

    # Step 25
    display(
    results_bands_reduce[time][band][pixel_x,pixel_y]
    )
    save_plots()

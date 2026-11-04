"""quality_filter_index_boxes: see the accompanying Markdown guide."""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parent)
from example_output import display, save_plots

if __name__ == "__main__":
    # Step 3
    from config import eo_service_url,user,passwd
    from demo_regions import s2
    import openeo
    conn = openeo.connect(eo_service_url)
    conn.authenticate_basic(username=user, password=passwd)
    #conn.authenticate_oidc()
    cube = conn.load_collection(
        s2.s2_msi_l2a,
        bands=["b01"],
        spatial_extent=s2.bbox.karlstad_mini_land,
        temporal_extent=["2020-03-01", "2020-08-01"]
    )
    args_course = {'data':cube,'filter':'sentinel2-scl-quality-coarse','threshold':0.8}

    coarsely_filtered_cube = cube.process(process_id='filter_quality', arguments=args_course)

    args_fine = {'data':coarsely_filtered_cube,'filter':'sentinel2-scl-quality-fine','threshold':0.99}
    good_data_cube = coarsely_filtered_cube.process(process_id='filter_quality', arguments=args_fine)

    # Tail a dummy process just to show how the process flow continues
    ndvi_cube = good_data_cube.ndvi()
    display(
    display(ndvi_cube)
    )
     
    save_plots()

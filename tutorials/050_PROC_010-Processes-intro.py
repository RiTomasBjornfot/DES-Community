"""050_PROC_010-Processes-intro: see the accompanying Markdown guide."""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parent)
from example_output import display, save_plots

if __name__ == "__main__":
    # Step 3
    import openeo
    from config import user,passwd,eo_service_url
    from demo_helpers import show_result
    from demo_regions import s2
        
    # a. connect to the openeo back-end
    conn = openeo.connect(eo_service_url)
    display(
    conn.authenticate_basic(username= user, password=passwd)
    )

    # Step 5
    display(
    conn.list_processes()
    )

    # Step 7
    # B. Loading the data
    cube=conn.load_collection(s2.s2_msi_l2a,
                             spatial_extent=s2.bbox.karlstad_mini_land,
                             temporal_extent=s2.timespans.one_image,
                             bands=['b04','b08'])
    # C.Building and Executing the NDVI Process
    res =cube.ndvi(nir="b08",red="b04").download(format="gtiff")
    # D. Visulizing the result
    _ = show_result(res,is_ndvi=True)
    save_plots()

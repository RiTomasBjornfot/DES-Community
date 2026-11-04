"""batch-processing: see the accompanying Markdown guide."""
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
    # B. Loading the data
    cube=conn.load_collection(s2.s2_msi_l2a,
                             spatial_extent=s2.bbox.karlstad_mini_land,
                             temporal_extent=s2.timespans.one_image,
                             bands=['b04','b08'])
    # C.Building and Executing the NDVI Process
    ndvi =cube.ndvi(nir="b08",red="b04")
    res = ndvi.download(format="gtiff")
    # D. Visulizing the result

    _ = show_result(res,is_ndvi=True)
    display(
    ndvi
    )

    # Step 7
    # Creating a batch job for the NDVI process defined in previous step
    job = ndvi.create_job(out_format="GTiff", title="NDVI Batch Job", description="Calculating NDVI for selected area")

    display(
    job
    )

    # Step 8
    display(
    job.start_and_wait()
    )

    # Step 9
    # Examining the results
    res = job.get_results()
    display(
    res
    )

    # Step 10
    display(
    job.logs()
    )

    # Step 11
    # We can even run the job again
    job.start_and_wait()
    display(
    job.logs()
    )

    # Step 13
    display(res.get_assets())
    print()
    data = None
    for asset in res.get_assets():
        print("NAME:    ",asset.name)
        print("HREF:    ",asset.href)
        print("METADATA:",asset.metadata)
        if asset.metadata['type']=='image/tiff; application=geotiff':
            data = asset.load_bytes()
        print()

    # Step 15
    display(
    show_result(data,is_ndvi=True)
    )

    # Step 17
    import json
    stac_file = [a for a in res.get_assets() if a.name == 'stac.json']
    stac = json.loads(stac_file[0].load_bytes())
    display(
    stac['properties']['data_sources']
    )
    save_plots()

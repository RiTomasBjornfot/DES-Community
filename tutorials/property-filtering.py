"""property-filtering: see the accompanying Markdown guide."""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parent)
from example_output import display, save_plots

if __name__ == "__main__":
    # Step 2
    import openeo
    from config import user,passwd,eo_service_url
    from demo_regions import s2
    from demo_helpers import load_netcdf_as_xarray
    # We define a dummy area over sweden that will return approximately 10 by 10 pixels
    small_area_like_10_by_10_pixels = {
                                                    "west": 15.8600, 
                                                    "east": 15.8618, 
                                                    "south": 59.1800, 
                                                    "north": 59.1809
                                     }

    # Step 3
    conn = openeo.connect(eo_service_url)
    display(
    conn.authenticate_basic(username= user, password=passwd)
    )

    # Step 6

    cube = conn.load_collection(collection_id = s2.s2_msi_l2a, 
                               spatial_extent =  small_area_like_10_by_10_pixels,
                               temporal_extent = ["2020-07-01T00:00:00Z", "2020-07-30T00:00:00Z"],
                               bands = ["scl",],
                 
                               )
    ncd_data = cube.download(format='netcdf',options={'max_files':30})
    data = load_netcdf_as_xarray(ncd_data)
    display(
    data.dims
    )

    # Step 8
    cube = conn.load_collection(collection_id = s2.s2_msi_l2a, 
                               spatial_extent =  small_area_like_10_by_10_pixels,
                               temporal_extent = ["2020-07-01T00:00:00Z", "2020-07-30T00:00:00Z"],
                               bands = ["scl",],
                
                               properties = {"eo:cloud_cover":  lambda val: val < 70}  
                               )
    ncd_data = cube.download(format='netcdf',options={'max_files':30})
    data = load_netcdf_as_xarray(ncd_data)
    display(
    data.dims
    )

    # Step 10
    cube = conn.load_collection(collection_id = s2.s2_msi_l2a, 
                               spatial_extent =  small_area_like_10_by_10_pixels,
                               temporal_extent = ["2020-07-01T00:00:00Z", "2020-07-30T00:00:00Z"],
                               bands = ["scl",],
                
                               properties = {"eo:cloud_cover":  lambda val: val < 70,
                                            "cloud_cover":  lambda val: val > 60}  
                               )
    ncd_data = cube.download(format='netcdf',options={'max_files':30})
    data = load_netcdf_as_xarray(ncd_data)
    display(
    data.dims
    )
    save_plots()

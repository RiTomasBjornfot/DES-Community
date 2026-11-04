"""060_EO_010-Masking-data: see the accompanying Markdown guide."""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parent)
from example_output import display, save_plots

if __name__ == "__main__":
    # Step 2
    import openeo
    from config import user, passwd, eo_service_url
    from demo_regions import s2
    from demo_helpers import show_result,show_binary_image_thumbnail
    import io
    import matplotlib.pyplot as plt
    import rasterio
    import rasterio.plot
    import numpy as np

    # Step 3
    conn = openeo.connect(eo_service_url)
    display(
    conn.authenticate_basic(username=user, password=passwd)
    )

    # Step 5
    ### Example: Creating and Visualizing a Value-Based Mask

    from demo_regions import s2

    # 1. Load the Sentinel-2 data cube for the Karlstad region, including the SCL band
    s2_datacube = conn.load_collection(s2.s2_msi_l2a,
                             spatial_extent=s2.bbox.karlstad_mini_land,
                             temporal_extent=s2.timespans.one_image,
                             bands=["b05", "scl"] 
    )

    # 2. Create a mask to exclude all pixels where the SCL value equals 4 (vegetation)
    vegetation_mask = s2_datacube.band("scl") == 4

    # 3. Execute process and Visualize the mask
    # Note: This visualization will show the mask itself, highlighting the areas that will be excluded

    scl_mask_data = vegetation_mask.download(format="gtiff")
    title="Logical Mask made out of the SCL Mask"
    scl_mask_image = show_result(scl_mask_data, title=title, colormap="binary", norm=False)
    display(
    show_binary_image_thumbnail(scl_mask_image, title=title)
    )

    # Step 8
    # 1. Load the Sentinel-2 B05 band (Red Edge 1) for the same region and time period
    b05_datacube = s2_datacube.band("b05") 

    # 2. Apply the vegetation mask to the B05 band
    masked_b05 = b05_datacube.mask(vegetation_mask) # Filtering out
    #masked_b05 = b05_datacube.mask(~vegetation_mask) # Keeping 

    # 3. Execute the process and visualize the masked B05 band
    res = masked_b05.download(format="gtiff")
    _ = show_result(res, title="Masked b05 band", colormap="Greys_r")

    # Step 11
    from demo_regions import s3

    # 1. Load the Sentinel-3 data cube for the Karlstad region, including the WSQF and oa08 band
    s3_datacube = conn.load_collection(
        s3.s3_olci_l2wfr,
        spatial_extent=s3.bbox.karlstad_mini_sea,
        temporal_extent=s3.timespans.one_image,
        bands=["wqsf_lsb", "oa08"]
    )

    # Step 12
    # 2. Extract and view  the oa08 band (red light, 665 nm) for analysis
    oa08_band = s3_datacube.band("oa08")
    oa08_data = oa08_band.download(format="gtiff")
    title="Original oa08 band before masking"
    oa08_image = show_result(oa08_data, title=title, colormap="gray", norm=False)
     
    print("Raw pixel values of the original (unmasked) image  (first 8 rows and 3 columns):")
    display(
    print(oa08_image[:8, :3])
    )

    # Step 13
    # 3. Extract and view the WSQF band for creating the quality mask
    wsqf_band = s3_datacube.band("wqsf_lsb") 

    wsqf_data = wsqf_band.download(format="gtiff")
    title="Original WSQF Band"
    wsqf_image = show_result(wsqf_data, title=title, colormap="gray", norm=False)
    display(
    show_binary_image_thumbnail(wsqf_image, title=title)
    )

    # Step 14
    # 4. Select all pixels in the WSWF band where the quality flags indicate coast line (Bit 3) or Sun Glint (Bit 20)
    #    Note that we selected those two since they obviously exist in the mask shown above, not because a particular
    #    interest or that it would make any sense. Focus here is to show the masking in two steps
    selected_bits = 0b00100 | 1<<20 # Bitwise OR operation to combine conditions
    masked_wsqf = wsqf_band.process("bitwise_and", x=wsqf_band, y=selected_bits)
      
    masked_wsqf_data = masked_wsqf.download(format="gtiff")
    title=f"WSQF band masked with {selected_bits:032b}:"
    masked_wsqf_image = show_result(masked_wsqf_data, title=title, colormap="gray", norm=False)
    display(
    show_binary_image_thumbnail(masked_wsqf_image, title=title)
    )

    # Step 16
    # 5. Create a logical mask based on our selected quality flags 
    #  Uncomment one of the options to explore the alternatives described above!

    # Option 1: Any Selected Bits Are Set (OR Logic)
    #quality_mask = masked_wsqf > 0  # Keep pixels where at least one selected bit is set (OR logic)
    #quality_mask = ~(masked_wsqf > 0)  # Filter pixels where at least one selected bit is set (OR logic)

    # Option 2: All Selected Bits Are Set (AND Logic)
    #quality_mask = masked_wsqf == selected_bits  # Keep pixels where all selected bits are set (AND logic)
    quality_mask = ~(masked_wsqf == selected_bits)  # Filter pixels where all selected bits are set (AND logic)

    qmask_data = quality_mask.download(format="gtiff")
    title="Logical Mask Created from the Masked WSQF band"
    qmask_image = show_result(qmask_data, title=title, colormap="gray", norm=False)
    display(
    show_binary_image_thumbnail(qmask_image, title=title)
    )

    # Step 17
     # 6. Apply the quality mask to the oa08 band
    masked_oa08 = oa08_band.mask(quality_mask)

    # 7. Execute the masking and visualize the masked oa08 band
    masked_data = masked_oa08.download(format="gtiff")
    masked_image = show_result(masked_data, title="Masked 08 band!", colormap="gray", norm=False)
    save_plots()

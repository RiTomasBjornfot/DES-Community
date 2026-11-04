"""spatial-filtering: see the accompanying Markdown guide."""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parent)
from example_output import display, save_plots

if __name__ == "__main__":
    # Step 2
    import openeo
    from config import user, passwd, eo_service_url
    from demo_regions import s2
    from demo_helpers import show_result
    import matplotlib.pyplot as plt

    # Step 3
    conn = openeo.connect(eo_service_url)
    display(
    conn.authenticate_basic(username=user, password=passwd)
    )

    # Step 6
    from demo_regions import s2

    # 1. Load the Sentinel-2 data cube for the Södermalm region, focusing on Band 8 (NIR)
    s2_datacube = conn.load_collection(
        s2.s2_msi_l2a,
        spatial_extent=s2.bbox.sodermalm,
        temporal_extent=s2.timespans.one_image,
        bands=["b08"]  # Near-Infrared band (b08)
    )

    # 2. Define a 5x5 mean kernel for stronger smoothing
    mean_kernel = [
        [1/25, 1/25, 1/25, 1/25, 1/25],
        [1/25, 1/25, 1/25, 1/25, 1/25],
        [1/25, 1/25, 1/25, 1/25, 1/25],
        [1/25, 1/25, 1/25, 1/25, 1/25],
        [1/25, 1/25, 1/25, 1/25, 1/25]
    ]

    # 3. Apply the stronger smoothing filter to the loaded data using the apply_kernel process
    smoothed_b08 = s2_datacube.apply_kernel(
        kernel=mean_kernel,
        factor=1.0  # Optional: factor to scale the result, here we keep it as 1
    )

    # 4. Execute the process and visualize the original B08 band
    original_b08 = s2_datacube.download(format="gtiff")
     
    _ = show_result(original_b08, is_ndvi=False, colormap="Greys_r", title="Original Image (b08) Södermalm (Stockholm)")

    # Step 7
    # 5. Execute the process and visualize the smoothed B08 band
    filtered_b08 = smoothed_b08.download(format="gtiff")
     
    _ = show_result(filtered_b08, is_ndvi=False, colormap="Greys_r",title = "Smoothed Image (b08)")

    # Step 11
    from demo_regions import s2

    # 1. Load the Sentinel-2 data cube for the Södermalm region, focusing on Band 8 (NIR)
    s2_datacube = conn.load_collection(
        s2.s2_msi_l2a,
        spatial_extent=s2.bbox.sodermalm,
        temporal_extent=s2.timespans.one_image_cloudfree_sthlm,
        bands=["b08"]  # Near-Infrared band (b08)
    )

    # 2. Define Sobel kernels for edge detection
    sobel_horizontal = [
        [1, 0, -1],
        [2, 0, -2],
        [1, 0, -1]
    ]

    sobel_vertical = [
        [1, 2, 1],
        [0, 0, 0],
        [-1, -2, -1]
    ]

    # 3. Apply the horizontal Sobel filter to the loaded data using the apply_kernel process
    edges_horizontal = s2_datacube.apply_kernel(
        kernel=sobel_horizontal,
        factor=1.0  # Optional: factor to scale the result, here we keep it as 1
    )

    # 4. Apply the vertical Sobel filter to the loaded data using the apply_kernel process
    edges_vertical = s2_datacube.apply_kernel(
        kernel=sobel_vertical,
        factor=1.0  # Optional: factor to scale the result, here we keep it as 1
    )

    # 5. Execute the process and visualize the horizontal edges
    filtered_horizontal = edges_horizontal.download(format="gtiff")

    _ = show_result(filtered_horizontal, is_ndvi=False, colormap="Greys_r", title="Horizontal Edges (Sobel)")

    # Step 12
    # 6. Execute the process and visualize the vertical edges
    filtered_vertical = edges_vertical.download(format="gtiff")
     
    _ = show_result(filtered_vertical, is_ndvi=False, colormap="Greys_r", title="Vertical Edges (Sobel)")
    save_plots()

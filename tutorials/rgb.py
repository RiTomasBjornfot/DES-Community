"""rgb: see the accompanying Markdown guide."""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parent)
from example_output import display, save_plots

if __name__ == "__main__":
    # Step 2
    import openeo
    from config import user,passwd,eo_service_url
    import io
    import rasterio.plot
    import numpy as np
    from demo_regions import s2
    from matplotlib import pyplot as plt
    plt.rcParams['figure.figsize'] = [20, 10]

    # Step 4

    connection = openeo.connect(eo_service_url) 
    display(
    connection.authenticate_basic(username=user, password=passwd)
    )

    # Step 6
    res = connection.load_collection(
        collection_id=s2.s2_msi_l2a,
        spatial_extent=s2.bbox.karlstad_mini_land,
        temporal_extent=s2.timespans.one_image,
        bands=['b04', 'b03', 'b02', 'b08'],
    )

    # Step 8
    # Download the cube as gtiff image data
    s2_image_data2 = res.download(format="gtiff")

    # Step 9
    # Open the image data using rasterio
    filelike = io.BytesIO(s2_image_data2)
    im = rasterio.open(filelike)

    # Step 12
    # 1. Read the bands as arrays
    r = im.read(1)  # Band 4 (Red)
    g = im.read(2)  # Band 3 (Green)
    b = im.read(3)  # Band 2 (Blue)
    nir = im.read(4) # Band 8 (NIR)
    print(r)
    print(g)
    print(b)
    display(
    print(nir)
    )

    # Step 14
    # 2. Normalize the data to the range 0-255 for display
    def normalize(array):
        array_min, array_max = np.percentile(array, (1, 99))  # Clip values between 1st and 99th percentile
        array = np.clip(array, array_min, array_max)  # Clip the extreme values
        return ((array - array_min) / (array_max - array_min) * 255).astype(np.uint8)

    # Step 15
    r_normalized = normalize(r)
    g_normalized = normalize(g)
    b_normalized = normalize(b)
    nir_normalized = normalize(nir)

    print(r_normalized)
    print(g_normalized)
    print(b_normalized)
    display(
    print(nir_normalized)
    )

    # Step 16
    # 3. Stack the bands into an RGB image
    rgb = np.dstack((r_normalized, g_normalized, b_normalized))

    # 4. Display the RGB image using matplotlib
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(rgb)
    ax.set_title(im.tags()["timestamp"])
    display(
    plt.show()
    )

    # Step 18
    # 3. Stack the bands into an RGB image
    nirgb = np.dstack((nir_normalized, g_normalized, b_normalized))

    # 4. Display the RGB image using matplotlib
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(nirgb)
    ax.set_title(im.tags()["timestamp"])
    display(
    plt.show()
    )
    save_plots()

"""040_VIZ_030-Difference-Analysis: see the accompanying Markdown guide."""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parent)
from example_output import display, save_plots

if __name__ == "__main__":
    # Step 2
    import openeo
    from config import user,passwd,eo_service_url
    import io
    import numpy as np
    from demo_regions import s2
    from matplotlib import pyplot as plt
    import rasterio
    plt.rcParams['figure.figsize'] = [20, 20]

    # Step 4
    connection = openeo.connect(eo_service_url)
     
    connection.authenticate_basic(username=user, password=passwd)

    small_area = {
        "west": 13.15986156462585,
        "east": 13.208441734323664,
        "south": 55.57836893130869,
        "north": 55.60441458279001
    }

    def show_single_result_as_rgb(image_byte_like_object: bytes, title: str=""):

        # Open the image data using rasterio
        filelike = io.BytesIO(image_byte_like_object)
        im = rasterio.open(filelike)

        # 1. Read the bands as arrays
        r = im.read(1)  # Band 4 (Red)
        g = im.read(2)  # Band 3 (Green)
        b = im.read(3)  # Band 2 (Blue)

        r_normalized = normalize(r)
        g_normalized = normalize(g)
        b_normalized = normalize(b)

        # 3. Stack the bands into an RGB image
        rgb = np.dstack((r_normalized, g_normalized, b_normalized))

        # 4. Display the RGB image using matplotlib
        _, ax = plt.subplots(figsize=(10, 10))
        ax.imshow(rgb)
        ax.set_title(title)
        plt.show()


    # Normalize the data to the range 0-255 for display
    def normalize(array):
        array_min, array_max = np.percentile(array, (1, 99))  # Clip values between 1st and 99th percentile
        array = np.clip(array, array_min, array_max)  # Clip the extreme values
        return ((array - array_min) / (array_max - array_min) * 255).astype(np.uint8)

    # Step 5
    res=connection.load_collection(collection_id=s2.s2_msi_l2a,
                             spatial_extent=small_area,
                             temporal_extent=["2024-06-02T00:00:00Z", "2024-08-28T10:00:00Z"],
                             bands=['b04', 'b03', 'b02'],
                            )

    # Step 6
    # `res` contains the loaded collection with two temporal extents
    # Split the collection by temporal extents

    first_image = res.reduce_dimension(dimension='t', reducer='first')
    last_image = res.reduce_dimension(dimension='t', reducer='last')

    show_single_result_as_rgb(first_image.download(format='gtiff'), "First image")

    display(
    show_single_result_as_rgb(last_image.download(format='gtiff'), "Last image")
    )

    # Step 8
    # Select the green band (which is b03)
    b03 = res.band("b03")

    # Reduce the green band over time for first and last temporal points
    b03_first_temporal = b03.reduce_dimension(dimension="t", reducer="first")
    b03_last_temporal = b03.reduce_dimension(dimension="t", reducer="last")

    # Calculate the temporal difference between the two images over the green band
    difference_green_band = b03_first_temporal - b03_last_temporal

    # Download the result for visualization
    result_green_band = difference_green_band.download()

    # Step 10

    # Load the difference image into rasterio
    filelike = io.BytesIO(result_green_band)
    raster_data = rasterio.open(filelike)

    # Read the data from the raster
    image_data_green = raster_data.read(1)  # Read the first band (since it's single-band)

    # Plot the difference image using imshow
    fig, ax = plt.subplots(figsize=(10, 10))

    # Adjust colormap to highlight differences in the green band
    cax = ax.imshow(image_data_green, cmap='RdBu', vmin=-1, vmax=1)  # Adjust vmin and vmax based on data range

    plt.title('Difference in Green Band between Two Time Points')

    # Add the colorbar representing the values
    plt.colorbar(cax, ax=ax)

    # Show the plot
    display(
    plt.show()
    )
    save_plots()

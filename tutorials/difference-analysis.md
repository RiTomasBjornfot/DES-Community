[Documentation home](../README.md) · [Download Python script](difference-analysis.py)

Run from this directory with `python difference-analysis.py`. Read the guide first: the script runs all steps in order and may submit remote jobs. Figures and maps are saved under `outputs/difference-analysis/`.

> Saved outputs below come from the original teaching material; they are illustrations, not a fresh run against the current service.

# Difference Between Two Images in Earth Observation (EO)

In Earth Observation (EO), calculating the difference between two images often involves comparing the same scene at different times to identify changes. This technique is widely used in remote sensing for monitoring environmental and human-induced changes.

## Objective:

The objective of this tutorial is to teach you how to calculate the temporal difference between two satellite images, visualize the differences, and interpret the results. This method is essential for identifying changes in land cover, vegetation, water levels, urban development, and more.

In this guide, you will explore temporal difference specifically, as spectral difference (such as band mathematics) has already been covered in previous guides.

*Temporal Difference*:

Temporal difference refers to the pixel-by-pixel subtraction of two images captured at different times over the same area. For instance: If the first image is taken on April 23, 2020, and the second on July 2, 2020, subtracting one from the other will show how the scene has changed (e.g., in vegetation, water levels, or urban growth).

*Why is Temporal Difference Useful?*

This technique is very useful in remote sensing for identifying changes over time, such as deforestation, urban expansion, crop health, or flood damage. The difference image highlights areas where significant changes have occurred, while areas with little or no change will have pixel values close to zero.

Tools You’ll Use:

- OpenEO: For interacting with satellite data and performing image subtraction.
- NumPy: To handle pixel-by-pixel calculations.
- Matplotlib: For visualizing the differences between the images.
- Pandas: For managing and analyzing metadata related to the images.
- Rasterio: For reading, writing, and handling geospatial raster data.


## Learning Outcomes:

By the end of this tutorial, you will be able to:

- Understand the concept of temporal differences in satellite imagery.
- Calculate the temporal difference between two images.
- Visualize and interpret the changes detected over time.
- Apply these techniques to different remote sensing datasets.

Let’s start by loading the example images and understanding their structure before moving on to calculating and visualizing their differences.

### Step 2

```python
import openeo
from config import user,passwd,eo_service_url
import io
import numpy as np
from demo_regions import s2
from matplotlib import pyplot as plt
import rasterio
plt.rcParams['figure.figsize'] = [20, 20]
```

In this part you will be executing the neccessary set up to be able to load and visualize the example we will work on.

### Step 4

```python
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

```

### Step 5

```python
res=connection.load_collection(collection_id=s2.s2_msi_l2a,
                         spatial_extent=small_area,
                         temporal_extent=["2024-06-02T00:00:00Z", "2024-08-28T10:00:00Z"],
                         bands=['b04', 'b03', 'b02'],
                        )

```

### Step 6

```python
# `res` contains the loaded collection with two temporal extents
# Split the collection by temporal extents

first_image = res.reduce_dimension(dimension='t', reducer='first')
last_image = res.reduce_dimension(dimension='t', reducer='last')

show_single_result_as_rgb(first_image.download(format='gtiff'), "First image")

display(
show_single_result_as_rgb(last_image.download(format='gtiff'), "Last image")
)
```

![Example output](assets/difference-analysis/6-0.png)

![Example output](assets/difference-analysis/6-1.png)

We can clearly see from the RGB image the difference in green in the two images. Therefore, in this example of calculating difference in image, we will pick out the green band.

### Step 8

```python
# Select the green band (which is b03)
b03 = res.band("b03")

# Reduce the green band over time for first and last temporal points
b03_first_temporal = b03.reduce_dimension(dimension="t", reducer="first")
b03_last_temporal = b03.reduce_dimension(dimension="t", reducer="last")

# Calculate the temporal difference between the two images over the green band
difference_green_band = b03_first_temporal - b03_last_temporal

# Download the result for visualization
result_green_band = difference_green_band.download()
```

Now we will visualize the difference in the green band using "RdBu" colormap.

### Step 10

```python

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
```

![Example output](assets/difference-analysis/10-0.png)

This difference plot shows the changes in reflectance values between two time points for the green band. Let’s break it down:

*Color Scheme (RdBu colormap)*:

- Red/Maroon Areas: These indicate negative values in the difference, meaning that the reflectance in the green band has decreased between the two time points.
- Blue Areas: These represent positive values in the difference, meaning that the reflectance in the green band has increased between the two time points.
- White Areas (around zero): These areas have little to no change in reflectance, indicating stability between the two time points.


*Spatial Patterns*:

- The large dark red regions are areas where the green reflectance has substantially decreased. This could be due to factors like vegetation loss, drying out.

- Areas in blue, where the reflectance has increased, might indicate vegetation growth, increased moisture, or any other factor that boosts green reflectance.

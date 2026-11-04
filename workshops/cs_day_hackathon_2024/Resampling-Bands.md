[Documentation home](../../README.md) · [Download Python script](Resampling-Bands.py)

Run from this directory with `python Resampling-Bands.py`. Read the guide first: the script runs all steps in order and may submit remote jobs. Figures and maps are saved under `outputs/Resampling-Bands/`.

> Historical workshop material. Examples may require additional services, credentials or repairs; they are preserved for reference.

> Saved outputs below come from the original teaching material; they are illustrations, not a fresh run against the current service.

## Resampling Sentinel-2 Bands with Different Resolutions Using OpenEO
### Introduction

In geospatial analysis, working with multi-band data from satellite imagery often involves dealing with bands of varying resolutions. This is particularly true for Sentinel-2 data, where different bands have different spatial resolutions. To combine these bands into a single data cube for analysis, we must first resample them to a common resolution. In this tutorial, we will demonstrate how to load two Sentinel-2 bands with different resolutions, resample one of the bands, and create a data cube using the OpenEO Python client.

### Step 2

```python
from config import eo_service_url,user,passwd
from demo_regions import  s2
```

### Sentinel-2 MSI bands are available in different pixel resolutions.

[![Datacube Timeseries](https://content.satimagingcorp.com/media2/filer_public_thumbnails/filer_public/44/9c/449caa01-64b9-417f-9547-964b66465554/cms_page_media1530image001.png__525.0x426.0_q85_subsampling-2.jpg)

If we want to work with red band (b04) and Short Wave Infra Red (b11) in the same datacube we need to resamble them to be the same resolation.



## A. Loading Sentinel-2 Bands (b04 and b11)

We start by connecting to the OpenEO backend and loading two Sentinel-2 bands: one with 10m resolution (e.g., B04) and another with 20m resolution (e.g., B11).

### Step 5

```python
import openeo
import xarray as xr
import matplotlib.pyplot as plt

# Connect to DES OpenEO backend
connection = openeo.connect(eo_service_url)
connection.authenticate_basic(username=user, password=passwd)

# Define the collection and bands to load
collection = s2.s2_msi_l2a
band_10m = "b04"  # Red band, 10m resolution
band_20m = "b11"  # SWIR band, 20m resolution

# Define a bounding box for the area of interest
bbox = {
          "west": 13.460930954751282,
          "east": 13.585449709728213,
          "south": 59.36327761288911,
          "north": 59.40107161575003
        }
timespan=["2024-06-12", "2024-06-13"]
# Load the data for both bands
datacube_10m = connection.load_collection(collection, bands=[band_10m], temporal_extent=timespan, spatial_extent=bbox)
datacube_20m = connection.load_collection(collection, bands=[band_20m], temporal_extent=timespan, spatial_extent=bbox)
```

Note that the above code only creates the process trees to send to the back-end. Nothing has been fetched yet.
## B. Resampling the 10m Band to 20m Resolution

Since the datacubes must have the same resolution, we need to resample the 10m band to match the 20m resolution of the other band

### Step 7

```python
# Resample the 20m datacube to 10m resolution
resampled_10m = datacube_10m.resample_cube_spatial(target=datacube_20m, method='bilinear')
```

### Interpolation Methods:

- **Nearest Neighbor** (`near`): Fastest but may result in blocky artifacts.
- **Bilinear** (`bilinear`): A good balance between performance and smoothing.
- **Cubic** (`cubic`): Produces smoother results but is computationally more expensive.
- **Cubic Spline** (`cubicspline`): Very smooth, suitable for continuous data; more computationally intensive.
- **Lanczos** (`lanczos`): Sharp, high-quality interpolation; more computationally expensive, good for resampling imagery.
- **Average** (`average`): Useful for downsampling; averages the values in the neighborhood.
- **Mode** (`mode`): Picks the most frequent value in the neighborhood; useful for categorical data.
- **Maximum** (`max`): Selects the maximum value in the neighborhood.
- **Minimum** (`min`): Selects the minimum value in the neighborhood.
- **Median** (`med`): Selects the median value in the neighborhood.
- **First Quartile** (`q1`): Selects the first quartile value in the neighborhood.
- **Third Quartile** (`q3`): Selects the third quartile value in the neighborhood.


You can choose any of these methods depending on your needs.

## C. Creating a Multi-band Data Cube

Now that both bands have the same resolution, we can combine them into a single data cube.

### Step 10

```python
# Merge the datacubes into a single multi-band cube
multi_band_cube = datacube_20m.merge_cubes(resampled_10m)

display(
multi_band_cube
)
```

[View saved example output](assets/Resampling-Bands/10-0.html)

### Step 11

```python
# This is typically a too big job for execute or download
job = multi_band_cube.create_job(out_format='GTiff',title="Combine bands of different resolution")
```

### Step 12

```python
display(
display(job)
)
```

[View saved example output](assets/Resampling-Bands/12-0.html)

### Step 13

```python
display(
job.start_and_wait()
)
```

```text
0:00:00 Job '63b00281-b7d1-457b-ab68-8fab005dbc10': send 'start'
0:00:00 Job '63b00281-b7d1-457b-ab68-8fab005dbc10': queued (progress 0.0%)
0:00:05 Job '63b00281-b7d1-457b-ab68-8fab005dbc10': running (progress 0.0%)
0:00:11 Job '63b00281-b7d1-457b-ab68-8fab005dbc10': finished (progress 0.0%)
```

[View saved example output](assets/Resampling-Bands/13-1.html)

### Step 14

```python
display(
job.get_results()
)
```

[View saved example output](assets/Resampling-Bands/14-0.html)

### Step 15

```python
results = job.get_results()
```

### Step 16

```python
path = list(filter(None,[str(p) if str(p).endswith(".tif") else None for p in results.download_files()]))
```

### Step 17

```python
from demo_helpers import show_result

with open(path[0], mode='rb') as file: # b is important -> binary
    fileContent = file.read()
display(
show_result(fileContent, "Reds")
)
```

![Example output](assets/Resampling-Bands/17-0.png)

![Example output](assets/Resampling-Bands/17-1.png)

```text
array([[[[2263.  , 2370.  , 2437.  , ..., 2016.  , 2224.  , 2729.  ],
         [2297.  , 2410.  , 2537.  , ..., 2013.  , 2416.  , 3036.  ],
         [2322.  , 2432.  , 2510.  , ..., 2165.  , 2135.  , 2086.  ],
         ...,
         [1105.  , 1409.  , 2329.  , ..., 1019.  , 1033.  , 1028.  ],
         [1110.  , 1314.  , 2208.  , ..., 1017.  , 1030.  , 1036.  ],
         [1103.  , 1295.  , 2124.  , ..., 1019.  , 1028.  , 1033.  ]],

        [[1276.  , 1313.5 , 1321.5 , ..., 1140.5 , 1168.5 , 1349.  ],
         [1262.5 , 1340.5 , 1379.5 , ..., 1159.5 , 1207.25, 1303.25],
         [1279.5 , 1329.  , 1358.25, ..., 1162.75, 1193.5 , 1124.  ],
         ...,
         [1071.  , 1079.75, 1253.25, ..., 1093.25, 1096.25, 1086.5 ],
         [1071.  , 1074.5 , 1213.  , ..., 1077.25, 1090.25, 1095.5 ],
         [1078.  , 1076.5 , 1186.25, ..., 1078.25, 1087.25, 1093.25]]]])
```

We can create jobs to download files in different formats. If you are working with multiple dates you might prefer loading them all into a single dataset using the NetCDF file format.

### Step 19

```python
job = multi_band_cube.create_job(out_format='netcdf',title="Combine bands of different resolution")
job.start_and_wait()
results = job.get_results()
display(
results.download_files()
)
```

```text
0:00:00 Job '8ab98d99-7fe0-4578-b834-5d1a2eff374e': send 'start'
0:00:00 Job '8ab98d99-7fe0-4578-b834-5d1a2eff374e': queued (progress 0.0%)
0:00:05 Job '8ab98d99-7fe0-4578-b834-5d1a2eff374e': running (progress 0.0%)
0:00:11 Job '8ab98d99-7fe0-4578-b834-5d1a2eff374e': finished (progress 0.0%)
```

```text
[PosixPath('/Users/jesperdejby/code/digital-earth-sweden-community/workshops/cs_day_hackathon_2024/process.json'),
 PosixPath('/Users/jesperdejby/code/digital-earth-sweden-community/workshops/cs_day_hackathon_2024/summary.nc'),
 PosixPath('/Users/jesperdejby/code/digital-earth-sweden-community/workshops/cs_day_hackathon_2024/stac.json'),
 PosixPath('/Users/jesperdejby/code/digital-earth-sweden-community/workshops/cs_day_hackathon_2024/py_proc_std_out.txt'),
 PosixPath('/Users/jesperdejby/code/digital-earth-sweden-community/workshops/cs_day_hackathon_2024/8ab98d99-7fe0-4578-b834-5d1a2eff374e.txt'),
 PosixPath('/Users/jesperdejby/code/digital-earth-sweden-community/workshops/cs_day_hackathon_2024/py_proc_std_err.txt'),
 PosixPath('/Users/jesperdejby/code/digital-earth-sweden-community/workshops/cs_day_hackathon_2024/job-results.json')]
```

We can open the dataset with the xarray python package

### Step 21

```python
ds = xr.open_dataset("summary.nc")
display(
ds
)
```

[View saved example output](assets/Resampling-Bands/21-0.html)

## Conclusion

In this guide, we've demonstrated how to load Sentinel-2 bands with different resolutions, resample one band to match the resolution of the other, and combine them into a single data cube using the OpenEO Python client. The choice of interpolation method for resampling can affect the results, so it's important to consider the trade-offs between speed and accuracy.
Next Steps

You can extend this workflow by applying further analyses to the multi-band data cube, such as computing vegetation indices or classifying land cover types.

### Step 23

```python
display(
job.delete()
)
```

[Documentation home](../README.md) · [Download Python script](property-filtering.py)

Run from this directory with `python property-filtering.py`. Read the guide first: the script runs all steps in order and may submit remote jobs. Figures and maps are saved under `outputs/property-filtering/`.

> Saved outputs below come from the original teaching material; they are illustrations, not a fresh run against the current service.

# Introduction

In satellite data processing, filtering based on specific properties can be used for refining datasets to meet particular analysis requirements. Whether you're interested in filtering data by cloud cover, spatial extent, or temporal range, understanding how to apply these filters effectively within the `load_collection` process is crucial.

This guide demonstrates examples of applying property filtering using the OpenEO API. By leveraging property filters, you can fine-tune the data you work with, ensuring that only the most relevant datasets are used in your analysis.

# Objective

The objective of this tutorial is to show how to apply property filtering in the `load_collection` process using the OpenEO API. We will cover various property filters, including numerical ranges and conditional statements, allowing for precise control over the data retrieval process.

In this guide, you will explore the following concepts:

1. **Understanding Property Filters**: Learn about the different properties available for filtering satellite data, such as cloud cover, spatial extent, and temporal range.
2. **Applying Simple Filters**: Use basic filtering techniques to narrow down datasets based on specific property criteria.
3. **Combining Filters for Complex Queries**: Combine multiple filters to create complex queries that refine datasets based on a combination of conditions.

# Let's Begin

We'll start by importing the necessary Python modules and establishing a connection to the OpenEO backend. Then, we'll proceed with applying property filters to fetch and analyze the relevant satellite imagery data.

 

### Step 2

```python
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
```

### Step 3

```python
conn = openeo.connect(eo_service_url)
display(
conn.authenticate_basic(username= user, password=passwd)
)
```

```text
<Connection to 'https://openeo.digitalearth.se/' with BasicBearerAuth>
```

### Understanding Property Filtering in Satellite Data Processing

When working with satellite data, it's essential to understand that the data is divided both spatially and temporally. The data is segmented into **granules** (which may be, for example, 100km a side depending on the collection), each covering specific portions of the Earth's surface. Additionally, each granule is associated with specific acquisition times, as satellites capture data in discrete passes.

For example, when analyzing an area in Sweden, your area of interest (AOI) may intersect multiple granules, each captured at different times and under varying conditions such as cloud cover. These granules have their own set of properties, including spatial attributes like `cloud_cover` and temporal attributes like `datetime`.

#### How Property and Temporal Filtering Works

When you specify a time range (e.g., "2020-07-01T00:00:00Z" to "2023-07-31T00:00:00Z"), OpenEO will consider only granules that overlap with your area of interest and fall within your specified temporal range.

After spatial and temporal filtering, OpenEO further evaluates each remaining granule against your property filters, such as `cloud_cover < 20%`. If, for example, your AOI intersects three granules within the time range, but only two meet the cloud cover criteria, only those two granules will be used in the data returned.

#### Example Scenario

Suppose you want to analyze vegetation in an area over the summer months from 2020 to 2023 with minimal cloud interference. You might set a temporal filter for June through August of each year and a cloud cover filter of less than 20%. OpenEO will:

1. **Select Granules**: Identify all granules that cover your AOI and were captured within your specified summer months.
2. **Apply Cloud Cover Filter**: Further filter these granules to include only those with less than 20% cloud cover.
3. **Stitch Data**: Combine the relevant parts of granules that match both the time and spatial criteria to "cover" the area of interest with data.
4. **Return Data**: Provide the final dataset, which includes only the portions of your AOI covered by the granules that met both the temporal and property filter criteria.

### Granule Properties

Here’s an overview of some typical properties associated with granules:

#### Property Set 1

| Property           | Value                                                                                     |
|--------------------|-------------------------------------------------------------------------------------------|
| **eo:gsd**         | `300`                                                                                     |
| **datetime**       | `None`                                                                                    |
| **proj:epsg**      | `4326`                                                                                    |
| **proj:shape**     | `[3113, 6098]`                                                                            |
| **eo:platform**    | `sentinel-3b`                                                                             |
| **odc:product**    | `s3_olci_l2wfr`                                                                           |
| **eo:instrument**  | `OLCI`                                                                                    |
| **eo:cloud_cover** | `45.0`                                                                                    |
| **proj:transform** | `[0.004184338346988613, 0.0, 16.480945, 0.0, -0.004184338346988613, 62.92023, 0.0, 0.0, 1.0]` |
| **cube:dimensions**| `{}`                                                                                      |
| **odc:file_format**| `geotiff`                                                                                 |

#### Property Set 2

| Property           | Value                                                                                                                 |
|--------------------|-----------------------------------------------------------------------------------------------------------------------|
| **creation_time**  | `None`                                                                                                                |
| **format**         | `geotiff`                                                                                                             |
| **label**          | `s3_ol2wfr_01_20210429_76534e20`                                                                                      |
| **lat**            | `Range(begin=49.8942, end=62.9202)`                                                                                    |
| **lon**            | `Range(begin=16.4813, end=41.9973)`                                                                                    |
| **time**           | `Range(begin=datetime.datetime(2021, 4, 29, 8, 38, 20, 983503, tzinfo=tzutc()), end=datetime.datetime(2021, 4, 29, 8, 41, 20, 983503, tzinfo=tzutc()))` |
| **platform**       | `sentinel-3b`                                                                                                         |
| **instrument**     | `OLCI`                                                                                                                |
| **cloud_cover**    | `45.0`                                                                                                                |
| **region_code**    | `None`                                                                                                                |
| **product_family** | `level2`                                                                                                              |
| **dataset_maturity** | `None`                                                                                                              |

Especially note that `cloud_cover` occurs in both sets which we will make use of later when making a composite filter. 

By understanding how spatial and temporal filtering works together, you can better tailor your queries to get the most accurate and useful satellite data for your specific needs.


### Exploring a Small Dummy Area with Sentinel-2 Data

In this example, we'll focus on a very small area (approximately 10x10 pixels at 10m resolution) within Sweden. This area is deliberately small, so the number of resulting files should be manageable even if we receive multiple data granules.  Since we're not applying a strict filter on cloud cover or other properties (using a relatively high threshold for cloud cover), we'll likely retrieve all available granules that match our spatial and temporal extent. Since there is a limit how many files you can download by default, we can safely increase that limit since each image will be very small. This is done with the `max_files` parameter in the `download` function. It specifies the maximum number of files to download. By setting `max_files` to 30, we're ensuring that we can get enough files to see the difference when applying the property filter and we do not risk that the number of files becomes overwhelming, even if many granules match our criteria.

Now, let's execute the code to load and download the data:

### Step 6

```python

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
```

```text
FrozenMappingWarningOnValuesAccess({'t': 17, 'y': 6, 'x': 6})
```

### Understanding `data.dims`

After loading the NetCDF data into an xarray object, the `data.dims` command provides a summary of the dataset's dimensions. This output gives you an overview of the different dimensions in your data, such as time (`t`), latitude (`y`), and longitude (`x`).

For example, if `data.dims` shows `t: 17, y: 10, x: 10`, this indicates that:

- **`t: 17`**: There are 17 time steps in the dataset. This means that the data cube contains information for 12 different times (or dates), which were retrieved by stitching together the available granules that met the specified spatial, temporal, and property criteria.
- **`y: 10` and `x: 10`**: The dataset covers a 10x10 pixel area, corresponding to the small geographic area you specified.

### Next Steps: Filtering Out Time Steps with High Cloud Cover

Now that we've confirmed our dataset contains 12 time steps, the next logical step is to filter out the time steps with higher cloud cover. 

- **Objective**: We want to focus on the time steps where the cloud cover is minimal to ensure that the data is as clear and useful as possible for further analysis.
- **Approach**: We'll apply an additional filter to select only those time steps where the cloud cover falls below a certain threshold, allowing us to work with the clearest imagery available.

In the following cell, we will apply this filtering to refine our dataset further.


### Step 8

```python
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
```

```text
FrozenMappingWarningOnValuesAccess({'t': 12, 'y': 6, 'x': 6})
```

As you can see the number of retrieved images (one per time step) has shrunk from 17 to 12. 
You can speciy more than one property filter, each property can only occur once due to how python handles dictionaries. Each property corresponds to a key in the dict, if we specify the same property more than once, the latest will be silently picked. 

However there is a nifty hack we can use when properties occur in both sets as described above. The property `cloud_coverage` is such a property. 
### Composed and Complex Filters
By stacking property filters we effectively create an `and` expression.

Let´s see how we can use this to retrieve images with a cloud coverage between, say, 60 and 70:

### Step 10

```python
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
```

```text
FrozenMappingWarningOnValuesAccess({'t': 1, 'y': 6, 'x': 6})
```

The Granules usually have more properties than the OpenEO client is aware about, hence the warning. You can find properties and try them out here: https://explorer.digitalearth.se/stac/collections/s2_msi_l2a/items/00e9106a-45de-5fd5-a403-bcbee7af6a4d. In upcoming execises we will take a closer look on how to select areas by specifying different geometries such as bounding boxes and polygons!

As you can see the number of images retrieved has shrunk even more!

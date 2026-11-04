[Documentation home](../README.md) · [Download Python script](050_PROC_030-Batch-Processing.py)

Run from this directory with `python 050_PROC_030-Batch-Processing.py`. Read the guide first: the script runs all steps in order and may submit remote jobs. Figures and maps are saved under `outputs/050_PROC_030-Batch-Processing/`.

> Saved outputs below come from the original teaching material; they are illustrations, not a fresh run against the current service.

## Batch Processing in openEO

### Introduction

In many geospatial analysis tasks, you need flexibility in how data is processed, especially when working with large datasets. While OpenEO lets you process data on powerful backend servers, you have options for how and when to retrieve the results. OpenEO supports both synchronous and asynchronous execution, allowing you to choose between running processes interactively or submitting them as batch jobs to the backend.

- **Synchronous Execution**: With synchronous commands like `execute` or `download`, OpenEO performs the computation on the backend, and you wait until the result is ready to use. While this approach is effective for smaller tasks, it requires your session to remain active until completion.

- **Batch Jobs (Asynchronous Execution)**: OpenEO also allows you to submit processes as asynchronous jobs. The same process graph you would use for interactive execution can be sent to the backend as a *job*. Once submitted, you can choose to wait for completion or disconnect and check back later. You can even configure the job to notify you by email when processing finishes, providing flexibility for tasks that require significant time or resources.

### Why Batch Processing?

Batch processing is advantageous for larger, more complex calculations where waiting is impractical. By sending a job to the backend, you allow the process to run independently of your active session, freeing you up for other tasks. Additionally, OpenEO makes it easy to rerun jobs without recreating the process graph, supporting reproducibility and analysis consistency. With batch processing, OpenEO also enables on-demand web services, allowing you to trigger computations through HTTP requests that return the result when completed.

### Objective

This tutorial will guide you through the differences between synchronous and asynchronous processing in OpenEO, highlighting the strengths of batch processing for large-scale analysis. We’ll demonstrate how to submit a process graph as a job and monitor its status, showing how OpenEO simplifies long-running computations.

### In this guide, you will explore the following concepts:

- **Synchronous vs. Asynchronous Execution**: Learn the differences between using `execute`/`download` and submitting batch jobs.
- **Job Management**: Understand how to submit, monitor, and retrieve results from a batch job, allowing you to optimize workflows for long-running tasks.
- **Web Services for Batch Jobs**: Explore how OpenEO supports web services, enabling you to request processing via HTTP, making results accessible with flexible parameters. <span style="color: goldenrod;">(FUTURE FEATURE)</span>

### Tools You'll Use:

- **openEO**: To build process graphs, execute them synchronously, or submit them as asynchronous jobs.
- **Backend Notifications**: Optionally configure email alerts for completed jobs.

### Learning Outcomes

By the end of this tutorial, you will be able to:

- Choose between synchronous and asynchronous execution in OpenEO.
- Submit and monitor batch jobs, retrieving results only when ready.
- Set up web services for automated result retrieval based on your process graph. <span style="color: goldenrod;">(FUTURE FEATURE)</span>

Using OpenEO’s batch processing capabilities, you can tackle complex analyses without being tied to your session, allowing you to efficiently utilize backend resources.


## Theory Behind Batch Processing in openEO

### Synchronous Execution: Immediate Results for Prototyping

OpenEO provides two main methods for synchronous execution: `execute` and `download`. Both options run your process on backend servers, handling all computation remotely, but they differ in how they return results:

- **`execute`**:
  - Runs the process graph and returns only the metadata or a lightweight summary, without transferring large data. This method is ideal for validating your process or checking structure without downloading extensive datasets.
  
- **`download`**:
  - Runs the full process and transfers the resulting dataset to your local environment, useful when you need the complete output for further local analysis or visualization.

With synchronous execution, you can test on smaller areas or shorter time spans, which is effective for interactive prototyping and intermediate validation.

### Asynchronous Execution: Submitting Production Jobs

Once your process graph is fully refined, OpenEO allows you to switch to asynchronous batch processing for a comprehensive run. Submitting the process graph as a batch job provides several benefits:

1. **Production-Ready Output**:
   - When you submit the job, OpenEO’s backend can process the entire time span or larger areas, efficiently producing your final output without needing you to stay connected.

2. **Job Management & Notifications**:
   - You can request notifications (e.g., by email) when the job completes, so you don’t need to monitor it directly.

3. **Reusability**:
   - Completed jobs can be rerun as needed. This is efficient for recalculating results with similar or updated data.

4. **On-Demand Services**:
   - OpenEO supports converting your job into a web service, allowing requests with parameters like time ranges or regions directly via HTTPS, ideal for automated and on-demand analysis.

### Efficient Workflow: From Prototype to Production

Using OpenEO, you can build your analysis step-by-step in a guide, experimenting with intermediate outputs on smaller data. When ready, submitting a job for full-scale analysis allows OpenEO to handle the heavy processing. This prototyping-to-production approach lets you efficiently progress from concept to final result with confidence in each stage of development.


### Step 3

```python
import openeo
from config import user,passwd,eo_service_url
from demo_helpers import show_result
from demo_regions import s2
# a. connect to the openeo back-end
conn = openeo.connect(eo_service_url)
display(
conn.authenticate_basic(username= user, password=passwd)
)
```

```text
<Connection to 'https://openeo.digitalearth.se/' with BasicBearerAuth>
```

## Revisiting Syncronous Execution
Let's revisit the NDVI processing we did in a previous exercise. As you remember, 
we created a process that loaded a collection and applied the pre-baked NDVI process 
to it and then  we used the syncronous `download` alternative to perform the actual execution in our back-end and then downloaded and showed the result. 
We will now first run this process as before to see what to expect when we submit the same process as batch job:

### Step 5

```python
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
```

![Example output](assets/050_PROC_030-Batch-Processing/5-0.png)

[View saved example output](assets/050_PROC_030-Batch-Processing/5-1.html)

## Creating and Submitting the NDVI Process as a Batch Job

Instead of running the NDVI process synchronously, we can create a batch job that submits the process to the backend, allowing us to handle larger or longer-running tasks asynchronously. Here, we'll use `ndvi.create_job()` to create the job, then start it and wait for completion. Firstly, we will start the job and wait for completion. This is actually no difference to the previous syncronous executions, but you are allowed to execute larger jobs this way.


### Step 7

```python
# Creating a batch job for the NDVI process defined in previous step
job = ndvi.create_job(out_format="GTiff", title="NDVI Batch Job", description="Calculating NDVI for selected area")

display(
job
)
```

[View saved example output](assets/050_PROC_030-Batch-Processing/7-0.html)

### Step 8

```python
display(
job.start_and_wait()
)
```

```text
0:00:00 Job 'b31b7b5d-b5b0-4a09-930e-acee996f49db': send 'start'
0:00:00 Job 'b31b7b5d-b5b0-4a09-930e-acee996f49db': queued (progress 0.0%)
0:00:05 Job 'b31b7b5d-b5b0-4a09-930e-acee996f49db': running (progress 0.0%)
0:00:11 Job 'b31b7b5d-b5b0-4a09-930e-acee996f49db': running (progress 0.0%)
0:00:19 Job 'b31b7b5d-b5b0-4a09-930e-acee996f49db': finished (progress 0.0%)
```

[View saved example output](assets/050_PROC_030-Batch-Processing/8-1.html)

### Step 9

```python
# Examining the results
res = job.get_results()
display(
res
)
```

[View saved example output](assets/050_PROC_030-Batch-Processing/9-0.html)

### Step 10

```python
display(
job.logs()
)
```

[View saved example output](assets/050_PROC_030-Batch-Processing/10-0.html)

### Step 11

```python
# We can even run the job again
job.start_and_wait()
display(
job.logs()
)
```

```text
0:00:00 Job 'b31b7b5d-b5b0-4a09-930e-acee996f49db': send 'start'
0:00:00 Job 'b31b7b5d-b5b0-4a09-930e-acee996f49db': queued (progress 0.0%)
0:00:05 Job 'b31b7b5d-b5b0-4a09-930e-acee996f49db': running (progress 0.0%)
0:00:11 Job 'b31b7b5d-b5b0-4a09-930e-acee996f49db': running (progress 0.0%)
0:00:19 Job 'b31b7b5d-b5b0-4a09-930e-acee996f49db': finished (progress 0.0%)
```

[View saved example output](assets/050_PROC_030-Batch-Processing/11-1.html)

# Working with the results
Either you click on above links or you can use `get_assets()` to do this programatically

### Step 13

```python
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
```

```text
[<ResultAsset 'process.json' (type application/json) at 'https://s3.rise.safedc.net/userdata/testuser_0/jobs/b31b7b5d-b5b0-4a09-930e-acee996f49db/process.json?AWSAccessKeyId=404f289445e14c4096da2a011c9a94ba&Signature=ymUDWyiEl7oSLePjqrr5VnOfv0A%3D&Expires=1729240281'>,
 <ResultAsset 'out_2021_11_12T10_22_51.tif' (type image/tiff; application=geotiff) at 'https://s3.rise.safedc.net/userdata/testuser_0/jobs/b31b7b5d-b5b0-4a09-930e-acee996f49db/out_2021_11_12T10_22_51.tif?AWSAccessKeyId=404f289445e14c4096da2a011c9a94ba&Signature=YR4k8XlrOVB6R1xv%2F%2BB8Mu3mfm4%3D&Expires=1729240281'>,
 <ResultAsset 'stac.json' (type application/json) at 'https://s3.rise.safedc.net/userdata/testuser_0/jobs/b31b7b5d-b5b0-4a09-930e-acee996f49db/stac.json?AWSAccessKeyId=404f289445e14c4096da2a011c9a94ba&Signature=S2n8CFBklSBY80ZgBBTxCPyDk1A%3D&Expires=1729240281'>,
 <ResultAsset 'py_proc_std_out.txt' (type application/yml) at 'https://s3.rise.safedc.net/userdata/testuser_0/jobs/b31b7b5d-b5b0-4a09-930e-acee996f49db/py_proc_std_out.txt?AWSAccessKeyId=404f289445e14c4096da2a011c9a94ba&Signature=2m8UzK0CdODuoC0RT5HHVELOvGc%3D&Expires=1729240281'>,
 <ResultAsset 'py_proc_std_err.txt' (type application/yml) at 'https://s3.rise.safedc.net/userdata/testuser_0/jobs/b31b7b5d-b5b0-4a09-930e-acee996f49db/py_proc_std_err.txt?AWSAccessKeyId=404f289445e14c4096da2a011c9a94ba&Signature=I6Vuci4D6w%2F3xrpJhHTR3OMRWvk%3D&Expires=1729240281'>,
 <ResultAsset 'b31b7b5d-b5b0-4a09-930e-acee996f49db.txt' (type application/yml) at 'https://s3.rise.safedc.net/userdata/testuser_0/jobs/b31b7b5d-b5b0-4a09-930e-acee996f49db/b31b7b5d-b5b0-4a09-930e-acee996f49db.txt?AWSAccessKeyId=404f289445e14c4096da2a011c9a94ba&Signature=%2Bg5xl3Wo5R9dXQakBx1vdZ7kCDY%3D&Expires=1729240281'>]
```

```text

NAME:     process.json
HREF:     https://s3.rise.safedc.net/userdata/testuser_0/jobs/b31b7b5d-b5b0-4a09-930e-acee996f49db/process.json?AWSAccessKeyId=404f289445e14c4096da2a011c9a94ba&Signature=ymUDWyiEl7oSLePjqrr5VnOfv0A%3D&Expires=1729240281
METADATA: {'type': 'application/json', 'title': 'process.json', 'roles': ['process', 'reproduction'], 'href': 'https://s3.rise.safedc.net/userdata/testuser_0/jobs/b31b7b5d-b5b0-4a09-930e-acee996f49db/process.json?AWSAccessKeyId=404f289445e14c4096da2a011c9a94ba&Signature=ymUDWyiEl7oSLePjqrr5VnOfv0A%3D&Expires=1729240281'}

NAME:     out_2021_11_12T10_22_51.tif
HREF:     https://s3.rise.safedc.net/userdata/testuser_0/jobs/b31b7b5d-b5b0-4a09-930e-acee996f49db/out_2021_11_12T10_22_51.tif?AWSAccessKeyId=404f289445e14c4096da2a011c9a94ba&Signature=YR4k8XlrOVB6R1xv%2F%2BB8Mu3mfm4%3D&Expires=1729240281
METADATA: {'type': 'image/tiff; application=geotiff', 'roles': ['data'], 'href': 'https://s3.rise.safedc.net/userdata/testuser_0/jobs/b31b7b5d-b5b0-4a09-930e-acee996f49db/out_2021_11_12T10_22_51.tif?AWSAccessKeyId=404f289445e14c4096da2a011c9a94ba&Signature=YR4k8XlrOVB6R1xv%2F%2BB8Mu3mfm4%3D&Expires=1729240281', 'title': 'out_2021_11_12T10_22_51.tif'}

NAME:     stac.json
HREF:     https://s3.rise.safedc.net/userdata/testuser_0/jobs/b31b7b5d-b5b0-4a09-930e-acee996f49db/stac.json?AWSAccessKeyId=404f289445e14c4096da2a011c9a94ba&Signature=S2n8CFBklSBY80ZgBBTxCPyDk1A%3D&Expires=1729240281
METADATA: {'type': 'application/json', 'title': 'stac.json', 'roles': ['data'], 'href': 'https://s3.rise.safedc.net/userdata/testuser_0/jobs/b31b7b5d-b5b0-4a09-930e-acee996f49db/stac.json?AWSAccessKeyId=404f289445e14c4096da2a011c9a94ba&Signature=S2n8CFBklSBY80ZgBBTxCPyDk1A%3D&Expires=1729240281'}

NAME:     py_proc_std_out.txt
HREF:     https://s3.rise.safedc.net/userdata/testuser_0/jobs/b31b7b5d-b5b0-4a09-930e-acee996f49db/py_proc_std_out.txt?AWSAccessKeyId=404f289445e14c4096da2a011c9a94ba&Signature=2m8UzK0CdODuoC0RT5HHVELOvGc%3D&Expires=1729240281
METADATA: {'type': 'application/yml', 'title': 'py_proc_std_out.txt', 'description': 'Process output metadata', 'roles': ['metadata'], 'href': 'https://s3.rise.safedc.net/userdata/testuser_0/jobs/b31b7b5d-b5b0-4a09-930e-acee996f49db/py_proc_std_out.txt?AWSAccessKeyId=404f289445e14c4096da2a011c9a94ba&Signature=2m8UzK0CdODuoC0RT5HHVELOvGc%3D&Expires=1729240281'}

NAME:     py_proc_std_err.txt
HREF:     https://s3.rise.safedc.net/userdata/testuser_0/jobs/b31b7b5d-b5b0-4a09-930e-acee996f49db/py_proc_std_err.txt?AWSAccessKeyId=404f289445e14c4096da2a011c9a94ba&Signature=I6Vuci4D6w%2F3xrpJhHTR3OMRWvk%3D&Expires=1729240281
METADATA: {'type': 'application/yml', 'title': 'py_proc_std_err.txt', 'description': 'Process output metadata', 'roles': ['metadata'], 'href': 'https://s3.rise.safedc.net/userdata/testuser_0/jobs/b31b7b5d-b5b0-4a09-930e-acee996f49db/py_proc_std_err.txt?AWSAccessKeyId=404f289445e14c4096da2a011c9a94ba&Signature=I6Vuci4D6w%2F3xrpJhHTR3OMRWvk%3D&Expires=1729240281'}

NAME:     b31b7b5d-b5b0-4a09-930e-acee996f49db.txt
HREF:     https://s3.rise.safedc.net/userdata/testuser_0/jobs/b31b7b5d-b5b0-4a09-930e-acee996f49db/b31b7b5d-b5b0-4a09-930e-acee996f49db.txt?AWSAccessKeyId=404f289445e14c4096da2a011c9a94ba&Signature=%2Bg5xl3Wo5R9dXQakBx1vdZ7kCDY%3D&Expires=1729240281
METADATA: {'type': 'application/yml', 'title': 'b31b7b5d-b5b0-4a09-930e-acee996f49db.txt', 'description': 'Process output metadata', 'roles': ['metadata'], 'href': 'https://s3.rise.safedc.net/userdata/testuser_0/jobs/b31b7b5d-b5b0-4a09-930e-acee996f49db/b31b7b5d-b5b0-4a09-930e-acee996f49db.txt?AWSAccessKeyId=404f289445e14c4096da2a011c9a94ba&Signature=%2Bg5xl3Wo5R9dXQakBx1vdZ7kCDY%3D&Expires=1729240281'}
```

As you can see above, we loaded the image result into the variable `data`. Obviously, if we had more than one image in our response, `data`would be overwritten in the loop but i hope you get the message here. And as you can see below, we got the very same data as we got before


### Step 15

```python
display(
show_result(data,is_ndvi=True)
)
```

![Example output](assets/050_PROC_030-Batch-Processing/15-0.png)

```text
array([[[[ 0.77311725,  0.73948718,  0.72940156, ...,  0.74707642,
           0.76218097,  0.71576898],
         [ 0.74733919,  0.71052632,  0.75570272, ...,  0.73126192,
           0.72354049,  0.727161  ],
         [ 0.71952818,  0.71492371,  0.767718  , ...,  0.66020525,
           0.51933124,  0.53654485],
         ...,
         [-0.34591195, -0.32173913, -0.10859729, ..., -0.37463127,
          -0.36206897, -0.47619048],
         [-0.33816425, -0.36150235, -0.14468085, ..., -0.42089552,
          -0.4789272 , -0.39784946],
         [-0.22      , -0.20487805, -0.1416122 , ..., -0.29861111,
          -0.34328358, -0.38867925]]]])
```

# Looking into the stac.json

### Step 17

```python
import json
stac_file = [a for a in res.get_assets() if a.name == 'stac.json']
stac = json.loads(stac_file[0].load_bytes())
display(
stac['properties']['data_sources']
)
```

```text
[{'source_epsg': '32633',
  'tile': '33VVF',
  'label': 'S2_MSIL2A_01_33VVF_20211112_75FDCDFC',
  'src_prod': 'S2A_MSIL2A_20211112T102251_N0301_R065_T33VVF_20211112T105701.SAFE'},
 {'source_epsg': '32633',
  'tile': '33VVF',
  'label': 'S2A_MSIL2A_20211112T102251_N0500_R065_T33VVF_20221231T115046.SAFE.COG',
  'src_prod': 'S2A_MSIL2A_20211112T102251_N0500_R065_T33VVF_20221231T115046.SAFE'}]
```

Above is the datasets from open datacube (cumulative from all load_collection processes in your job)

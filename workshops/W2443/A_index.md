[Documentation home](../../README.md)

> Historical workshop material. Examples may require additional services, credentials or repairs; they are preserved for reference.

# Workshop Preparations
2024-10-21 daniel.flemstrom@ri.se , nuria.agues.paszkowsky@ri.se

The following is a workshop on OpenEO held 2024-10-23 with swedish authorities. This document summarizes a Q/A session during the workshop. We chose to publish it here since it may be useful for others having a workshop or just want to learn more


- Send a geometry and get back: A time series with averages, An image for visualization, Cloud-masked image, Shadow %,Cloud %, All band data, NDVI values

    - [OpenEO Processes: cloud_detection](https://processes.openeo.org/#cloud_detection) (Not implemented yet)
    - <p style="color:green">We gathered this in a guide (linked below): </p>

      --> [Stats etc ](./gathering_examples_workshop.md)

- Number of pixels with vegetation
    - <p style="color:green">Load SCL with a geometry and count the pixels</p>

    --> [SCL Mask](../../tutorials/masking-data.md) <br>
    --> [Geometry Area](../../tutorials/polygon-areas.md)

- Image with clouds, image without clouds
    - <p style="color:green">We plan to use filter_quality, filter fine_quality (See guide)</p>
    
        - [OpenEO Processes: load_stac](https://processes.openeo.org/#load_stac) (Not implemented yet)
        - [OpenEO Processes: load_uploaded_files](https://processes.openeo.org/#load_uploaded_files) (Not implemented yet)
        - [OpenEO Processes: load_url](https://processes.openeo.org/#load_url) (Not implemented yet)
        
    --> [filtering](./quality_filter_index_boxes.md)

- Performance testing
  - <span style="color:red">We are currently running on minimal hardware resources.</span><span style="color:green"> BUT discussing performance REQUIREMENTS is very interesting for us. E.g., NumberOfAnalyses x NumberOfApplications x TimeInterval. </span>
  
- Data from other agencies
  - <p style="color:green">In the OpenEO concept, it is possible to load files from external storage or uploaded data (needs to be implemented). Here is an example where we show SKS Histogram data, though from the client side</p>
  
    --> [SKS Histogram Service](./python_and_other_APIs.md)

- Interpolate directly in the images, apply kernels (calculation boxes)
  - <span style="color:red">We did not fully understand the interpolation.</span> <span style="color:green">Could this be something for kernels?</span>
  
    --> [Spatial Filtering](../../tutorials/spatial-filtering.md)
 
- Apply something known, e.g., done on the height model, to something else
    - <p style="color:green">We have a 10m height model for the Nordics that could be added as a product (and then query for a subset). However, we currently do not have a distribution license for it (Nordic DEM)</p>


 

-  Create a guide comparing median values in Level 1C and Level 2A for a series of polygons

    - <p style="color:red">Due to a "known" issue, spatial aggregate with median is currently not working, but we have a Jira card for it.</p>

-  Contrast-stretch data for common band combinations used at SKS (Swedish Forest Agency). As input, we use histogram information from the bands we want to apply and then apply a gamma function with a gamma value of 1.3 (in most cases). This stretch is then applied to all data regardless of when the image was taken, so it is not dynamically updated based on the image appearance.
   
    - **PASS** <p style="color:red">We need to dig deeper into this to provide a sensible answer.</p>

-  Compare old data (pre-2022) where ESA updated to baseline 5.0
   - Compare geometries with old data we have, and examine the SCL layer compared to previous versions.
   
    - <p style="color:green">When we have baseline as a property in the STAC files, we will be able to filter based on it, provided the old baseline is available to us. The OpenEO concept allows both uploading own data and loading images directly from external storage (still needs to be implemented).</p>
       
       --> [General Comparison](../../tutorials/difference-analysis.md)

-  How to make requests to select a specific date and only display pixels that match a criterion (e.g., pixel values greater than x)

   - <p style="color:green">Load the image, create a binary mask (all pixels > x), and apply the mask to the image.</p>
         
         - [OpenEO Processes: if](https://processes.openeo.org/#if) (Not implemented yet)
           
       --> [Masking Data](../../tutorials/masking-data.md)
    
-  Can we consume DES data with REST calls?

   - <p style="color:green">YES. OpenEO is a REST API, so this works perfectly for both input and output. However, it might be easier to use the client and set the debug flag to capture the REST requests between OpenEO API and the client.</p>  
   
       --> [OpenEO REST API](https://openeo.digitalearth.se/openapi.json)

-  How does STAC integration work in OpenEO for reading mosaics of granules from DES on a certain date?

   - <p style="color:green">NO, OpenEO takes a geometry (polygon/multipolygon), crops out a square, and then geometry. A time range is always specified, but you can choose the first or last image in that range.</p>

       --> [Check Understanding Property Filtering in Satellite Data Processing](../../tutorials/property-filtering.md)

-  Handling different bands where data has equal pixel size, e.g., band combinations with both 10m and 20m bands + SCL (which is 20m)

   - <span style="color:green">The conceptual solution is to load a data cube with the bands that have resolution 1, another with bands of resolution 2, interpolate one, and merge into a single cube. This is implemented but</span><span style="color:red">will come in the next OpenEO release (w2444):</span>
    
       --> [Working with Resolutions](./Resampling-Bands.md)

-  Does DES have something similar to the Swedish Forest Agency's database with information per 5km grid, storing histograms of pixels for each class in the SCL band?

   - <p style="color:green">We have started working on this. Below is a "work in progress" representation. <img src="https://lucid.app/publicSegments/view/137c8631-287b-41bd-b0f2-a1a67c6cbed9/image.png" alt="Quality Filtering" style="width:80%;">
     <br> We also have the following internal Python APIs:  
        <list><li><p style="color:green">SKS service</p></li>
        <li> <p style="color:green">our own variant (Quality index with histogram for sufficiently cloud-free index boxes)</p></li>
        <li><p style="color:green">index5km tiles</p></li>
        <li><p style="color:green">sentinel2 tiles</p></li>
  <p style="color:green">Typical function is (original) or request a geometry and get a list of overlapping tiles/geometries. Or just search by name.</p>
  
 <br> --> [Quality Filtering](./quality_filter_index_boxes.md)
 <br> --> [External APIs](./python_and_other_APIs.md)


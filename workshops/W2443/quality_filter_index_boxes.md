[Documentation home](../../README.md) · [Download Python script](quality_filter_index_boxes.py)

Run from this directory with `python quality_filter_index_boxes.py`. Read the guide first: the script runs all steps in order and may submit remote jobs. Figures and maps are saved under `outputs/quality_filter_index_boxes/`.

> Historical workshop material. Examples may require additional services, credentials or repairs; they are preserved for reference.

> Saved outputs below come from the original teaching material; they are illustrations, not a fresh run against the current service.

# Cloud FREE images
2024-10-22 daniel.flemstrom@ri.se 

## Cloud free images using course and fine filtering
<span style="color:red">Note that this under construction and is expected to be released during spring 2025</span>

### Step 3

```python
from config import eo_service_url,user,passwd
from demo_regions import s2
import openeo
conn = openeo.connect(eo_service_url)
conn.authenticate_basic(username=user, password=passwd)
#conn.authenticate_oidc()
cube = conn.load_collection(
    s2.s2_msi_l2a,
    bands=["b01"],
    spatial_extent=s2.bbox.karlstad_mini_land,
    temporal_extent=["2020-03-01", "2020-08-01"]
)
args_course = {'data':cube,'filter':'sentinel2-scl-quality-coarse','threshold':0.8}

coarsely_filtered_cube = cube.process(process_id='filter_quality', arguments=args_course)

args_fine = {'data':coarsely_filtered_cube,'filter':'sentinel2-scl-quality-fine','threshold':0.99}
good_data_cube = coarsely_filtered_cube.process(process_id='filter_quality', arguments=args_fine)

# Tail a dummy process just to show how the process flow continues
ndvi_cube = good_data_cube.ndvi()
display(
display(ndvi_cube)
)
 
```

[View saved example output](assets/quality_filter_index_boxes/3-0.html)

The above is not yet executing in the platform but shows how it is conceptually intended to work.  
![Quality Filters](./images/q_filter.png)

- `<courier> sentinel2-scl-quality-**coarse** </courier>` checks the grid cells that the geometry overlaps.
- `<courier> sentinel2-scl-quality-**fine** </courier>` checks individual pixels within the clipped geometry.

The quality is classified the same way in the grid cells and inside the geometry, following the pattern below:

<img src="./images/q_classing.png" alt="Filter Criteria" style="width:30%;">


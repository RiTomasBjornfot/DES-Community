# Migration notes

The teaching material in this repository now uses Markdown and ordinary Python scripts. Markdown and Python are now the editable sources; no conversion tool is needed by readers or maintainers.

The original language and order are retained. Interactive display calls now print results, save Folium maps as HTML, or save Matplotlib figures as PNG. Automatic plotting hooks are provided by the ordinary Python module `example_output.py`.

Existing unsupported operations and commented-out exercises remain as documented. Workshop scripts are historical references and are not certified to run end to end. Original saved HTML may contain old links or embedded JavaScript and is supplementary, not required to run the scripts.

The former kernel-based test harness has been replaced by standard-library offline checks and opt-in integration tests that execute the same selected tutorials as Python scripts. CI runs the offline checks on every change; manual workflow dispatch can also run the DES integration tests. Container image publishing has been removed. Markdown can be read directly on GitHub; a publishing theme can be added separately.

## Content inventory

| Original guide | Code steps | Saved outputs |
|---|---:|---:|
| moocs/from_satellite_data_to_insights/session1_welcome_to_des | 6 | 5 |
| moocs/from_satellite_data_to_insights/session2_loading_and_visualizing | 10 | 8 |
| moocs/from_satellite_data_to_insights/session3_band_arithmetic_ndvi | 5 | 5 |
| moocs/from_satellite_data_to_insights/session4_temporal_reduction | 6 | 6 |
| moocs/from_satellite_data_to_insights/session5_cloud_masking_compositing | 7 | 7 |
| moocs/from_satellite_data_to_insights/session6_urban_green_mapping | 12 | 11 |
| tutorials/terms-and-conditions | 0 | 0 |
| tutorials/system-overview | 0 | 0 |
| tutorials/user-accounts | 0 | 0 |
| tutorials/tutorial-overview | 0 | 0 |
| tutorials/loading-data | 9 | 9 |
| tutorials/property-filtering | 5 | 4 |
| tutorials/bounding-box | 4 | 4 |
| tutorials/polygons | 10 | 17 |
| tutorials/polygon-areas | 4 | 4 |
| tutorials/rgb | 10 | 5 |
| tutorials/images-on-base-map | 9 | 5 |
| tutorials/difference-analysis | 6 | 3 |
| tutorials/processes | 3 | 3 |
| tutorials/operators | 8 | 11 |
| tutorials/batch-processing | 10 | 15 |
| tutorials/masking-data | 10 | 13 |
| tutorials/reductions | 13 | 20 |
| tutorials/spatial-filtering | 6 | 5 |
| tutorials/further-reading | 0 | 0 |
| workshops/W2443/A_index | 0 | 0 |
| workshops/W2443/Resampling-Bands | 14 | 9 |
| workshops/W2443/gathering_examples_workshop | 23 | 11 |
| workshops/W2443/python_and_other_APIs | 2 | 1 |
| workshops/W2443/quality_filter_index_boxes | 1 | 1 |
| workshops/cs_day_hackathon_2024/Introduction | 10 | 12 |
| workshops/cs_day_hackathon_2024/Resampling-Bands | 14 | 11 |

## Verification

- Python syntax checked for all 39 Python files.
- Local Markdown file links checked.
- Every generated code step checked against its accompanying script.
- No interactive-shell syntax or IPython imports remain in the scripts.
- Offline validation passes with `./start_tests.sh`: four checks passed; the live integration suite was skipped.
- Live execution, dependency installation and visual rendering have not been tested; the local environment lacks the required scientific packages.
- Workshop imports now include shared helper modules, and the local-container backend URL has been replaced with the public DES endpoint.

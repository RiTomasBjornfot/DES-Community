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
| tutorials/000-Terms-and-Conditions | 0 | 0 |
| tutorials/010_INTRO-010-System-Overview | 0 | 0 |
| tutorials/010_INTRO-020-User-Handling | 0 | 0 |
| tutorials/01_INTRO_001-Tutorial-Overview | 0 | 0 |
| tutorials/020_DATA_010-Loading-DataCubes | 9 | 9 |
| tutorials/020_DATA_020-Property_Filtering | 5 | 4 |
| tutorials/030_GEOM_010-Bounding-box | 4 | 4 |
| tutorials/030_GEOM_020-Polygons-Intro | 10 | 17 |
| tutorials/030_GEOM_030-Polygons-Areas | 4 | 4 |
| tutorials/040_VIZ_010-RGB | 10 | 5 |
| tutorials/040_VIZ_020-Drawing-Images-On-Base-Map | 9 | 5 |
| tutorials/040_VIZ_030-Difference-Analysis | 6 | 3 |
| tutorials/050_PROC_010-Processes-intro | 3 | 3 |
| tutorials/050_PROC_020-Operators | 8 | 11 |
| tutorials/050_PROC_030-Batch-Processing | 10 | 15 |
| tutorials/060_EO_010-Masking-data | 10 | 13 |
| tutorials/060_EO_020-Reductions | 13 | 20 |
| tutorials/060_EO_030-Spatial-Filtering | 6 | 5 |
| tutorials/0990_Further-Reading | 0 | 0 |
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

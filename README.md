# Digital Earth Sweden Community

Learn to access and analyse satellite data with Digital Earth Sweden (DES).
Read these Markdown guides directly on GitHub or in your editor, and run the accompanying Python scripts in your preferred Python environment.

## Get started

1. Install Python 3.12 or newer, or use an existing compatible installation.
2. Clone or download this repository, including its helper modules and input files.
3. Install the example dependencies into your chosen environment:

   ```shell
   python -m pip install -r requirements.txt
   ```

A virtual environment is recommended to avoid dependency conflicts, but is optional. Use whichever environment manager you normally use. Reading the guides requires no Python installation.

Start with the system overview and account information below. Then try:

```shell
python tutorials/020_DATA_010-Loading-DataCubes.py
```

The Python code runs on your computer. openEO builds a description of the analysis and submits it to DES, where the satellite processing happens. Downloaded data, plotting and subsequent Python analysis run locally.

## Reading and running examples

Each practical guide contains explanations, code sections and a link to a complete Python script. Edit the area, dates and bands in the script, then run it. All steps execute in order. Batch examples can create and rerun remote jobs.

Text results appear in the terminal. Figures are written as PNG files; interactive maps are written as HTML files. Output paths are printed in the terminal. Scripts use their own directory as their working directory, so relative input paths work regardless of where you launch them.

The examples retain the original dataset IDs and dates. Check availability on the current backend before using them for a new analysis. Saved illustrations show earlier runs.

## Accounts

The tutorials default to the public demonstration account from the original material. Its jobs and results are shared. For the main tutorials, set `DES_USER` and `DES_PASSWORD` to use your own account, and optionally `DES_URL` to select a backend. The MOOC examples retain their explicit connection code, which you can edit. The original account-registration link is still missing; contact DES for personal access.

## Guides

### From satellite data to insights

- [session1 welcome to des](moocs/from_satellite_data_to_insights/session1_welcome_to_des.md)
- [session2 loading and visualizing](moocs/from_satellite_data_to_insights/session2_loading_and_visualizing.md)
- [session3 band arithmetic ndvi](moocs/from_satellite_data_to_insights/session3_band_arithmetic_ndvi.md)
- [session4 temporal reduction](moocs/from_satellite_data_to_insights/session4_temporal_reduction.md)
- [session5 cloud masking compositing](moocs/from_satellite_data_to_insights/session5_cloud_masking_compositing.md)
- [session6 urban green mapping](moocs/from_satellite_data_to_insights/session6_urban_green_mapping.md)

### Tutorials

- [000-Terms-and-Conditions](tutorials/000-Terms-and-Conditions.md)
- [010 INTRO-010-System-Overview](tutorials/010_INTRO-010-System-Overview.md)
- [010 INTRO-020-User-Handling](tutorials/010_INTRO-020-User-Handling.md)
- [01 INTRO 001-Tutorial-Overview](tutorials/01_INTRO_001-Tutorial-Overview.md)
- [020 DATA 010-Loading-DataCubes](tutorials/020_DATA_010-Loading-DataCubes.md)
- [020 DATA 020-Property Filtering](tutorials/020_DATA_020-Property_Filtering.md)
- [030 GEOM 010-Bounding-box](tutorials/030_GEOM_010-Bounding-box.md)
- [030 GEOM 020-Polygons-Intro](tutorials/030_GEOM_020-Polygons-Intro.md)
- [030 GEOM 030-Polygons-Areas](tutorials/030_GEOM_030-Polygons-Areas.md)
- [040 VIZ 010-RGB](tutorials/040_VIZ_010-RGB.md)
- [040 VIZ 020-Drawing-Images-On-Base-Map](tutorials/040_VIZ_020-Drawing-Images-On-Base-Map.md)
- [040 VIZ 030-Difference-Analysis](tutorials/040_VIZ_030-Difference-Analysis.md)
- [050 PROC 010-Processes-intro](tutorials/050_PROC_010-Processes-intro.md)
- [050 PROC 020-Operators](tutorials/050_PROC_020-Operators.md)
- [050 PROC 030-Batch-Processing](tutorials/050_PROC_030-Batch-Processing.md)
- [060 EO 010-Masking-data](tutorials/060_EO_010-Masking-data.md)
- [060 EO 020-Reductions](tutorials/060_EO_020-Reductions.md)
- [060 EO 030-Spatial-Filtering](tutorials/060_EO_030-Spatial-Filtering.md)
- [0990 Further-Reading](tutorials/0990_Further-Reading.md)

### Historical workshops

- [A index](workshops/W2443/A_index.md)
- [Resampling-Bands](workshops/W2443/Resampling-Bands.md)
- [gathering examples workshop](workshops/W2443/gathering_examples_workshop.md)
- [python and other APIs](workshops/W2443/python_and_other_APIs.md)
- [quality filter index boxes](workshops/W2443/quality_filter_index_boxes.md)
- [Introduction](workshops/cs_day_hackathon_2024/Introduction.md)
- [Resampling-Bands](workshops/cs_day_hackathon_2024/Resampling-Bands.md)

## Community and resources

Use the [community repository](https://github.com/DigitalEarthSweden/digital-earth-sweden-community) to report bugs, discuss features and ask or answer questions. The community is shared by developers, stakeholders and users.

- [Map viewer](https://maps.digitalearth.se)
- [Data Explorer](https://explorer.digitalearth.se)
- [openEO web editor](https://editor.openeo.org/?server=https%3A%2F%2Fopeneo.digitalearth.se)

The original support guidance says the small team typically monitors the forum on Mondays; please use the forum rather than personal messages or Teams.

## Migration status

All original tutorial, MOOC and workshop guides have been transferred to Markdown, with code in ordinary Python scripts. Narrative text, code comments, available saved outputs and supporting files are retained where possible. Installation-specific material has been replaced by the instructions above.

Scripts have been checked for Python syntax, but have not been run against DES. Historical workshop examples and pre-existing backend limitations need a separate execution review. Dependency versions are not locked or verified as a complete installation yet. See [migration notes](MIGRATION.md).

## Checks

Run `python -m unittest discover -s tests -v` for offline documentation and syntax checks (standard library only). To execute the selected tutorial scripts against DES, first install the dependencies and run `DES_RUN_INTEGRATION=1 ./start_tests.sh`. These integration checks download data and may consume backend resources. The same opt-in check is available through the GitHub Actions workflow dispatch form.

# Digital Earth Sweden Community

Learn to access and analyse satellite data with Digital Earth Sweden (DES).
Read these Markdown guides directly on GitHub or in your editor, and run the accompanying Python scripts in your preferred Python environment.

## Get started

1. Install Python 3.12 or newer, or use an existing compatible installation.
2. Clone or download this repository, including its helper modules and input files.

    ```shell
    git clone https://github.com/RiTomasBjornfot/DES-Community.git
    ```

3. Create a virtual environment to avoid dependency conflicts:

    ```shell
    cd DES-Community
    python3 -m venv .venv
    ```

4. Activate your virtual environment:

    Linux:

    ```bash
    source .venv/bin/activate
    ```

    Windows (PowerShell):

    ```powershell
    .venv\Scripts\Activate.ps1
    ```

5. Install the example dependencies into your chosen environment:

    ```shell
    python -m pip install -r requirements.txt
    ```
Start with the system overview and account information below. Then try:

```shell
python tutorials/loading-data.py
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

- [Terms and conditions](tutorials/terms-and-conditions.md)
- [System overview](tutorials/system-overview.md)
- [User accounts](tutorials/user-accounts.md)
- [Tutorial overview](tutorials/tutorial-overview.md)
- [Loading data](tutorials/loading-data.md)
- [Property filtering](tutorials/property-filtering.md)
- [Bounding box](tutorials/bounding-box.md)
- [Polygons](tutorials/polygons.md)
- [Polygon areas](tutorials/polygon-areas.md)
- [RGB](tutorials/rgb.md)
- [Images on base map](tutorials/images-on-base-map.md)
- [Difference analysis](tutorials/difference-analysis.md)
- [Processes](tutorials/processes.md)
- [Operators](tutorials/operators.md)
- [Batch processing](tutorials/batch-processing.md)
- [Masking data](tutorials/masking-data.md)
- [Reductions](tutorials/reductions.md)
- [Spatial filtering](tutorials/spatial-filtering.md)
- [Further reading](tutorials/further-reading.md)

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

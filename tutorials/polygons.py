"""polygons: see the accompanying Markdown guide."""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parent)
from example_output import display, save_plots

if __name__ == "__main__":
    # Step 2
    import openeo
    import io
    import numpy as np
    import xarray as xr
    import geopandas as gpd
    import matplotlib.pyplot as plt
    import json

    from shapely.geometry import shape, Polygon

    import rasterio
    from rasterio.plot import show
    import matplotlib.pyplot as plt

    from pyproj import Transformer

    import cartopy.crs as ccrs
    import cartopy.io.img_tiles as cimgt

    from config import user,passwd,eo_service_url
    from demo_helpers import show_result
    from demo_regions import s2

    plt.rcParams['figure.figsize'] = [20, 10]

    # Step 3
    # Connect to OpenEO
    conn = openeo.connect(eo_service_url)

    display(
    conn.authenticate_basic(username=user, password=passwd)
    )
    #conn.authenticate_oidc()

    # Step 5
    three_polys_from_geojson_editor = {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature", "geometry": {"type": "Polygon",
            "coordinates": [ [(16.514, 59.616), (16.436, 59.571), (16.444, 59.527), (16.493, 59.506), (16.684, 59.499), (16.825, 59.493), (16.892, 59.525), (16.901, 59.621), (16.514, 59.616)]]
          },
          "properties": None
        },
        {
          "type": "Feature", "geometry": {"type": "Polygon",
            "coordinates": [ [(16.552, 59.583), (16.49, 59.578), (16.495, 59.545), (16.574, 59.559), (16.552, 59.583)]]
          },
          "properties": None
        },
        {
          "type": "Feature",
          "geometry": {
            "type": "Polygon",
            "coordinates": [[(16.82, 59.55), (16.727, 59.55), (16.727, 59.586), (16.82, 59.586), (16.82, 59.55)]]
          },
          "properties": None
        }
      ]
    } 
    # Move the hole polygons inside to create the holes
    proper_poly_with_hole={
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature", "geometry": {"type": "Polygon",
            "coordinates": [  
                            [(16.514, 59.616), (16.436, 59.571), (16.444, 59.527), (16.493, 59.506), (16.684, 59.499), (16.825, 59.493), (16.892, 59.525), (16.901, 59.621), (16.514, 59.616)],
                            [(16.552, 59.583), (16.49, 59.578), (16.495, 59.545), (16.574, 59.559), (16.552, 59.583)],
                            [(16.82, 59.55), (16.727, 59.55), (16.727, 59.586), (16.82, 59.586), (16.82, 59.55)]

                           ]
          },
          "properties": None
        },
      ]
    } 

    # Step 7
    print("From GeoJSON editor:")
    display(gpd.GeoDataFrame.from_features(three_polys_from_geojson_editor))
    print("Moved holes inside the polygon")
    display(
    display(gpd.GeoDataFrame.from_features(proper_poly_with_hole))
    )

    # Step 8
    # Choose the corrected polygon structure for visualization
    poly = proper_poly_with_hole
    #poly = three_polys_from_geojson_editor  # Uncomment to see the uncorrected structure

    # Convert the GeoJSON to a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(poly)

    # Create a plot to visualize the geometry
    fig, ax = plt.subplots()
    gdf.plot(ax=ax, color='blue', edgecolor='black', alpha=0.5)

    # Set labels and title
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Polygon over Lake Mälaren with Holes')

    display(
    plt.show()
    )

    # Step 10
    # Download S2MSI2A data
    cube = conn.load_collection(
        s2.s2_msi_l2a,
        bands=["b04", "b03", "b02"],  # RGB channels
        spatial_extent=poly,
        temporal_extent=["2022-06-01", "2022-06-05"],
    )

    # Reduce the dimension over time by selecting the first image in the time range
    cube = cube.reduce_dimension(dimension="t", reducer="first")

    # Download the resulting image in GeoTIFF format
    s2_image_data2 = cube.download(format="gtiff")

    # Visualize the fetched image to check how the holes are represented
    display(
    show_result(s2_image_data2, colormap="gray", norm=False)
    )

    # Step 12
    from datetime import datetime
    fname = f"img_{datetime.now().strftime('%Y%m%d-T%H%M%S.%f')}.nc" # needs to be different each time, see explanation further down in the guide

    # Request a time series of Sentinel-2 images
    cube = conn.load_collection(
        s2.s2_msi_l2a,
        bands=["b04", "b03", "b02"],  # RGB channels
        spatial_extent=poly,
        temporal_extent=["2022-06-01", "2022-06-10"],
    )

    # Download the resulting time series as a NetCDF file
    res = cube.download(outputfile=fname, format="netcdf")

    # Load the data into an xarray dataset for further analysis
    loaded_data = xr.open_dataset(fname, engine='h5netcdf', decode_times=True)

    # Handle no-data values
    nodata = loaded_data.attrs.get("nodata", None)
    loaded_data = loaded_data.where(loaded_data != nodata, np.nan)

    # Import helper functions for plotting
    from demo_helpers import plot_xr_dataarray_contact_copy, plot_xr_dataarray_on_map

    # Visualize one of the bands ('b02') across the time series
    display(
    plot_xr_dataarray_contact_copy(loaded_data['b02'], figsize=(20,10), cmap="PiYG")
    )

    # Step 16
    from demo_regions import s2

    # Load the large polygon in WGS84 format
    original_polygon_geojson = s2.polygons.a

    # Extract the polygon geometry from the GeoJSON
    original_polygon = Polygon(original_polygon_geojson['features'][0]['geometry']['coordinates'][0])

    # Print the number of points in the original polygon
    print(f"Original number of points: {len(original_polygon.exterior.coords)}")

    # Convert the GeoJSON to a GeoDataFrame and plot it
    gdf_wgs84 = gpd.GeoDataFrame.from_features(original_polygon_geojson)
    gdf_wgs84.set_crs(epsg=4326, inplace=True)

    # Plot the original polygon
    gdf_wgs84.plot(edgecolor='black', color='lightblue', alpha=0.6)
    plt.title("Original Polygon in WGS84 (Before Simplification)")
    display(
    plt.show()
    )

    # Step 17
    # Simplify the polygon with a specified tolerance value
    from shapely.geometry import mapping  
    tolerance = 0.0001  # Small tolerance value for minimal simplification
    simplified_polygon = original_polygon.simplify(tolerance, preserve_topology=True)

    # Print the number of points after simplification
    print(f"Simplified number of points: {len(simplified_polygon.exterior.coords)}")

    # Create a new GeoDataFrame to hold the simplified geometry
    simplified_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": original_polygon_geojson['features'][0]['properties'],
                "id": original_polygon_geojson['features'][0].get('id', None),
                "geometry": mapping(simplified_polygon)
            }
        ]
    }

    gdf_simplified = gpd.GeoDataFrame.from_features(simplified_geojson)
    gdf_simplified.set_crs(epsg=4326, inplace=True)

    # Plot the simplified polygon
    gdf_simplified.plot(edgecolor='black', color='lightgreen', alpha=0.6)
    plt.title("Simplified Polygon in WGS84")
    display(
    plt.show()
    )

    # Step 18
    import matplotlib.patches as mpatches

    # Simplify the polygon with a specified tolerance value
    tolerance = 0.0001  # Small tolerance value for minimal simplification
    simplified_polygon = original_polygon.simplify(tolerance, preserve_topology=True)

    # Print the number of points after simplification
    print(f"Simplified number of points: {len(simplified_polygon.exterior.coords)}")

    # Create a new GeoDataFrame to hold the simplified geometry
    simplified_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": original_polygon_geojson['features'][0]['properties'],
                "id": original_polygon_geojson['features'][0].get('id', None),
                "geometry": mapping(simplified_polygon)  # Use mapping from shapely.geometry
            }
        ]
    }

    gdf_original = gpd.GeoDataFrame.from_features(original_polygon_geojson)
    gdf_original.set_crs(epsg=4326, inplace=True)

    gdf_simplified = gpd.GeoDataFrame.from_features(simplified_geojson)
    gdf_simplified.set_crs(epsg=4326, inplace=True)

    # Plot both the original and simplified polygons
    fig, ax = plt.subplots()
    gdf_original.plot(ax=ax, edgecolor='blue', color='none', linewidth=2, alpha=0.6)
    gdf_simplified.plot(ax=ax, edgecolor='green', color='none', linewidth=2, alpha=0.6)

    # Create custom legend
    original_patch = mpatches.Patch(color='blue', label='Original Polygon')
    simplified_patch = mpatches.Patch(color='green', label='Simplified Polygon')
    plt.legend(handles=[original_patch, simplified_patch])

    plt.title("Original vs Simplified Polygon in WGS84")
    display(
    plt.show()
    )
    save_plots()

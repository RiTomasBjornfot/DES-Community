[Documentation home](../README.md)

# Digital Earth Sweden: System Overview

Digital Earth Sweden (DES) is a powerful platform designed to provide easy access to satellite data over Sweden and the Baltic Sea. By consolidating storage, processing, and analysis capabilities into one integrated system, DES supports a wide range of users—from government agencies to universities—enabling efficient and effective use of Earth observation data.

In this guide, we’ll introduce you to the key components of the DES platform, focusing on the services we offer and how you can leverage them using the OpenEO API.

## What We Do, So You Can...

<center>
<div style="width: 60%; text-align: center;">
    <img src="https://lucid.app/publicSegments/view/5bc47e06-e7a0-4023-8085-2b18349c0fcc/image.png" alt="The big deal">
    <h5>Figure 1. The Four Core Features of Digital Earth Sweden</h5>
</div>
</center>

### The Four Core Features of DES:

1. **Data Collection and Refinement**: We gather and refine satellite imagery over Sweden from various sources, ensuring that data is presented in a standardized and efficient format, stored locally for swift access.

2. **Unified Search and Access**: Our platform provides a unified method for searching, browsing, and viewing satellite data. You can retrieve time series data over specific regions, structured as a DataCube, ready for further analysis.

3. **DataCube Processing**: DES enables you to apply processing operations directly on the time series data within our infrastructure. This makes calculations significantly faster, allowing you to download only the processed results, conserving bandwidth.

4. **User-Centric Approach**: The entire system is designed with the user in mind, providing easy-to-use interfaces and APIs for accessing and analyzing data.

## Available Services

<center>
<div style="width: 100%; text-align: center;">
    <img src="https://lucid.app/publicSegments/view/e9e8e820-cb5a-4f7f-ae21-5bab0f2766c3/image.png" alt="Available Services">
    <h5>Figure 2. How our services contribute to the core features of Digital Earth Sweden.</h5>
</div>
</center>

### Key Services Provided by DES:

- **Data Acquisition and Processing System (DAP)**: Our in-house developed system for discovering, downloading, and processing satellite data. The DAP system ensures that the data is up-to-date, standardized, and readily available.

- **OpenDataCube Explorer**: A quantitative visualization tool that lets you explore the datasets available in DES.

- **TerriaMap**: An intuitive map-based interface for visually exploring satellite data layers.

- **OpenEO API**: Our implementation of the [OpenEO](https://r-spatial.org/2016/11/29/openeo.html) API allows you to connect to DES, load satellite image collections, perform processing tasks (like calculating NDVI), and download the results using Python, R, or JavaScript.

### Exploring Data with Our Tools

Before diving into the code, it's beneficial to explore our data offerings using the following tools:

- **[Digital Earth Sweden Explorer](https://explorer.digitalearth.se)**: Use this tool to search, filter, and preview satellite datasets available on the platform. It provides spatial and temporal filtering capabilities, making it easier to find the right data for your analysis.

- **[TerriaMap](https://map.digitalearth.se)**: This tool offers a more visual way to explore the datasets, allowing you to overlay different data layers on a map and gain insights into spatial patterns.

- **OpenEO**: This is an API that can be used from 3:rd party tools such as [OpenEO Webeditor](https://editor.openeo.org/?server=https%3A%2F%2Fopeneo.digitalearth.se) or OpenEO scripting client, available in languages such as Python, R and JavaScript. The Python client will be used throughout this tutorial.
- **Official Homepage**:[Digital Earth Sweden](https://www.digitalearth.se)



### What is OpenEO?

OpenEO is a collaborative European project designed to simplify access and processing of Earth observation data by offering a **standardized API** for cloud-based geospatial platforms. It allows users to perform large-scale satellite data analyses in a consistent way, without needing to manage complex infrastructure.

Several major initiatives, such as Digital Earth Africa, Digital Earth Australia, and even Google Earth, utilize OpenEO to streamline workflows, making satellite data processing accessible to a wider audience.


### Why Use OpenEO?

- Standardized Workflows: OpenEO unifies how different platforms handle Earth observation data, enabling the same operations across multiple cloud providers.
- Backend Processing: You don’t need powerful local machines. All heavy computations, such as mosaicking or time series analyses, run on the backend infrastructure.
- Simplified Data Access: With just a few commands, you can access pre-processed satellite data collections and perform complex analyses like calculating vegetation indices or change detection.

### Typical Workflow with OpenEO

A typical workflow using the OpenEO API involves:

1. **Connecting to the OpenEO Backend**: Establish a connection to the DES OpenEO service using e.g. Python.
2. **Loading Data**: Define your area of interest and time span to load a satellite image collection.
3. **Processing Data**: Apply calculations, such as NDVI, directly on the DES infrastructure.
4. **Downloading Results**: Retrieve the processed data for further analysis or visualization on your local machine.

In this tutorial you will get aquainted with the core aspects of our OpenEO implementation.  


## Getting Started
 
If you are new to OpenEO, we recommend starting with the [OpenEO API documentation](https://openeo.org/documentation/1.0/) to familiarize yourself with the core concepts and API structure.

Let's get started with exploring and analyzing satellite data over Sweden!


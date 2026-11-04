[Documentation home](../../README.md) · [Download Python script](python_and_other_APIs.py)

Run from this directory with `python python_and_other_APIs.py`. Read the guide first: the script runs all steps in order and may submit remote jobs. Figures and maps are saved under `outputs/python_and_other_APIs/`.

> Historical workshop material. Examples may require additional services, credentials or repairs; they are preserved for reference.

> Saved outputs below come from the original teaching material; they are illustrations, not a fresh run against the current service.


# Load Data from Other Agencies

2024-10-22 daniel.flemstrom@ri.se, nuria.agues.paszkowsky@ri.se

The following example shows how to create a neat Python interface for another agency’s REST API. In this example, we have chosen the Swedish Forest Agency's Histogram service as an example.

To be useful, the API should ideally be integrated into a process that can then be used in a similar way to the quality filter example here: [Index Box Filtering](./quality_filter_index_boxes.md)


### Step 2

```python
from dataclasses import dataclass
from shapely import Polygon
from shapely import wkt
from typing import Union
from typing import Iterable
import requests
import os


# --------------------------------------------------------------------------------
#                            HistogramDateSummaryRequest
# --------------------------------------------------------------------------------
# {
#   "minDatum": "2023-06-16T12:00:00.000Z",
#   "maxDatum": "2023-06-26T06:39:18.427Z",
#   "minTackningIndexruta": 0,
#   "minBraData": 0,
#   "extent": "POLYGON ((480000 , ......,7020000))"
# }
@dataclass
class HistogramDateSummaryRequest:
    minDatum: str = None
    maxDatum: str = None
    minTackningIndexruta: float = -1.0
    minBraData: float = -1.0
    extent: Union[str | Polygon] = None

    def as_dict(self):
        if isinstance(self.extent, Polygon):
            extent = wkt.dumps(self.extent) if self.extent else None
        else:
            extent = self.extent
        d = {
            "minDatum": self.minDatum,
            "maxDatum": self.maxDatum,
            "minTackningIndexruta": self.minTackningIndexruta,
            "minBraData": self.minBraData,
            "extent": extent,
        }
        return d

 
# --------------------------------------------------------------------------------
#                             HistogramDateSummaryResponse
# --------------------------------------------------------------------------------
# From SKS API endpoint
#  {
#     "datum": "2023-06-16T00:00:00+00:00",
#     "antalIndexrutor": 9,
#     "summaBraData": 9,
#     "genomsnittligBraData": 1,
#     "minBraData": 0.9999999999999999,
#     "maxBraData": 1,
#     "minTackningIndexruta": 1
#   },
@dataclass
class HistogramDateSummaryResponse:
    datum: str
    antalIndexrutor: int
    summaBraData: int
    genomsnittligBraData: float
    minBraData: float
    maxBraData: float
    minTackningIndexruta: float
    # allGoodData: str

    def as_dict(self):
        d = {
            "datum": self.datum,
            "antalIndexrutor": self.antalIndexrutor,
            "summaBraData": self.summaBraData,
            "genomsnittligBraData": self.genomsnittligBraData,
            "minBraData": self.minBraData,
            "maxBraData": self.maxBraData,
            "minTackningIndexruta": self.minTackningIndexruta,
            # "allGoodData": self.allGoodData
        }
        return d

# --------------------------------------------------------------------------------
#                             SclHistogramByBkidRequest
# --------------------------------------------------------------------------------
@dataclass
class SclHistogramByBkidRequest:
    minDatum: str = None
    maxDatum: str = None
    minTackningIndexruta: float = -1.0
    bkId: str = None
    minBraData: float = -1.0

    def as_dict(self):
        d = {
            "minDatum": self.minDatum,
            "maxDatum": self.maxDatum,
            "minTackningIndexruta": self.minTackningIndexruta,
            "bkId": self.bkId,
            "minBraData": self.minBraData,
        }
        return d

# --------------------------------------------------------------------------------
#                             SclHistogramByBkidResponse
# --------------------------------------------------------------------------------
@dataclass
class SclHistogramByBkidResponse:
    bk: str
    datum: datetime
    braData: float
    counts: int
    pixelSize: int
    indexFramePixelCount: 0
    indexFrameCoverage: 0

    def as_dict(self):
        d = {
            "bk": self.bk,
            "datum": self.datum,
            "braData": self.braData,
            "counts": self.counts,
            "pixelSize": self.pixelSize,
            "indexFramePixelCount": self.indexFramePixelCount,
            "indexFrameCoverage": self.indexFrameCoverage,
        }
        return d



# ====================================================================================
#   API                                 SksAPI
# ====================================================================================
class SksAPI:
    # --------------------------------------------------------------------------------
    #  (API)                         get_access_token
    # --------------------------------------------------------------------------------
    @classmethod
    def get_access_token(cls, client_id=None, client_secret=None):
        # Get OAuth credentials from environment variables
        client_id = client_id or os.environ.get("SKS_CLIENT_ID")
        client_secret = client_secret or os.environ.get("SKS_CLIENT_SECRET")
        token_url = "https://auth.skogsstyrelsen.se/connect/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "sks_api"
        }
        response = requests.post(token_url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            print("Error while obtaining access token:", response.status_code, response.text)
            return None

    # --------------------------------------------------------------------------------
    #  API                                SclHistogramByBkid
    # --------------------------------------------------------------------------------
    @classmethod
    def SclHistogramByBkid(
        cls,
        access_token,
        params: SclHistogramByBkidRequest,
        debug: bool = False,
    ) -> Iterable[SclHistogramByBkidResponse]:
        """
        Returns the same structure as the SKS official API
        """
        url = "https://api.skogsstyrelsen.se/sksapi/v1/Raster/SclHistogramByBkid"
        if not access_token:
            raise ValueError("You need an access token!")

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, json=params.as_dict())

        if response.status_code != 200:
            msg = "Error in API request: {response.status_code} and {response.text}"
            print(msg)
            raise RuntimeError(msg)

        result = response.json()

        if not result:
            return None  # Or handle the no-result case appropriately

        result2 = [SclHistogramByBkidResponse(**row) for row in result]

        return result2

    # --------------------------------------------------------------------------------
    #   API                          HistogramDateSummary
    # --------------------------------------------------------------------------------
    @classmethod
    def HistogramDateSummary(
        cls,
        access_token,
        params: HistogramDateSummaryRequest,
        debug: bool = False,
    ) -> Iterable[HistogramDateSummaryResponse]:
        """
        Returns the same structure as the SKS official API
        """
        url = "https://api.skogsstyrelsen.se/sksapi/v1/Raster/Scl/HistogramDateSummary"
        if not access_token:
            raise ValueError("You need an access token!")

        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

        response = requests.post(url, headers=headers, json=params.as_dict())

        if response.status_code != 200:
            msg = "Error in API request: {response.status_code} and {response.text}"

            print(msg)
            raise RuntimeError(msg)

        result = response.json()

        if not result:
            return []  

        result2 = [HistogramDateSummaryResponse(**row) for row in result]

        return result2
```

### Step 3

```python
# Här är ett exempel på hur man kan komma åt en extern datakälla från python
# För att kunna använda denna data i en processgraf behöver man förstås skapa en 
# motsvarande process för datat. 


os.environ['SKS_CLIENT_ID']="<use your own id>"
os.environ['SKS_CLIENT_SECRET']="<use your own key>"

access_token = SksAPI.get_access_token()

params = SclHistogramByBkidRequest(
    minDatum="2022-05-01",
    maxDatum="2022-07-01",
    minTackningIndexruta=0.9,
    bkId="701_48_50",
    minBraData=0.9,
)

if not access_token:
    print("Failed to obtain access token.")

results = SksAPI.SclHistogramByBkid(access_token, params, debug=True)

for result in results:
    print(result)
```

```text
SclHistogramByBkidResponse(bk='701_48_50', datum='2022-05-17T00:00:00', braData=0.9999999999999999, counts=62500, pixelSize=20, indexFramePixelCount=62500, indexFrameCoverage=1.0)
SclHistogramByBkidResponse(bk='701_48_50', datum='2022-05-22T00:00:00', braData=0.9999999999999999, counts=62500, pixelSize=20, indexFramePixelCount=62500, indexFrameCoverage=1.0)
```

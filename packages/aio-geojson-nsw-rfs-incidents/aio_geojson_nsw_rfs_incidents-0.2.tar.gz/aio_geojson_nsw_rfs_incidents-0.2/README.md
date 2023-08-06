# python-aio-geojson-nsw-rfs-incidents

[![Build Status](https://travis-ci.org/exxamalte/python-aio-geojson-nsw-rfs-incidents.svg)](https://travis-ci.org/exxamalte/python-aio-geojson-nsw-rfs-incidents)
[![Coverage Status](https://coveralls.io/repos/github/exxamalte/python-aio-geojson-nsw-rfs-incidents/badge.svg?branch=master)](https://coveralls.io/github/exxamalte/python-aio-geojson-nsw-rfs-incidents?branch=master)
[![PyPi](https://img.shields.io/pypi/v/aio-geojson-nsw-rfs-incidents.svg)](https://pypi.python.org/pypi/aio-geojson-nsw-rfs-incidents)
[![Version](https://img.shields.io/pypi/pyversions/aio-geojson-nsw-rfs-incidents.svg)](https://pypi.python.org/pypi/aio-geojson-nsw-rfs-incidents)

This library provides convenient async access to the [NSW Rural Fire Service](https://www.rfs.nsw.gov.au/fire-information/fires-near-me) incidents feed.
 
## Installation
`pip install aio-geojson-nsw-rfs-incidents`

## Usage
See below for examples of how this library can be used. After instantiating a 
particular class - feed or feed manager - and supply the required parameters, 
you can call `update` to retrieve the feed data. The return value 
will be a tuple of a status code and the actual data in the form of a list of 
feed entries specific to the selected feed.

Status Codes
* _OK_: Update went fine and data was retrieved. The library may still 
  return empty data, for example because no entries fulfilled the filter 
  criteria.
* _OK_NO_DATA_: Update went fine but no data was retrieved, for example 
  because the server indicated that there was not update since the last request.
* _ERROR_: Something went wrong during the update

**Parameters**

| Parameter          | Description                               |
|--------------------|-------------------------------------------|
| `home_coordinates` | Coordinates (tuple of latitude/longitude) |

**Supported Filters**

| Filter     |                     | Description |
|------------|---------------------|-------------|
| Radius     | `filter_radius`     | Radius in kilometers around the home coordinates in which events from feed are included. |
| Categories | `filter_categories` | Array of category names. Only events with a category matching any of these is included. |

**Example**
```python
import asyncio
from aiohttp import ClientSession
from aio_geojson_nsw_rfs_incidents import NswRuralFireServiceIncidentsFeed
async def main() -> None:
    async with ClientSession() as websession:    
        # Home Coordinates: Latitude: -33.0, Longitude: 150.0
        # Filter radius: 50 km
        # Filter categories: 'Advice'
        feed = NswRuralFireServiceIncidentsFeed(websession, 
                                                (-33.0, 150.0), 
                                                filter_radius=50, 
                                                filter_categories=['Advice'])
        status, entries = await feed.update()
        print(status)
        print(entries)
asyncio.get_event_loop().run_until_complete(main())
```

## Feed entry properties
Each feed entry is populated with the following properties:

| Name               | Description                                                                                         | Feed attribute |
|--------------------|-----------------------------------------------------------------------------------------------------|----------------|
| geometry           | All geometry details of this entry.                                                                 | `geometry`     |
| coordinates        | Best coordinates (latitude, longitude) of this entry.                                               | `geometry`     |
| external_id        | The unique public identifier for this incident.                                                     | `guid`         |
| title              | Title of this entry.                                                                                | `title`        |
| attribution        | Attribution of the feed.                                                                            | n/a            |
| distance_to_home   | Distance in km of this entry to the home coordinates.                                               | n/a            |
| category           | The alert level of the incident ('Emergency Warning', 'Watch and Act', 'Advice','Not Applicable').  | `category`     |
| publication_date   | The publication date of the incidents.                                                              | `pubDate`      |
| description        | The description of the incident.                                                                    | `description`  |
| location           | Location description of the incident.                                                               | `description` -> `LOCATION`            |
| council_area       | Council are this incident falls into.                                                               | `description` -> `COUNCIL AREA`        |
| status             | Status of the incident.                                                                             | `description` -> `STATUS`              |
| type               | Type of the incident (e.g. Bush Fire, Grass Fire, Hazard Reduction).                                | `description` -> `TYPE`                |
| fire               | Indicated if this incident is a fire or not (`True`/`False`).                                       | `description` -> `FIRE`                |
| size               | Size in ha.                                                                                         | `description` -> `SIZE`                |
| responsible_agency | Agency responsible for this incident.                                                               | `description` -> `RESPONSIBLE AGENCY`  |


## Feed Manager

The Feed Manager helps managing feed updates over time, by notifying the 
consumer of the feed about new feed entries, updates and removed entries 
compared to the last feed update.

* If the current feed update is the first one, then all feed entries will be 
  reported as new. The feed manager will keep track of all feed entries' 
  external IDs that it has successfully processed.
* If the current feed update is not the first one, then the feed manager will 
  produce three sets:
  * Feed entries that were not in the previous feed update but are in the 
    current feed update will be reported as new.
  * Feed entries that were in the previous feed update and are still in the 
    current feed update will be reported as to be updated.
  * Feed entries that were in the previous feed update but are not in the 
    current feed update will be reported to be removed.
* If the current update fails, then all feed entries processed in the previous
  feed update will be reported to be removed.

After a successful update from the feed, the feed manager provides two
different dates:

* `last_update` will be the timestamp of the last update from the feed 
  irrespective of whether it was successful or not.
* `last_update_successful` will be the timestamp of the last successful update 
  from the feed. This date may be useful if the consumer of this library wants 
  to treat intermittent errors from feed updates differently.
* `last_timestamp` (optional, depends on the feed data) will be the latest 
  timestamp extracted from the feed data. 
  This requires that the underlying feed data actually contains a suitable 
  date. This date may be useful if the consumer of this library wants to 
  process feed entries differently if they haven't actually been updated.

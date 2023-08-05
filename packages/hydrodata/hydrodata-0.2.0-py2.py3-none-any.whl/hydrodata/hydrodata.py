#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The main module for generating an instance of hydrodata.

It can be used as follows:
    >>> from hydrodata import Dataloader
    >>> wshed = Dataloader('2010-01-01', '2015-12-31', station_id='01467087')

For more information refer to the Usage section of the document.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import geopandas as gpd
from numba import njit, prange
import requests
from tqdm import tqdm
import urllib


class Dataloader:
    """Generate an instance of hydrodata package.

    Downloads climate and streamflow observation data from Daymet and USGS,
    respectively. The data is saved to a HDF5 file. Either coords or station_id
    argument should be specified.
    """
    def __init__(
        self,
        start,
        end,
        station_id=None,
        coords=None,
        gis_dir="gis_data",
        data_dir="data",
        phenology=False,
        width=2000,
    ):
        """Initialize the instance.

        Parameters
        ----------
        start : string or datetime
            The starting date of the time period.
        end : string or datetime
            The end of the time period.
        station_id : string
            USGS station ID
        coords : tuple
            A tuple including longitude and latitude of the point of interest.
        gis_dir : string
            Path to the location of NHDPlusV21 root directory;
            GageLoc and GageInfo are required.
        data_dir : string
            Path to the location of climate data. The naming
            convention is data_dir/{watershed name}_climate.h5
        phenology : bool
            consider phenology for computing PET based on
            Thompson et al., 2011 (https://doi.org/10.1029/2010WR009797)
        width : float
            Width of the geotiff image for LULC in pixels.
            Default is 2000 px. The height is computed automatically
            from the domain's aspect ratio.

        """
        self.start = pd.to_datetime(start)
        self.end = pd.to_datetime(end)

        self.gis_dir = Path(gis_dir)
        self.info_path = Path(gis_dir, "NHDPlusNationalData", "GageInfo.dbf")
        self.loc_path = Path(gis_dir, "NHDPlusNationalData", "GageLoc.shp")

        self.phenology = phenology
        self.width = width

        if not self.info_path.exists() or not self.loc_path.exists():
            get_nhd(self.gis_dir)

        if station_id is None and coords is not None:
            self.coords = coords
            self.get_id()
        elif coords is None and station_id is not None:
            self.station_id = str(station_id)
            self.get_coords()
        else:
            raise RuntimeError("Either coordinates or station ID" +
                               " should be specified.")

        self.lon, self.lat = self.coords
        self.data_dir = Path(data_dir, self.comid)

    def get_coords(self):
        """Get coordinates of the station from station ID."""
        ginfo = gpd.read_file(self.info_path)

        try:
            station = ginfo[ginfo.GAGEID == self.station_id]
            self.coords = (station.LonSite.values[0],
                           station.LatSite.values[0])
            self.DASqKm = station.DASqKm.values[0]  # drainage area
            self.wshed_name = station.STATION_NM.values[0]
            print("The gauge station is located in the following watershed:")
            print(self.wshed_name)
        except IndexError:
            raise IndexError("Station ID was not found in the USGS database.")

        if not self.loc_path.exists():
            raise FileNotFoundError(
                f"GageLoc.shp cannot be found in {self.loc_path}")
        else:
            gloc = gpd.read_file(self.loc_path)
        station_loc = gloc[gloc.SOURCE_FEA == self.station_id]
        self.comid = str(station_loc.FLComID.values[0])

    def get_id(self):
        """Get station ID based on the specified coordinates."""
        from shapely.ops import nearest_points
        from shapely.geometry import Point

        gloc = gpd.read_file(self.loc_path)
        lon, lat = self.coords

        point = Point(lon, lat)
        pts = gloc.geometry.unary_union
        station_loc = gloc[gloc.geometry.geom_equals(
            nearest_points(point, pts)[1])]
        self.station_id = str(station_loc.SOURCE_FEA.values[0])
        self.comid = str(station_loc.FLComID.values[0])

        ginfo = gpd.read_file(self.info_path)
        station = ginfo[ginfo.GAGEID == self.station_id]
        self.DASqKm = station.DASqKm.values[0]  # drainage area
        self.wshed_name = station.STATION_NM.values[0]
        print("The gage station is located in the following watershed:")
        print(self.wshed_name)

    def get_climate(self):
        """Get climate data from the Daymet database.

        The function first downloads climate data then computes potential
        evapotranspiration using ETo python package. Then downloads streamflow
        data from USGS database and saves the data as an HDF5 file and return
        it as a Pandas dataframe. The naming convention for the HDF5 file is
        <station_id>_<start>_<end>.h5. If the files already exits on the disk
        it is read and returned as a Pandas dataframe.
        """
        import json
        import daymetpy
        import eto
        import h5py

        # Get datum of the station
        url = ("https://waterservices.usgs.gov/nwis/site/?format=rdb&sites=" +
               self.station_id)
        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.HTTPError or \
                requests.exceptions.ConnectionError or \
                requests.exceptions.Timeout or \
                requests.exceptions.RequestException:
            raise

        r_text = r.text.split("\n")
        r_list = [l.split("\t") for l in r_text if "#" not in l]
        r_dict = dict(zip(r_list[0], r_list[2]))
        # convert ft to meter
        self.datum = float(r_dict["alt_va"]) * 0.3048

        fname = ("_".join([
            str(self.start.strftime("%Y%m%d")),
            str(self.end.strftime("%Y%m%d"))
        ]) + ".h5")
        self.clm_file = Path(self.data_dir, fname)

        if self.clm_file.exists():
            print(f"Using existing climate data file: {self.clm_file}")
            with h5py.File(self.clm_file, "r") as f:
                self.climate = pd.DataFrame(f["c"])
            self.climate.columns = [
                "prcp (mm/day)",
                "tmin (C)",
                "tmax (C)",
                "tmean (C)",
                "pet (mm)",
                "qobs (cms)",
            ]
            # daymet doesn't account for leap years.
            # It removes Dec 31 when leap year.
            index = pd.date_range(self.start, self.end)
            nl = index[~index.is_leap_year]
            lp = index[(index.is_leap_year)
                       & (~index.strftime("%Y-%m-%d").str.endswith("12-31"))]
            index = index[(index.isin(nl)) | (index.isin(lp))]
            self.climate.index = index
            return

        print("Downloading climate data from the Daymet database")
        climate = daymetpy.daymet_timeseries(
            lon=round(self.lon, 6),
            lat=round(self.lat, 6),
            start_year=self.start.year,
            end_year=self.end.year,
        )
        climate.drop("year", inplace=True, axis=1)
        climate = climate[self.start:self.end]
        climate["tmean"] = climate[["tmin", "tmax"]].mean(axis=1)

        print("Computing potential evapotranspiration (PET) using FAO method")
        df = climate[["tmax", "tmin", "vp"]].copy()
        df.columns = ["T_max", "T_min", "e_a"]
        df["R_s"] = climate.srad * climate.dayl * 1e-6  # to MJ/m2
        df["e_a"] *= 1e-3  # to kPa

        et1 = eto.ETo()
        freq = "D"
        et1.param_est(df[["R_s", "T_max", "T_min", "e_a"]], freq, self.datum,
                      self.lat, self.lon)
        climate["pet"] = et1.eto_fao()

        # Multiply pet by growing season index, GSI, for phenology
        # (Thompson et al., 2011)
        # https://doi.org/10.1029/2010WR009797
        if self.phenology:
            tmax, tmin = 10.0, -5.0
            trng = 1.0 / (tmax - tmin)

            def gsi(row):
                if row.tmean < tmin:
                    return 0
                elif row.tmean > tmax:
                    return row.pet
                else:
                    return (row.tmean - tmin) * trng * row.pet

            climate["pet"] = climate.apply(gsi, axis=1)

        print("Downloading stream flow data from USGS database")
        err = pd.read_html(
            "https://waterservices.usgs.gov/rest/DV-Service.html")[0]

        try:
            r = requests.get(
                "https://waterservices.usgs.gov/nwis/dv/?format=json" +
                f"&sites={self.station_id}" +
                f'&startDT={self.start.strftime("%Y-%m-%d")}' +
                f'&endDT={self.end.strftime("%Y-%m-%d")}' +
                "&parameterCd=00060&siteStatus=all")
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            print(err[err["HTTP Error Code"] ==
                      r.status_code].Explanation.values[0])
            raise
        except requests.exceptions.ConnectionError or \
                requests.exceptions.Timeout or \
                requests.exceptions.RequestException:
            raise

        df = json.loads(r.text)
        df = df["value"]["timeSeries"][0]["values"][0]["value"]
        df = pd.DataFrame.from_dict(df, orient="columns")
        df["dateTime"] = pd.to_datetime(df["dateTime"],
                                        format="%Y-%m-%dT%H:%M:%S")
        df.set_index("dateTime", inplace=True)
        # Convert cfs to cms
        climate["qobs"] = df.value.astype("float64") * 0.028316846592

        climate = climate[["prcp", "tmin", "tmax", "tmean", "pet", "qobs"]]
        climate.columns = [
            "prcp (mm/day)",
            "tmin (C)",
            "tmax (C)",
            "tmean (C)",
            "pet (mm)",
            "qobs (cms)",
        ]
        self.climate = climate[self.start:self.end].dropna()

        if not self.clm_file.parent.is_dir():
            try:
                import os

                os.makedirs(self.clm_file.parent)
            except OSError:
                raise OSError(
                    f"input directory cannot be created: {self.data_dir}")

        with h5py.File(self.clm_file, "w") as f:
            f.create_dataset("c", data=self.climate, dtype="d")

        print("climate data was downloaded successfuly and" +
              f"saved to {self.clm_file}")

    def get_lulc(self, geom_path=None):
        """Get LULC data from NLCD 2016 database.

        Download and compute land use, canopy and cover from NLCD2016
        database inside a given Polygon geometry with epsg:4326 projection.
        Note: NLCD data has a 30 m resolution.

        Parameters
        ----------
        geom_path : string
            Path to the shapefile.
            The default is <gis_dir>/<comid>/geometry.shp.

        Returns
        -------
        impervious : dict
            A dictionary containing min, max, mean and count of the
            imperviousness of the watershed
        canpoy : dict
            A dictionary containing min, max, mean and count of the canpoy
            of the watershed
        cover : dataframe
            A dataframe containing watershed's land coverage percentage.
        """
        from owslib.wms import WebMapService
        import rasterstats
        from hydrodata.nlcd_helper import NLCD

        if geom_path is None:
            geom_path = self.gis_dir.joinpath(self.comid, "geometry.shp")
        else:
            geom_path = Path(geom_path)

        if not geom_path.exists():
            msg = (
                f"{geom_path} cannot be found." +
                " Watershed geometry needs to be specified for LULC. " +
                "The `nhdplus.R` script can be used to download the geometry.")
            raise FileNotFoundError(msg)
        else:
            wshed_info = gpd.read_file(geom_path)

        self.geometry = wshed_info.geometry.values[0]

        if not Path(self.data_dir).is_dir():
            try:
                import os

                os.mkdir(self.data_dir)
            except OSError:
                print("input directory cannot be created: {:s}".format(
                    self.data_dir))

        def mrlc_url(service):
            if service == "impervious":
                s = "NLCD_2016_Impervious_L48"
            elif service == "cover":
                s = "NLCD_2016_Land_Cover_L48"
            elif service == "canopy":
                s = "NLCD_2016_Tree_Canopy_L48"
            return ("https://www.mrlc.gov/geoserver/mrlc_display/" + s +
                    "/wms?service=WMS&request=GetCapabilities")

        urls = {
            "impervious": mrlc_url("impervious"),
            "cover": mrlc_url("cover"),
            "canopy": mrlc_url("canopy"),
        }

        params = {}
        for data_type, url in urls.items():
            data = Path(self.data_dir, f"{data_type}.geotiff")
            if Path(data).exists():
                print(f"Using existing {data_type} data file: {data}")
            else:
                bbox = self.geometry.bounds
                height = int(
                    np.abs(bbox[1] - bbox[3]) / np.abs(bbox[0] - bbox[2]) *
                    self.width)
                print(f"Downloadin {data_type} data from NLCD 2016 database")
                wms = WebMapService(url, version="1.3.0")
                try:
                    img = wms.getmap(
                        layers=list(wms.contents),
                        srs="epsg:4326",
                        bbox=bbox,
                        size=(self.width, height),
                        format="image/geotiff",
                        transparent=True,
                    )
                except ConnectionError:
                    raise ("Data is not availble on the server.")

                with open(data, "wb") as out:
                    out.write(img.read())

                print(f"{data_type} data was downloaded successfuly" +
                      f" and saved to {data}")

            categorical = True if data_type == "cover" else False
            params[data_type] = rasterstats.zonal_stats(
                self.geometry,
                data,
                categorical=categorical,
                category_map=NLCD().values)[0]

        self.impervious = params["impervious"]
        self.canopy = params["canopy"]
        self.cover = params["cover"]

    def separate_snow(self, prcp, tmean, tcr=0.0):
        """Separate snow and rain from the precipitation.

        The separation is based on a critical temperature (C) with the default
        value of 0 degree C.
        """
        return _separate_snow(prcp, tmean, tcr)

    def plot(self, Q_dict=None, figsize=(13, 12), threshold=1e-3, output=None):
        """Plot hydrological signatures with precipitation as the second axis.

        Plots includes daily, monthly and annual hydrograph as well as
        regime curve (monthly mean) and flow duration curve. The input
        discharges are converted from cms to mm/day based on the watershed
        area.

        Parameters
        ----------
        daily_dict : dict or dataframe
            A series containing daily discharges in m$^3$/s.
            A series or a dictionary of series can be passed where its keys
            are the labels and its values are the series.
        figsize : tuple
            Width and height of the plot in inches. The default is (8, 10)
        threshold : float
            The threshold for cutting off the discharge for the flow duration
            curve to deal with log 0 issue. The default is 1e-3.
        output : string
            Path to save the plot as png. The default is `None` which means
            the plot is not saved to a file.
        """
        from hydrodata.plotter import plot

        if Q_dict is None:
            Q_dict = self.climate["qobs (cms)"]

        plot(
            Q_dict,
            self.climate["prcp (mm/day)"],
            self.DASqKm,
            self.wshed_name,
            figsize=figsize,
            threshold=threshold,
            output=output,
        )
        return

    def plot_discharge(
        self,
        Q_dict=None,
        title="Streaflow data for the watersheds",
        figsize=(13, 12),
        threshold=1e-3,
        output=None,
    ):
        """Plot hydrological signatures without precipitation.

        The plots include daily, monthly and annual hydrograph as well as
        regime curve (monthly mean) and flow duration curve.

        Parameters
        ----------
        daily_dict : dict or series
            A series containing daily discharges in m$^3$/s.
            A series or a dictionary of series can be passed where its keys
            are the labels and its values are the series.
        title : string
            Plot's supertitle.
        figsize : tuple
            Width and height of the plot in inches. The default is (8, 10)
        threshold : float
            The threshold for cutting off the discharge for the flow duration
            curve to deal with log 0 issue. The default is 1e-3.
        output : string
            Path to save the plot as png. The default is `None` which means
            which means the plot is not saved to a file.
        """
        from hydrodata.plotter import plot_discharge

        if Q_dict is None:
            Q_dict = self.climate["qobs (cms)"]

        plot_discharge(
            Q_dict,
            self.DASqKm,
            title,
            figsize=figsize,
            threshold=threshold,
            output=output,
        )
        return


@njit(parallel=True)
def _separate_snow(prcp, tmean, tcr=0.0):
    """Separate snow and rain based on a critical temperature."""
    nt = prcp.shape[0]
    pr = np.zeros(nt, np.float64)
    ps = np.zeros(nt, np.float64)
    for t in prange(nt):
        if tmean[t] > tcr:
            pr[t] = prcp[t]
            ps[t] = 0.0
        else:
            pr[t] = 0.0
            ps[t] = prcp[t]
    return pr, ps


def get_nhd(gis_dir):
    """Download and extract NHDPlus V2.1 database."""
    gis_dir = Path(gis_dir)

    if not gis_dir.is_dir():
        try:
            import os

            os.mkdir(gis_dir)
        except OSError:
            print(f"{gis_dir} directory cannot be created")

    print(f"Downloading USGS gage information data to {str(gis_dir)}")
    base = "https://s3.amazonaws.com/edap-nhdplus/NHDPlusV21/" + \
        "Data/NationalData/"
    dbname = [
        "NHDPlusV21_NationalData_GageInfo_05.7z",
        "NHDPlusV21_NationalData_GageLoc_05.7z",
    ]

    for db in dbname:
        download_extract(base + db, gis_dir)
    return gis_dir.joinpath("NHDPlusNationalData")


class DownloadProgressBar(tqdm):
    """A tqdm-based class for download progress."""
    def update_to(self, b=1, bsize=1, tsize=None):
        """Inspired from a tqdm example.

        Parameters
        ----------
        b : int, optional
            Number of blocks transferred so far [default: 1].
        bsize : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize : int, optional
            Total size (in tqdm units). If [default: None] or -1,
            remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url, out_dir):
    """Progress bar for downloading a file."""
    with DownloadProgressBar(unit="B",
                             unit_scale=True,
                             miniters=1,
                             desc=url.split("/")[-1]) as t:
        urllib.request.urlretrieve(url,
                                   filename=Path(out_dir,
                                                 url.split("/")[-1]),
                                   reporthook=t.update_to)


def download_extract(url, out_dir):
    """Download and extract a `.7z` file."""
    import py7zr

    file = Path(out_dir).joinpath(url.split("/")[-1])
    if file.exists():
        py7zr.unpack_7zarchive(str(file), str(out_dir))
        print(f"Successfully extracted {file}.")
    else:
        download_url(url, out_dir)
        py7zr.unpack_7zarchive(str(file), str(out_dir))
        print(f"Successfully downloaded and extracted {str(file)}.")


def get_h5data(h5_file, dbname):
    """Read HDF5 file and return it as a Pandas dataframe."""
    import tables

    with tables.open_file(h5_file, "r") as db:
        return db.root[dbname][:]

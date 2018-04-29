# Documentation

## Submit

```shell
python submit.py file.csv
```

## Data

aq

```
Beijing_AirQuality_Stations_cn.xlsx
beijing_17_18_aq.csv
beijing_201802_201803_aq.csv
London_AirQuality_Stations.csv
London_historical_aqi_forecast_stations_20180331.csv
London_historical_aqi_other_stations_20180331.csv
```

me

```
beijing_17_18_meo.csv
beijing_201802_201803_me.csv
Beijing_grid_weather_station.csv
Beijing_historical_meo_grid.csv
London_historical_meo_grid.csv
London_grid_weather_station.csv
```

## Init

```
python3 init.py （运行前将csv文件header中的单位去掉）

beijing_data.pkl
type : numpy 2D array
axis 0:
        35 air quality stations (order is consistent with Beijing_AirQuality_Stations.xlsx) * 6 air pollution (PM2.5 PM10 NO2 CO O3 SO2)
        18 weather stations (alphabetical order) * 5 meo features (temperature pressure humidity wind_direction wind_speed)
        651 grids * 5 meo features
axis 1:
        hourly sequence
        start datetime: 2017-01-01 0:00:00
        end datetime: 2018-04-01 0:00:00
        

london_data.pkl
type : numpy 2D array
axis 0:
       13 prediction stations (order is consistent with London_AirQuality_Stations.csv) * 3 air pollution (PM2.5 PM10 NO2)
       11 other stations (order is consistent with London_AirQuality_Stations.csv) * 3 air pollution (PM2.5 PM10 NO2)
       861 grids * 5 meo features
axis 1:
       hourly sequence
       start datetime: 2017-01-01 0:00:00
       end datetime: 2018-03-31 23:00:00



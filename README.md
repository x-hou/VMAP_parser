## NASDAQ ITCH50 Dataset Parser

### Usage

This program can calculate VWAP per hour based on NASDAQ ITCH50 dataset.

To run this program, put "01302019.NASDAQ_ITCH50.gz" file in the same folder with "parser.py", open terminal and run
```
Python3 parser.py
```
The output will be stored as "vwap_01302019.csv" on the same folder.

### [Introduction of NASDAQ ITCH50 Dataset](http://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHspecification.pdf)

NasdaqTotalView--ITCH is a direct data feed product offered by The Nasdaq Stock Market,LLC.

"01302019.NASDAQ_ITCH50.gz" can be downloaded from <ftp://emi.nasdaq.com/ITCH/Nasdaq_ITCH/>

### [What is VWAP](https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:vwap_intraday)

Volume-Weighted Average Price (VWAP) is exactly what it sounds like: the average price weighted by volume.VWAP equals the dollar value of all trading periods divided by the total trading volume for the current day.The calculation starts when trading opens and ends when it closes.

Because it is good for the current trading day only, intraday periods and data are used in the calculation.

### Requirement
    Python >= 3.0
    Pandas >= 0.24

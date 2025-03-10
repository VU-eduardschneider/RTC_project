# Cases
This folder contains three cases which were created to showcase the functionalities of RTC for a Master's thesis. Below is a brief description of each case and how they were ran.

## Case 1 - Data over IP
This case study generates row by row with `feature9.csv` data. To run this case study, run `rtc_main.py` in the main folder and `ip_server.py` in the Case 1 folder. Then, use IP connect to connect to IP address 127.0.0.1 and port 5000.

## Case 2 - Streaming PageViews data
Similarly to Case 1, rung `gz_server.py` and connect to IP address 127.0.0.1 and port 5000.

## Case 3 - Streaming SQLite database data
For Case 3, the data is already stored in the main folder as `sensor_data.bd`. Run `rtc_main.py` with the SQLite connector. Simultaneously, add data with INSERT statements or db transformations to see the changes to row data in real-time within RTC.

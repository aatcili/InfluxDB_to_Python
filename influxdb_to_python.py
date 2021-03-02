# lets import the required libraries
from influxdb_client import InfluxDBClient
import pandas as pd

# need some information about your influxdb account
my_token = "my_token"
my_org = "my_organisation"
bucket = "my_bucket"

query= '''
from(bucket: "Your_bucket_name")
  |> range(start: -3d, stop:now())  
  |> filter(fn: (r) => r["_measurement"] == "Your_measurement")
  |> filter(fn: (r) => r["TAG"] == "Your_Tag_name")
  |> filter(fn: (r) => r["_field"] == "Your_field_name")
  |> sort(columns:["_time"], desc: false )'''

# lets define the client
client = InfluxDBClient(url="http://localhost:9000", token=my_token, org=my_org, debug=False)

# lets get the results as dataframe. Be aware, If your results has more than one table, you will have a list. 
# And each element of this list will be a dataframe 
system_stats = client.query_api().query_data_frame(query=query) # check if its a dataframe or list
# see the result
display(system_stats)

# if its a list, you can use this codes to see the graphs:
for i in range(len(system_stats)):
    DataIO = system_stats[i]
#    DataIO.drop(['_start', '_stop', 'result', 'table'], axis=1, inplace=True)
    DataIO.rename(columns={'_time': 'time', '_value': 'value'}, inplace=True)
    DataIO = DataIO.astype({"machineID": int})
    DataIO = DataIO.sort_values('time')
    DataIO.set_index("time", inplace=True)
    plt.figure(figsize=(14,8))
    plt.plot(DataIO.value)

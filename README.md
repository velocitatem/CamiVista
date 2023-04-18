# CamiVista (CV)


https://user-images.githubusercontent.com/60182044/232873538-5a0e2b2f-12ab-4a06-a7f4-c7ff084703f9.mp4



![Figure_1.png](Figure_1.png)

  > Why does Spain have so many great highways?

This project aims to track traffic in Spain and provide a visualization of the traffic in real time. The data is obtained from the [DGT](https://opendata.dgt.es/) (Dirección General de Tráfico).

Over time, with enough data, we might be able to infer the general migration patterns of the Spanish population. Identify dead zones, and even predict traffic jams.


## How does it work?
1. An algorithm downloads the data from the DGT API.
2. Each image is processed and all the vehicles are counted.
3. The data is stored in a database.
4. The data is visualized in a web application using a map of Spain.

### Long-term Analysis
1. The above process is repeated every 40 minutes (by default).
2. The data is stored in the database and can then be used for long-term analysis.
3. The data can be used to generate insights about the mobility patterns in Spain.

## Possible Insights
1. The number of vehicles on the roads can be used to determine the peak traffic hours.
2. The number of vehicles on the roads can also be used to identify traffic hotspots.
3. The data can be used to identify the most popular routes for drivers.
4. The data can also be used to measure the effects of public policies on traffic.

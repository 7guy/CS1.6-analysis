# CS 1.6 Player Performance Dashboard

## Project Overview

This project aims to provide data-driven insights into gameplay performance, enabling players to improve their strategies and make informed decisions. By analyzing game logs, the dashboard helps players understand their performance, identify strengths and weaknesses, and optimize their gameplay based on detailed metrics.

![csdash1](https://github.com/user-attachments/assets/7f514f19-d0cc-4a2a-b15f-d3c71956c7e7)
![csdash2](https://github.com/user-attachments/assets/aa595f33-88d4-4da4-a749-2bfee46847bd)

## Setup
1. Before running the analysis, you need to add two essential plugins to your game. These plugins log important data regarding kill's distance and headshots, which is later parsed and analyzed.
Plugins to add:
 - kill-distance2.sma
 - headshot_logger2.sma
   
2. under 'utils' folder run the script that add the plugin to the game:
   
   ```python utils/add_plugin.py -f X.sma```
   
4. Handle the log files and insert them to the DB:

  ```python logs/copy.py```

  ```python logs/parse.py```

  ```python database/msg2db.py``` (demand DB password)


4. Run the Dashboard:
   
```python -m streamlit run dashboard/run.py```



## Project Pipeline

The following pipeline illustrates the end-to-end process of data collection, analysis, and visualization:
![image](https://github.com/user-attachments/assets/5053024c-cf24-4162-b125-3251d119afb2)

## Metrics

These key metrics give a clear look at your gameplay performance. They focus on things like kills, weapon use, and accuracy, helping you spot what you're doing well and where you can get better.

1. Kill-Death Ratio (KDR)
Displays the KDR percentage to assess overall performance.

2. Kills and Deaths per Weapon
Tracks the number of kills and deaths for each weapon.

3. Kills and Deaths per Distance
Shows how effective you are at various distances.

4. Average Kill and Death Distance per Weapon
Displays the average distance of kills and deaths for each weapon, offering insights into weapon effectiveness by range.

5. Headshot Rate
Measures the percentage of kills that were headshots.

6. Headshot Rate per Day for Major Weapons
Tracks daily headshot rates for AK-47, M4A1, and Deagle to monitor accuracy over time.






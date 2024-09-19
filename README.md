# CS 1.6 Game Performance Analysis Dashboard

## Project Overview

This project aims to provide data-driven insights into gameplay performance, enabling players to improve their strategies and make informed decisions. By analyzing game logs, the dashboard helps players understand their performance, identify strengths and weaknesses, and optimize their gameplay based on detailed metrics.

## Setup
1. Before running the analysis, you need to add two essential plugins to your game. These plugins log important data regarding kill's distance and headshots, which is later parsed and analyzed.
Plugins to add:
 - kill-distance.sma
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


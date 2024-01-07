# Intraday-GARCH-strategy-in-Python
The script implements an intraday trading strategy, combining GARCH for daily volatility forecasting and intraday technical indicators. It generates signals based on prediction premiums, integrating daily and intraday data. The strategy's cumulative returns are visualized for performance evaluation.



### Overview:
This Python script implements an intraday trading strategy, merging GARCH daily volatility forecasting with intraday technical indicators. The strategy generates signals based on prediction premiums, combining daily and intraday data for enhanced decision-making.


### Files:
1. **`intraday_trading_strategy.py`**: Python script containing the intraday trading strategy implementation.

2. **Data Files**:
   - `daily_data.csv`: Simulated daily financial data.
   - `5min_data.csv`: Simulated 5-minute intraday data.

### Dependencies:
- `pandas`, `matplotlib`, `arch`, `pandas_ta`, `numpy`

### Instructions:
1. Ensure Python and required libraries are installed.
2. Adjust the `data_folder` variable in the script to the correct path.
3. Run the script (`intraday_trading_strategy.py`).

### Output:
- The script generates visualizations of daily signals and cumulative returns of the intraday trading strategy.

![Screenshot 2024-01-07 at 12 40 14 AM](https://github.com/mayank-bharwal/Intraday-GARCH-strategy-in-Python/assets/119955673/16e51cde-f4a8-43a0-a2b6-35b8f803b91b)


![Screenshot 2024-01-07 at 12 41 15 AM](https://github.com/mayank-bharwal/Intraday-GARCH-strategy-in-Python/assets/119955673/5b2bbe4e-717a-439f-b75d-f1ac65b27127)


### Notes:
- The strategy combines GARCH for volatility forecasting with intraday technical indicators for robust decision-making.
- Results may vary based on market conditions and simulated data.

### Author:
Mayank Bharwal

### Date:
7Th January,2024

Feel free to reach out for any inquiries or improvements. Happy trading!

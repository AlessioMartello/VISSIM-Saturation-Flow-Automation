# Import relevant modules
from datetime import datetime
import pathlib
import pandas as pd
import time
import openpyxl

maximum_headway_accepted = int(input("Enter the maximum headway accepted as an integer: "))

start = time.time()
results = pd.DataFrame(columns=['ID', "Saturation_flow"])
for path in pathlib.Path("Special_eval_files").iterdir():
    try:
        my_cols = [str(col) for col in range(100)]
        use_cols = my_cols[3:]  # We are only concerned with the fourth column, onwards.

        # Read the file, delimeter set as space separated
        df = pd.read_csv(path, sep="\s+|:", names=my_cols, header=None, engine="python", skiprows=10, index_col=None,
                         usecols=use_cols)

        # Remove excess empty columns
        df.dropna(axis="columns", how="all", inplace=True)

        # Make a list of Column names using the length of the df
        col_names = ["Column " + col for col in df]

        # Assign the names to the df
        df.columns = col_names

        # Replace null values with zeros
        df.fillna(0, inplace=True)

        # Remove the brackets and parenthesis so that data can be returned as int
        for col_name in col_names:
            df[col_name] = df[col_name].astype(str).str.replace("(", "-")
            df[col_name] = df[col_name].str.replace(")", "")
            df[col_name] = df[col_name].str.replace("]", "")

        # Make the data numerical
        for col_name in col_names:
            df[col_name] = pd.to_numeric(df[col_name])

        # The Macro doesnt count anything above the maximum acceptable headway. So set anything above this to zero,
        # so it gets ignored.
        df[df > maximum_headway_accepted] = 0

        # The Macro rounds the values. Replicate this.
        df = df.round()

        # Convert to numpy array for easier and faster manipulation.
        df = df.to_numpy()

        # Find the row which doesnt contain useful data, from the shape of the array. This is constant throughout
        # data-sets.
        number_of_rows = df.shape[0]
        vehicle_position_index_row = number_of_rows - 3

        # Loop through each row. If the value (discharge rate) is over the headway limit, go to the next line.
        # Otherwise increase the count and add this discharge rate to the cumulative_discharge_rate. Skip the row
        # containing un-useful data and after this row, shift the loop one column to the right, to account for the
        # indent in the data.
        cumulative_discharge_rate = 0
        discharge_rate_count = 0
        current_row = 0
        for row in df:
            current_row += 1
            if current_row == vehicle_position_index_row:
                continue
            elif current_row > vehicle_position_index_row:
                for col in row[1:]:
                    if 0 < col <= maximum_headway_accepted:
                        cumulative_discharge_rate = cumulative_discharge_rate + col
                        discharge_rate_count += 1
                    else:
                        break
            else:
                for col in row:
                    if 0 < col <= maximum_headway_accepted:
                        cumulative_discharge_rate = cumulative_discharge_rate + col
                        discharge_rate_count += 1
                    else:
                        break

        # Perform the Saturation Flow calculation
        sat_flow = round(3600 / (cumulative_discharge_rate / discharge_rate_count))

        # print(str(path)[-3:] + " Satflow: " + str(sat_flow))

        # Append the results per stop-line (file suffix) to a dataFrame
        results = results.append({'ID': str(path)[-3:], "Saturation_flow": sat_flow, "Number of measurements": discharge_rate_count}, ignore_index=True)
    except:
        print("Error on file: " + str(path))
end = time.time()
print(end - start)

# Group the same stop-lines together using the file suffix and get the average of the Saturation flows and the total
# number of measurements for that saturation flow.
results = results.groupby("ID").agg({"Saturation_flow": "mean", "Number of measurements": "sum"})

now = datetime.now()

results.to_excel("Satflow_results_" + now.strftime("%d-%m_%H.%M") + ".xlsx")
# print("Count: " + str(count))
# print("Total: " + str(cumulative_discharge_rate))

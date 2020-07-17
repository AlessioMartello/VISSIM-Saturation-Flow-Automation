# Import relevant modules
import pathlib
import pandas as pd

maximum_headway_accepted = int(input("Enter the maximum headway accepted as an integer: "))

for path in pathlib.Path("Special_eval_files").iterdir():
    try:
        my_cols = [str(i) for i in range(25)]
        use_cols = my_cols[3:] #We are only concerned with the fourth column, onwards.

        # Read the file, delimeter set as space separated
        df= pd.read_csv(path, sep="\s+|;|:", names=my_cols, header=None, engine="python", skiprows=10, index_col=None, usecols=use_cols)

        # Remove excess empty columns
        df.dropna(axis="columns", how="all", inplace=True)

        # Make a list of Column names using the length of the df
        names = ["Column " + i for i in df]

        # Assign the names to the df
        df.columns = names

        # Replace null values with zeros
        df=df.fillna(0)

        # Remove the brackets and parenthesis so that data can be returned as int
        for i in names:
            df[i]=df[i].astype(str).str.replace("(", "-")
            df[i]=df[i].str.replace(")", "")
            df[i]=df[i].str.replace("]", "")

        # Make the data numerical
        for i in names:
            df[i]=pd.to_numeric(df[i])

        # The Macro doesnt count anything above the maximum acceptable headway. So set anything above this to zero, so ot gets ingored.
        df[df>maximum_headway_accepted] =0

        # The Macro rounds the values. Replicate this.
        df=df.round()

        # Convert to numpy array for easier and faster manipulation.
        df=df.to_numpy()

        # Find the row which doesnt contain useful data, from the shape of the array. This is constant throughout datasets.
        number_of_rows=df.shape[0]
        vehicle_position_index_row = number_of_rows - 3

        # Loop through each row. If the value (discharge rate) is over the headway limit, go to the next line. Otherwise increase the count and add this discharge rate to the total.
        # Skip the row containing unuseful data and after this row, shift the loop one column to the right, to account for the indent in the data.
        total=0
        count=0
        row=0
        for i in df:
            row+=1
            if row==vehicle_position_index_row:
                continue
            elif row>vehicle_position_index_row:
                for j in i[1:]:
                    if 0< j <= maximum_headway_accepted:
                        total = total +j
                        count +=1
                    else:
                        break
            else:
                for j in i:
                    if 0< j <= maximum_headway_accepted:
                        total = total +j
                        count +=1
                    else:
                        break

        # Perform the Saturation Flow calculation
        sat_flow = round(3600/(total/count))

        print("File: " + str(path) + " Satflow: " +str(sat_flow))
    except:
        print("Error on file: " + str(path))
# print("Count: " + str(count))
# print("Total: " + str(total))


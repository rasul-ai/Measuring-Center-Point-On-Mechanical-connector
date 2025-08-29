import pandas as pd

def calc_diff(predicted_data, measured_data):
    # Rearrange the columns (assume the input columns are already properly named)
    data1 = predicted_data[["Center_X", "Center_Y"]]
    data2 = measured_data[["Measured_data_x", "Measured_data_y"]]

    # Initialize a list to store the matched rows
    matched_data = []

    # Nested loop to calculate the sum of differences for each row in data1
    for i, row1 in data1.iterrows():
        min_diff_sum = float('inf')
        min_row2 = None

        # Loop through all rows in data2
        for j, row2 in data2.iterrows():
            # Calculate absolute differences in x and y
            x_diff = abs(row1["Center_X"] - row2["Measured_data_x"])
            y_diff = abs(row1["Center_Y"] - row2["Measured_data_y"])

            # Sum the differences
            diff_sum = x_diff + y_diff

            # If this is the smallest difference, update the minimum
            if diff_sum < min_diff_sum:
                min_diff_sum = diff_sum
                min_row2 = row2

        # After finding the closest match, append it to the matched data
        matched_data.append({
            "Measured_data_x": min_row2["Measured_data_x"],
            "Measured_data_y": min_row2["Measured_data_y"],
            "Center_X": row1["Center_X"],
            "Center_Y": row1["Center_Y"],
            "X_diff": min_row2["Measured_data_x"] - row1["Center_X"],
            "Y_diff": min_row2["Measured_data_y"] - row1["Center_Y"]
        })

    # Convert the matched data list back into a DataFrame
    matched_df = pd.DataFrame(matched_data)
    
    return matched_df

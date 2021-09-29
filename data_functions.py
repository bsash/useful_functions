"""Some useful functions for importing, exporting, manipulating data.
"""
import csv
import pandas as pd

def read_csv_with_empty_values(file_name):
    """Meant to read a csv where each row represents some time-series.
    Returns a list with each element containing one time-series.
    """
    graph = []
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            tmp_row = pd.Series(row)
            tmp_row.replace([''], np.nan, inplace=True)
            tmp_row.dropna(inplace=True)
            app_row = tmp_row.astype('float')
            app_row = np.array(app_row)
            # Remove zeros at end
            if not app_row[-1]:
                app_row = app_row[0:(np.where(app_row[-10:] == 0)[0][0]-10)]
            graph.append(np.array(app_row))
    return graph
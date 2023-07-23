import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pandas as pd

def generate_paths(folder_path):
    """Generate a list of file paths for files named "aseg.stats" within a given folder.

        Parameters
        ----------
        folder_path : str
            The path to the folder to search for files.

        Returns
        -------
        list
            A list of file paths for files named "aseg.stats" within the specified folder.
        """

    file_paths = []
    
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for file_name in filenames:
            if file_name == "aseg.stats":
                file_path = os.path.join(dirpath, file_name)
                file_paths.append(file_path)

    return file_paths


def generate_table_volume(file_paths):
    """Generate a table of volume metrics from a list of file paths.

        Parameters
        ----------
        file_paths : list
            A list of file paths for files containing volume metrics.

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing the volume metrics extracted from the files.
            The DataFrame has columns: 'subject', 'StructName', 'SegId', 'NVoxels',
            'Volume_mm3', 'normMean', 'normStdDev', 'normMin', 'normMax', 'normRange'.
            'subject' represents the name of the subject, 'StructName' represents the
            structure name, 'SegId' represents the segmentation ID, 'NVoxels' represents
            the number of voxels, 'Volume_mm3' represents the volume in cubic millimeters,
            'normMean' represents the normalized mean, 'normStdDev' represents the
            normalized standard deviation, 'normMin' represents the normalized minimum,
            'normMax' represents the normalized maximum, and 'normRange' represents the
            normalized range.
        """

    dfs = []

    for file_path in file_paths:
        extracted_lines = []
        with_col_headers = False

        with open(file_path, 'r') as file:
            for line in file:
                if with_col_headers:
                    extracted_lines.append(line.strip())
                elif line.startswith("# ColHeaders  Index SegId NVoxels Volume_mm3 StructName normMean normStdDev normMin normMax normRange"):
                    extracted_lines.append(line.strip())
                    with_col_headers = True

        df2 = pd.DataFrame([x.split() for x in extracted_lines], columns=extracted_lines[0].split())
        df2 = df2.drop(0)
        df2 = df2.rename(columns={
            '#': 'Index',
            'ColHeaders': 'SegId',
            'Index': 'NVoxels',
            'SegId': 'Volume_mm3',
            'NVoxels': 'StructName',
            'Volume_mm3': 'normMean',
            'StructName': 'normStdDev',
            'normMean': 'normMin',
            'normStdDev': 'normMax',
            'normMin': 'normRange'
        })
        df2 = df2.drop(df2.columns[0], axis=1)
        df2 = df2.loc[:, ~df2.columns.duplicated()]
        df2 = df2.reset_index(drop=True)
        df2 = df2[['StructName', 'SegId', 'NVoxels', 'Volume_mm3', 'normMean', 'normStdDev', 'normMin', 'normMax', 'normRange']]

        
        with open(file_path, "r") as file:
            lines = file.readlines()
        for line in lines:
            if line.startswith("# subjectname"):
                subject_name = line.strip("# subjectname").strip()
                break

        if subject_name is not None:
            df2.insert(0, "subject", subject_name) 

        dfs.append(df2)

    header_df = pd.DataFrame(columns=['subject', 'StructName', 'SegId', 'NVoxels', 'Volume_mm3', 'normMean', 'normStdDev', 'normMin', 'normMax', 'normRange'])
    dfs.append(header_df)

    dfs = pd.concat(dfs, ignore_index=True)

    return dfs

def generate_volume_dictionary(df):
    volume_dict = {}
    
    grouped = df.groupby(['StructName', 'Volume_mm3', 'normMean'])

    def process_group(group):
        struct_name = group['StructName'].iloc[0].replace('_', ' ')
        volume = group['Volume_mm3'].iloc[0]
        norm_mean = group['normMean'].iloc[0]
        
        return {'value': f"{volume} mm3", 'normMean': f"{norm_mean} mm3"}

    volume_dict['Region'] = {'value': 'value', 'normMean': 'normMean'}  # Ajouter la première ligne au dictionnaire

    for _, group_df in grouped:
        values_dict = process_group(group_df)
        volume_dict[group_df['StructName'].iloc[0]] = values_dict

    return volume_dict
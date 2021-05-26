import json
import glob
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys

def create_data_frame(raw_data):
    data = {}
    data['latex'] = []
    data['seq_len'] = []
    data['font'] = []
    data['image_ratio'] = []
    data['image_width'] = []
    data['image_height'] = []
    all_latex_lst = []
    for image in raw_data:
        data['latex'].append(image['image_data']['full_latex_chars'])
        data['seq_len'].append(len(image['image_data']['full_latex_chars']))
        data['font'].append(image['font'])
        data['image_ratio'].append(round(image['image_data']['width'] / image['image_data']['height'],1))
        data['image_width'].append(image['image_data']['width'])
        data['image_height'].append(image['image_data']['height'])
        all_latex_lst = all_latex_lst + image['image_data']['full_latex_chars']
        df = pd.DataFrame.from_dict(data)
    return df, all_latex_lst

for i in range(1, len(sys.argv)):
    with open(file = sys.argv[i]) as f:
        raw_data = json.load(f)

        df, all_latex_lst = create_data_frame(raw_data)

        print(df.columns)

        print(df.describe())

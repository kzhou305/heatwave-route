import pandas as pd
import matplotlib.pyplot as plt

def plot_comfort_trend(nid_list, seg_csv="../data/reg_result201.csv"):
    df = pd.read_csv(seg_csv)
    df = df[df['nid'].isin(nid_list)].sort_values("nid")
    df['comfort'] = df['pct_tree']*0.4 + df['pct_sky']*0.3 - df['pct_road']*0.3
    df.plot(x='nid', y=['pct_tree', 'pct_road', 'pct_sky', 'comfort'])
    plt.savefig("../docs/comfort_trend.png")

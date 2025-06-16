import pandas as pd
import matplotlib.pyplot as plt

def plot_seg_index(seg_csv, nid_list):
    df = pd.read_csv(seg_csv)
    df = df[df['nid'].isin(nid_list)].sort_values('nid')
    plt.plot(df['nid'], df['pct_tree'], label='Tree')
    plt.plot(df['nid'], df['pct_building'], label='Building')
    plt.plot(df['nid'], df['pct_road'], label='Road')
    plt.xlabel('NID')
    plt.ylabel('Percent')
    plt.legend()
    plt.tight_layout()
    plt.savefig('../output/comfort_chart.png')

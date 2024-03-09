"""
Created on Tue Dec 12 12:19:33 2023

@author: gianlucabollo
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter

file_path = '/Users/gianlucabollo/Documents/Projects/NYC Electricity Project/nycElectricityDataset.csv'

def initial_checks(data_frame):
    print(data_frame.info())
    print(data_frame.head())
    print(data_frame.describe())
    print(data_frame.isnull().sum())
    for column in data_frame.columns:
        print(data_frame[column].value_counts())
    
def clean_data(data_frame):
    clean_df = data_frame.drop(['EDP', 'UMIS BILL ID', 'Account Name', 'Bill Analyzed',
                                'Rate Class', 'Meter Number', 'AMP #', 'RC Code', 'TDS #',
                                'Meter Scope', 'Location'], axis=1)
    clean_df = clean_df.dropna()
    clean_df = clean_df[clean_df['Borough'] != "FHA"]
    clean_df = clean_df[clean_df['Borough'] != "NON DEVELOPMENT FACILITY"]
    
    clean_df['Revenue Month'] = pd.to_datetime(clean_df['Revenue Month'])
    clean_df = clean_df.loc[(clean_df != 0).any(axis=1)]
    return clean_df

def subset_by_borough(data_frame):
    unique_boroughs = data_frame['Borough'].unique()
    borough_subsets = {}
    for borough in unique_boroughs:
        borough_subsets[borough] = data_frame[data_frame['Borough'] == borough]
    return borough_subsets

def visualize_nyc_usage(data_frame):
    plt.figure(figsize=(12, 6)) 
    
    plt.subplot(1, 2, 1)
    plt.hist(data_frame['Consumption (KWH)'], bins = 50)
    plt.title('Distribution of monthly energy consumption in NYC')
    plt.xlabel('Total Consumption (KWH)')
    plt.ylabel('Frequency')
    plt.ticklabel_format(style='plain', axis='both')

    plt.subplot(1, 2, 2)
    plt.hist(data_frame['Consumption (KW)'], bins= 50, color='orange')  
    plt.title('Distribution of the energy usage rate in NYC')  
    plt.xlabel('Rate of consumption (KW)')
    plt.ylabel('Frequency')
    plt.tight_layout()
    
    plt.show()
    
def visualize_borough_usage(borough_dict):
    for borough_name, subset_df in borough_dict.items(): 
        plt.figure(figsize=(12, 6)) 
        
        plt.subplot(1, 2, 1)
        plt.hist(subset_df['Consumption (KWH)'], bins = 25)
        plt.title(f'Distribution of monthly energy consumption in {borough_name}')
        plt.xlabel('Total consumption (KWH)')
        plt.ylabel('Frequency')
        plt.ticklabel_format(style='plain', axis='both')

        plt.subplot(1, 2, 2)
        plt.hist(subset_df['Consumption (KW)'], bins=25, color='orange')  
        plt.title(f'Distribution of the energy consumption rate in {borough_name}')  
        plt.xlabel('Rate of consumption (KW)')
        plt.ylabel('Frequency')
        plt.tight_layout()
        
        plt.show()
        
def describe_nyc_usage(data_frame):
    return (f'The total energy consumption for NYC is {data_frame["Consumption (KWH)"].sum():,.0f} KWH. '
          f'The median and mean monthly energy usage in NYC is {data_frame["Consumption (KWH)"].median():,.0f} '
          f'and {data_frame["Consumption (KWH)"].mean():,.0f} KWH, respectively.')

def describe_borough_usage(borough_dict):
    descripString = ''
    for borough_name, subset_df in borough_dict.items(): 
        descripString += (f'The total energy consumption for {borough_name} is {subset_df["Consumption (KWH)"].sum():,.0f} KWH. '
                          f'The median and mean monthly energy usage in {borough_name} is {subset_df["Consumption (KWH)"].median():,.0f} '
                          f'and {subset_df["Consumption (KWH)"].mean():,.0f} KWH, respectively.\n')
    return descripString

def visualize_borough_comparison(borough_dict):
    means = [subset_df['Consumption (KWH)'].mean() for subset_df in borough_dict.values()]
    medians = [subset_df['Consumption (KWH)'].median() for subset_df in borough_dict.values()]
    totals = [subset_df['Consumption (KWH)'].sum() for subset_df in borough_dict.values()]
    labels = list(borough_dict.keys())

    bar_width = 0.25 
    r1 = np.arange(len(labels))
    r2 = [x + bar_width for x in r1]
    r3 = [x + 2 * bar_width for x in r1]

    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.bar(r1, means, color='blue', width=bar_width, label='Mean')
    ax1.bar(r2, medians, color='orange', width=bar_width, label='Median')
    
    ax1.set_ylabel('Mean and Median Consumption (KWH)')
    ax1.set_xticks([r + 1.5 * bar_width for r in r1])
    ax1.set_xticklabels(labels, ha='right')

    ax2 = ax1.twinx()
    ax2.bar(r3, totals, color='green', width=bar_width, label='Total')
    ax2.set_ylabel('Total Consumption (KWH, in billions)')

    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')

    plt.title('Mean, Median, and Total Energy Consumption by Borough')
    plt.show()
    
def time_series_analysis(data_frame):
    time_data = data_frame.set_index('Revenue Month')    
    
    monthly_consumption = time_data.resample('M').sum()
    monthly_consumption = monthly_consumption.loc[(monthly_consumption != 0).any(axis=1)]
    
    window_size = 12
    trend = monthly_consumption['Consumption (KWH)'].rolling(window=window_size, center=True).mean()

    plt.figure(figsize=(12, 12))

    plt.subplot(3, 1, 1)
    plt.plot(monthly_consumption.index, monthly_consumption['Consumption (KWH)'], label='Original')
    plt.title('NYC Energy Consumption Over Time')
    plt.ylabel('Consumption (KWH, by one hundred million)')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(monthly_consumption.index, trend, label='Trend')
    plt.xlabel('Time')
    plt.ylabel('Consumption (KWH, by one hundred million)')

    plt.legend()

    plt.tight_layout()
    plt.show()
 
def main():    
    raw_df = pd.read_csv(file_path)
    initial_checks(raw_df)
    
    clean_df = clean_data(raw_df)
    initial_checks(clean_df)
        
    borough_subset_dict = subset_by_borough(clean_df)    
    
    visualize_nyc_usage(clean_df)
    print(describe_nyc_usage(clean_df))
    
    visualize_borough_usage(borough_subset_dict)    
    visualize_borough_comparison(borough_subset_dict)
    print(describe_borough_usage(borough_subset_dict))
    
    time_series_analysis(clean_df)

if __name__ == '__main__':
    main()
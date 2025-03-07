#!/usr/bin/env python3
import argparse
import pandas as pd
import matplotlib.pyplot as plt

def load_and_plot(files, outfile):
  plt.figure(figsize=(12, 8))
  
  for file in files:
      # Read CSV file
      df = pd.read_csv(file)
      
      # Convert nanoseconds to milliseconds
      df['time_ms'] = df['time_ns'] / 1_000_000
      
      # Plot this dataset
      label = file.replace('.csv', '')  # Remove extension for legend
      plt.plot(df['height'], df['time_ms'], marker='o', markersize=3, label=label)
  
  plt.xlabel('Block Height')
  plt.ylabel('Time (ms)')
  plt.title('Bitcoin Core Reindex Performance Comparison')
  plt.grid(True, linestyle='--', alpha=0.7)
  plt.legend()
  
  # Save plot to disk
  plt.savefig(outfile)
  print("[PLOT] Graph saved as benchmark_results.png")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Plot benchmark results from multiple CSV files")
  parser.add_argument("outfile", help="File to save image to")
  parser.add_argument("files", nargs="+", help="CSV files containing benchmark data")
  
  args = parser.parse_args()
  load_and_plot(args.files, args.outfile)
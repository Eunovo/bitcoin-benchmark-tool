# Bitcoin Core Benchmark Tool

A tool for benchmarking Bitcoin Core's block validation performance across different commits.

## Overview

This tool consists of two main components:
- `bt-bench.py`: Runs Bitcoin Core with different commits and measures block validation time
- `bt-plot.py`: Generates performance comparison graphs from collected data

## Requirements

- Python 3.7+
- Required Python packages:
  ```
  pandas
  matplotlib
  ```
- Git
- CMake
- C++ compiler (GCC/Clang)
- Bitcoin Core source code

## Usage

1. Benchmark multiple commits:
```bash
python3 bt-bench.py <datadir> <stopheight> <commit1> <commit2> ... --args -par=2 -dbcache=450
```

Example:
```bash
python3 bt-bench.py ~/.bitcoin 8844533 master v24.0.1 v23.0 --args -par=4 -dbcache=4096
```

This will:
- Switch to each commit
- Build Bitcoin Core
- Run with specified parameters
- Generate CSV files with timing data

2. Generate comparison plot:
```bash
python3 bt-plot.py <commit1>_output.csv <commit2>_output.csv ... <commitN>_output.csv
```

## Output

- Each benchmark run creates a CSV file named `<commit>_output.csv`
- The plot script generates `benchmark_results.png`

## Important Notes

- The datadir should contain a fully synchronized Bitcoin blockchain
- Block at stopheight should be in the datadir
- Use `-assumevalid=0` to force full validation
- Building Bitcoin Core requires sufficient disk space
- Benchmarking can take significant time depending on hardware

## Advanced Usage

Customize Bitcoin Core parameters after --args:
```bash
python3 bt-bench.py ~/.bitcoin 884453 master --args -par=4 -dbcache=4096 -assumevalid=0 -checkblocks=100
```

Common parameters:
- `-par=n`: Number of script verification threads
- `-dbcache=n`: Database cache size in MiB
- `-assumevalid=0`: Disable assumed-valid blocks

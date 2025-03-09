# Bitcoin Core Benchmark Tool

A performance measurement tool for Bitcoin Core block validation across different commits.

## Prerequisites

- Python 3.7+ with pandas and matplotlib
- Git, CMake, and C++ compiler
- Bitcoin Core source code
- Synchronized blockchain data directory

## Tools

- `bt-bench.py`: Executes benchmarks across different commits, running multiple iterations
- `bt-plot.py`: Generates performance visualization graphs using average times

## Basic Usage

Run benchmark in source code directory:
```bash
./bt-bench.py <datadir> <stopheight> <commits...> [--runs N] [--args <bitcoin-core-args>]
```

Generate plot:
```bash
./bt-plot.py output.png <commit_1>.csv ... <commit_N>.csv
```

## Examples

Benchmark multiple versions:
```bash
./bt-bench.py ~/.bitcoin 800000 master v25.0 v24.0 --args -par=4 -dbcache=4096
```

Compare results:
```bash
./bt-plot.py comparison.png master.csv v25.0.csv v24.0.csv
```

## Parameter Sweep Benchmarking

Running with different thread counts:

```bash
./bt-bench.py ~/.bitcoin 800000 master v25.0 v24.0 --i 1 2 3 4 5 6 7 8 9 10 11 12 --args -par={i} -dbcache=4096
```

Compare results:
```bash
find *_*.csv | xargs ./bt-plot.py comparison.png
```

## Key Parameters

Benchmark script:
- `datadir`: Path to Bitcoin data directory
- `stopheight`: Block height to stop at
- `commits`: Git refs to benchmark
- `--runs`: Number of iterations per benchmark (default: 3)
- `--i`: Parameter values for sweep benchmarking
- `--args`: Additional Bitcoin Core arguments

## Output Format

The benchmark tool produces CSV files with the following columns:
- `max_ns`: Maximum time in nanoseconds across all runs
- `min_ns`: Minimum time in nanoseconds across all runs
- `avg_ns`: Average time in nanoseconds across all runs
- `height`: Block height

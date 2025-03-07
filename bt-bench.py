#!/usr/bin/env python3
import argparse
import os
import sys
import time

def parse_line(line: str):
  data = line.split(' ')

  if len(data) < 2:
    return (0, False)
  
  new_tip = 0
  shutdown = False
  
  if data[1] == 'UpdateTip:':
    height_dat = data[4].split('=')
    new_tip = int(height_dat[1])

  if data[1] == 'Shutdown:':
    shutdown = data[2] == 'done'
  
  return (new_tip, shutdown)

if __name__ == "__main__":
  parser = argparse.ArgumentParser("bench-tool")
  parser.add_argument("datadir")
  parser.add_argument("stopheight")
  parser.add_argument("targets", nargs="*")
  parser.add_argument("--args")

  args = None
  bitcoin_args = []
  try:
    bitcoin_args_index = sys.argv.index("--args")
    args = parser.parse_args(sys.argv[1:bitcoin_args_index])
    bitcoin_args = sys.argv[bitcoin_args_index+1:]
  except ValueError:
    # do nothing
    args = parser.parse_args(sys.argv[1:])

  datadir = args.datadir
  targets = args.targets
  numcores = len(os.sched_getaffinity(0))
  stopheight = int(args.stopheight)

  for target in targets:
    print("[BENCH-TOOL] Switching to "+target)
    os.system("git checkout "+target)
    print("[BENCH-TOOL] Building bitcoin")
    os.system("rm -rf build")
    os.system("cmake -B build -DENABLE_WALLET=OFF")
    os.system("cmake --build build -j {0}".format(numcores))
    
    target_out_dir = "{0}_output.csv".format(target)

    cmd = "build/src/bitcoind -datadir={0} -daemon=0 -networkactive=0 -prune=0 -reindex -stopatheight={1} {2}".format(datadir, stopheight, ' '.join(bitcoin_args))
    print("[BENCH-TOOL] Running: "+cmd)
    with open(target_out_dir, 'xt') as file:
      print("[BENCH-TOOL] Writing data to "+target_out_dir)
      file.write("time_ns,height\n")
      with os.popen(cmd) as output:
        start_time = time.time_ns()
        count = 0
        while count < (stopheight * 10): # Use limit to prevent inifinite loop
          (new_tip, shutdown) = parse_line(output.readline())
          duration_ns = time.time_ns() - start_time
          count += 1
          if shutdown:
            break
          if new_tip > 0:
            file.write("{0},{1}\n".format(duration_ns, new_tip))
  
  print("[BENCH-TOOl] Done")

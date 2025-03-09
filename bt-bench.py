#!/usr/bin/env python3
import argparse
import os
import sys
import time

def parse_line(line: str):
  new_tip = 0
  shutdown = False

  shutdown_msg = 'Shutdown: done'
  update_tip_msg = 'UpdateTip:'

  if (line[21:21+len(update_tip_msg)] == update_tip_msg):
    height_dat = []
    cursor = 113
    while cursor < len(line):
      char = line[cursor]
      height_dat.append(char)
      if (char == ' '):
        break
      cursor += 1

    new_tip = int(''.join(height_dat))

  if (line[21:21+len(shutdown_msg)] == shutdown_msg):
    shutdown = True
  
  return (new_tip, shutdown)

def parse_arg(arg: str, value):
  if (value == None):
    return arg
  try:
    index = arg.index("{i}")
    return "{0}{1}{2}".format(arg[:index], value, arg[index+3:])
  except ValueError:
    return arg

if __name__ == "__main__":
  parser = argparse.ArgumentParser("bench-tool")
  parser.add_argument("datadir")
  parser.add_argument("stopheight")
  parser.add_argument("targets", nargs="*")
  parser.add_argument("--i", nargs="+", default=[None])
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

  values = args.i

  for target in targets:
    print("[BENCH-TOOL] Switching to "+target)
    os.system("git checkout "+target)
    print("[BENCH-TOOL] Building bitcoin")
    os.system("rm -rf build")
    os.system("cmake -B build -DENABLE_WALLET=OFF")
    os.system("cmake --build build -j {0}".format(numcores))

    for value in values:
      target_outfile = "{0}.csv".format(target)
      if value != None:
        target_outfile = "{0}_{1}.csv".format(target, value)
      parsed_bitcoin_args = [parse_arg(arg, value) for arg in bitcoin_args]

      cmd = "build/src/bitcoind -datadir={0} -daemon=0 -networkactive=0 -prune=0 -reindex -stopatheight={1} {2}".format(datadir, stopheight, ' '.join(parsed_bitcoin_args))
      print("[BENCH-TOOL] Running: "+cmd)
      data = [(0,0) for i in range(stopheight)] # Reserve space for data
      with os.popen(cmd) as output:
        start_time = time.time_ns()
        count = 0
        while count < (stopheight * 10): # Use limit to remove the possibility of inifinite loop
          (new_tip, shutdown) = parse_line(output.readline())
          duration_ns = time.time_ns() - start_time
          count += 1
          if shutdown:
            break
          if new_tip > 0:
            data[new_tip - 1] = (duration_ns, new_tip)

      with open(target_outfile, 'xt') as file:
        print("[BENCH-TOOL] Writing data to "+target_outfile)
        file.write("time_ns,height\n")
        for line in data:
          file.write("{0},{1}\n".format(line[0], line[1]))
  
  print("[BENCH-TOOl] Done")

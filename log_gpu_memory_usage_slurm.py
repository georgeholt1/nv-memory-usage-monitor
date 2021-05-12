# Author: George K. Holt
# License: MIT
# Version: 0.2
"""
Part of NV Memory Usage Monitor.

This script can be used to log GPU memory usage around a SLURM job. See README
for usage instructions.
"""
import argparse
import os
import subprocess
import time



parser = argparse.ArgumentParser(
    prog='NV Memory Usage Monitor',
    description="Visualise GPU memory usage."
)
parser.add_argument(
    '-v', '--version', action='version', version='%(prog)s 0.2'
)
parser.add_argument(
    '-j', '--job-id', metavar='', required=True,
    help="SLURM job ID."
)
parser.add_argument(
    '-o', '--outdir', metavar='', default=os.getcwd(),
    help="Directory in which to create log. Defaults to current directory."
)
parser.add_argument(
    '-t', '--timestep', metavar='', default=2,
    help="How often to query the memory usage. Defaults to 2."
)
args = parser.parse_args()



if __name__ == "__main__":
    # check proposed output directory exists
    if not os.path.isdir(args.outdir):
        raise SystemExit(
            f"Proposed output directory {args.outdir} does not exist."
        )
    
    # periodically query squeue until job starts
    started = False
    while not started:
        print("Waiting for job to start (if not already started)")
        query = subprocess.run(
            ["sacct", "-j", f"{args.job_id}", "-o", "start,end", "-X"],
            stdout=subprocess.PIPE,
            universal_newlines=True
        )
        if not "Unknown" in query.stdout.splitlines()[2].split()[0]:
            started = True
            print("Job started")
        time.sleep(2)
        
    # log until job finishes
    print("Starting logging")
    log_file = os.path.join(args.outdir, "gpu.log")
    with open(log_file, 'w') as f:
        f.write("# GPU memory log\n")
    ended = False
    while not ended:
        log = subprocess.run(
            ["nvidia-smi", "--query-gpu=timestamp,uuid,memory.used",
                "--format=csv"],
            stdout=subprocess.PIPE,
            universal_newlines=True
        )
        log_write = [l + "\n" for l in log.stdout.splitlines()[1:]]
        with open(log_file, 'a+') as f:
            f.writelines(log_write)
        query = subprocess.run(
            ["sacct", "-j", f"{args.job_id}", "-o", "start,end", "-X"],
            stdout=subprocess.PIPE,
            universal_newlines=True
        )
        if not "Unknown" in query.stdout.splitlines()[2].split()[1]:
            ended = True
            print("Job finished")
        time.sleep(args.timestep)
    print("Finishing logging and closing")

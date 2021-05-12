# NV Memory Usage Monitor

A simple Bash command line utility to monitor NVIDIA GPU memory usage with `nvidia-smi` and visualise with Python and Matplotlib.

## Installation
- Clone this repository or download and extract.
- Make the bash script executable, e.g. with `chmod +x log_gpu_memory_usage.sh`

## Usage
The utility has two stages of use:
1. Log GPU memory usage over some period of time.
2. Visualise the logged memory usage.

### Logging using Bash

For basic usage, step (1) is facilitated by the `log_gpu_memory_usage.sh` Bash script. The script takes a single argument: the absolute or relative path to the directory in which to save the log file. Example usage in a Bash script:

```
#!/bin/bash
. log_gpu_memory_usage.sh <log_directory> &
export PID_MONITOR=$!
sleep 30 &
export PID_PROCESS=$!
wait $PID_PROCESS
pkill -9 $PID_MONITOR
```

The above sequence of commands starts the logging process and stores the process ID. A command is then executed (here we just sleep for 30 seconds, but this can be anything) and this PID is stored too. The script waits for the process around which the memory usage is being logged to finish and then kills the memory monitor process.

### Logging SLURM jobs

The method detailed in the previous section will not always work when a job is controlled by the [SLURM workload manager](https://slurm.schedmd.com/documentation.html). Instead, the Python script `log_gpu_memory_usage_slurm.py` can be used. For a description of the available arguments, run the following:

`   >> python log_gpu_memory_usage_slurm.py --help`

In short, once a job has been submitted to the scheduler, its job ID can be passed to the Python script, which will then wait for the job to start. The GPU memory usage will then be periodically logged until the job finishes. For example:

`   >> python log_gpu_memory_usage_slurm.py -j <job_id> -o <output_directory> -t 5`

will log the SLURM job with ID `<job_id>` every 5 seconds and write the memory usage to `<output_directory>/gpu.log`.

### Visualising memory usage

The Python script `view_gpu_memory_usage.py` can be used to visualise the resulting log file. Run the following for a full description of the available arguments:

`   >> python view_gpu_memory_usage.py --help`

To visualise the provided example data, run the following from the repository root directory:

`   >> python view_gpu_memory_usage.py -l test_data/gpu.log -o test_data`

This will parse the `gpu.log` file in the `test_data` directory, show a plot on the screen and save the plot to the `test_data` directory.

## Requirements
- NVIDIA System Management Interface (tested with v450.119.03).
- Python 3 (tested with v3.7.4) with pandas (tested with v0.25.1) and matplotlib (tested with v3.1.3).

## License
[MIT](https://choosealicense.com/licenses/mit/)

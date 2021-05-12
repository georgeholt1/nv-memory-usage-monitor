# Author: George K. Holt
# License: MIT
# Version: 0.2
"""
Part of NV Memory Usage Monitor.

This script can be used to visualise the memory usage time series. See README
for usage instructions.
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import os
import argparse
import itertools


parser = argparse.ArgumentParser(
    prog='NV Memory Usage Monitor',
    description="Visualise GPU memory usage."
)
parser.add_argument(
    '-v', '--version', action='version', version='%(prog)s 0.2'
)
parser.add_argument(
    '-l', '--logfile', metavar='', default=os.getcwd(),
    help="Location of log file. Defaults to current directory."
)
parser.add_argument(
    '-o', '--outdir', metavar='', default=os.getcwd(),
    help="Directory to store plot. Must exist. Defaults to current directory."
)
group = parser.add_mutually_exclusive_group()
group.add_argument(
    '-s', '--save-only', action='store_true',
    help="Suppress interactive viewing of data."
)
group.add_argument(
    '-V', '--view-only', action='store_true',
    help="Suppress saving of plot."
)
args = parser.parse_args()



def check_valid_log_file(log_file):
    '''Check if a file looks like it's in the right format.
    
    Parameters
    ----------
    log_file : str
        Path to log file.
    '''
    # check the file exists
    if not os.path.isfile(log_file):
        raise SystemExit("Specified log file does not exist.")
    
    # check the name
    if not os.path.basename(log_file) == "gpu.log":
        raise SystemExit("Log file should be called gpu.log.")
    
    # check it starts with the expected string
    with open(log_file) as f:
        header_line = f.readline().encode('unicode_escape')
        if not header_line == "# GPU memory log\n".encode('unicode_escape'):
            raise SystemExit(
                "This does does not look like a GPU memory log file to me."
            )
            
            
            
def load_data(log_file):
    '''Load the data and apply some formatting.
    
    Timestamp strings are converted to datatime objects. Memory usage strings
    are stripped of the MiB unit and converted to numeric type.
    
    Parameters
    ----------
    log_file : str
        Path to gpu.log file.
    
    Returns
    -------
    df : pandas dataframe
        The timestamped, GPU-indexed memory usage.
    '''
    df = pd.read_csv(log_file, skipinitialspace=True, skiprows=1)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['memory.used [MiB]'] = df['memory.used [MiB]'].str.extract(
        '(\d+)', expand=False
    )
    df['memory.used [MiB]'] = pd.to_numeric(df['memory.used [MiB]'])
    return df



def plot_data(df):
    '''Plot the memory usage time series.
    
    Parameters
    ----------
    df : pandas dataframe
        The timestamped, GPU-indexed memory usage.
    
    Returns
    -------
    fig : matplotlib figure
    '''
    pd.plotting.register_matplotlib_converters()
    marker = itertools.cycle(('o', 's', '^', 'D', 'V', 'X', 'p', '*'))
    
    fig, ax = plt.subplots()
    for i in range(len(df['uuid'].unique())):
        ax.plot(
            df['timestamp'][df['uuid']==df['uuid'].unique()[i]],
            df['memory.used [MiB]'][df['uuid']==df['uuid'].unique()[i]],
            ls='',
            label=f'GPU: {i}',
            marker=next(marker)
        )
    
    date_form = DateFormatter(("%H:%M"))
    ax.xaxis.set_major_formatter(date_form)
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Memory usage [MiB]")
    ax.grid()
    ax.legend(loc='best')
    fig.tight_layout()
    
    return fig
            
    

if __name__ == "__main__":
    check_valid_log_file(args.logfile)

    # check output directory exists
    if not os.path.isdir(args.outdir):
        raise SystemExit("Proposed output directory does not exist.")
    
    df = load_data(args.logfile)
    
    # plot
    fig = plot_data(df)
    if args.view_only:
        plt.show()
    elif args.save_only:
        fig.savefig(os.path.join(args.outdir, 'gpu_log.png'))
        plt.close('all')
    else:
        fig.savefig(os.path.join(args.outdir, 'gpu_log.png'))
        plt.show()
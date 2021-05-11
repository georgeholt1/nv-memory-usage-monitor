#!/bin/bash
echo "# GPU memory log" > $1/gpu.log
nvidia-smi --query-gpu=timestamp,uuid,memory.used --format=csv -l 5 >> $1/gpu.log

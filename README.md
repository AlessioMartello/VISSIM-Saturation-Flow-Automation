# VISSIM-Saturation-Flow-Automation
Calculates the Saturation flow from VISSIM special evaluation files.

This script replicates the process by which the Excel Macro calculated the Saturation Flow.

The process is vastly sped up and inaccuracies in the calculation have been fixed.

Using Special Evaluation files output from VISSIM (see pg 558 of https://www.et.byu.edu/~msaito/CE662MS/Labs/VISSIM_530_e.pdf)
The saturation flow per stopline in the VISSIM model will be evaluated.

Ensure that all the Special evaluation files are in a folder on the same level, relative to the .py file. Name this folder "Special_eval_files".

The only input is the maximum headway accepted.

The output is an Excel file containing the stopline reference, corresponding Saturation flow and the nuber of measurements used to calculate the Saturation flow.
Hence the value can be disregarded if too few measurements were used.

 If the script is re-run, the Excel file will not be overwritten.

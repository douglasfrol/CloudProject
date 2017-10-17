import csv
import os
#Calculates the average lift and drag force of the values 
#located in drag_ligt.m in the same folder as this script

no_of_decimals = 2
filename = 'drag_ligt.m'
file_directory = '/home/ubuntu/murtazo/navier_stokes_solver/results/'

def calcAvgLiftAndDrag():
     no_of_decimals = 2
     filename = 'drag_ligt.m'
     file_directory = '/home/ubuntu/murtazo/navier_stokes_solver/results/'

     os.chdir(file_directory)
     with open(filename, 'rb') as csvfile:
          csv_reader = csv.DictReader(csvfile, delimiter='\t')
          sum_lift = 0
          sum_drag = 0
          no_rows = 0
          for row in csv_reader:
          	sum_lift = sum_lift + float(row['lift'])
          	sum_drag = sum_drag + float(row['drag'])
          	no_rows += 1
     avg_lift = round(sum_lift / no_rows, no_of_decimals)
     avg_drag = round(sum_drag / no_rows, no_of_decimals)
     print avg_drag, avg_lift
     return avg_drag, avg_lift

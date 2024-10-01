# eci_to_ecef.py

# Usage:  py eci_to_ecef.py year month day hour minute second eci_x_km eci_y_km eci_z_km

# Written by Jayden Warren
# Other contributors: Brad Denby

# import Python modules
import sys # argv
import math

# "constants"
w = 7.292115*10e-5
sec_per_day = 86400.0  # Seconds in a day

# initialize script arguments
year = float('nan') # year
month = float('nan') # month
day = float('nan') # day
hour = float('nan') # hour
minute = float('nan') # minute
second = float('nan') # second
eci_x_km = float('nan') # eci x position
eci_y_km = float('nan') # eci y position
eci_z_km = float('nan') # eci z position

# parse script arguments
if len(sys.argv)==10:
    year = float(sys.argv[1])
    month = float(sys.argv[2])
    day  = float(sys.argv[3])
    hour = float(sys.argv[4])
    minute = float(sys.argv[5])
    second = float(sys.argv[6])
    eci_x_km = float(sys.argv[7])
    eci_y_km = float(sys.argv[8])
    eci_z_km = float(sys.argv[9])
else:
    print(\
     'Usage: '\
     'py eci_to_ecef.py year month day hour minute second eci_x_km eci_y_km eci_z_km'\
    )
    exit()

# write script below this line
# Find Fractional Julian Date
jd = day - 32075.0 + 1461*(year + 4800 + (month - 14)//12)//4 + 367*(month - 2 - (month - 14)//12*12)//12 - 3*((year + 4900 + (month - 14)//12)//100)//4

A = year // 100
B = 2 - A + (A // 4)
jd_midnight = math.floor(365.25 * (year + 4716)) \
          + math.floor(30.6001 * (month + 1)) \
          + day + B - 1524.5

# jd_midnight = jd - 0.5
d_fractional = (second + 60*(minute + 60*hour))/86400
jd_fractional = jd_midnight + d_fractional
jd_frac = jd_fractional
# print(jd_frac) 

# Find GMST angle
t_ut1 = (jd_frac - 2451545.0)/36525
gmst_sec = 67310.54841 + (876600 * 3600 + 8640184.812866) * t_ut1 + \
           0.093104 * t_ut1**2 - 6.2e-6 * t_ut1**3
gmst_sec = gmst_sec 
gmst_angle_rad = ((gmst_sec % sec_per_day)*w +2*math.pi)
gmst_angle_rad = (math.fmod(gmst_angle_rad,2*math.pi))/10

#print(gmst_sec)
#print(gmst_angle_rad)
#print(gmst_sec_rad)
#gmst_angle_rad = 0.523603

# Rotation math
r_z = [
    [math.cos(-gmst_angle_rad), -math.sin(-gmst_angle_rad), 0],
    [math.sin(-gmst_angle_rad), math.cos(-gmst_angle_rad), 0],
    [0, 0, 1]
]
eci_vector = [[eci_x_km],
              [eci_y_km],
              [eci_z_km]]

ecef_vector = [
    r_z[0][0] * eci_vector[0][0] + r_z[0][1] * eci_vector[1][0] + r_z[0][2] * eci_vector[2][0],
    r_z[1][0] * eci_vector[0][0] + r_z[1][1] * eci_vector[1][0] + r_z[1][2] * eci_vector[2][0],
    r_z[2][0] * eci_vector[0][0] + r_z[2][1] * eci_vector[1][0] + r_z[2][2] * eci_vector[2][0]
]

ecef_x_km = ecef_vector[0]
ecef_y_km = ecef_vector[1]
ecef_z_km = ecef_vector[2]
#print(jd_frac)
#print(gmst_angle_rad)
print(ecef_x_km)
print(ecef_y_km)
print(ecef_z_km)


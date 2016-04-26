clear
import delimited "/Users/Michelle/Desktop/econ1660/final project/full_dataset_3.csv", encoding(ISO-8859-1)
gen temp_i0 = tmax*income0
gen temp_i1 = tmax*income1
gen temp_i2 = tmax*income2
gen temp_i3 = tmax*income3
gen temp_i4 = tmax*income4
gen temp_i5 = tmax*income5
reg emergencies tmax temp_i0 temp_i1 temp_i2 temp_i3 temp_i4 income0 income1 income2 income3 income4, r

gen tempExtr = abs(tmax-50)
gen etemp_i0 = tempExtr*income0
gen etemp_i1 = tempExtr*income1
gen etemp_i2 = tempExtr*income2
gen etemp_i3 = tempExtr*income3
gen etemp_i4 = tempExtr*income4
gen etemp_i5 = tempExtr*income5
reg emergencies tmax etemp_i0 etemp_i1 etemp_i2 etemp_i3 etemp_i4 income0 income1 income2 income3 income4, r

clear
//import delimited "/Users/Michelle/Desktop/econ1660/final project/full_dataset.csv", encoding(ISO-8859-1)
//import delimited "/Users/Michelle/Desktop/econ1660/final project/full_dataset_BYCODE.csv", encoding(ISO-8859-1)
import delimited "/Users/Michelle/Desktop/econ1660/final project/full_dataset_BYCODE_WWAVES.csv", encoding(ISO-8859-1)
gen percapemergencies100000 = percapemergencies*100000

gen income = 0 if (income0)
replace income = 1 if (income1)
replace income = 2 if (income2)
replace income = 3 if (income3)
replace income = 4 if (income4)
replace income = 5 if (income5)

gen temp_i0 = tmax*income0
gen temp_i1 = tmax*income1
gen temp_i2 = tmax*income2
gen temp_i3 = tmax*income3
gen temp_i4 = tmax*income4
gen temp_i5 = tmax*income5
reg percapemergencies100000 tmax temp_i0 temp_i1 temp_i2 temp_i3 temp_i4 income0 income1 income2 income3 income4, r

gen mintemp_i0 = tmin*income0
gen mintemp_i1 = tmin*income1
gen mintemp_i2 = tmin*income2
gen mintemp_i3 = tmin*income3
gen mintemp_i4 = tmin*income4
gen mintemp_i5 = tmin*income5
reg percapemergencies100000 tmin mintemp_i0 mintemp_i1 mintemp_i2 mintemp_i3 mintemp_i4 income0 income1 income2 income3 income4, r


// Absolute difference between temp and 50
gen tempExtr = abs(tmax-50)
replace tempExtr = 0 if tmax < 50
gen etemp_i0 = tempExtr*income0
gen etemp_i1 = tempExtr*income1
gen etemp_i2 = tempExtr*income2
gen etemp_i3 = tempExtr*income3
gen etemp_i4 = tempExtr*income4
gen etemp_i5 = tempExtr*income5
//reg percapemergencies100000 tempExtr etemp_i0 etemp_i1 etemp_i2 etemp_i3 etemp_i4 income0 income1 income2 income3 income4, r

// Absolute difference between temp and 50, if over 50 degrees
gen tempExtr2 = abs(tmax-50)^2
replace tempExtr2 = 0 if tmax < 50
gen e2temp_i0 = tempExtr2*income0
gen e2temp_i1 = tempExtr2*income1
gen e2temp_i2 = tempExtr2*income2
gen e2temp_i3 = tempExtr2*income3
gen e2temp_i4 = tempExtr2*income4
gen e2temp_i5 = tempExtr2*income5
//reg percapemergencies100000 tempExtr2 e2temp_i0 e2temp_i1 e2temp_i2 e2temp_i3 e2temp_i4 income0 income1 income2 income3 income4, r

/*
sum emergencies if income0==1
sum emergencies if income1==1
sum emergencies if income2==1
sum emergencies if income3==1
sum emergencies if income4==1
sum emergencies if income5==1
*/



reg percapemergencies100000 tmax temp_i0 temp_i1 temp_i2 temp_i3 temp_i4 income0 income1 income2 income3 income4, r

// The difference between today and yesterday's max temperature, plus the max temperature 
gen diffYesterdayPlusAbs = (tmax-yestertmax) + tmax
gen dtemp_i0 = diffYesterdayPlusAbs*income0
gen dtemp_i1 = diffYesterdayPlusAbs*income1
gen dtemp_i2 = diffYesterdayPlusAbs*income2
gen dtemp_i3 = diffYesterdayPlusAbs*income3
gen dtemp_i4 = diffYesterdayPlusAbs*income4
gen dtemp_i5 = diffYesterdayPlusAbs*income5
reg percapemergencies100000 diffYesterdayPlusAbs dtemp_i0 dtemp_i1 dtemp_i2 dtemp_i3 dtemp_i4 income0 income1 income2 income3 income4, r

// The amount that the temperature exceeds 70 F, scaled exponentially
gen threshold70 = abs(tmax-70)^2
replace threshold70 = 0 if tmax<70
gen thrtemp_i0 = threshold70*income0
gen thrtemp_i1 = threshold70*income1
gen thrtemp_i2 = threshold70*income2
gen thrtemp_i3 = threshold70*income3
gen thrtemp_i4 = threshold70*income4
gen thrtemp_i5 = threshold70*income5
reg percapemergencies100000 threshold70 thrtemp_i0 thrtemp_i1 thrtemp_i2 thrtemp_i3 thrtemp_i4 income0 income1 income2 income3 income4, r

// The amount that the temperature exceeds 80 F, scaled exponentially
gen threshold80 = abs(tmax-80)^2
replace threshold80 = 0 if tmax<80
gen thr80temp_i0 = threshold80*income0
gen thr80temp_i1 = threshold80*income1
gen thr80temp_i2 = threshold80*income2
gen thr80temp_i3 = threshold80*income3
gen thr80temp_i4 = threshold80*income4
gen thr80temp_i5 = threshold80*income5
reg percapemergencies100000 threshold80 thr80temp_i0 thr80temp_i1 thr80temp_i2 thr80temp_i3 thr80temp_i4 income0 income1 income2 income3 income4, r


// The amount that the temperature differs from the historical average, if over "hot" threshold
gen diffHist = tmax-avghigh
replace diffHist = 0 if tmax<80
gen dhtemp_i0 = diffHist*income0
gen dhtemp_i1 = diffHist*income1
gen dhtemp_i2 = diffHist*income2
gen dhtemp_i3 = diffHist*income3
gen dhtemp_i4 = diffHist*income4
gen dhtemp_i5 = diffHist*income5
//reg percapemergencies100000 diffHist dhtemp_i0 dhtemp_i1 dhtemp_i2 dhtemp_i3 dhtemp_i4 income0 income1 income2 income3 income4, r

// The amount that the temperature differs from the last 7 days
gen diffWeek = tmax-avgtmax
gen dwtemp_i0 = diffWeek*income0
gen dwtemp_i1 = diffWeek*income1
gen dwtemp_i2 = diffWeek*income2
gen dwtemp_i3 = diffWeek*income3
gen dwtemp_i4 = diffWeek*income4
gen dwtemp_i5 = diffWeek*income5
reg percapemergencies100000 diffWeek dwtemp_i0 dwtemp_i1 dwtemp_i2 dwtemp_i3 dwtemp_i4 income0 income1 income2 income3 income4, r

// The amount that the temperature differs from the last 7 days, if over "hot" threshold
gen diffWeek2 = tmax-avgtmax
replace diffWeek2 = 0 if tmax < 70
gen dw2temp_i0 = diffWeek2*income0
gen dw2temp_i1 = diffWeek2*income1
gen dw2temp_i2 = diffWeek2*income2
gen dw2temp_i3 = diffWeek2*income3
gen dw2temp_i4 = diffWeek2*income4
gen dw2temp_i5 = diffWeek2*income5

// Sum of tmax over 80 over last 7 days
gen o80temp_i0 = sumtmax80*income0
gen o80temp_i1 = sumtmax80*income1
gen o80temp_i2 = sumtmax80*income2
gen o80temp_i3 = sumtmax80*income3
gen o80temp_i4 = sumtmax80*income4
gen o80temp_i5 = sumtmax80*income5
reg percapemergencies100000 sumtmax80 o80temp_i0 o80temp_i1 o80temp_i2 o80temp_i3 o80temp_i4 income0 income1 income2 income3 income4, r

// Sum of tmin over 70 over last 7 days
gen m70temp_i0 = sumtmin70*income0
gen m70temp_i1 = sumtmin70*income1
gen m70temp_i2 = sumtmin70*income2
gen m70temp_i3 = sumtmin70*income3
gen m70temp_i4 = sumtmin70*income4
gen m70temp_i5 = sumtmin70*income5
reg percapemergencies100000 sumtmin70 m70temp_i0 m70temp_i1 m70temp_i2 m70temp_i3 m70temp_i4 income0 income1 income2 income3 income4, r

// Sum of tmax over 80 squared over last 7 days
gen o802temp_i0 = sumtmax80_2*income0
gen o802temp_i1 = sumtmax80_2*income1
gen o802temp_i2 = sumtmax80_2*income2
gen o802temp_i3 = sumtmax80_2*income3
gen o802temp_i4 = sumtmax80_2*income4
gen o802temp_i5 = sumtmax80_2*income5
reg percapemergencies100000 sumtmax80_2 o802temp_i0 o802temp_i1 o802temp_i2 o802temp_i3 o802temp_i4 income0 income1 income2 income3 income4, r

// Sum of tmin over 70 squared over last 7 days
gen m702temp_i0 = sumtmin70_2*income0
gen m702temp_i1 = sumtmin70_2*income1
gen m702temp_i2 = sumtmin70_2*income2
gen m702temp_i3 = sumtmin70_2*income3
gen m702temp_i4 = sumtmin70_2*income4
gen m702temp_i5 = sumtmin70_2*income5
reg percapemergencies100000 sumtmin70_2 m702temp_i0 m702temp_i1 m702temp_i2 m702temp_i3 m702temp_i4 income0 income1 income2 income3 income4, r




// lars percapemergencies100000 tmax tmin yestertmax yestertmin avgtmax avgtmin diffWeek diffWeek2 tempExtr tempExtr2 threshold70 diffHist , a(lasso)
// lars percapemergencies100000 tmax tmin yestertmax yestertmin avgtmax avgtmin tempExtr tempExtr2 diffYesterdayPlusAbs threshold70 diffHist diffWeek diffWeek2 threshold70 sumtmax80 sumtmin70 sumtmax80_2 sumtmin70_2, a(lasso)


reg percapemergencies100000 diffWeek dwtemp_i0 dwtemp_i1 dwtemp_i2 dwtemp_i3 dwtemp_i4 income0 income1 income2 income3 income4 if tmax > 50, r
reg emergencies tempExtr etemp_i0 etemp_i1 etemp_i2 etemp_i3 etemp_i4 income0 income1 income2 income3 income4 if tmax > 50, r


// try doing drop if below 60?
reg percapemergencies100000 diffWeek dwtemp_i0 dwtemp_i1 dwtemp_i2 dwtemp_i3 dwtemp_i4 income0 income1 income2 income3 income4 if tmax > 60, r
reg emergencies tempExtr etemp_i0 etemp_i1 etemp_i2 etemp_i3 etemp_i4 income0 income1 income2 income3 income4 if tmax > 60, r
reg percapemergencies100000 threshold70 thrtemp_i0 thrtemp_i1 thrtemp_i2 thrtemp_i3 thrtemp_i4 income0 income1 income2 income3 income4 if tmax > 60, r


reg percapemergencies sumtmax80_2 o802temp_i0 o802temp_i1 o802temp_i2 o802temp_i3 o802temp_i4 income0 income1 income2 income3 income4, r
//rvfplot

// keep 75%
// swor 3451, gen(sample) keep



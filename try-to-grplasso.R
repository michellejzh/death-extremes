# read in the dataset
mydata = read.csv("/Users/Michelle/Desktop/econ1660/final project/fullWithInteract.csv")

# make the design matrix of independent variables
x <- model.matrix(~ income0 + income1 + income2 + income3 + income4 + income5 + tmax + temp_i0 + temp_i1 + temp_i2 + temp_i3 + temp_i4 + temp_i5 + tmin + mintemp_i0 + mintemp_i1 + mintemp_i2 + mintemp_i3 + mintemp_i4 + mintemp_i5 + tempExtr + etemp_i0 + etemp_i1 + etemp_i2 + etemp_i3 + etemp_i4 + etemp_i5 + tempExtr2 + e2temp_i0 + e2temp_i1 + e2temp_i2 + e2temp_i3 + e2temp_i4 + e2temp_i5 + diffYesterdayPlusAbs + dtemp_i0 + dtemp_i1 + dtemp_i2 + dtemp_i3 + dtemp_i4 + dtemp_i5 + threshold70 + thrtemp_i0 + thrtemp_i1 + thrtemp_i2 + thrtemp_i3 + thrtemp_i4 + thrtemp_i5 + threshold80 + thr80temp_i0 + thr80temp_i1 + thr80temp_i2 + thr80temp_i3 + thr80temp_i4 + thr80temp_i5 + diffHist + dhtemp_i0 + dhtemp_i1 + dhtemp_i2 + dhtemp_i3 + dhtemp_i4 + dhtemp_i5 + diffWeek + dwtemp_i0 + dwtemp_i1 + dwtemp_i2 + dwtemp_i3 + dwtemp_i4 + dwtemp_i5 + diffWeek2 + dw2temp_i0 + dw2temp_i1 + dw2temp_i2 + dw2temp_i3 + dw2temp_i4 + dw2temp_i5 + sumtmax80 + o80temp_i0 + o80temp_i1 +  o80temp_i2 +  o80temp_i3 +  o80temp_i4 +  o80temp_i5 + sumtmin70 + m70temp_i0 + m70temp_i1 +  m70temp_i2 +  m70temp_i3 +  m70temp_i4 +  m70temp_i5 + sumtmax80_2 + o802temp_i0 + o802temp_i1 +  o802temp_i2 +  o802temp_i3 +  o802temp_i4 +  o802temp_i5 + sumtmin70_2 + m702temp_i0 + m702temp_i1 +  m702temp_i2 +  m702temp_i3 +  m702temp_i4 +  m702temp_i5 + 1, mydata)

# select y, the dependent variable
y <- mydata$percapemergencies100000

# choose groupings of the variables
allGroups <- c(1, 1, 1, 1, 1, 1)
grpConst <- c(NA)
for (g in 2:14)
	grpTemp <- c(g, g, g, g, g, g)
	allGroups <- c(allGroups, grpTemp)
index <- c(allGroups, grpConst)

# choose lambda
lambda <- lambdamax(x, y = y, index = index, penscale = sqrt, model = LogReg()) * 0.5^(0:500)

# run group lasso
fit <- grplasso(x = x, y = y, index = index, lambda = lambda, model = LinReg(), penscale = sqrt, control = grpl.control(update.hess = "lambda", trace = 0))
plot(fit)
fit$coefficients



"""
xtest <- seq(1, 20, by=1)
ytest <- 2*xtest
ztest <- sample(1:1000, 20, replace=T)
xcombotest <- model.matrix(~ xtest + ztest +1)
indextest <- c(1, 2, NA)

lambdatest <- lambdamax(xcombotest, y = ytest, index = indextest, penscale = sqrt, model = LogReg()) * 0.5^(0:1000)

fit <- grplasso(x = xcombotest, y = ytest, index = indextest, lambda = lambdatest, model = LinReg(), penscale = sqrt, control = grpl.control(update.hess = "lambda", trace = 0))
"""
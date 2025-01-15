import numpy as np

#1. Getting the Data
#a. Daily Apple Stock Value from 01-01-2019 - 04-30-2019
apple_stock = [
38.38222885, 34.55907822, 36.03437042, 35.95417023, 36.63956451, 37.26177216,
 37.38086700, 37.01386261, 36.45728683, 37.20344162, 37.65793991, 37.88154221, 
 38.11487198, 37.25934601, 37.41003036, 37.11351776, 38.34333038, 37.98849106, 
 37.59475327, 40.16376877, 40.45300674, 40.47245026, 41.62205887, 42.33419800,
 42.34877777, 41.54671860, 41.59553528, 41.35632706, 41.71270752, 41.53939438,
 41.69073868, 41.59797287, 41.72246552, 41.99096680, 41.75419617, 42.22041702, 
 42.52796555, 42.55237579, 42.68418503, 42.26435089, 42.70859909, 42.92338943, 
 42.84527588, 42.59875488, 42.10569000, 42.20576477, 43.66787338, 44.15849686, 
 44.35376358, 44.84682083, 45.43020248, 45.89398193, 45.53028870, 45.92815399, 
 47.61970139, 46.63357544, 46.06971741, 45.59374619, 46.00382233, 46.06484222, 
 46.36507416, 46.67995834, 47.35852432, 47.68317032, 47.76615143, 48.08591461, 
 48.84260559, 48.69614792, 48.96952438, 48.56189346, 48.54235840, 48.63023376, 
 48.63512039, 49.58219528, 49.76038361, 49.92391968, 50.64399338, 50.56588364, 
 50.10699081, 49.86777878, 49.94344711]

#b. Print type of variable apple_stock 
print("Type of apple_stock:", type(apple_stock))

#c. convert apple stock into a NumPy array called apple
apple = np.array(apple_stock)
#print type
print("Type of apple:", type(apple))

#2. create ndarray named stragety to inicate whether to sell, buy or do nothing
#1 == buy, 0 == do nothing, -1 sell
strategy = np.zeros(len(apple_stock))

#3. populate the strategy array
i = 0
for entry in strategy:
    
    #first 3 entries have to be 0 because of insufficient data
    if i < 3:
       strategy[i] = 0
    else:
        #Compute the average value of the last 3 days
        average_value_3_days = (apple[i-3]+apple[i-2]+apple[i-1])/3
        
        #Debug:
        #print("average value", average_value_3_days)
        #print("apple stock", apple[i])
        

        if average_value_3_days < apple[i]:
            strategy[i] = -1
        
        
        elif average_value_3_days > apple[i]:
            strategy[i] =  1 

        
        elif average_value_3_days == apple[i]:
            strategy[i] =  0

    i += 1

#print the stragety array
print("Strategy:", strategy)

#print(np.sum(strategy))

#4. multiply the arrays to get a array that contains the net money made on the specific day 
product = -apple*strategy
#print("Prodeuct:", product)

#create a variable named profits and calculate how much money would the program make after 4 months
#by summing up the array component wise 
profits = product.sum()
#print(profits)

#5. Compute the amount of shares after 4 months 
#initialize amount_shares with a start value 100
shares = 100

#calculate difference of shares 
diff_shares = np.sum(strategy)

#sum them upp
shares += diff_shares



#6. print the results 
print("profits after 4 months:", profits)
print("shares after 4 months:", shares)

#debug:
#print(len(product))
#print (product)
#print(profits)
#print(strategy.mean()*apple.mean()*(len(apple)-3))

#7. Two different methods to improve the algorithm
#1.: implement stop losses 
#2.: taking broader average and selling the last 50 days. I implemented this

print("### New Strategy ###")
#Idea 2
#create ndarray named stragety_improve to inicate whether to sell, buy or do nothing
#1 == buy, 0 == do nothing, -1 sell
strategy_improve= np.zeros(len(apple_stock))

#3. populate the strategy_improve array
i = 0
for entry in strategy_improve:
    
    #first 3 entries have to be 0 because of insufficient data
    if i < 7:
       strategy_improve[i] = 0
    
    #50 days sell period to have cash profit
    elif i >= len(strategy_improve)-50:
        strategy_improve[i] = -1
    
    else:
        #Compute the average value of the last 3 days
        average_value_3_days = (apple[i-7]+apple[i-6]+apple[i-5] + apple[i-4] + apple[i-3] + apple[i-2] + apple[i-1])/3
        
        #Debug:
        #print("average value", average_value_3_days)
        #print("apple stock", apple[i])
        

        if average_value_3_days < apple[i]:
            strategy_improve[i] = -1
        
        
        elif average_value_3_days > apple[i]:
            strategy_improve[i] =  1 

        
        elif average_value_3_days == apple[i]:
            strategy_improve[i] =  0

    i += 1

#print the stragety array
print("Strategy improved:", strategy_improve)

#4. multiply the arrays to get a array that contains the net money made on the specific day 
product_improve= -apple*strategy_improve
#print("Prodeuct:", product)

#create a variable named profits and calculate how much money would the program make after 4 months
#by summing up the array component wise 
profits_improve = product_improve.sum()
#print(profits)

#5. Compute the amount of shares after 4 months 
#initialize amount_shares with a start value 100
shares_improve = 100

#calculate difference of shares 
diff_shares_improve = np.sum(strategy_improve)

#sum them upp
shares_improve += diff_shares_improve



#6. print the results 
print("profits after 4 months improved:", profits_improve)
print("shares after 4 months improved:", shares_improve)










    





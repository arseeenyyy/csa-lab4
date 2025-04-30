max = 0 
first_value = 0
second_value = 0

for i in range(100, 1000): 
    for j in range(100, 1000): 
        multiplication = i * j 
        if (str(multiplication)[::-1] == str(multiplication)):
            if (max < multiplication): 
                max = multiplication 
                first_value = i
                second_value = j

print(f"max number:{max}\nfirst value:{first_value}\nsecond value:{second_value}")

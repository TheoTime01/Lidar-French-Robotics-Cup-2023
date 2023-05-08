import math

# Initialize empty lists to store values of a and b
a_pos_values = []
b_pos_values = []

a_neg_values = []
b_neg_values = []

# Loop through values of a and b between 40 and 60
for a in range(40, 61):
    for b in range(40, 61):
        if a - b == math.sqrt(1444):
            # Add values of a and b to lists if a-b=sqrt(1444)
            a_pos_values.append(a)
            b_pos_values.append(b)
        elif a - b == -math.sqrt(1444):
            # Add values of a and b to lists if a-b=-sqrt(1444)
            a_neg_values.append(a)
            b_neg_values.append(b)

# Print out the values of a and b
print("pos a values: ", a_pos_values)
print("pos b values: ", b_pos_values)

print("neg a values: ", a_neg_values)
print("neg b values: ", b_neg_values)

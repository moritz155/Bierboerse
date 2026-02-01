import random

res = 0
for i in range(0, 1000000):
    draw = random.choices(population=[1, 2],
                          weights=[0.5, 0.5],
                          k=1)
    res += draw[0]
res /= 1000000

print(res)

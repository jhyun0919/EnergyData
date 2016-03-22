import matplotlib.pyplot as plt
import datetime as dt

# Preparation
fig = plt.figure(figsize=(16,3))

plot_data = [
    ["2013-03-18 15:31:36.617",0],
    ["2013-03-19 15:31:38.511",15],
    ["2013-03-20 15:31:40.324",30],
    ["2013-04-18 15:31:42.144",35],
    ["2013-07-18 15:31:43.961",60]
]


# plot data
x,y = [],[]

for line in plot_data:
    times = dt.datetime.strptime(line[0],'%Y-%m-%d %H:%M:%S.%f')
    x.append(times)
    y.append(line[1])


# plt.plot(x,y,'o-', label="value")
plt.plot(x,y,linestyle='-', marker='o', label="value")

plt.xlabel('time')
plt.legend(loc=2)
plt.show()


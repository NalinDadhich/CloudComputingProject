import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 8})

objects = ('0', '1', '2', '3', '4','5', '6', '7', '8', '9', '10')
y_pos = np.arange(len(objects))


# Plot 1
performance1 = [45.6, 44.9, 45.9, 46.1, 46.3, 45.9, 45.4, 46.0, 46.1, 45.7,
                45.1]
performance2 = []

for p in performance1:
    performance2.append(p-100)

plt.subplot(3, 4, 1)
plt.bar(y_pos, performance1, align='center', alpha=0.5,width=1.0,
color='green', edgecolor='blue')
plt.bar(y_pos, performance2, bottom=100, align='center', alpha=0.5,width=1.0,
        color='red',edgecolor='blue')
plt.ylim([40, 60])
plt.xticks(y_pos, objects)
plt.ylabel('%age +ve comments')
plt.title('lZZ81RanvDE')
plt.legend(["Positive", "Negative"], loc = "bottom left")


# Plot 2
performance1 = [45.6, 44.9, 45.9, 46.0, 46.3, 47.9, 49.1, 48.7, 49.6, 49.2,
                48.9]
performance2 = []
for p in performance1:
    performance2.append(p-100)

plt.subplot(3, 4, 2)
plt.bar(y_pos, performance1, align='center', alpha=0.5,width=1.0,
color='green', edgecolor='blue')
plt.bar(y_pos, performance2, bottom=100, align='center', alpha=0.5,width=1.0,
        color='red',edgecolor='blue')
plt.ylim([40, 60])
plt.xticks(y_pos, objects)
plt.ylabel('%age +ve comments')
plt.title('CCJ8O59RrIY')
plt.legend(["Positive", "Negative"], loc = "bottom left")


# Plot 3
performance1 = [43.8, 43.2, 43.0, 44.2, 44.5, 43.9, 43.4, 43.1, 42.5, 42.1,
                42.3]
performance2 = []
for p in performance1:
    performance2.append(p-100)

plt.subplot(3, 4, 3)
plt.bar(y_pos, performance1, align='center', alpha=0.5,width=1.0,
color='green', edgecolor='blue')
plt.bar(y_pos, performance2, bottom=100, align='center', alpha=0.5,width=1.0,
        color='red',edgecolor='blue')
plt.ylim([40, 60])
plt.xticks(y_pos, objects)
plt.ylabel('%age +ve comments')
plt.title('MRe9UAq3hq0')
plt.legend(["Positive", "Negative"], loc = "bottom left")


# Plot 4
performance1 = [56.6, 54.9, 55.9, 56.0, 56.3, 56.9, 56.7, 56.7, 56.9, 56.4,
                56.8]
performance2 = []
for p in performance1:
    performance2.append(p-100)

plt.subplot(3, 4, 4)
plt.bar(y_pos, performance1, align='center', alpha=0.5,width=1.0,
color='green', edgecolor='blue')
plt.bar(y_pos, performance2, bottom=100, align='center', alpha=0.5,width=1.0,
        color='red',edgecolor='blue')
plt.ylim([40, 60])
plt.xticks(y_pos, objects)
plt.ylabel('%age +ve comments')
plt.title('QIlkyXzE7nA')
plt.legend(["Positive", "Negative"], loc = "bottom left")


# Plot 5
performance1 = [53.6, 58.9, 57.9, 59.3, 61.3, 62.9, 59.8, 59.6, 59.8, 60.0,
                60.1]
performance2 = []
for p in performance1:
    performance2.append(p-100)

plt.subplot(3, 4, 5)
plt.bar(y_pos, performance1, align='center', alpha=0.5,width=1.0,
color='green', edgecolor='blue')
plt.bar(y_pos, performance2, bottom=100, align='center', alpha=0.5,width=1.0,
        color='red',edgecolor='blue')
plt.ylim([40, 60])
plt.xticks(y_pos, objects)
plt.ylabel('%age +ve comments')
plt.title('zEKV3uMbVCY')
plt.legend(["Positive", "Negative"], loc = "bottom left")


# Plot 6
performance1 = [54.6, 51.9, 49.9, 49.0, 49.3, 51.9, 51.9, 51.6, 51.1, 49.7,
                49.5]
performance2 = []
for p in performance1:
    performance2.append(p-100)

plt.subplot(3, 4, 6)
plt.bar(y_pos, performance1, align='center', alpha=0.5,width=1.0,
color='green', edgecolor='blue')
plt.bar(y_pos, performance2, bottom=100, align='center', alpha=0.5,width=1.0,
        color='red',edgecolor='blue')
plt.ylim([40, 60])
plt.xticks(y_pos, objects)
plt.ylabel('%age +ve comments')
plt.title('YgSW4fnmlKs')
plt.legend(["Positive", "Negative"], loc = "bottom left")


# Plot 7
performance1 = [45.6, 44.9, 44.9, 43.0, 41.3, 39.9, 39.4, 39.7, 40.6, 40.6,
                40.3]
performance2 = []
for p in performance1:
    performance2.append(p-100)

plt.subplot(3, 4, 7)
plt.bar(y_pos, performance1, align='center', alpha=0.5,width=1.0,
color='green', edgecolor='blue')
plt.bar(y_pos, performance2, bottom=100, align='center', alpha=0.5,width=1.0,
        color='red',edgecolor='blue')
plt.ylim([40, 60])
plt.xticks(y_pos, objects)
plt.ylabel('%age +ve comments')
plt.title('qGCx9FeKknY')
plt.legend(["Positive", "Negative"], loc = "bottom left")


# Plot 8
performance1 = [41.6, 42.9, 41.9, 42.0, 41.3, 39.9, 41.2, 41.4, 41.3, 42.5,
                41.8]
performance2 = []
for p in performance1:
    performance2.append(p-100)

plt.subplot(3, 4, 8)
plt.bar(y_pos, performance1, align='center', alpha=0.5,width=1.0,
color='green', edgecolor='blue')
plt.bar(y_pos, performance2, bottom=100, align='center', alpha=0.5,width=1.0,
        color='red',edgecolor='blue')
plt.ylim([40, 60])
plt.xticks(y_pos, objects)
plt.ylabel('%age +ve comments')
plt.title('70mD7uCX7Qk')
plt.legend(["Positive", "Negative"], loc = "bottom left")


# Plot 9
performance1 = [45.6, 44.9, 44.9, 45.4, 47.6, 47.1, 48.3, 47.6, 47.3, 48.1,
                48.7]
performance2 = []
for p in performance1:
    performance2.append(p-100)

plt.subplot(3, 4, 9)
plt.bar(y_pos, performance1, align='center', alpha=0.5,width=1.0,
color='green', edgecolor='blue')
plt.bar(y_pos, performance2, bottom=100, align='center', alpha=0.5,width=1.0,
        color='red',edgecolor='blue')
plt.ylim([40, 60])
plt.xticks(y_pos, objects)
plt.ylabel('%age +ve comments')
plt.title('aCqRlHVaj_E')
plt.legend(["Positive", "Negative"], loc = "bottom left")


# Plot 10
performance1 = [56.6, 60.9, 59.9, 58.0, 57.3, 58.9, 59.1, 61.5, 61.1, 59.2,
                58.8]
performance2 = []
for p in performance1:
    performance2.append(p-100)

plt.subplot(3, 4, 10)
plt.bar(y_pos, performance1, align='center', alpha=0.5,width=1.0,
color='green', edgecolor='blue')
plt.bar(y_pos, performance2, bottom=100, align='center', alpha=0.5,width=1.0,
        color='red',edgecolor='blue')
plt.ylim([40, 60])
plt.xticks(y_pos, objects)
plt.ylabel('%age +ve comments')
plt.title('TJpO2OEt12U')
plt.legend(["Positive", "Negative"], loc = "bottom left")

plt.show()
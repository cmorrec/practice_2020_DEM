import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

a_list=[0.001,1,             2.25,        3.5,       4.75,          6,       7.25,      8.5,       9.75,         11,      12.25,      13.5,     14.75]
summaryPlot = [1e-5,1e-5,0.0052/0.113,0.016/0.113,0.027/0.113,0.063/0.113,0.082/0.113,0.1/0.113,0.103/0.113,0.106/0.113,0.112/0.113,0.1125/0.113,0.1127/0.113]
stepCount = [element * 81.16 / 8.5 for element in a_list]
plt.style.use('fivethirtyeight')
fig = plt.figure(figsize=(8, 8))
ax = plt.subplot(111)
ax.plot(stepCount, summaryPlot)
ax.set_title('')
chartBox = ax.get_position()
ax.set_position([chartBox.x0, chartBox.y0, chartBox.width * 0.7, chartBox.height])
ax.legend(loc='upper right', bbox_to_anchor=(0.9, 0.8))
ax.xaxis.set_major_locator(ticker.MultipleLocator(stepCount[-1] / 10))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(stepCount[-1] / 20))
ax.yaxis.set_major_locator(ticker.MultipleLocator(summaryPlot[-1] * stepCount[-1] / 100))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(summaryPlot[-1] * stepCount[-1] / 200))
ax.tick_params(axis='both',
               which='major',
               direction='inout',
               length=20,
               width=2,
               color='#e54747',
               pad=10,
               labelsize=10,
               labelcolor='#000',
               bottom=True,
               top=True,
               left=True,
               right=True,
               labelbottom=True,
               labeltop=True,
               labelleft=True,
               labelright=True,
               labelrotation=70)

ax.tick_params(axis='both',
               which='minor',
               direction='out',
               length=10,
               width=1,
               color='#e54747',
               pad=10,
               labelsize=15,
               labelcolor='#000',
               bottom=True,
               top=True,
               left=True,
               right=True)
ax.grid(which='major',
        color='k')
ax.minorticks_on()
ax.grid(which='minor',
        color='gray',
        linestyle=':')
ax.set_ylabel('Эффективность')
ax.set_xlabel('Угловая скорость, об/мин')
# ax.set_xlim(xmin=nrg[0], xmax=nrg[-1])
fig.tight_layout()

plt.show()
import PIL
from PIL import Image
from PIL import ImageGrab
import numpy as np
import time
from matplotlib import pyplot as plt
import threading

def busca(region):
    start = time.time()
    screen = ImageGrab.grab(region)
    cor = (0,0,0)
    final = []
    pixel_matrix = np.array(screen)
    for x in range(0,screen.size[0]):
        for y in range(0,screen.size[1]):
            if cor == tuple(pixel_matrix[y][x]):
                final.append((x,y))
    end_time = time.time() - start
    # if region != '':
    #     x = region[2]-region[0]
    #     y = region[3]-region[1]
    #     print(end_time, region, x*y)
    return end_time

regiao_de_teste = (0,0,1366,768)
screen_total = ImageGrab.grab(regiao_de_teste)
speedup = []
area = []
tempo_0 = busca(regiao_de_teste)
print(tempo_0)
print()
print()
for i in range(2,10):
    step_x = round(screen_total.size[0]/i)
    step_y = round(screen_total.size[1]/i)
    regions = []
    y_count = 0
    threads = list()
    while y_count+5 < screen_total.size[1]:
        x_count = 0
        while x_count+5 < screen_total.size[0]:
            region_to_append = (x_count, y_count, x_count+step_x, y_count+step_y)
            if x_count+step_x+5 > screen_total.size[0]:
                region_to_append = (x_count, y_count, screen_total.size[0], y_count+step_y)
            elif y_count+step_y+5 > screen_total.size[1]:
                region_to_append = (x_count, y_count,x_count+step_x, screen_total.size[1])
            elif y_count+step_y+5 > screen_total.size[1] and x_count+step_x+5 > screen_total.size[0]:
                region_to_append = (x_count, y_count, screen_total.size[0], screen_total.size[1])
            regions.append(region_to_append)
            x_count += step_x
        y_count += step_y
    #print(regions)
    #input()
    tempo_inicio = time.time()
    for region in regions:
        thread_aaa = threading.Thread(target=busca, args=(region,))
        thread_aaa.start()
        threads.append(thread_aaa)
    for thread in threads:
        thread.join()
    tempo_total = time.time() - tempo_inicio
    print(tempo_total)
    speedup.append(tempo_total)
    area.append(round(step_x*step_y))
    print('################################')

# plt.plot(area,speedup)
# plt.show()
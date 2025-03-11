from Functions import *
death_radius = death_radius(0)

'''
Bacteria Setup
'''
bacteria.create_defaults()

'''
Grid Setup
'''
grid = grid(140,100,10)

grid.window.protocol("WM_DELETE_WINDOW", grid.handler)

'''
Main Loop
'''
nf_amount = []

run = True

while run:
    '''
    Canvas
    '''
    grid.canvas.delete("all")

    for r in range(len(heatmap)):
        for c in range(len(heatmap[0])):
            grid.canvas.create_rectangle((10*c,10*r), (10*(c+1), 10*(r+1)),
                                    fill=bacteria.dic[heatmap[r][c]].colour)

            bacteria.dictionary[heatmap[r][c]].ammend_count()
            
    N = nf.count + np.count + nc.count + ncp.count
    '''
    Moverment
    '''
    order = heatmap_order_shuffle(heatmap)
    heatmap = move_random(heatmap,0.25,order)
    
    grid.window.update()
    #sleep(0.5)

    print([nf.count,np.count,nc.count,ncp.count])
    nf_amount.append(nf.count)

    bacteria.reset_all_counts()

grid.window.mainloop()

plt.plot(nf_amount)
plt.show()

'''
References/ Resources
'''
#https://stackoverflow.com/questions/7966119/display-fullscreen-mode-on-tkinter

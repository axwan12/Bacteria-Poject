from Functions import *
'''
Bacteria Setup
'''
bacteria.create_defaults()
bacteria.accumalate_all_spawn()

'''
Grid Setup
'''
grid = grid(140,100,10,bacteria,'bacteria')

'''
Main Loop
'''
grid.run = True

while grid.run:
    heatmap = grid.heatmap
    '''
    Canvas
    '''
    grid.canvas.delete("all")

    for r in range(len(heatmap)):
        for c in range(len(heatmap[0])):
            colour(heatmap,grid.canvas,r,c)

            bacteria.dic[heatmap[r][c]].ammend_count()
    '''
    Moverment
    '''
    heatmap = move_random(heatmap,0.25,2)
    
    grid.window.update()
    sleep(0.5)
    
    bacteria.dic['nf'].bacteria_history()
    bacteria.reset_all_counts()
    
grid.window.mainloop()

plt.plot(bacteria.dic['nf'].history)
plt.show()

'''
References/ Resources
'''
#https://stackoverflow.com/questions/7966119/display-fullscreen-mode-on-tkinter

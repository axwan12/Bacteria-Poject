from Functions import *
'''
Bacteria Setup
'''
bacteria.create_defaults()

'''
Grid Setup
'''
grid = grid(200,200,10,bacteria,'bacteria')

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
    heatmap = Behaviour(heatmap,0.25,2,1)
    
    grid.window.update()
    sleep(0.5)
    
    bacteria.dic['nf'].bacteria_history()
    bacteria.dic['np'].bacteria_history()
    bacteria.dic['nc'].bacteria_history()
    bacteria.dic['ncp'].bacteria_history()
    bacteria.reset_all_counts()
    
grid.window.mainloop()

plt.plot(bacteria.dic['nf'].history)
plt.plot(bacteria.dic['np'].history)
plt.plot(bacteria.dic['nc'].history)
plt.plot(bacteria.dic['ncp'].history)
plt.show()

print(bacteria.dic[heatmap[10][15]].plasmid)

'''
References/ Resources
'''
#https://stackoverflow.com/questions/7966119/display-fullscreen-mode-on-tkinter
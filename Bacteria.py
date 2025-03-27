from Functions import *
'''
Bacteria Setup
'''
bacteria.create_defaults()

'''
Grid Setup
'''
grid = grid(50,50,20,bacteria,'bacteria')

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
            colour(heatmap,grid.canvas,r,c,20)

            bacteria.dic[heatmap[r][c]].ammend_count()
    '''
    Moverment
    '''
    heatmap = Behaviour(heatmap,0.25,2,1)
    
    grid.window.update()
    sleep(0.1)
    
    bacteria.dic['nf'].bacteria_history()
    bacteria.dic['np'].bacteria_history()
    bacteria.dic['nc'].bacteria_history()
    bacteria.dic['ncp'].bacteria_history()
    bacteria.reset_all_counts()
    
grid.window.mainloop()

# Plot with colors and labels
plt.plot(bacteria.dic['nf'].history, color='red', label='NF Bacteria')
plt.plot(bacteria.dic['nc'].history, color='black', label='NC Bacteria')
plt.plot(bacteria.dic['np'].history, color='blue', label='NP Bacteria')
plt.plot(bacteria.dic['ncp'].history, color='green', label='NCP Bacteria')

# Add labels and title
plt.xlabel("Time Steps")
plt.ylabel("Bacteria Count")
plt.title("Bacteria Growth Over Time")

# Add a legend
plt.legend()

# Show the plot
plt.show()

print(bacteria.dic[1].reproduction_rate)

'''
References/ Resources
'''
#https://stackoverflow.com/questions/7966119/display-fullscreen-mode-on-tkinter
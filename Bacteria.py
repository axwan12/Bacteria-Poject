from Functions import *
global size
size = [140 , 100]
square_size = 10

death_radius = death_radius(0)

'''
Bacteria Setup
'''
bacteria.create_defaults()
nf = bacteria(1,0,1,'red')
np = bacteria(0,0,2,'blue')
nc = bacteria(0,0,3,'black')
ncp = bacteria(0,0,4,'green')

'''
Grid Setup
'''
heatmap = []
for r in range(size[1]):
    thisrow = []
    for c in range(size[0]):
        if random() < nf.spawn_rate:
            thisrow.append(1)
        else:
            thisrow.append(0)
    heatmap.append(thisrow)
#heatmap[35][45] = 1

window = Tk()
window.attributes('-fullscreen', False)
window.title("Bacteria")

x = window.winfo_screenwidth()
y = window.winfo_screenheight()
print([x,y])

canvas = Canvas(window, width=size[0]*square_size, height=size[1]*square_size, bg='white')
canvas.pack(anchor=CENTER, expand=True)

def handler():
    global run
    run = False
    window.destroy()
window.protocol("WM_DELETE_WINDOW", handler)

'''
Main Loop
'''
nf_amount = []

run = True

while run:
    '''
    Canvas
    '''
    canvas.delete("all")

    for r in range(len(heatmap)):
        for c in range(len(heatmap[0])):
            canvas.create_rectangle((10*c,10*r), (10*(c+1), 10*(r+1)),
                                    fill=bacteria.dictionary[heatmap[r][c]].colour)

            bacteria.dictionary[heatmap[r][c]].ammend_count()
            
    N = nf.count + np.count + nc.count + ncp.count
    '''
    Moverment
    '''
    order = heatmap_order_shuffle(heatmap)
    heatmap = move_random(heatmap,0.25,order)
    
    window.update()
    #sleep(0.5)

    print([nf.count,np.count,nc.count,ncp.count])
    nf_amount.append(nf.count)

    bacteria.reset_all_counts()

window.mainloop()

plt.plot(nf_amount)
plt.show()

'''
References/ Resources
'''
#https://stackoverflow.com/questions/7966119/display-fullscreen-mode-on-tkinter

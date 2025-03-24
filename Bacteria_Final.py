from Functions_Final import *
def update_colony():
    global colony
    colony = colony_var.get()
    print(f"Colony is {'ON' if colony else 'OFF'}")

def sim_choice():
    global gui_running
    gui_running = False
    gui.destroy()

# Initial variable states
gui_running = True
colony = False

# Run GUI loop
while gui_running:
    # Create main window
    gui = Tk()
    gui.title("Bacteria Simulation")
    gui.geometry("400x100")

    # Variable to track checkbox state
    colony_var = BooleanVar()
    colony_var.set(False)  # Default to unchecked

    # Create checkbox
    colony_checkbox = Checkbutton(gui, text="Colony Initial Condition", variable=colony_var, command=update_colony)
    colony_checkbox.pack()

    # Create start button
    start_button = Button(gui, text="Start", command=sim_choice)
    start_button.pack()

    gui.mainloop()

'''
Bacteria Setup
'''
bacteria.create_defaults()

'''
Grid Setup
'''
bacteria_grid = grid(50,50,20,bacteria,'bacteria',colony,'np')

death_radius = 2
  
death_zone = AOE(death_radius)
interaction_zone = AOE(2)

'''
Main Loop
'''
bacteria_grid.run = True

while bacteria_grid.run:
    heatmap = bacteria_grid.heatmap
    '''
    Canvas
    '''
    bacteria_grid.canvas.delete("all")

    for r in range(len(heatmap)):
        for c in range(len(heatmap[0])):
            colour(heatmap,bacteria_grid.canvas,r,c,bacteria_grid)

            bacteria.dic[heatmap[r][c]].ammend_count()

    '''
    Moverment
    '''
    heatmap = Behaviour(heatmap,0.25,death_radius,death_zone,interaction_zone)
    
    bacteria_grid.window.update()
    sleep(0.1)
    
  

    if bacteria.dic['ncp'].count == 0:
        bacteria_grid.handler()
    
    bacteria.reset_all_counts()
    
bacteria_grid.window.mainloop()

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

'''
References/ Resources
'''
#https://stackoverflow.com/questions/7966119/display-fullscreen-mode-on-tkinter
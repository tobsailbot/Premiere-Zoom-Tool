
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import pymiere


#  solucionar que cuando selecciono otro clip se actualice el pymiere selected clip
#  agregar transicion de medio segundo al zoom, estableciendo un valor inicial a partir del 100% anterior al zoom



try:
    seq = pymiere.objects.app.project.activeSequence
    tracks = seq.videoTracks
except Exception as e:
    root = Tk()
    root.withdraw()
    tkinter.messagebox.showinfo('Error', 'No hay una secuencia activa de Premiere Pro')
    exit()



# cantidad de tracks
tracks_num = tracks.numTracks

selected_clip = None

# hacer un loop entre los distintos clips de los distintos tracks
def getClips(i):
    num = 0
    try:
        while True:
            selection = tracks[i].clips[num].isSelected()
            # print(tracks[i].clips[num].name)
            if selection == True:
                global selected_clip
                selected_clip = [i,num]
                print('el clip seleccionado es:')
                print(tracks[i].clips[num].name)
                # print(i,num)
                break
            num += 1

    # si aparece error no hacer nada..
    except:
        None



def loopTracks():
    i = 0
    # por cada track, obetner el clip correspondiente al index (i)
    for t in tracks:
        # print(f'clips del track numero {i}:')
        getClips(i)
        # print('\n')
        i += 1



def addFrames(track,clip,i,j,sca,sec): # t = track, c = clip, i = x, j = y, s = scale

    project = pymiere.objects.app.project

    # seleccionar video sequence
    videoTracks = project.activeSequence.videoTracks
    #seleccionar el track uno de la sequence

    #seleccionar clip de la sequence
    clip = videoTracks[track].clips[clip]

    components = clip.components[1]

    # seleccioanr la propiedad : 0 = position,  1 = scale
    position = components.properties[0]
    scale = components.properties[1]

    # activa el relojito
    position.setTimeVarying(True)
    scale.setTimeVarying(True)

    # obtiene el valor actual del parametro
    actual_scale = scale.getValue()
    actual_position = position.getValue()

    # add keyframes inpoint 0s
    scale.addKey(clip.inPoint.seconds)
    position.addKey(clip.inPoint.seconds)
    # setear valor inicial en inpoint
    position.setValueAtKey(clip.inPoint.seconds,actual_position, True)
    scale.setValueAtKey(clip.inPoint.seconds, actual_scale, True)

    # add frames inpoint +sec (segundos)
    scale.addKey(clip.inPoint.seconds + sec)
    position.addKey(clip.inPoint.seconds + sec) 
    # setear valores de las propiedades
    position.setValueAtKey(clip.inPoint.seconds + sec, [i, j], True)

    # setear valor de escala absoluta (125%, 150% etc..)
    # scale.setValueAtKey(clip.inPoint.seconds + sec, sca, True)

    # setear valor de escala relativa (% basado en la inicial)
    scale.setValueAtKey(clip.inPoint.seconds + sec, actual_scale * (sca/100), True)

    # cambia interpolacion de frames a smooth curve (Premiere v22)
    # position.setInterpolationTypeAtKey(1)
    



#----------------------------------------------------------

window = Tk()
# Main window configuration
window.configure(bg="gray25")
window.title("Premiere Zoom Tools")
window.resizable(False, False)
window.attributes('-topmost', True)

positions_frame = Frame(window)
positions_frame.configure(bg='gray25',pady=5,padx=5)
positions_frame.pack()

# Tkinter string variable able to store any string value
v = StringVar(window, "1")

# Dictionary to create multiple buttons
values = {"0": [0,0], 
          "1": [0,1],
          "2": [0,2],
          "3": [0,3],
          "4": [0,4],

          "5": [1,0],
          "6": [1,1],
          "7": [1,2],
          "8": [1,3],
          "9": [1,4],

          "10": [2,0],
          "11": [2,1],
          "12": [2,2],
          "13": [2,3],
          "14": [2,4],
          }



# Loop is used to create multiple Radiobuttons rather than creating each button separately
for (key, value) in values.items():
    i = int(key)
    Radiobutton(positions_frame, text='', variable=v, width=7,height=3,
                value=value, indicator=0, borderwidth=0,activebackground="grey20",selectcolor='gray40',
                background="gray15").grid(row=str(value[0]),column=str(value[1]),pady=1,padx=1)

v.set("1")

# slider values stick to whole numbers
def whole_number_only_zoom(e=None):
    value = zoom.get()
    if int(value) != value:
        zoom.set(round(value))

# crea un slider para el zoom scale
styleW = ttk.Style()
styleW.configure("TScale", background="grey25", foreground="grey25", troughcolor="grey25",)
zoom = ttk.Scale(window, from_=1, to=4, length=275, style="TScale", command=whole_number_only_zoom)
       
zoom.set(2) # set the default value


# slider values stick to whole numbers
def whole_number_only_duration(e=None):
    value = duration.get()
    if int(value) != value:
        duration.set(round(value))


# crea un slider para el zoom scale
style = ttk.Style()
style.configure("TScale", background="grey25", foreground="grey25", troughcolor="grey25",)
duration = ttk.Scale(window, from_=1, to=4, length=275, style="TScale", command=whole_number_only_duration)

duration.set(2) # set the default value



#  funcion que tome como parametros index (0,0) ,
#  haga los calculos sobre base y escala correspondientes al slider
#  y retorne la lista con el index

def PosAndScale():

    b = 0.5  # base center position value
    scale_value = zoom.get() # get the scale value
    seconds_value = duration.get() # get the duration value

    if seconds_value == 1:
        sec = 0.2
    if seconds_value == 2:
        sec = 0.5
    if seconds_value  == 3:
        sec = 0.8
    if seconds_value == 4:
        sec = 1.5

    if scale_value == 1:
        s = 0.125
        sca = 125
    if scale_value == 2:
        s = 0.25
        sca = 150
    if scale_value == 3:
        s = 0.375
        sca = 175
    if scale_value == 4:
        s = 0.5
        sca = 200

    # lista que contiene las coordenadas teniendo en cuenta las b(base) y s(scale)
    arr_list = [[[b + s, b + s], [((b + s) + b) / 2, b + s], [b, b + s], [((b - s) + b) / 2, b + s], [b - s, b + s]],
                [[b + s, b], [((b + s) + b) / 2, b], [b, b], [((b - s) + b) / 2, b], [b - s, b]],
                [[b + s, b - s], [((b + s) + b) / 2, b - s], [b, b - s], [((b - s) + b) / 2, b - s], [b - s, b - s]]]

    # obtener valores del radialbutton = '0 0'
    button_value = v.get()
    
    # convertir valores en una lista de strings = ['0','0']
    listRes = list(button_value.split(" "))

    # convertir lista de str en lista de int = [0,0]
    integer_map = map(int, listRes)
    integer_list = list(integer_map)

    # pasar la lista como index para obtener los valores de array list [0.5, 0.5]
    try:
        pos = arr_list[integer_list[0]][integer_list[1]]
    except IndexError:
        pos = [0.5, 0.5]

    loopTracks()
    # imprime lista con el track = [0] y el clip = [1] seleccionado

    sel_track = selected_clip[0]
    sel_clip = selected_clip[1]

    # pasa parametros a la funcion addFrames()
    addFrames(sel_track, sel_clip,pos[0] , pos[1], sca, sec)
    # print an f string
    print(f'{sca}%')
    print('--- Frames Added ---')
    


# -----------------------------------------------

def RemoveFrames():
    loopTracks()
    # imprime lista con el track = [0] y el clip = [1] seleccionado

    project = pymiere.objects.app.project

    # seleccionar video sequence
    videoTracks = project.activeSequence.videoTracks
    #seleccionar el track uno de la sequence

    #seleccionar clip de la sequence
    clip = videoTracks[selected_clip[0]].clips[selected_clip[1]]

    components = clip.components[1]

    # seleccioanr la propiedad : 0 = position,  1 = scale
    position = components.properties[0]
    scale = components.properties[1]

    # desactiva el relojito
    position.setTimeVarying(False)
    scale.setTimeVarying(False)

    # remove keyframes
    position.removeKeyRange(clip.inPoint.seconds,clip.outPoint.seconds,True)
    scale.removeKeyRange(clip.inPoint.seconds,clip.outPoint.seconds,True)
    print('--- Frames Removed ---')


# ------------------------------------------------------

scale_name = Label(window, text="Zoom level:", anchor="w")
scale_name.configure(bg="grey25",fg="grey75", width=39)
scale_name.pack(pady=(6,1))

zoom.pack()

scale_label = Label(window, text="125%                 150%                    175%                  200%")
scale_label.configure(bg="grey25",fg="grey75")
scale_label.pack()

duration_name = Label(window, text="Time (seconds):", anchor="w")
duration_name.configure(bg="grey25",fg="grey75", width=39)
duration_name.pack(pady=(7,1))

duration.pack()

duration_label = Label(window, text="0.2                       0.5                        0.8                        1.5")
duration_label.configure(bg="grey25",fg="grey75")
duration_label.pack()

buttons_frame = Frame(window)
buttons_frame.pack(pady=(20,15))
buttons_frame.configure(bg="grey25")

def onEnterApply(e):
    e.widget['background'] = '#307cff'
    return

def onLeaveApply(e):
    e.widget['background'] = '#2663cc'
    return

def onEnterRemove(e):
    e.widget['background'] = 'grey45'
    return

def onLeaveRemove(e):
    e.widget['background'] = 'grey40'
    return


applyBtn = Button(buttons_frame)
applyBtn.configure(command=PosAndScale, text='Apply', bg="#2663cc", fg="grey93", width=10, height=2, bd=0,
                   activebackground="grey70", activeforeground="white", highlightbackground="light grey",
                   cursor="hand2")
applyBtn.grid(column=1, row=0, padx=(20, 5))
applyBtn.bind("<Enter>", onEnterApply)
applyBtn.bind("<Leave>", onLeaveApply)

removeBtn = Button(buttons_frame)
removeBtn.configure(command=RemoveFrames, text='Remove', bg="grey40", fg="grey93", width=10, bd=0, height=2,
                    activebackground="grey70", activeforeground="white", highlightbackground="white",
                    cursor="hand2")
removeBtn.grid(column=0, row=0, padx=(5, 40))
removeBtn.bind("<Enter>", onEnterRemove)
removeBtn.bind("<Leave>", onLeaveRemove)





mainloop()


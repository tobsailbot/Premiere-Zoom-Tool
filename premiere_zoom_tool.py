from tkinter import *
import pymiere



#  solucionar que cuando selecciono otro clip se actualice el pymiere selected clip
#  agregar transicion de medio segundo al zoom, estableciendo un valor inicial a partir del 100% anterior al zoom




window = Tk()


seq = pymiere.objects.app.project.activeSequence
tracks = seq.videoTracks

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



def addFrames(t,c,i,j,s):

    project = pymiere.objects.app.project

    # seleccionar video sequence
    videoTracks = project.activeSequence.videoTracks
    #seleccionar el track uno de la sequence

    #seleccionar clip de la sequence
    clip = videoTracks[t].clips[c]

    components = clip.components[1]

    # seleccioanr la propiedad : 0 = position,  1 = scale
    position = components.properties[0]
    scale = components.properties[1]

    # activa el relojito
    position.setTimeVarying(True)
    scale.setTimeVarying(True)


    # add frames centerpoint
    scale.addKey(clip.inPoint.seconds+0.5)
    position.addKey(clip.inPoint.seconds+0.5)

    position.setValueAtKey(clip.inPoint.seconds+0.5, [i, j], True)
    scale.setValueAtKey(clip.inPoint.seconds+0.5,s, True)

    # obtiene el valor actual del parametro
    actual_scale = scale.getValue()
    # actual_position = position.getValue()

    # add keyframes before
    scale.addKey(clip.inPoint.seconds)
    position.addKey(clip.inPoint.seconds)

    position.setValueAtKey(clip.inPoint.seconds,[0.5,0.5], True)
    scale.setValueAtKey(clip.inPoint.seconds, actual_scale, True)



#----------------------------------------------------------


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
    # print(value[0])
    Radiobutton(positions_frame, text='', variable=v, width=10,height=4,
                value=value, indicator=0, borderwidth=0,activebackground="grey20",selectcolor='gray40',
                background="gray15").grid(row=str(value[0]),column=str(value[1]),pady=1,padx=1)



w = Scale(window, from_=1, to=4, length=300, orient=HORIZONTAL,bg = "grey25",bd=0,fg="grey25",
          highlightbackground="grey25")
w.set(2)


# funcion que tome como parametros index (0,0) , haga los calculos sobre base y escala correspondientes al slider y retorne la lista con el index

def PosAndScale():
    b = 0.5  # base center position value
    scale_value = w.get()

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

    # lista que contiene las coordenadas teniendo e ncuenta las b(base) y s(scale)
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
    # print(integer_list)

    # pasar la lista como index para obtener los valores de array list [0.5, 0.5]
    pos = arr_list[integer_list[0]][integer_list[1]]

    loopTracks()
    # imprime lista con el track = [0] y el clip = [1] seleccionado

    sel_track = selected_clip[0]
    sel_clip = selected_clip[1]

    # pasa parametros a la funcion addFrames()
    addFrames(sel_track, sel_clip,pos[0] , pos[1], sca)

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

    # remove keyframes
    position.removeKeyRange(clip.inPoint.seconds,clip.outPoint.seconds,True)
    scale.removeKeyRange(clip.inPoint.seconds,clip.outPoint.seconds,True)
    print('--- Frames Removed ---')


# ------------------------------------------------------

w.pack()



scale_label = Label(window, text="125%                    150%                    175%                    200%")
scale_label.configure(bg="grey25",fg="grey75")
scale_label.pack()

buttons_frame= Frame(window)
buttons_frame.pack(pady=(20,15))
buttons_frame.configure(bg="grey25")

applyBtn = Button(buttons_frame)
applyBtn.configure(command=PosAndScale, text='Apply',bg="grey40",fg="grey93",width=10,height=2,bd=0,
                   activebackground="grey70",activeforeground="white")
applyBtn.grid(column= 1, row=0,padx=(50,5))


removeBtn = Button(buttons_frame)
removeBtn.configure(command= RemoveFrames,text='Remove',bg="grey40",fg="grey93",width=10,bd=0,height=2,
                    activebackground="grey70",activeforeground="white")
removeBtn.grid(column= 0, row=0,padx=(5,40))



mainloop()


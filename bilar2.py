import PySimpleGUI as sg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("prog1/bilar.csv")

def andra(): 
    layout = [
        [sg.Text("Utav de alternativ du ser nedan, vad vill du veta?")],
        [sg.Text("Type,AWD,RWD,Retail Price,Dealer Cost,Engine Size (l),Cyl,Horsepower(HP)")],
        [sg.Text("City Miles Per Gallon,Highway Miles Per Gallon,Weight,Wheel Base,Len,Width")],
        [sg.InputText(key="info")],
        [sg.Button("OK")],
        [sg.Text(size=(50, 1), key="-ERROR-", text_color="red")]
    ]

    window = sg.Window('Bilprogram', layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if values["info"] in ["Horsepower(HP)", "Engine Size (l)", "Retail Price", "Dealer Cost", "Cyl", "City Miles Per Gallon", "Highway Miles Per Gallon", "Weight", "Wheel Base", "Len", "Width"]:
            most = sg.popup_get_text("Vill du sortera minst eller mest?")
            nummer(values["info"], most)
        elif values["info"] in ["AWD", "RWD"]:
            hjul()
        elif values["info"] == "Type":
            biltyper()
        else:
            window["-ERROR-"].update(f"Ogiltig inmatning: {values['info']}") 
    window.close()

def graf():
    categories = ['Retail Price', 'Dealer Cost', 'Engine Size (l)', 'Cyl', 'Horsepower(HP)',
                  'City Miles Per Gallon', 'Highway Miles Per Gallon', 'Weight']
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    ax = plt.subplot(111, polar=True)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    plt.xticks(angles[:-1], categories)
    values = [df['Retail Price'].mean(), df['Dealer Cost'].mean(), df['Engine Size (l)'].mean(), df['Cyl'].mean(),
              df['Horsepower(HP)'].mean(), df['City Miles Per Gallon'].mean(), df['Highway Miles Per Gallon'].mean(),
              df['Weight'].mean()]
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid')
    ax.fill(angles, values, 'b', alpha=0.1)
    ax.set_rlim(0, 1000)
    plt.show()

def nummer(info, most):
    if most == "mest":
        sorted_df = df.sort_values(by=[info], ascending=False).head(10)
    elif most == "minst":
        sorted_df = df.sort_values(by=[info], ascending=True).head(10)
    else:
        return
    plt.bar(sorted_df['Name'], sorted_df[info])
    plt.xticks(rotation=90)
    plt.ylabel(info)
    plt.title(f'Bilar med mest {info}')
    plt.show()

def hjul():
    layout = [[sg.Text("vill du veta information om AWD eller RWD")],
              [sg.InputText(key="info3")],
              [sg.Button("OK")],
              [sg.Text(size=(50,1), key="-ERROR-", text_color="red")]]
    window = sg.Window('Bilprogram', layout)
    antal_awd = df['AWD'].value_counts()[1]
    antal_rwd = 388 - antal_awd
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        info = values["info3"]
        if "info3" == "AWD":
            text1 = 'antal bilar med AWD är 78'
        elif "info3" == "RWD":
            text2 = 'antal bilar med RWD är 310'
        
        labels = ['AWD', 'RWD']
        values = [antal_awd, antal_rwd]
        colors = ['blue', 'red']
        plt.pie(values, labels=labels, colors=colors, autopct='%1.0f%%')
        plt.title(f"{info}")
        plt.show()

def namn():
    layout = [[sg.Text("Vilken bil vill du veta mer om?")],
              [sg.Input(key='model')],
              [sg.Text("Vill du veta någon specifik information om bilen? (ja/nej)")],
              [sg.Input(key='yes_no')],
              [sg.Text("Vilken information?")],
              [sg.Input(key='info')],
              [sg.Button('OK')]]
    window = sg.Window('Bilprogram', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'OK':
            model = values['model']
            selected_row = df.loc[df['Name'] == model]
            info2 = values['yes_no']
            if info2 == "ja":
                info3 = values['info']
                if info3 == "AWD":
                    if selected_row[info3].iloc[0] == 1:
                        sg.popup(f"{model} har AWD")
                    else:
                        sg.popup(f"{model} har inte AWD")
                elif info3 == "RWD":
                    if selected_row[info3].iloc[0] == 1:
                        sg.popup(f"{model} har RWD")
                    else:
                        sg.popup(f"{model} har inte RWD")
                else:
                    sg.popup(f"{model} har {selected_row[info3].values[0]} {info3}")
            elif info2 == "nej":
                graf()
            else:
                sg.popup("Skriv ja eller nej")
                continue
            break
    window.close()

def biltyper():
    type_counts = df['Type'].value_counts()
    plt.bar(type_counts.index, type_counts.values)
    plt.xticks(rotation=90)
    plt.ylabel('Antal bilar')
    plt.title('Antal bilar per typ')
    plt.show()

layout = [
    [sg.Text("hur vill du sortera vad du ska söka på")],
    [sg.Button("specifik information om specifik bil")],
    [sg.Button("specifik information utan specifik bil")],
]

window = sg.Window("Bilprogram", layout, size=(600, 170))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == "specifik information utan specifik bil":
        andra()
    elif event == "specifik information om specifik bil":
        namn()

window.close() 

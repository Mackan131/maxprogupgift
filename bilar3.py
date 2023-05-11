import PySimpleGUI as sg   # Importera PySimpleGUI-biblioteket för att skapa ett grafiskt användargränssnitt
import pandas as pd        # Importera Pandas-biblioteket för att arbeta med data frames
import numpy as np         # Importera NumPy-biblioteket för numeriska beräkningar
import matplotlib.pyplot as plt  # Importera Matplotlib-biblioteket för att plotta grafer

# Läs in CSV-filen "bilar.csv" med Pandas och lagra den i en data frame som heter df
df = pd.read_csv("prog1/bilar.csv")

# Definiera en funktion som heter "andra" som kommer att användas för att fråga användaren om information om datan
def andra():
    # Definiera layouten för användargränssnittet
    layout = [
        [sg.Text("Utav de alternativ du ser nedan, vad vill du veta?")],
        [sg.Text("Type,AWD,RWD,Retail Price,Dealer Cost,Engine Size (l),Cyl,Horsepower(HP)")],
        [sg.Text("City Miles Per Gallon,Highway Miles Per Gallon,Weight,Wheel Base,Len,Width")],
        [sg.InputText(key="info")],
        [sg.Button("OK")],
        [sg.Text(size=(50, 1), key="-ERROR-", text_color="red")]
    ]
    window = sg.Window('Bilprogram', layout)    # Skapa ett fönster med namnet "Bilprogram" och använd layouten ovan
    while True:
        event, values = window.read()   # Läs in användarens val och spara dem i variabeln "values"
        if event == sg.WINDOW_CLOSED:   # Om användaren stänger fönstret, avsluta programmet
            break
        if values["info"] in ["Horsepower(HP)", "Engine Size (l)", "Retail Price", "Dealer Cost", "Cyl", "City Miles Per Gallon", "Highway Miles Per Gallon", "Weight", "Wheel Base", "Len", "Width"]:
            # Om användaren har valt en kolumn som innehåller numeriska värden, fråga användaren om de vill sortera minst eller mest
            most = sg.popup_get_text("Vill du sortera minst eller mest?")
            nummer(values["info"], most)
        elif values["info"] in ["AWD", "RWD"]:
            # Om användaren har valt kolumnen "AWD" eller "RWD", visa bilmodeller med det drivningssättet
            hjul()
        elif values["info"] == "Type":
            # Om användaren har valt kolumnen "Type", visa olika biltyper
            biltyper()
        else:
            # Om användaren har angett en ogiltig inmatning, visa ett felmeddelande
            window["-ERROR-"].update(f"Ogiltig inmatning: {values['info']}")
    window.close()

# Skapa en funktion som ritar ett spideldiagram baserat på medelvärden för olika fordonsegenskaper från en DataFrame (df).
def graf():
    # Definiera en lista med kategorinamn.
    categories = ['Retail Price', 'Dealer Cost', 'Engine Size (l)', 'Cyl', 'Horsepower(HP)',
                  'City Miles Per Gallon', 'Highway Miles Per Gallon', 'Weight']
    
    # Beräkna antalet kategorier (N) och vinklarna för varje kategori (angles).
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    # Skapa en polar axel och ställ in polarinställningarna.
    ax = plt.subplot(111, polar=True)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    # Ställ in tick-märken på x-axeln med kategorinamnen.
    plt.xticks(angles[:-1], categories)
    
    # Beräkna medelvärdena för olika fordonsdata-egenskaper och spara dessa i en lista (values).
    values = [df['Retail Price'].mean(), df['Dealer Cost'].mean(), df['Engine Size (l)'].mean(), df['Cyl'].mean(),
              df['Horsepower(HP)'].mean(), df['City Miles Per Gallon'].mean(), df['Highway Miles Per Gallon'].mean(),
              df['Weight'].mean()]
    
    # Lägg till det första värdet på slutet av listan (för att "stänga" polygontformen).
    values += values[:1]
    
    # Rita linjen som representerar medelvärdena för olika fordonsdata-egenskaper på radarplotten.
    ax.plot(angles, values, linewidth=1, linestyle='solid')
    
    # Fyll i polygontformen med en blå färg.
    ax.fill(angles, values, 'b', alpha=0.1)
    
    # Ställ in gränserna för r-axeln (radien) till 0-1000.
    ax.set_rlim(0, 1000)
    
    # Visa diagrammet.
    plt.show()

def nummer(info, most):
    # Sortera dataframen df efter den angivna kolumnen i antingen stigande eller fallande ordning
    # beroende på värdet av most-parameteren, och välj de tio första raderna.
    if most == "mest":
        sorted_df = df.sort_values(by=[info], ascending=False).head(10)
    elif most == "minst":
        sorted_df = df.sort_values(by=[info], ascending=True).head(10)
    else:
        # Om most inte är "mest" eller "minst", returnera ingenting.
        return
    # Skapa ett stapeldiagram med bilnamnen på x-axeln och den angivna kolumnen på y-axeln.
    plt.bar(sorted_df['Name'], sorted_df[info])
    # Rotera x-axeltexten 90 grader så att den är lättare att läsa.
    plt.xticks(rotation=90)
    # Ange etiketttext för y-axeln baserat på info-parametern.
    plt.ylabel(info)
    # Ange en titel för diagrammet baserat på info-parametern.
    plt.title(f'Bilar med mest {info}')
    # Visa diagrammet i ett nytt fönster.
    plt.show()

def hjul():
    # Skapa ett layout-objekt för fönstret med en textfråga, en textruta för input och en knapp
    layout = [[sg.Text("Vill du veta information om AWD eller RWD?")],
              [sg.InputText(key="info3")],
              [sg.Button("OK")],
              [sg.Text(size=(50,1), key="-ERROR-", text_color="red")]]
    
    # Skapa ett fönster-objekt med titeln "Bilprogram" och den tidigare definierade layouten
    window = sg.Window('Bilprogram', layout)
    
    # Beräkna antalet bilar med AWD och RWD från en dataframe (df) och spara i variabler
    antal_awd = df['AWD'].value_counts()[1]
    antal_rwd = 388 - antal_awd
    
    # Skapa en evighets-loop som körs tills användaren stänger fönstret
    while True:
        # Läs in användarens input från textrutan och vilket event som inträffar (knapptryck eller stängning av fönstret)
        event, values = window.read()
        
        # Om användaren stänger fönstret bryter vi loopen
        if event == sg.WIN_CLOSED:
            break
        
        # Annars sparar vi användarens input i en variabel
        info = values["info3"]
        
        # Om användaren skrev "AWD" skapar vi en textsträng med information om antalet bilar med AWD
        if info == "AWD":
            text1 = f'Antal bilar med AWD är {antal_awd}'
        
        # Om användaren skrev "RWD" skapar vi en textsträng med information om antalet bilar med RWD
        elif info == "RWD":
            text1 = f'Antal bilar med RWD är {antal_rwd}'
        
        # Annars visar vi en felmeddelande-text i rött
        else:
            window['-ERROR-'].update('Felaktig input, skriv "AWD" eller "RWD"')
            continue
        
        # Skapa en pie chart med antalet bilar med AWD och RWD, och visa den med hjälp av matplotlib
        labels = ['AWD', 'RWD']
        values = [antal_awd, antal_rwd]
        colors = ['blue', 'red']
        plt.pie(values, labels=labels, colors=colors, autopct='%1.0f%%')
        plt.title(f"{info}")
        plt.show()

# Funktionen "namn" skapar ett grafiskt användargränssnitt
def namn():
    layout = [[sg.Text("Vilken bil vill du veta mer om?")],  # Textfråga för att få användarens input
              [sg.Input(key='model')],  # Användaren skriver in bilmodell här
              [sg.Text("Vill du veta någon specifik information om bilen? (ja/nej)")],  # Fråga om användaren vill ha mer information eller inte
              [sg.Input(key='yes_no')],  # Användaren svarar ja eller nej här
              [sg.Text("Vilken information?")],  # Om användaren svarar ja, fråga vilken information som efterfrågas
              [sg.Input(key='info')],
              [sg.Button('OK')]]  # OK-knapp för att lämna in användarinput
    window = sg.Window('Bilprogram', layout)  # Skapar ett fönster med layouten ovan
    while True:
        event, values = window.read()  # Läser in användarinput och event som OK-knappen trycks
        if event == sg.WIN_CLOSED:  # Om användaren stänger fönstret, avsluta programmet
            break
        if event == 'OK':  # Om användaren trycker på OK-knappen, fortsätt
            model = values['model']  # Hämta bilmodellen från användarinput
            selected_row = df.loc[df['Name'] == model]  # Hämta raden i dataframen som motsvarar bilmodellen
            info2 = values['yes_no']  # Hämta svaret på ja/nej-frågan från användaren
            if info2 == "ja":  # Om användaren vill ha mer information
                info3 = values['info']  # Hämta vilken information som efterfrågas
                if info3 == "AWD":  # Om användaren efterfrågar information om AWD
                    if selected_row[info3].iloc[0] == 1:  # Om bilen har AWD
                        sg.popup(f"{model} har AWD")  # Skriv ut att bilen har AWD
                    else:
                        sg.popup(f"{model} har inte AWD")  # Annars skriv ut att bilen inte har AWD
                elif info3 == "RWD":  # Om användaren efterfrågar information om RWD
                    if selected_row[info3].iloc[0] == 1:  # Om bilen har RWD
                        sg.popup(f"{model} har RWD")  # Skriv ut att bilen har RWD
                    else:
                        sg.popup(f"{model} har inte RWD")  # Annars skriv ut att bilen inte har RWD
                else:
                    sg.popup(f"{model} har {selected_row[info3].values[0]} {info3}")  # Skriv ut vald information för bilen
            elif info2 == "nej":  # Om användaren inte vill ha mer information
                graf()  # Visa en graf över dataframen
            else:
                sg.popup("Skriv ja eller nej")  # Om användaren skriver något annat än ja eller nej,

# Funktion för att räkna och visualisera antalet bilar per typ
def biltyper():
    # Räkna antalet bilar per typ från DataFrame df
    type_counts = df['Type'].value_counts()

    # Skapa ett stapeldiagram med antalet bilar per typ
    plt.bar(type_counts.index, type_counts.values)

    # Vrid x-axelns etiketter med 90 grader för att de inte ska överlappa varandra
    plt.xticks(rotation=90)

    # Sätt en etikett på y-axeln för att beskriva vad den visar
    plt.ylabel('Antal bilar')

    # Sätt en titel på diagrammet
    plt.title('Antal bilar per typ')

    # Visa diagrammet
    plt.show()

# Skapa layouten för GUI:et med två knappar
layout = [
    [sg.Text("hur vill du sortera vad du ska söka på")],
    [sg.Button("specifik information om specifik bil")],
    [sg.Button("specifik information utan specifik bil")],
]

# Skapa fönstret med layouten
window = sg.Window("Bilprogram", layout, size=(600, 170))

# Loopa programmet tills användaren stänger programmet
while True:
    event, values = window.read()  # Läs in användarens interaktion med GUI:et
    if event == sg.WIN_CLOSED:  # Om användaren stänger fönstret
        break  # Avsluta programmet
    elif event == "specifik information utan specifik bil":  # Om användaren väljer att söka generell information
        andra()  # Anropa funktionen "andra" för att visa generell information
    elif event == "specifik information om specifik bil":  # Om användaren väljer att söka specifik information
        namn()  # Anropa funktionen "namn" för att visa specifik information

# Stäng fönstret när programmet avslutas
window.close()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg
df = pd.read_csv("prog1/bilar.csv")

def graf():
    categories = ['Retail Price', 'Dealer Cost', 'Engine Size (l)', 'Cyl', 'Horsepower(HP)', 'City Miles Per Gallon', 'Highway Miles Per Gallon', 'Weight']
    N = len(categories)

    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    ax = plt.subplot(111, polar=True)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    plt.xticks(angles[:-1], categories)

    values = [df['Retail Price'].mean(), df['Dealer Cost'].mean(), df['Engine Size (l)'].mean(), df['Cyl'].mean(), df['Horsepower(HP)'].mean(), df['City Miles Per Gallon'].mean(), df['Highway Miles Per Gallon'].mean(), df['Weight'].mean()]
    values += values[:1]

    ax.plot(angles, values, linewidth=1, linestyle='solid')

    ax.fill(angles, values, 'b', alpha=0.1)

    ax.set_rlim(0, 1000)
    
    plt.show()


def nummer():
    sorted_df = df.sort_values(by=[info], ascending=False).head(10)
    plt.bar(sorted_df['Name'], sorted_df[info])
    plt.xticks(rotation=90)
    plt.ylabel(info)
    plt.title(f'Bilar med mest {info}')
    plt.show()

def nummer2():
    sorted_df = df.sort_values(by=[info], ascending=True).head(10)
    plt.bar(sorted_df['Name'], sorted_df[info])
    plt.xticks(rotation=90)
    plt.ylabel(info)
    plt.title(f'Bilar med mest {info}')
    plt.show()

def hjul():
    antal_awd = df['AWD'].value_counts()[1]
    antal_rwd = 388 - antal_awd
    if info == 'AWD':
        text = 'antal bilar med AWD är 78'
    elif info == 'RWD':
        text = 'antal bilar med RWD är 310'
    else:
        text = 'okänt drivsystem'
    labels = ['AWD', 'RWD']
    values = [antal_awd, antal_rwd]
    colors = ['blue', 'red']
    plt.pie(values, labels=labels, colors=colors, autopct='%1.0f%%')
    plt.title(f"{text}")
    plt.show()

def namn():
    model = input("vilken bil vill du vete mer om? ")
    selected_row = df.loc[df['Name'] == model]
    info2 = input(f"vill du veta någon specifik information om {model}?(skriv ja eller nej)-->")
    if info2 == "ja":
        info3 = input("vilken information? ")
        if info3 == "AWD":
            if selected_row[info3].iloc[0] == 1:
                print(f"{model} har AWD")
            else:
                print(f"{model} har inte AWD")
        elif info3 == "RWD":
            if selected_row[info3].iloc[0] == 1:
                print(f"{model} har RWD")
            else:
                print(f"{model} har inte RWD")
        else:
            print(f"{model} har {selected_row[info3].values[0]} {info3}")
    elif info2 == "nej":
        graf()
    else:
        print("skriv något av dessa altenativ")
        print("Type,AWD,RWD,Retail Price,Dealer Cost,Engine Size (l),Cyl,Horsepower(HP)")
        print("City Miles Per Gallon,Highway Miles Per Gallon,Weight,Wheel Base,Len,Width")

def biltyper():
    type_counts = df['Type'].value_counts()
    plt.bar(type_counts.index, type_counts.values)
    plt.xticks(rotation=90)
    plt.ylabel('Antal bilar')
    plt.title('Antal bilar per typ')
    plt.show()

while True:
    print("Name,Type,AWD,RWD,Retail Price,Dealer Cost,Engine Size (l),Cyl,Horsepower(HP)")
    print("City Miles Per Gallon,Highway Miles Per Gallon,Weight,Wheel Base,Len,Width")
    print("skriv exit för att gå ur programmet")
    info = input("Utav de alternativ du ser ovan, vad vill du veta? ")
    if info == "exit":
        print("Programmet avslutas")
        break
    elif info == "Horsepower(HP)" or info == "Engine Size (l)" or info == "Retail Price" or info == "Dealer Cost" or info == "Cyl" or info == "City Miles Per Gallon" or info == "Highway Miles Per Gallon" or info == "Weight" or info == "Wheel Base" or info == "Len" or info == "Width":
        most = input("Vill du sortera minst eller mest? ")
        if most == "mest":
            nummer()
        elif most == "minst":
            nummer2()
        else:
            print("Du skrev inte minst eller mest så då får du inte testa igen")
    elif info == "AWD" or info == "RWD":
        hjul()
    elif info == "Type":
        biltyper()
    elif info == "Name":
        namn()
    else:
        print("Du skrev fel!!!")
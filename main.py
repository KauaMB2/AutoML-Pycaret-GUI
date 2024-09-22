import tkinter as tk
from tkinter import *
import os
from tkinter import messagebox
from tkinter import font
import pandas as pd
from Model import Model
import json

df=None
CSVAlreadyReaded=False
columnNamesList=[""]
modelsList=[]
selectModelMenu=None
configData={"modelsAmount":-1}
DIR = os.path.dirname(os.path.abspath(__file__))
inputEntries=[]

percentageList=["50%", "55%", "60%", "65%", "70%", "75%", "80%", "85%", "90%"]

def trainModel():
    global df
    if len(outputListBox.get(0,END))==0 or len(inputListBox.get(0,END))==0:
        messagebox.showwarning("WARNING", "The features list or the targets list is void! Please, firstly select the inputs and the outputs of the model.")
        return
    trainObject=Model(currentPercentageOption.get(), list(inputListBox.get(0, END)), list(outputListBox.get(0, END)))
    trainObject.trainModel(df)
    defineModelsList()
def predictTargets():
    global inputEntries, configData, DIR
    if "modelsInput" not in configData:
        messagebox.showwarning("WARNING", "Configuration data is missing 'modelsInput'.")
        return
    folderName=currentModelOption.get()
    inputData = []
    for entry in inputEntries:  # Collect and validate the input values
        value = entry.get()
        if not value.isdigit():  # Check if the input is a valid integer
            messagebox.showwarning("WARNING", "The inputs are not in the correct format.")
            return
        inputData.append(int(value))  # Convert to integer and add to input_data
    modelObject=Model(currentPercentageOption.get(), list(inputListBox.get(0, END)), list(outputListBox.get(0, END)))
    predictionsMessage=modelObject.Predict(inputData, configData, folderName, DIR)
    messagebox.showinfo("Predictions", predictionsMessage)
def readModel():
    global inputEntries, configData
    selectedModel = currentModelOption.get()
    if selectedModel == "":
        messagebox.showwarning("WARNING", "Please, firstly select a model.")
        return
    with open(fr"{DIR}\models\{selectedModel}\config.json", 'r') as json_file:
        configData = json.load(json_file)
    for entry in inputEntries:# Clear previous entries if any
        entry.destroy()
    inputEntries.clear()  # Clear the list
    for i in range(len(configData["modelsInput"])):# Create new entries
        predictLabel = tk.Label(root, text=f"{configData['modelsInput'][i]} value:", font=("calibri", 9), bg=PURPLE_COLOR, fg=WHITE_COLOR)
        predictLabel.place(x=(60 * i + 10), y=265)
        entry = tk.Entry(root, width=5)
        entry.place(x=(60 * i + 15), y=280)
        inputEntries.append(entry)  # Store the entry reference
    predictButton = Button(root, text="Predict", command=predictTargets, bg=PURPLE_COLOR, fg=WHITE_COLOR)# Create the Predict button
    predictButton.place(x=330, y=310)


def readCSVFile():
    global columnNamesList, df, CSVAlreadyReaded
    fileName=inputName.get()
    if fileName=="":
        messagebox.showerror("ERROR", "Please, firstly inform the file name.")
        return
    try:
        df=pd.read_csv(f"{fileName}.csv", low_memory=False)
    except:
        messagebox.showerror("Error", "It wasn't possible read the file. Please, be sure the file exist.")
        return
    columnNamesList = df.columns
    inputColumnNamesMenu['menu'].delete(0, END)  # Clear the current menu
    for column in columnNamesList:  # Add new column names
        inputColumnNamesMenu['menu'].add_command(label=column, command=lambda value=column: currentInputOption.set(value))
    outputColumnNamesMenu['menu'].delete(0, END)  # Clear the current menu
    for column in columnNamesList:  # Add new column names
        outputColumnNamesMenu['menu'].add_command(label=column, command=lambda value=column: currentOutputOption.set(value))
    if CSVAlreadyReaded:
        inputListBox.delete(0, END)
        outputListBox.delete(0, END)
        currentInputOption.set("")
        currentOutputOption.set("")
    CSVAlreadyReaded=True

def updateColumnNameList():
    global columnNamesList
    inputColumnNamesMenu['menu'].delete(0, END)  # Clear the current menu
    outputColumnNamesMenu['menu'].delete(0, END)  # Clear the current menu
    for column in columnNamesList:  # Add new column names
        inputColumnNamesMenu['menu'].add_command(label=column, command=lambda value=column: currentInputOption.set(value))
        outputColumnNamesMenu['menu'].add_command(label=column, command=lambda value=column: currentOutputOption.set(value))
def defineModelsList():
    global modelsList, selectModelMenu
    modelsList.clear()
    for folder in os.listdir('models'):# Iterate over items in the models directory
        if os.path.isdir(os.path.join('models', folder)):# Check if the item is a directory
            modelsList.append(folder)# Add the folder name to the list
    if len(modelsList)==0:
        modelsList=[""]
    if selectModelMenu!=None:
        selectModelMenu['menu'].delete(0, END)  # Clear the current menu
        for column in modelsList:  # Add new column names
            if column!="":
                selectModelMenu['menu'].add_command(label=column, command=lambda value=column: currentModelOption.set(value))
defineModelsList()

def addToInputListBox():
    global columnNamesList
    item = currentInputOption.get()
    if item=="":
        messagebox.showwarning("WARNING", "The input option is not selected. Please, firstly select the input option.")
        return
    if item in inputListBox.get(0, END):  # Verifica se o item já está no Listbox
        messagebox.showwarning("WARNING", f"The item '{item}' was already added.")
    else:
        inputListBox.insert(END, item)
        currentInputOption.set("")
        if type(columnNamesList)!=list:
            columnNamesList = columnNamesList.tolist()
        columnNamesList.remove(item)
        updateColumnNameList()

def addToOutputListBox():
    global columnNamesList
    item = currentOutputOption.get()
    if item=="":
        messagebox.showwarning("WARNING", "The output option is not selected. Please, firstly select the output option.")
        return
    if item in outputListBox.get(0, END):# Verifica se o item já está no Listbox
        messagebox.showwarning("WARNING", f"O item '{item}' já foi adicionado.")
    else:
        outputListBox.insert(END, item)
        currentOutputOption.set("")
        if type(columnNamesList)!=list:
            columnNamesList = columnNamesList.tolist()
        columnNamesList.remove(item)
        updateColumnNameList()

def removeFromInputListBox():# Function to remove selected feature
    global columnNamesList
    # Get the index of the selected item
    selectedIndex = inputListBox.curselection()
    if (len(selectedIndex)==0):
        messagebox.showwarning("WARNING", "Please, select a feature to be removed.")
        return
    selectedValue=inputListBox.get(selectedIndex[0])
    if selectedIndex:  # Check if an item is selected
        inputListBox.delete(selectedIndex)
        if type(columnNamesList)!=list:
            columnNamesList = columnNamesList.tolist()
        columnNamesList.append(selectedValue)
        updateColumnNameList()
    else:
        messagebox.showinfo("INFO", "Before remove a feature, you must select the feature clicking on it")

def removeFromOutputListBox():# Function to remove selected output
    global columnNamesList
    selectedIndex = outputListBox.curselection()# Get the index of the selected item
    if (len(selectedIndex)==0):
        messagebox.showwarning("WARNING", "Please, select a target to be removed.")
        return
    selectedValue=outputListBox.get(selectedIndex[0])
    if selectedIndex:  # Check if an item is selected
        outputListBox.delete(selectedIndex)
        if type(columnNamesList)!=list:
            columnNamesList = columnNamesList.tolist()
        columnNamesList.append(selectedValue)
        updateColumnNameList()
    else:
        messagebox.showinfo("INFO", "Before remove an output, you must select the output clicking on it")

DIR=os.path.dirname(os.path.abspath(__file__))
PURPLE_COLOR="#6a0dad"
WHITE_COLOR="white"
RED_COLOR="red"

root = tk.Tk()
img = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'icons', 'icon.png'))
root.iconphoto(False, img)
root.title("AutoML")
root.geometry("400x350")
root.configure(bg=PURPLE_COLOR)  # Cor de fundo roxo

currentInputOption=StringVar()
currentInputOption.set(columnNamesList[0])
currentModelOption=StringVar()
currentModelOption.set(modelsList[0])
currentOutputOption=StringVar()
currentOutputOption.set(columnNamesList[0])
currentPercentageOption=StringVar()
currentPercentageOption.set(percentageList[0]) 

# Block resizing
root.resizable(False, False)  # (width, height)

addOutputButton = Button(root, text="Read CSV file", command=readCSVFile, bg=PURPLE_COLOR, fg=WHITE_COLOR)
addOutputButton.place(x=158, y=115)

selectModelLabel = tk.Label(root, text="Select a model:", font=("calibri", 9), bg=PURPLE_COLOR, fg="white")
selectModelLabel.place(x=150, y=140)
selectModelMenu = OptionMenu(root, currentModelOption, *modelsList)
selectModelMenu.config(bg=PURPLE_COLOR, fg=WHITE_COLOR, highlightbackground=PURPLE_COLOR, highlightcolor=PURPLE_COLOR, width=9)
selectModelMenu.place(x=147, y=155)

readModelButton = Button(root, text="Read model", command=readModel, bg=PURPLE_COLOR, fg=WHITE_COLOR)
readModelButton.place(x=158, y=190)

trainModelButton = Button(root, text="TRAIN MODEL", command=trainModel, bg=PURPLE_COLOR, fg=RED_COLOR, font=font.Font(weight="bold", size=10))
trainModelButton.place(x=145, y=220)

fileNameLabel = tk.Label(root, text="Type the file name(csv): ", font=("calibri", 12), bg=PURPLE_COLOR, fg="white")
fileNameLabel.pack(side=tk.TOP)

inputName = tk.Entry(root, width=40)
inputName.pack(side=tk.TOP)

inputFeaturesLabel = tk.Label(root, text="Select the\ninput features: ", font=("calibri", 9), bg=PURPLE_COLOR, fg="white")
inputFeaturesLabel.place(x=10, y=60)
inputColumnNamesMenu = OptionMenu(root, currentInputOption, *columnNamesList)
inputColumnNamesMenu.config(bg=PURPLE_COLOR, fg=WHITE_COLOR, highlightbackground=PURPLE_COLOR, highlightcolor=PURPLE_COLOR, width=5)
inputColumnNamesMenu.place(x=10, y=90)

inputListLabel = tk.Label(root, text="Inputs list: ", font=("calibri", 9), bg=PURPLE_COLOR, fg="white")
inputListLabel.place(x=10, y=125)

inputListBox = Listbox(root, bg=WHITE_COLOR, fg=PURPLE_COLOR, height=3, width=12)
inputListBox.place(x=10, y=145)

addInputButton = Button(root, text="Add feature", command=addToInputListBox, bg=PURPLE_COLOR, fg=WHITE_COLOR)
addInputButton.place(x=10, y=205)

addInputButton = Button(root, text="Remove feature", command=removeFromInputListBox, bg=PURPLE_COLOR, fg=WHITE_COLOR)
addInputButton.place(x=10, y=235)

trainingPercentageLabel = tk.Label(root, text="Select the training\nset percentage: ", font=("calibri", 9), bg=PURPLE_COLOR, fg="white")
trainingPercentageLabel.pack(side=tk.TOP)
trainingPercentageMenu = OptionMenu(root, currentPercentageOption, *percentageList)
trainingPercentageMenu.config(bg=PURPLE_COLOR, fg=WHITE_COLOR, highlightbackground=PURPLE_COLOR, highlightcolor=PURPLE_COLOR, width=5)
trainingPercentageMenu.pack(side=tk.TOP)

outputLabel = tk.Label(root, text="Select the output\n target: ", font=("calibri", 9), bg=PURPLE_COLOR, fg="white")
outputLabel.place(x=295, y=60)
outputColumnNamesMenu = OptionMenu(root, currentOutputOption, *columnNamesList)
outputColumnNamesMenu.config(bg=PURPLE_COLOR, fg=WHITE_COLOR, highlightbackground=PURPLE_COLOR, highlightcolor=PURPLE_COLOR, width=5)
outputColumnNamesMenu.place(x=295, y=90)

outputListLabel = tk.Label(root, text="Outputs list: ", font=("calibri", 9), bg=PURPLE_COLOR, fg="white")
outputListLabel.place(x=295, y=125)

outputListBox = Listbox(root, bg=WHITE_COLOR, fg=PURPLE_COLOR, height=3, width=12)
outputListBox.place(x=295, y=145)

addOutputButton = Button(root, text="Add output", command=addToOutputListBox, bg=PURPLE_COLOR, fg=WHITE_COLOR)
addOutputButton.place(x=295, y=205)

addOutputButton = Button(root, text="Remove output", command=removeFromOutputListBox, bg=PURPLE_COLOR, fg=WHITE_COLOR)
addOutputButton.place(x=295, y=235)

root.mainloop()
import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import ttk
from Data import *
from HTFunctions import *

versionnum = "1.0.0"

window = tk.Tk()
window.title("Table Interpolator v" + versionnum)
window.resizable(width=True, height=True)

mainfont = ('Yu Gothic UI',16)

fram = tk.Frame(master=window)

UnitsText = tk.Label(master=fram,text='Unit system: ',font=mainfont)
unitsCombobox = ttk.Combobox(fram,font=mainfont)
unitsCombobox['values'] = ('Metric','Imperial')

TableText = tk.Label(master=fram,text='Table: ',font=mainfont)
TableCombobox = ttk.Combobox(fram,font=mainfont)

ValueComboBox = ttk.Combobox(fram,font=mainfont)
ValueEntry = tk.Entry(master=fram, width=10,font=mainfont)
Workingunits = ttk.Combobox(fram,font=mainfont)

def ButtonClick():
    Cur_Units = unitsCombobox.get()
    current_table = TableCombobox.get()
    current_Parameter = ValueComboBox.get()
    current_Value = ValueEntry.get()
    inputunits = Workingunits.get()

    if Cur_Units == '' or current_table == '' or current_Parameter == '' or current_Value == '':
        showinfo(
            title='Results',
            message='Input Missing Values'
        )
        return None

    current_Value = float(current_Value)

    if Cur_Units == 'Metric':
        if current_table == 'Saturated Water':
            current_Value = convUnits(metricsatwater,current_Parameter,inputunits,current_Value)
            up,low= findVals(metricsatwater,current_Parameter,current_Value)
            outlist = Betweentwolines(up,low,current_Parameter,current_Value)
        if current_table == 'Saturated Air':
            current_Value = convUnits(metricair,current_Parameter,inputunits,current_Value)
            up,low= findVals(metricair,current_Parameter,current_Value)
            outlist = Betweentwolines(up,low,current_Parameter,current_Value) 
        if current_table == 'Ideal Air':
            current_Value = convUnits(metricIdealAir,current_Parameter,inputunits,current_Value)
            up,low= findVals(metricIdealAir,current_Parameter,current_Value)
            outlist = Betweentwolines(up,low,current_Parameter,current_Value)
        if current_table == 'Saturated refrigerant-134a':
            current_Value = convUnits(metricsatrefig,current_Parameter,inputunits,current_Value)
            up,low= findVals(metricsatrefig,current_Parameter,current_Value)
            outlist = Betweentwolines(up,low,current_Parameter,current_Value)
    else:
        if current_table == 'Saturated Water':
            current_Value = convUnits(imperialsatwater,current_Parameter,inputunits,current_Value)
            up,low= findVals(imperialsatwater,current_Parameter,current_Value)
            outlist = Betweentwolines(up,low,current_Parameter,current_Value)
        if current_table == 'Saturated Air':
            current_Value = convUnits(imperialsatwater,current_Parameter,inputunits,current_Value)
            up,low= findVals(imperialsatwater,current_Parameter,current_Value)
            outlist = Betweentwolines(up,low,current_Parameter,current_Value)

    outstr = ''
    for items in outlist:
        outstr = outstr + ' ' + str(items[0]) + ' ' + str(items[1]) + ' ' + str(items[2]) + '\n'

    showinfo(
        title='Results',
        message=f'{outstr}'
    )


FinishedButton = tk.Button(master=fram,text='OK',font=mainfont,command=ButtonClick)

UnitsText.grid(row=0, column=0, sticky="e")
unitsCombobox.grid(row=0, column=1, sticky="w")

TableText.grid(row=1, column=0, sticky="e")
TableCombobox.grid(row=1, column=1, sticky="w")

ValueComboBox.grid(row=2, column=0, sticky="e")
ValueEntry.grid(row=2, column=1,columnspan=3, sticky="w")
Workingunits.grid(row=2, column=2, sticky="w")

FinishedButton.grid(row=3,column=1,sticky='w')

fram.grid(row=0, column=0, padx=10)

def UpdateParameters(event):
    Cur_Units = unitsCombobox.get()
    current_table = TableCombobox.get()

    parlist=[]
    if Cur_Units == 'Metric':
        if current_table == 'Saturated Water':
            for parameter in metricsatwater[0]:
                parlist.append(parameter)
        if current_table == 'Saturated Air':
            for parameter in metricair[0]:
                parlist.append(parameter)
        if current_table == 'Ideal Air':
            for parameter in metricIdealAir[0]:
                parlist.append(parameter)
        if current_table == 'Saturated refrigerant-134a':
            for parameter in metricsatrefig[0]:
                parlist.append(parameter)
    else:
        if current_table == 'Saturated Water':
            for parameter in imperialsatwater[0]:
                parlist.append(parameter)
        if current_table == 'Saturated Air':
            for parameter in imperialair[0]:
                parlist.append(parameter)

    ValueComboBox['values'] = parlist
    ValueComboBox.current(0)

    getUnits(None)


def UpdateTables(event):
    Cur_Units = unitsCombobox.get()
    #print(Cur_Units)
    if Cur_Units == 'Metric':
        TableCombobox['values'] = ['Saturated Water', 'Saturated Air','Ideal Air','Saturated refrigerant-134a']
    else:
        TableCombobox['values'] = ['Saturated Water', 'Saturated Air']

def getUnits(event):
    #print('Running')
    Cur_system = unitsCombobox.get()
    current_Parameter = ValueComboBox.get()
    #print(Cur_system,current_Parameter)

    unitsdict = {'Metric':
                    {'Temperature':['C','K'],'Enthalpy': ['kJ/kg'], 'Relative Pressure': ['No Units'], 'Internal Energy': ['kJ/kg'], 'Relative Volume': ['No Units'], 'Entropy': ['kJ/(kg*K)'],'Saturation Pressure':['bar','kPa','Pa'],'Density Liquid':['kg/m^3'],'Density Vapour':['kg/m^3'],'Enthalpy of Vapourization':['kJ/kg'],'Specific Heat Liquid':['J/(kg*K)'],'Specific Heat Vapour': ['J/(kg*K)'], 'Thermal Conductivity Liquid': [ 'W/(m*K)'], 'Thermal Conductivity Vapour': ['W/(m*K)'],'Specific Heat Vapour':['J/(kg*K)'],'Dynamic Viscosity Liquid': ['kg/(m*s)'],'Dynamic Viscosity Vapour':['kg/(m*s)'],'Prandlt Number Liquid':['No Units'],'Prandlt Number Vapour': ['No Units'],'Volume Expansion Coefficent':['1/K']},
                'Imperial':
                    {'Temperature':['F','R']}
                }
    
    try:
        unitlist = unitsdict[Cur_system][current_Parameter]
    except Exception as EGC:
        print(EGC)
        unitlist = ['No units found']

    Workingunits['values'] = unitlist
    Workingunits.current(0)

unitsCombobox.bind('<<ComboboxSelected>>', UpdateTables)
TableCombobox.bind('<<ComboboxSelected>>', UpdateParameters)
ValueComboBox.bind('<<ComboboxSelected>>', getUnits)

window.mainloop()
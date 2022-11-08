from Data import *

def interpolate(value,x1,y1,x2,y2):
    outputval = ((y1-y2)/(x1-x2))*(value-x1)+y1
    return outputval

def writetotempfile(object):
    file = open('testfile.txt','w')
    file.write(str(object))
    file.close()

def sciconv(number):
    if ',' in number:
        for index in range(len(number)-1):
            char = number[index]
            if char == ',':
                number = number[0:index] + number[index+1:]
                break

    #print(number)
    try:
        return float(number)
    except:
        numblist = number.split('*')
        try:
            numblist.remove('')
        except:
            pass

        return (float(numblist[0]))*(int(numblist[1])**int(numblist[2]))

def getdata(inputfilename,columnlist,units):
    datafile = open(inputfilename,'r')

    datalist =[]
    for line in datafile:
        #print(line)
        linelist = line.split()
        #print(linelist)
        templist =[]
        for ind in range(len(linelist)):
            item=linelist[ind]
            #print('step 1')
            #print(item)
            try:
                if item == 'Ã—':
                    #print('reject 1')
                    pass
                elif len(item) == 6 and item[2] == 'â' and item[3] == 'ˆ' and item[4] == '’':
                    #print('reject 2')
                    pass
                else:
                    #print('step 2')
                    item = item.replace('âˆ’','-')
                    item = item.replace('âˆž','999999')
                    item = item.replace('â€”','999999')
                    #print('step 3')
                    try:
                        if linelist[ind+1] == 'Ã—':
                            lastpart = linelist[ind+2].replace('âˆ’','-')
                            item = item + '*'+ lastpart[0:2] +'**' + lastpart[-2:]
                            #print(item)
                    except:
                        pass
                    #print('step 4')
                    templist.append(item)
                    #print(templist)
                if ind == len(linelist)-1:
                    #print('step 5')
                    datalist.append(templist)
            except Exception as EGC:
                print(EGC)
        
    #print(datalist)
    # cleanlist =[]
    # for line in datalist:
    #     for item in line:
    #         if len(item) == 4 and item[2] == '-':
    #             pass
    #         else:
    #             cleanlist.append(item)

    # print('clean',cleanlist)

    finallist =[]
    for line in datalist:
        linedict ={}
        #print(line)
        for index in range(len(columnlist)):
            try:
                linedict[columnlist[index]] = (int(line[index]),units[index])
            except ValueError:
                linedict[columnlist[index]] = (sciconv(line[index]),units[index])
                #print('conver')
            except IndexError:
                linedict[columnlist[index]] = (0,units[index])
            #print(linedict)
            if index == len(columnlist)-1:
                finallist.append(linedict)
    #print(finallist)
    writetotempfile(finallist)

def convUnits(data,parameter,currentunits,value):

    specifiedunits = data[0][parameter][1]
    #print(specifiedunits)

    if currentunits == specifiedunits:
        return value
    else:
        if currentunits == 'C' and specifiedunits == 'K':
            return value + 273.15
        elif currentunits == 'K' and specifiedunits == 'C':
            return value + 273.15
        elif currentunits == 'bar' and specifiedunits == 'kPa':
            return 100*value
        elif currentunits == 'Pa' and specifiedunits == 'kPa':
            return value/1000
        else:
            print('convUnits Error: dont know specified units')
            return value

def findVals(dicts,parameter,val):
    val = float(val)
    lowervalue = 0
    uppervalue = 0
    for line in dicts:
        current = line[parameter][0]
        if current < val:
            lowerline = line
        else:
            upperline = line
            break

    return upperline,lowerline

def Betweentwolines(upper,lower,setparameter,number):
    number = float(number)
    newlist =[]
    referupper = upper[setparameter][0]
    referlower = lower[setparameter][0]
    for parameter in upper:
        if parameter == setparameter:
            units = upper[parameter][1]
            newlist.append((parameter,number,units))
        else:
            uppervalue = upper[parameter][0]
            lowervalue = lower[parameter][0]
            units = upper[parameter][1]

            newval = interpolate(number,referupper,uppervalue,referlower,lowervalue)
            newlist.append((parameter,newval,units))
    return newlist


#up,low= findVals(metricIdealAir,'Tempature',215)
#print(Betweentwolines(up,low,'Tempature',215))

getdata('metsatrefrig.txt',
['Temperature','Saturation Pressure','Specific Volume Saturated Liquid','Specific Volume Saturated Vapour','Internal Energy Saturated Liquid','Internal Energy Evaporation','Internal Energy Saturated Vapour','Enthalpy Saturated Liquid','Enthalpy Evaporation','Enthalpy Saturated Vapour','Entropy Saturated Liquid','Entropy Evaporation','Entropy Saturated Vapour'],
['C','kPa','m^3/kg','m^3/kg','kJ/kg','kJ/kg','kJ/kg','kJ/kg','kJ/kg','kJ/kg','kJ/(kg*K)','kJ/(kg*K)','kJ/(kg*K)'])

#print(3*10**4)
        # templist=[]
        # start=0
        # for index in range(len(line)-1):
        #     character = line[index]
        #     if character == ' ' and line[index+1] != '×':
        #         end = index
        #         if len(templist) == 0:
        #             templist.append(line[start:end])
#print(interpolate(251,250,1.43,260,1.37))

#Removed A from impsat water
#cahnged 57-53 psi to 55 on impsatwater 290F

#Potential Column Names
#['Tempature','Enthalpy','Relative Pressure','Internal Energy','Relative Volume','Entropy'],['K','kJ/kg','None','kJ/kg','None','kJ/(kg*K)']
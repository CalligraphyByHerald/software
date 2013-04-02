from math import *
import os
def gcodeDict(fontsize, file):
    #creates a dictionary of the font information.
    fin = open(file)
    d = dict()
    for line in fin:
        Char = []
        lineTup = line.partition("; ")
        #create key and find width
        sigTup = lineTup[0].partition("_")
        cleanTup = sigTup[2].partition(" ")
        key = cleanTup[0]
        width = cleanTup[2]
        Char.append(float(width)/21.14*4.2175*(fontsize/12.0))
        #process points     
        data = lineTup[2]
        strokeList = data.split("; ")

        for item in strokeList:
            pointList = []
            coords = item.split(" ")
            for point in coords:
                XY = point.split(",")
                if len(XY) == 2:
                    pointList.append(XY)
            for point in pointList:
                temp  = point[1].partition('\r\n')
                point[0] = float(point[0])
                point[1] = float(temp[0])
                for i in range(2):
                    point[i] = point[i]/21.14*4.2175*(fontsize/12.0)        #mm
            Char.append(pointList)
    #create Dict
        d[key] = Char #Char is a list.  The first element is the width.  All the other elements are lists of lists containing the points.
    '''   
    for key in d:
        print key, d[key]
    '''  
    return d

def getData(letter, dictionary):
    ''' gathers the x and y data for a given letter from the dictionary'''
    decval = ord(letter)
    hexval = hex(decval)
    hexstring = str(hexval).partition('x')[2]
    hexstring = hexstring.upper()
    data = dictionary[hexstring]
    return data
def pressure(dx, dy):
    '''calculates the variable pressure component of Z based on dx and dy'''
    if dx == 0 and dy == 0:
        return 0
    overAngle = -40*(pi/180)
    a = (1/sqrt(tan(overAngle)**2+1)) * tan(overAngle); #x component
    b = (1/sqrt(tan(overAngle)**2+1)) # y component

    dxNorm=dx*(1/sqrt(dx**2+dy**2))
    dyNorm=dy*(1/sqrt(dx**2+dy**2))
    return abs(dxNorm*a + dyNorm*b) #dot product of "over" angle vector and input stroke vector

def findLwidth(line, dict, cspace, wspace, Pwidth):
    '''calculates the width of a line of text, checking to make sure it does not exceed the maximum'''
    LWidth = 0
    for word in line:
        for letter in word:
            data = getData(letter, dict)
            width = data[0]
            LWidth += (width + cspace)
        LWidth += (wspace)
    if LWidth > Pwidth:
        return -1
    else:
        return LWidth




def writer(font, fontsize, text, hMarg, vMarg, Hcentered, Vcentered, first, pageW, pageH, tool, headerspace=0, GCODElines=0):
    '''GCODE creating engine.  takes parameters in from GUI, adds GCODE to file.'''

    #set up parameters, font dictionary
    if first != 1 and Vcentered == 1:
        return "We do not currently support multiple font sizes with Vertical centering."
    dict = gcodeDict(fontsize, font)
    gcodeList = []
    width = pageW - 2*hMarg
    length = pageH - 2*vMarg
    
    #finds line height
    dataM = dict['4D']
    M = dataM[1:]
    max = 0
    for stroke in M:
        for point in stroke:
            if point[1] > max:
                max = point[1]
    height = max
    
    #more parameters
    if font == 'CamBam.txt':
        cspace = -height/2.5
    else:
        cspace = 0
    wspace = fontsize/4.0
    lspace = fontsize/4.0

    #process text, deal with more parameters
    textList = text.split('*')
    for i in range(len(textList)):
        textList[i] = textList[i].split(' ')
    nLines = len(textList)
    tLength = nLines*height+(nLines-1)*lspace

    if Vcentered:
        currPos = [hMarg,(length+2*vMarg+tLength)/2-height]
    else:
        currPos = [hMarg,length + vMarg-height-headerspace]
    lineN = 0
    for line in textList:
        lineN += 1;
        flag = 0
        lwidth = findLwidth(line, dict, cspace, wspace, width)
        if lwidth == -1:
            return "Line " + str(textList.index(line)+1) + " is too long!"
        if Hcentered:
            currPos[0] = (width - lwidth)/2 + hMarg
        else:
            currPos[0] = hMarg
        currPos[1] -= (height + lspace)
        if currPos[1] - height < vMarg:
            return "You cannot have more than " + str(lineN) + " lines."
        #Create GCODE for each word, updating positions   
        for word in line:
            for letter in word:
                data = getData(letter, dict)
                strokes = data[1:]
                for stroke in strokes:
                    for point in stroke:
                        X = currPos[0] + point[0]
                        Y = currPos[1] + point[1]
                        if flag == 0:
                            gcodeList.append('G00 X' + "{0:.3f}".format(X) + " Y" + "{0:.3f}".format(Y))
                            gcodeList.append('G01 Z0.0')
                            flag = 1
                        elif stroke.index(point) == 0:
                            gcodeList.append('X' + "{0:.3f}".format(X) + " Y" + "{0:.3f}".format(Y))
                            gcodeList.append('Z0.0')
                        else:
                            dx = X - oldX
                            dy = Y - oldY

                            #z axis
                            PCoef = pressure(dx, dy)
                            if tool == 'marker':
                                Z = -(1+.5*PCoef + 4.7/203*X + .15/203*Y) 
                            else:
                                Z = -(.52+.5*PCoef + 9.0/203*X + .13/203*Y)
                            gcodeList.append('Z' + "{0:.3f}".format(Z))
                            gcodeList.append('X' + "{0:.3f}".format(X) + " Y" + "{0:.3f}".format(Y))
                        
                        oldX = X
                        oldY = Y
                    gcodeList.append('Z10.0')
                charWidth = data[0]
                currPos[0] += (charWidth + cspace)
            currPos[0] += wspace
    
    #write to file, with different specifications depending on whether this GCODE is for a title or not.    
    if first:
        try:
            os.remove('grbl.gcode')
        except OSError:
            pass
        fin = open('grbl.gcode', 'w')
        header = '#region\n($Millimeters) \n#endregion\nZ10\n\n'
        fin.write(header)
    else:
        fin = open('grbl.gcode', 'a')  
        pass
    N = GCODElines
    for line in gcodeList:
        N+=1
        fin.write('N'+str(N)+'0 ' + line + '\n')
    fin.write('N'+str(N+1)+'0 ' + 'G01 Z40\n'+'N'+str(N+2)+'0 '+'G01 X0 Y0\n') #go home.
        
    return [tLength, N]

#test
if __name__=="__main__":
    text = 'Allegra'
    print writer('CamBam5.txt', 50, text, 25, 25, 0, 1, 1, 203, 280, 'pen')

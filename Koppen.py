#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 20:08:49 2020

@author: stephen
"""
from netCDF4 import Dataset
import numpy as np
import csv
from PIL import Image, ImageOps
RunName = '6Hrs'
RunYear = '1950'

Jan = Dataset('JAN'+RunYear+'.aij'+RunName+'.nc')
Feb = Dataset('FEB'+RunYear+'.aij'+RunName+'.nc')
Mar = Dataset('MAR'+RunYear+'.aij'+RunName+'.nc')
Apr = Dataset('APR'+RunYear+'.aij'+RunName+'.nc')
May = Dataset('MAY'+RunYear+'.aij'+RunName+'.nc')
Jun = Dataset('JUN'+RunYear+'.aij'+RunName+'.nc')
Jul = Dataset('JUL'+RunYear+'.aij'+RunName+'.nc')
Aug = Dataset('AUG'+RunYear+'.aij'+RunName+'.nc')
Sep = Dataset('SEP'+RunYear+'.aij'+RunName+'.nc')
Oct = Dataset('OCT'+RunYear+'.aij'+RunName+'.nc')
Nov = Dataset('NOV'+RunYear+'.aij'+RunName+'.nc')
Dec = Dataset('DEC'+RunYear+'.aij'+RunName+'.nc')

Months = [Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec]

Koppen = np.arange(Jan.variables['tsurf'].shape[0] * Jan.variables['tsurf'].shape[1]).reshape(Jan.variables['tsurf'].shape[0],Jan.variables['tsurf'].shape[1])
Koppen = Koppen.astype('U256')


Image=Image.new('RGBX',(Jan.variables['tsurf'].shape[1],Jan.variables['tsurf'].shape[0]), color=(125,125,125))


for i in range(Jan.variables['tsurf'].shape[0]):
    for j in range(Jan.variables['tsurf'].shape[1]):
            TMax=-100
            TMin=100
            TTen=0
            TAve=0
            PMax=0
            PMin=0
            PTotal=0
            PSMax=0
            PSMin=0
            PWMax=0
            PWMin=0
            if i < Jan.variables['tsurf'].shape[0]/2:
                #Northern Summer June, July, and August
                Summer=[Jun.variables['prec'][i,j],Jul.variables['prec'][i,j],Aug.variables['prec'][i,j]]
                PSMin=min(Summer)
                PSMax=max(Summer)
                #Northern Winter Dec, Jan, Feb
                Winter=[Dec.variables['prec'][i,j],Jan.variables['prec'][i,j],Feb.variables['prec'][i,j]]
                PSMin=min(Winter)
                PSMax=max(Winter)
            if i > Jan.variables['tsurf'].shape[0]/2:
                #Southern Summer Dec, Jan, Feb
                Summer=[Dec.variables['prec'][i,j],Jan.variables['prec'][i,j],Feb.variables['prec'][i,j]]
                PSMin=min(Summer)
                PSMax=max(Summer)
                #Southern Winter June, July, and August
                Winter=[Jun.variables['prec'][i,j],Jul.variables['prec'][i,j],Aug.variables['prec'][i,j]]
                PWMin=min(Winter)    
                PWMax=max(Winter)
            for k in range(len(Months)):
                if TMax < Months[k].variables['tsurf'][i,j]:
                    TMax = Months[k].variables['tsurf'][i,j]
                if TMin > Months[k].variables['tsurf'][i,j]:
                    TMin = Months[k].variables['tsurf'][i,j]
                if Months[k].variables['tsurf'][i,j] >10:
                    TTen=TTen+1
                if PMax < Months[k].variables['prec'][i,j]:
                    PMax = Months[k].variables['prec'][i,j]
                if PMin > Months[k].variables['prec'][i,j]:
                    PMin = Months[k].variables['prec'][i,j]
                PTotal=PTotal+Months[k].variables['prec'][i,j]
                TAve= Months[k].variables['tsurf'][i,j] +TAve
            TAve=TAve/12
                
#Group A (Tropical Climates)
            if TMax >= 18:
                if PMax >= 2:
                    Koppen[i,j]='Af'
                    Image.putpixel((j,i),(11,36,250,int(Jan.variables['ocnfr'][i,j]*2.55)))
                if PMin <2 and (PMin *30) > (100-PTotal):
                    Koppen[i,j]='Am'
                    Image.putpixel((j,i),(21,123,251,int(Jan.variables['ocnfr'][i,j]*2.55)))
                if PMin < 2 and (PMin *30) < (100-PTotal):
                    Koppen[i,j]='Aw'
                    Image.putpixel((j,i),(76,171,247,int(Jan.variables['ocnfr'][i,j]*2.55)))

#Group B (Dry Climates)
            # Weird seasonal things that I don't want to deal with right now

#This type of climate is defined by little precipitation.
#
#Multiply the average annual temperature in Celsius by 20, then add
            Dry = 20*TAve
#
#(a) 280 if 70% or more of the total precipitation is in the spring and summer 
#months (April–September in the Northern Hemisphere, or October–March in the 
#        Southern), or
            
#(b) 140 if 30%–70% of the total precipitation is received during the spring and 
#summer, or
            if i < Jan.variables['tsurf'].shape[0]/2:
                if Apr.variables['prec'][i,j]+May.variables['prec'][i,j]+Jun.variables['prec'][i,j]+Jul.variables['prec'][i,j]+Aug.variables['prec'][i,j]+Sep.variables['prec'][i,j] > (.3 * PTotal):
                    Dry=Dry+140
            if i > Jan.variables['tsurf'].shape[0]/2:
                if Oct.variables['prec'][i,j]+Nov.variables['prec'][i,j]+Dec.variables['prec'][i,j]+Jan.variables['prec'][i,j]+Feb.variables['prec'][i,j]+Mar.variables['prec'][i,j]> (.3 * PTotal):
                    Dry=Dry+140
            
            if i < Jan.variables['tsurf'].shape[0]/2:
                if Apr.variables['prec'][i,j]+May.variables['prec'][i,j]+Jun.variables['prec'][i,j]+Jul.variables['prec'][i,j]+Aug.variables['prec'][i,j]+Sep.variables['prec'][i,j] > (.7 * PTotal):
                    Dry=Dry+280
            if i > Jan.variables['tsurf'].shape[0]/2:
                if Oct.variables['prec'][i,j]+Nov.variables['prec'][i,j]+Dec.variables['prec'][i,j]+Jan.variables['prec'][i,j]+Feb.variables['prec'][i,j]+Mar.variables['prec'][i,j]> (.7 * PTotal):
                    Dry=Dry+280

#(c) 0 if less than 30% of the total precipitation is received during the spring 
#and summer.
            if PTotal < (.5 * Dry) and TAve>=18:
                Koppen[i,j]='BWh'
                Image.putpixel((j,i),(251,13,27,int(Jan.variables['ocnfr'][i,j]*2.55)))
            if PTotal > (.5 *Dry) and (PTotal<Dry) and TAve<=18:
                Koppen[i,j]='BSh'
                Image.putpixel((j,i),(243,162,39,int(Jan.variables['ocnfr'][i,j]*2.55)))
            if PTotal < (.5 * Dry) and TAve<18:
                Koppen[i,j]='BWk'
                Image.putpixel((j,i),(252,151,151,int(Jan.variables['ocnfr'][i,j]*2.55)))
            if PTotal > (.5 *Dry) and (PTotal<Dry) and TAve<18:
                Koppen[i,j]='BSk'
                Image.putpixel((j,i),(243,162,39,int(Jan.variables['ocnfr'][i,j]*2.55)))
                
#If the annual precipitation is less than 50% of this threshold, the classification 
#is BW (arid: desert climate); if it is in the range of 50%–100% of the threshold, 
#the classification is BS (semi-arid: steppe climate).[1][10]
#
#A third letter can be included to indicate temperature. Originally, h signified 
#low-latitude climate (average annual temperature above 18 °C (64.4 °F)) while k 
#signified middle-latitude climate (average annual temperature below 18 °C), but 
#the more common practice today, especially in the United States, is to use h to 
#mean the coldest month has an average temperature above 0 °C (32 °F) (or −3 °C (27 °F)),
# with k denoting that at least one month's averages below 0 °C (or −3 °C (27 °F)). 
# The n is used to denote a climate characterized by frequent fog.[13][14][15]
#
#BWh = Hot desert climate
#BWk = Cold desert climate
#BSh = Hot semi-arid climate
#BSk = Cold semi-arid climate

#Group C (Temerate climates)
            if (TMin >0 and TMin <18) and TMax > 10:
#Cfa = Humid subtropical climate; coldest month averaging above 0 °C (32 °F) 
#(or −3 °C (27 °F)), at least one month's average temperature above 22 °C (71.6 
#°F), and at least four months averaging above 10 °C (50 °F). No significant 
#precipitation difference between seasons (neither abovementioned set of conditions 
#fulfilled). No dry months in the summer.
                if TMin>0 and TMax>10 and TTen>=4 and PMin>0:
                    Koppen[i,j]='Cfa'
                    Image.putpixel((j,i),(199,253,92,int(Jan.variables['ocnfr'][i,j]*2.55)))
                    
#Cfb = Temperate oceanic climate; coldest month averaging above 0 °C (32 °F) 
#(or −3 °C (27 °F)), all months with average temperatures below 22 °C (71.6 °F), 
#and at least four months averaging above 10 °C (50 °F). No significant precipitation 
#difference between seasons (neither abovementioned set of conditions fulfilled).
                if TMin>0 and TMax<22 and TTen>=4:
                    Koppen[i,j]='Cfb'
                    Image.putpixel((j,i),(109,253,70,int(Jan.variables['ocnfr'][i,j]*2.55)))
                    
#Cfc = Subpolar oceanic climate; coldest month averaging above 0 °C (32 °F) 
#(or −3 °C (27 °F)) and 1–3 months averaging above 10 °C (50 °F). No significant 
#precipitation difference between seasons (neither abovementioned set of conditions 
#fulfilled).                    
                if TMin>0 and TTen>0 and TTen<4 and TTen>0:
                    Koppen[i,j]='Cfc'
                    Image.putpixel((j,i),(60,197,35,int(Jan.variables['ocnfr'][i,j]*2.55)))
                    
#Cwa = Monsoon-influenced humid subtropical climate; coldest month averaging 
#above 0 °C (32 °F) (or −3 °C (27 °F)), at least one month's average temperature 
#above 22 °C (71.6 °F), and at least four months averaging above 10 °C (50 °F). 
#At least ten times as much rain in the wettest month of summer as in the driest 
#month of winter (alternative definition is 70% or more of average annual precipitation 
#is received in the warmest six months).                    
                if TMin>0 and TMax >22 and TTen>=4 and PMax>(10*PMin):
                    Koppen[i,j]='Cwa'
                    Image.putpixel((j,i),(153,253,154,int(Jan.variables['ocnfr'][i,j]*2.55)))
                    
 #Cwb = Subtropical highland climate or Monsoon-influenced temperate oceanic 
#climate; coldest month averaging above 0 °C (32 °F) (or −3 °C (27 °F)), all 
#months with average temperatures below 22 °C (71.6 °F), and at least four months 
#averaging above 10 °C (50 °F). At least ten times as much rain in the wettest 
#month of summer as in the driest month of winter (an alternative definition is 
#70% or more of average annual precipitation received in the warmest six months).                   
                if TMin>0 and TMax <22 and TTen >=4 and PMax>(PMin*10):
                    Koppen[i,j]='Cwb'
                    Image.putpixel((j,i),(103,197,104,int(Jan.variables['ocnfr'][i,j]*2.55)))

#Cwc = Cold subtropical highland climate or Monsoon-influenced subpolar oceanic 
#climate; coldest month averaging above 0 °C (32 °F) (or −3 °C (27 °F)) and 1–3 
#months averaging above 10 °C (50 °F). At least ten times as much rain in the 
#wettest month of summer as in the driest month of winter (alternative definition is 
#70% or more of average annual precipitation is received in the warmest six months).
                if TMin>0 and TTen>0 and TTen<4 and PMax>(PMin*10):
                    Koppen[i,j]='Cwc'
                    Image.putpixel((j,i),(55,149,57,int(Jan.variables['ocnfr'][i,j]*2.55)))

#Csa = Hot-summer Mediterranean climate; coldest month averaging above 0 °C (32 °F) 
#(or −3 °C (27 °F)), at least one month's average temperature above 22 °C (71.6 °F), 
#and at least four months averaging above 10 °C (50 °F). At least three times as much 
#precipitation in the wettest month of winter as in the driest month of summer, and 
#driest month of summer receives less than 30 mm (1.2 in).
                if TMin>0 and TMax>22 and TTen>=4 and PMax>(PMin*3) and PMax<1:
                    Koppen[i,j]='Csa'
                    Image.putpixel((j,i),(255,253,56,int(Jan.variables['ocnfr'][i,j]*2.55)))
                    
#Csb = Warm-summer Mediterranean climate; coldest month averaging above 0 °C (32 °F) 
#(or −3 °C (27 °F)), all months with average temperatures below 22 °C (71.6 °F), and 
#at least four months averaging above 10 °C (50 °F). At least three times as much 
#precipitation in the wettest month of winter as in the driest month of summer, and 
#driest month of summer receives less than 30 mm (1.2 in).
                if TMin>0 and TMax<22 and TTen>=4 and PMax>(PMin*3)and PMax<1:
                    Koppen[i,j]='Csb'
                    Image.putpixel((j,i),(198,197,41,int(Jan.variables['ocnfr'][i,j]*2.55)))


#Csc = Cold-summer Mediterranean climate; coldest month averaging above 0 °C (32 °F) 
#(or −3 °C (27 °F)) and 1–3 months averaging above 10 °C (50 °F). At least three times 
#as much precipitation in the wettest month of winter as in the driest month of summer, 
#and driest month of summer receives less than 30 mm (1.2 in).
                if TMin>0 and TTen>0 and TTen<4 and PMax>(PMin*3) and PMax<1:
                    Koppen[i,j]='Csc'
                    Image.putpixel((j,i),(150,149,28,int(Jan.variables['ocnfr'][i,j]*2.55)))
                    



            
#Group D (Continetal Climates)
            if TMin<0 and TMax>10:

                #Dfa = Hot-summer humid continental climate; coldest month averaging below 
#−0 °C (32 °F) (or −3 °C (27 °F)), at least one month's average temperature 
#above 22 °C (71.6 °F), and at least four months averaging above 10 °C (50 °F). 
#No significant precipitation difference between seasons (neither 
#abovementioned set of conditions fulfilled).
                if TMin<0 and TMax>22 and TTen >= 4:
                    Koppen[i,j]='Dfa'
                    Image.putpixel((j,i),(252,40,251,int(Jan.variables['ocnfr'][i,j]*2.55)))

#Dfb = Warm-summer humid continental climate; coldest month averaging 
#below −0 °C (32 °F) (or −3 °C (27 °F)), all months with average temperatures 
#below 22 °C (71.6 °F), and at least four months averaging above 10 °C (50 °F). 
#No significant precipitation difference between seasons (neither abovementioned 
#set of conditions fulfilled).
                if TMin<0 and TMax<22 and TTen >= 4:
                    Koppen[i,j]='Dfb'
                    Image.putpixel((j,i),(196,29,197,int(Jan.variables['ocnfr'][i,j]*2.55)))

#Dfc = Subarctic climate; coldest month averaging below 0 °C (32 °F) (or −3 
#°C (27 °F)) and 1–3 months averaging above 10 °C (50 °F). No significant 
#precipitation difference between seasons (neither abovementioned set of conditions fulfilled).
                if TMin<0 and TTen>0 and TTen<4:
                    Koppen[i,j]='Dfc'
                    Image.putpixel((j,i),(149,55,147,int(Jan.variables['ocnfr'][i,j]*2.55)))

#Dfd = Extremely cold subarctic climate; coldest month averaging below −38 °C 
#(−36.4 °F) and 1–3 months averaging above 10 °C (50 °F). No significant 
#precipitation difference between seasons (neither abovementioned set of conditions fulfilled).
                if TMin<-38 and TTen>0 and TTen<4:
                    Koppen[i,j]='Dfd'
                    Image.putpixel((j,i),(149,101,148,int(Jan.variables['ocnfr'][i,j]*2.55)))

#Dwa = Monsoon-influenced hot-summer humid continental climate; coldest month 
#averaging below 0 °C (32 °F) (or −3 °C (27 °F)), at least one month's average 
#temperature above 22 °C (71.6 °F), and at least four months averaging above 
#10 °C (50 °F). At least ten times as much rain in the wettest month of summer 
#as in the driest month of winter (alternative definition is 70% or more of 
#average annual precipitation is received in the warmest six months).
                if TMin<0 and TMax>22 and TTen>=4 and (PMax>PMin*10):
                    Koppen[i,j]='Dwa'
                    Image.putpixel((j,i),(172,179,253,int(Jan.variables['ocnfr'][i,j]*2.55)))
                    
#Dwb = Monsoon-influenced warm-summer humid continental climate; coldest month 
#averaging below 0 °C (32 °F) (or −3 °C (27 °F)), all months with average 
#temperatures below 22 °C (71.6 °F), and at least four months averaging above 
#10 °C (50 °F). At least ten times as much rain in the wettest month of summer 
#as in the driest month of winter (alternative definition is 70% or more of 
#average annual precipitation is received in the warmest six months).                    
                if TMin<0 and TMax<22 and TTen >=4 and (PMax>PMin*10):
                    Koppen[i,j]='Dwb'
                    Image.putpixel((j,i),(92,122,216,int(Jan.variables['ocnfr'][i,j]*2.55)))
                    
#Dwc = Monsoon-influenced subarctic climate; coldest month averaging below 0 
#°C (32 °F) (or −3 °C (27 °F)) and 1–3 months averaging above 10 °C (50 °F). 
#At least ten times as much rain in the wettest month of summer as in the driest 
#month of winter (alternative definition is 70% or more of average annual 
#precipitation is received in the warmest six months).
                if TMin<0 and TTen>0 and TTen<4 and 10*PSMax>PWMin:
                    Koppen[i,j]='Dwc'
                    Image.putpixel((j,i),(77,84,178,int(Jan.variables['ocnfr'][i,j]*2.55)))
                    
#Dwd = Monsoon-influenced extremely cold subarctic climate; coldest month 
#averaging below −38 °C (−36.4 °F) and 1–3 months averaging above 10 °C (50 °F). 
#At least ten times as much rain in the wettest month of summer as in the driest 
#month of winter (alternative definition is 70% or more of average annual precipitation 
#is received in the warmest six months).
                if TMin<-38 and TTen>0 and TTen<4 and PSMax*10>PWMin:
                    Koppen[i,j]='Dwd'
                    Image.putpixel((j,i),(50,14,133,int(Jan.variables['ocnfr'][i,j]*2.55)))
                    
                    
#Dsa = Mediterranean-influenced hot-summer humid continental climate; coldest 
#month averaging below 0 °C (32 °F) (or −3 °C (27 °F)), average temperature of 
#the warmest month above 22 °C (71.6 °F) and at least four months averaging 
#above 10 °C (50 °F). At least three times as much precipitation in the wettest 
#month of winter as in the driest month of summer, and driest month of summer 
#receives less than 30 mm (1.2 in).
                if TMin<0 and TMax>22 and TTen >=4 and PWMax*3 > PSMin:
                    Koppen[i,j]='Dsa'
                    Image.putpixel((j,i),(45,255,254,int(Jan.variables['ocnfr'][i,j]*2.55)))
                    
                    
#Dsb = Mediterranean-influenced warm-summer humid continental climate; coldest 
#month averaging below 0 °C (32 °F) (or −3 °C (27 °F)), average temperature of the 
#warmest month below 22 °C (71.6 °F) and at least four months averaging above 10 
#°C (50 °F). At least three times as much precipitation in the wettest month of 
#winter as in the driest month of summer, and driest month of summer 
#receives less than 30 mm (1.2 in).
                if TMin<0 and TMax<22 and TTen>=4 and PWMax*3 > PSMin and PSMin <1:
                    Koppen[i,j]='Dsb'
                    Image.putpixel((j,i),(66,200,252,int(Jan.variables['ocnfr'][i,j]*2.55)))
                    
                    
#Dsc = Mediterranean-influenced subarctic climate; coldest month averaging 
#below 0 °C (32 °F) (or −3 °C (27 °F)) and 1–3 months averaging above 10 °C (50 °F). 
#At least three times as much precipitation in the wettest month of winter as in the 
#driest month of summer, and driest month of summer receives less than 30 mm (1.2 in).
                if TMin<0 and TTen >0 and TTen<4 and PWMax*3 > PSMin and PSMin <1:
                    Koppen[i,j]='Dsc'
                    Image.putpixel((j,i),(16,126,124,int(Jan.variables['ocnfr'][i,j]*2.55)))               
                    
#Dsd = Mediterranean-influenced extremely cold subarctic climate; coldest month 
#averaging below −38 °C (−36.4 °F) and 1–3 months averaging above 10 °C (50 °F). At 
#least three times as much precipitation in the wettest month of winter as in the driest 
#month of summer, and driest month of summer receives less than 30 mm (1.2 in).
                if TMin<-38 and TTen >0 and TTen<4 and PWMax*3 > PSMin and PSMin <1:
                    Koppen[i,j]='Dsd'  
                    Image.putpixel((j,i),(6,69,93,int(Jan.variables['ocnfr'][i,j]*2.55)))
#Group E (Polar and Alpine Climates)

#ET = Tundra climate; average temperature of warmest month between 0 °C (32 °F) and 10 °C (50 °F).[1][10]
#EF = Ice cap climate; eternal winter, with all 12 months of the year with average temperatures below 0 °C (32 °F).[1][10]            

            if TMax <= 0:   
                Koppen[i,j]='EF'
                Image.putpixel((j,i),(104,104,104,int(Jan.variables['ocnfr'][i,j]*2.55)))
            if TMax <= 10 and TMax >= 0:
                Koppen[i,j]='ET'
                Image.putpixel((j,i),(178,178,178,int(Jan.variables['ocnfr'][i,j]*2.55)))
                
            #print (i,j,TMax,TMin,TAve,TTen,PMax,PMin,PTotal,Koppen[i,j])
            with open('KoppenD'+RunName+RunYear+'.csv',mode='a') as KoppenD:
              KoppenAdd=csv.writer(KoppenD,delimiter=',')
              KoppenAdd.writerow([i,j,TMax,TMin,TAve,TTen,PMax,PMin,PTotal,Koppen[i,j]])
Image=ImageOps.flip(Image)
Image.save('Koppen'+RunYear+RunName+'.tiff')
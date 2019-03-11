#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 09:40:26 2019

@author: farthcl1
"""

import numpy as np
import pandas as pd

from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Range1d, TextInput, Paragraph, Select
from bokeh.plotting import Figure, curdoc,show

def lonrot(phi):
    
    rotmat=np.array([[np.cos(phi),-np.sin(phi),0],[np.sin(phi),np.cos(phi),0],[0,0,1]])

    return rotmat;

def tiltrot(tilt):
    
    rotmat=np.array([[1,0,0],[0,np.cos(tilt),-np.sin(tilt)],[0,np.sin(tilt),np.cos(tilt)]])

    return rotmat;

def rollrot(roll):
    
    rotmat=np.array([[np.cos(tilt),0,np.sin(tilt)],[0,1,0],[-np.sin(tilt),0,np.cos(tilt)]])

    return rotmat;

series360=np.pi/180*np.array([x*1 for x in range(0, 361)])
zbias=pd.DataFrame(dict(x=0*series360,y=0*series360,z=0*series360+1))

londf=pd.DataFrame(dict(x=np.sin(series360),y=0*series360,z=np.cos(series360)))
lonprim=ColumnDataSource(londf)

freqin=TextInput(title='Frequency (MHz)', value='3000')
lattice=Select(title="Lattice:", value="Triangular", options=["Rectangular", "Triangular"])
dxin=TextInput(title='dx (cm)', value='5.74')
dyin=TextInput(title='dy (cm)', value='7.13')
tiltin=TextInput(title='Tilt (degrees)', value='22.5')
scanazin=TextInput(title='Azimuth Scan (degrees)', value='-60 60')
scanelin=TextInput(title='Elevation Scan (degrees)', value='0 45')

kgxout=Paragraph(width=200, height=15)
kgyout=Paragraph(width=200, height=15)
wlout=Paragraph(width=200, height=15)

p=Figure(match_aspect=True)

tilt=float(tiltin.value)*np.pi/180
wl=2.997e4/float(freqin.value)
wlout.text='Wavelength = '+str(wl)+' cm'
kgy=wl/float(dyin.value)
if lattice.value=='Triangular':
    kgx=2*wl/float(dxin.value)
    kmult=0.5
else:
    kgx=wl/float(dxin.value)
    kmult=1
kgxout.text='kgx = '+str(kgx)
kgyout.text='kgy = '+str(kgy)

newscanazstr = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in scanazin.value)
newscanelstr = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in scanelin.value)
scanaz = [float(i) for i in newscanazstr.split()]
scanel = [float(i) for i in newscanelstr.split()]

phi1=np.pi/6
lon1=np.dot(np.dot(londf,lonrot(phi1)),tiltrot(tilt))
lon1[lon1[:,1]<=0]=np.nan
lonprim1=ColumnDataSource(pd.DataFrame(dict(x=lon1[:,0],y=lon1[:,1],z=lon1[:,2])))

phi2=np.pi/3
lon2=np.dot(np.dot(londf,lonrot(phi2)),tiltrot(tilt))
lon2[lon2[:,1]<=0]=np.nan
lonprim2=ColumnDataSource(pd.DataFrame(dict(x=lon2[:,0],y=lon2[:,1],z=lon2[:,2])))

phi3=np.pi/2
lon3=np.dot(np.dot(londf,lonrot(phi3)),tiltrot(tilt))
lon3[lon3[:,1]<=0]=np.nan
lonprim3=ColumnDataSource(pd.DataFrame(dict(x=lon3[:,0],y=lon3[:,1],z=lon3[:,2])))

phi4=2*np.pi/3
lon4=np.dot(np.dot(londf,lonrot(phi4)),tiltrot(tilt))
lon4[lon4[:,1]<=0]=np.nan
lonprim4=ColumnDataSource(pd.DataFrame(dict(x=lon4[:,0],y=lon4[:,1],z=lon4[:,2])))

phi5=5*np.pi/6
lon5=np.dot(np.dot(londf,lonrot(phi5)),tiltrot(tilt))
lon5[lon5[:,1]<=0]=np.nan
lonprim5=ColumnDataSource(pd.DataFrame(dict(x=lon5[:,0],y=lon5[:,1],z=lon5[:,2])))


latdf=pd.DataFrame(dict(x=np.sin(series360),y=np.cos(series360),z=0*series360))

theta1=np.pi/6
lat1=np.dot(latdf.values*np.sin(theta1)+zbias.values*np.cos(theta1),tiltrot(tilt))
lat1[lat1[:,1]<=0]=np.nan
latprim1=ColumnDataSource(pd.DataFrame(dict(x=lat1[:,0],y=lat1[:,1],z=lat1[:,2])))

theta2=np.pi/3
lat2=np.dot(latdf.values*np.sin(theta2)+zbias.values*np.cos(theta2),tiltrot(tilt))
lat2[lat2[:,1]<=0]=np.nan
latprim2=ColumnDataSource(pd.DataFrame(dict(x=lat2[:,0],y=lat2[:,1],z=lat2[:,2])))

theta3=np.pi/2
lat3=np.dot(latdf.values*np.sin(theta3)+zbias.values*np.cos(theta3),tiltrot(tilt))
lat3[lat3[:,1]<=0]=np.nan
latprim3=ColumnDataSource(pd.DataFrame(dict(x=lat3[:,0],y=lat3[:,1],z=lat3[:,2])))

theta4=2*np.pi/3
lat4=np.dot(latdf.values*np.sin(theta4)+zbias.values*np.cos(theta4),tiltrot(tilt))
lat4[lat4[:,1]<=0]=np.nan
latprim4=ColumnDataSource(pd.DataFrame(dict(x=lat4[:,0],y=lat4[:,1],z=lat4[:,2])))

theta5=5*np.pi/6
lat5=np.dot(latdf.values*np.sin(theta5)+zbias.values*np.cos(theta5),tiltrot(tilt))
lat5[lat5[:,1]<=0]=np.nan
latprim5=ColumnDataSource(pd.DataFrame(dict(x=lat5[:,0],y=lat5[:,1],z=lat5[:,2])))
    
p.line(x='x',y='z',source=lonprim)
p.line(x='x',y='z',source=lonprim1,line_dash='dotted')
p.line(x='x',y='z',source=lonprim2,line_dash='dotted')
p.line(x='x',y='z',source=lonprim3,line_dash='dotted')
p.line(x='x',y='z',source=lonprim4,line_dash='dotted')
p.line(x='x',y='z',source=lonprim5,line_dash='dotted')

p.line(x='x',y='z',source=latprim1,line_dash='dotted')
p.line(x='x',y='z',source=latprim2,line_dash='dotted')
p.line(x='x',y='z',source=latprim3,line_dash='solid')
p.line(x='x',y='z',source=latprim4,line_dash='dotted')
p.line(x='x',y='z',source=latprim5,line_dash='dotted')

left=np.linspace(start=scanel[0],stop=scanel[1],num=101)
top=np.linspace(start=scanaz[0],stop=scanaz[1],num=101)
scanpts=np.append(np.stack((left*0+scanaz[0],left),axis=-1),
                  np.stack((top,top*0+scanel[1]),axis=-1),axis=0)
scanpts=np.append(scanpts,np.stack((left*0+scanaz[1],np.flipud(left)),axis=-1),axis=0)
scanpts=np.append(scanpts,np.stack((np.flipud(top),top*0+scanel[0]),axis=-1),axis=0)*np.pi/180

scanu=np.sin(scanpts[:,0])*np.cos(scanpts[:,1])
scanv=np.sin(scanpts[:,1])*np.cos(tilt)-np.cos(scanpts[:,0])*np.cos(scanpts[:,1])*np.sin(tilt)

scansource = ColumnDataSource(dict(x=scanu, y=scanv))

p.patch(x='x',y='y',source=scansource,alpha=0.3,line_width=5)
p.line(x='x',y='y',source=scansource)

grate1=ColumnDataSource(dict(x=londf.values[:,0]-kgx*kmult,y=londf.values[:,2]+kgy*kmult))
grate2=ColumnDataSource(dict(x=londf.values[:,0]+kgx*kmult,y=londf.values[:,2]-kgy*kmult))
grate3=ColumnDataSource(dict(x=londf.values[:,0]+kgx*kmult,y=londf.values[:,2]+kgy*kmult))
grate4=ColumnDataSource(dict(x=londf.values[:,0]-kgx*kmult,y=londf.values[:,2]-kgy*kmult))
grate5=ColumnDataSource(dict(x=londf.values[:,0]-kgx,y=londf.values[:,2]))
grate6=ColumnDataSource(dict(x=londf.values[:,0]+kgx,y=londf.values[:,2]))
grate7=ColumnDataSource(dict(x=londf.values[:,0],y=londf.values[:,2]+kgy))
grate8=ColumnDataSource(dict(x=londf.values[:,0],y=londf.values[:,2]-kgy))

p.line(x='x',y='y',source=grate1, color="red",line_width=5)
p.line(x='x',y='y',source=grate2, color="red",line_width=5)
p.line(x='x',y='y',source=grate3, color="red",line_width=5)
p.line(x='x',y='y',source=grate4, color="red",line_width=5)
p.line(x='x',y='y',source=grate5, color="red",line_width=5)
p.line(x='x',y='y',source=grate6, color="red",line_width=5)
p.line(x='x',y='y',source=grate7, color="red",line_width=5)
p.line(x='x',y='y',source=grate8, color="red",line_width=5)

p.x_range=Range1d(-1 , 1)
p.y_range=Range1d(-1 , 1)

def update():

    tilt=float(tiltin.value)*np.pi/180
    wl=2.997e4/float(freqin.value)
    wlout.text='Wavelength = '+str(wl)+' cm'
    kgy=wl/float(dyin.value)
    if lattice.value=='Triangular':
        kgx=2*wl/float(dxin.value)
        kmult=0.5
    else:
        kgx=wl/float(dxin.value)
        kmult=1
    kgxout.text='kgx = '+str(kgx)
    kgyout.text='kgy = '+str(kgy)

    newscanazstr = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in scanazin.value)
    newscanelstr = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in scanelin.value)
    scanaz = [float(i) for i in newscanazstr.split()]
    scanel = [float(i) for i in newscanelstr.split()]
    
    grate1.data=dict(x=londf.values[:,0]-kgx*kmult,y=londf.values[:,2]+kgy*kmult)
    grate2.data=dict(x=londf.values[:,0]+kgx*kmult,y=londf.values[:,2]-kgy*kmult)
    grate3.data=dict(x=londf.values[:,0]+kgx*kmult,y=londf.values[:,2]+kgy*kmult)
    grate4.data=dict(x=londf.values[:,0]-kgx*kmult,y=londf.values[:,2]-kgy*kmult)
    grate5.data=dict(x=londf.values[:,0]-kgx,y=londf.values[:,2])
    grate6.data=dict(x=londf.values[:,0]+kgx,y=londf.values[:,2])
    grate7.data=dict(x=londf.values[:,0],y=londf.values[:,2]+kgy)
    grate8.data=dict(x=londf.values[:,0],y=londf.values[:,2]-kgy)
    
    phi1=np.pi/6
    lon1=np.dot(np.dot(londf,lonrot(phi1)),tiltrot(tilt))
    lon1[lon1[:,1]<=0]=np.nan
    lonprim1.data=dict(x=lon1[:,0],y=lon1[:,1],z=lon1[:,2])
    
    phi2=np.pi/3
    lon2=np.dot(np.dot(londf,lonrot(phi2)),tiltrot(tilt))
    lon2[lon2[:,1]<=0]=np.nan
    lonprim2.data=dict(x=lon2[:,0],y=lon2[:,1],z=lon2[:,2])
    
    phi3=np.pi/2
    lon3=np.dot(np.dot(londf,lonrot(phi3)),tiltrot(tilt))
    lon3[lon3[:,1]<=0]=np.nan
    lonprim3.data=dict(x=lon3[:,0],y=lon3[:,1],z=lon3[:,2])
    
    phi4=2*np.pi/3
    lon4=np.dot(np.dot(londf,lonrot(phi4)),tiltrot(tilt))
    lon4[lon4[:,1]<=0]=np.nan
    lonprim4.data=dict(x=lon4[:,0],y=lon4[:,1],z=lon4[:,2])
    
    phi5=5*np.pi/6
    lon5=np.dot(np.dot(londf,lonrot(phi5)),tiltrot(tilt))
    lon5[lon5[:,1]<=0]=np.nan
    lonprim5.data=dict(x=lon5[:,0],y=lon5[:,1],z=lon5[:,2])
    
    
    latdf=pd.DataFrame(dict(x=np.sin(series360),y=np.cos(series360),z=0*series360))
    
    theta1=np.pi/6
    lat1=np.dot(latdf.values*np.sin(theta1)+zbias.values*np.cos(theta1),tiltrot(tilt))
    lat1[lat1[:,1]<=0]=np.nan
    latprim1.data=dict(x=lat1[:,0],y=lat1[:,1],z=lat1[:,2])
    
    theta2=np.pi/3
    lat2=np.dot(latdf.values*np.sin(theta2)+zbias.values*np.cos(theta2),tiltrot(tilt))
    lat2[lat2[:,1]<=0]=np.nan
    latprim2.data=dict(x=lat2[:,0],y=lat2[:,1],z=lat2[:,2])
    
    theta3=np.pi/2
    lat3=np.dot(latdf.values*np.sin(theta3)+zbias.values*np.cos(theta3),tiltrot(tilt))
    lat3[lat3[:,1]<=0]=np.nan
    latprim3.data=dict(x=lat3[:,0],y=lat3[:,1],z=lat3[:,2])
    
    theta4=2*np.pi/3
    lat4=np.dot(latdf.values*np.sin(theta4)+zbias.values*np.cos(theta4),tiltrot(tilt))
    lat4[lat4[:,1]<=0]=np.nan
    latprim4.data=dict(x=lat4[:,0],y=lat4[:,1],z=lat4[:,2])
    
    theta5=5*np.pi/6
    lat5=np.dot(latdf.values*np.sin(theta5)+zbias.values*np.cos(theta5),tiltrot(tilt))
    lat5[lat5[:,1]<=0]=np.nan
    latprim5.data=dict(x=lat5[:,0],y=lat5[:,1],z=lat5[:,2])
        
    left=np.linspace(start=scanel[0],stop=scanel[1],num=101)
    top=np.linspace(start=scanaz[0],stop=scanaz[1],num=101)
    scanpts=np.append(np.stack((left*0+scanaz[0],left),axis=-1),
                      np.stack((top,top*0+scanel[1]),axis=-1),axis=0)
    scanpts=np.append(scanpts,np.stack((left*0+scanaz[1],np.flipud(left)),axis=-1),axis=0)
    scanpts=np.append(scanpts,np.stack((np.flipud(top),top*0+scanel[0]),axis=-1),axis=0)*np.pi/180
    
    scanu=np.sin(scanpts[:,0])*np.cos(scanpts[:,1])
    scanv=np.sin(scanpts[:,1])*np.cos(tilt)-np.cos(scanpts[:,0])*np.cos(scanpts[:,1])*np.sin(tilt)
    
    scansource.data = dict(x=scanu, y=scanv)

controls=[freqin, dxin, dyin, lattice, tiltin, scanazin, scanelin]

for control in controls:
    control.on_change('value', lambda attr, old, new: update())

layout=row(column(freqin,lattice,dxin,dyin,tiltin,scanazin,scanelin,wlout,kgxout,kgyout),p)

#show(layout)
curdoc().add_root(layout)
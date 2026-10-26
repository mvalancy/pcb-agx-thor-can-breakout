"""Original dimensioned reference models, NOT manufacturer STEP files.
Drawing authority: research/mating-dsub-measurements.json.
Unspecified contours/capture positions are conservative envelopes or assumptions.
"""
import cadquery as cq
from cadagent.fasteners import socket_head_envelope, insert_envelope

def box(x,y,z,dx,dy,dz): return cq.Solid.makeBox(dx,dy,dz,cq.Vector(x,y,z))
def along_y(x,y,z,r,length): return cq.Solid.makeCylinder(r,length,cq.Vector(x,y,z),cq.Vector(0,-1,0))

def mating_set(x, axis, male_flange, separation=6.73, grow=0):
    """Female flange at male_flange-separation; hood capture assumed at rear flange.
    Screw display assumes 2.5 mm insertion, expressly not verified engagement.
    """
    f=male_flange-separation
    flange=box(x-15.405,f-.8,axis-6.275,30.81,.8,12.55)
    for dx in [-12.495,12.495]: flange=flange.cut(along_y(x+dx,f+.1,axis,1.525,1))
    # Conservative rectangular shell envelope; omit cosmetic keystone corners.
    shell=box(x-8.165,f,axis-3.95,16.33,5.8,7.9)
    shell=shell.cut(box(x-7.7,f-.1,axis-3.5,15.4,6,7))
    female=flange.fuse(shell)
    hood=box(x-16.9-grow/2,f-.8-33.3-grow,axis-7.4-grow/2,33.8+grow,33.3+grow,14.8+grow)
    # Hollow hood with representative wall; outer envelope dimensions control clearance.
    hood=hood.cut(box(x-14.9,f-.8-31.3,axis-5.4,29.8,31.5,10.8))
    hood=hood.cut(along_y(x,f-32,axis,4,5))
    screws=[]
    tip=male_flange-4.8+2.5
    for dx in [-12.495,12.495]:
        # 48.5 = threaded 8.7 + collar 1.5 + shaft 28.6 + head 9.7.
        s=along_y(x+dx,tip,axis,1.4224,8.7)
        s=s.fuse(along_y(x+dx,tip-8.7,axis,2,1.5))
        s=s.fuse(along_y(x+dx,tip-10.2,axis,1.3,28.6))
        s=s.fuse(along_y(x+dx,tip-38.8,axis,3.5,9.7))
        screws.append(s)
        hood=hood.cut(along_y(x+dx,f+.1,axis,2.2,36))
    cable=along_y(x,f-.8-33.3,axis,3,20)
    return female,hood,cq.Compound.makeCompound(screws),cable

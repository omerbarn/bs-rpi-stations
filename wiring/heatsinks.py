# Top view of a Raspberry Pi 4 showing where the stick-on heatsinks go (approximate, not to scale)
S=9; OX=60; OY=110   # mm -> px scale and board origin
def r(x,y,w,h,fill,stroke="#1f2937",sw=1.5,rx=2): return f'<rect x="{OX+x*S}" y="{OY+y*S}" width="{w*S}" height="{h*S}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def t(x,y,s,size=13,w=400,fill="#111827",anchor="middle"): return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}">{s}</text>'
W=1180; H=760
o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">',
   f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="#fff" stroke="#d1d5db"/>',
   t(28,40,"Raspberry Pi 4: where the heatsinks go",22,700,anchor="start"),
   t(28,64,"Top view, USB and ethernet ports on the right · peel the backing and press each one on for 10 seconds, with the Pi unplugged",13,400,"#6b7280","start")]
# board 85 x 56 mm
o.append(r(0,0,85,56,"#2f7d4a","#14532d",2,14))
# GPIO header along top
o.append(r(7,1,51,5,"#111827","#111827",1,1))
for i in range(20):
    for j in range(2): o.append(f'<circle cx="{OX+(8.3+i*2.54)*S}" cy="{OY+(2.3+j*2.54)*S}" r="5" fill="#d4af37"/>')
o.append(t(OX+32*S,OY-10,"GPIO pins (the wiring goes here)",12,600,"#374151"))
# wireless shield
o.append(r(4,9,13,12,"#c0c4c8","#6b7280",1.5,3)); o.append(t(OX+10.5*S,OY+15.8*S,"Wi-Fi can",11,400,"#374151"))
# ports right edge: ethernet top, 2 usb stacks
o.append(r(66,2,21,16,"#9ca3af","#4b5563",1.5,2)); o.append(t(OX+76*S,OY+11*S,"Ethernet",12,600))
o.append(r(68,21,19,14,"#3b82f6","#1e3a8a",1.5,2)); o.append(t(OX+77.5*S,OY+29*S,"USB 3",12,600,"#fff"))
o.append(r(68,38,19,14,"#111827","#111827",1.5,2)); o.append(t(OX+77.5*S,OY+46*S,"USB 2",12,600,"#fff"))
# bottom edge: usb-c, 2 micro hdmi, audio
for x,w,l in [(7.5,9,"USB-C power"),(22,7,"HDMI 0"),(35.5,7,"HDMI 1")]:
    o.append(r(x,51,w,6,"#9ca3af","#4b5563",1.5,2)); o.append(t(OX+(x+w/2)*S,OY+56*S+22,l,12,600,"#374151"))
o.append(r(50,49,7,8,"#111827","#111827",1.5,3)); o.append(t(OX+53.5*S,OY+56*S+22,"Audio jack",12,600,"#374151"))
# chips + heatsinks (amber outline = heatsink)
hs="#f59e0b"
def chip(x,y,w,h,fill,label,num):
    o.append(r(x,y,w,h,fill,"#111827",1.5,3))
    o.append(r(x-0.8,y-0.8,w+1.6,h+1.6,"none",hs,4,5))
    cx=OX+(x+w/2)*S; cy=OY+(y+h/2)*S
    o.append(f'<circle cx="{cx}" cy="{cy}" r="17" fill="{hs}"/>'); o.append(t(cx,cy+6,str(num),18,700,"#111827"))
chip(22,18,15,15,"#d1d5db","CPU",1)
chip(43,19,12,14,"#1f2937","RAM",2)
chip(59,38,6,6,"#1f2937","USB",3)
# legend on right
L=[("1","Biggest heatsink → the shiny metal square in the middle (the processor, says Broadcom). This is the one that matters most."),
   ("2","Medium heatsink → the black rectangular chip right next to it (the memory)."),
   ("3","Small heatsink → the small black square chip just behind the USB ports (USB controller)."),
   ("·","Any extra tiny one: optional, it isn't needed. Don't stick anything on the metal Wi-Fi can or on the pins."),
   ("·","Check the case lid still closes, and that no heatsink touches the GPIO pins or the jumper plugs.")]
y=130
o.append(t(880,y-14,"Which heatsink where",15,700,anchor="start"))
for n,s in L:
    import textwrap
    if n.isdigit():
        o.append(f'<circle cx="892" cy="{y+12}" r="12" fill="{hs}"/>'); o.append(t(892,y+17,n,13,700))
    lines=textwrap.wrap(s,34)
    for i,l in enumerate(lines): o.append(t(912,y+17+i*17,l,12.5,400,"#374151","start"))
    y+=17*len(lines)+22
o.append(t(28,H-26,"Layout is a simplified guide, not to scale. Go by what the chips look like: big shiny square = 1, black rectangle beside it = 2, small black square by the USB ports = 3.",12,400,"#6b7280","start"))
o.append('</svg>')
open("pi4-heatsinks.svg","w").write("\n".join(o))

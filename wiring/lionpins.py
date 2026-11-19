# Pin-by-pin wiring sketch for the lion: Pi 4 GPIO header, Jaycar XC4442 ultrasonic sensor, XC4486 level converter
import html
W,H=1180,910
o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">',
   f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="#fff" stroke="#d1d5db"/>']
def t(x,y,s,size=13,w=400,fill="#111827",anchor="middle"): return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}">{html.escape(s)}</text>'
o.append(t(28,40,"Lion (bs-rpi2): Pi, level converter and sensor, pin by pin",22,700,anchor="start"))
o.append(t(28,64,"8 female-to-female jumpers · wire with the Pi unplugged · numbers on the wires match the list at the bottom",13,400,"#6b7280","start"))
RED,BLK,ORG,BLU,GRN,PUR="#dc2626","#111827","#f97316","#2563eb","#16a34a","#9333ea"
# --- Pi header, drawn upright like a pinout chart (pin 1 top-left)
def pin(n): r=(n+1)//2; return (210 if n%2 else 260), 170+(r-1)*46
o.append(f'<rect x="118" y="130" width="236" height="500" rx="10" fill="#2f7d4a" stroke="#14532d" stroke-width="2"/>')
o.append(f'<rect x="188" y="148" width="94" height="{46*10+0}" rx="4" fill="#111827"/>')
o.append(t(230,652,"Pi GPIO header (first 20 pins)",13,700))
use={1:("3.3V",ORG),2:("5V",RED),4:("5V",RED),6:("GND",BLK),14:("GND",BLK),16:("GPIO 23",BLU),18:("GPIO 24",GRN)}
names={1:"3.3V",2:"5V",3:"GPIO2",4:"5V",5:"GPIO3",6:"GND",7:"GPIO4",8:"GPIO14",9:"GND",10:"GPIO15",11:"GPIO17",12:"GPIO18",13:"GPIO27",14:"GND",15:"GPIO22",16:"GPIO23",17:"3.3V",18:"GPIO24",19:"GPIO10",20:"GND"}
for n in range(1,21):
    x,y=pin(n); on=n in use
    o.append(f'<circle cx="{x}" cy="{y}" r="{13 if on else 9}" fill="{use[n][1] if on else "#b8a14a"}" stroke="#fff" stroke-width="{2 if on else 0}"/>')
    o.append(t(x,y+4,str(n),10,700,"#fff" if on else "#3f3f1a"))
    lab=names[n]
    if n%2: o.append(t(182,y-12,lab,10,700 if on else 400,"#ffffff" if on else "#c7e3cf","end"))
    else: o.append(t(288,y-12,lab,10,700 if on else 400,"#ffffff" if on else "#c7e3cf","start"))
o.append(t(230,674,"Pin 1 = the corner pin at the end away",12,600,"#374151"))
o.append(t(230,690,"from the USB ports, inner row",12,600,"#374151"))
# --- converter
o.append(f'<rect x="520" y="225" width="180" height="250" rx="8" fill="#1f2937"/>')
o.append(t(610,205,"Level converter XC4486",14,700))
o.append(t(560,500,"3.3 V side",12,700,"#16a34a")); o.append(t(660,500,"5 V side",12,700,"#dc2626"))
LV_SIDE=[("TXI",250,0),("RXO",290,1),("LV",330,1),("GND",370,1),("RXO",410,0),("TXI",450,0)]
HV_SIDE=[("TXO",250,0),("RXI",290,1),("HV",330,1),("GND",370,0),("RXI",410,0),("TXO",450,0)]
for k,y,u in LV_SIDE:
    o.append(f'<rect x="506" y="{y-5}" width="20" height="10" fill="{"#d4af37" if u else "#6b7280"}"/>'); o.append(t(534,y+5,k,12,700,"#86efac" if u else "#6b7280","start"))
for k,y,u in HV_SIDE:
    o.append(f'<rect x="694" y="{y-5}" width="20" height="10" fill="{"#d4af37" if u else "#6b7280"}"/>'); o.append(t(686,y+5,k,12,700,"#fca5a5" if u else "#6b7280","end"))
    if not u: o.append(t(720,y+4,"not used",10,400,"#9ca3af","start"))
o.append(t(610,520,"Grey pins = not used",11,400,"#6b7280")); o.append(t(610,536,"(top channel used, bottom free)",11,400,"#6b7280"))
# --- sensor
o.append(f'<rect x="900" y="225" width="200" height="250" rx="10" fill="#1e40af"/>')
for cy in (300,410):
    o.append(f'<circle cx="1020" cy="{cy}" r="44" fill="#d1d5db" stroke="#6b7280" stroke-width="3"/><circle cx="1020" cy="{cy}" r="28" fill="#4b5563"/>')
o.append(t(1000,205,"Ultrasonic sensor XC4442",14,700))
S={"VCC":260,"Trig":310,"Echo":360,"GND":410}
for k,y in S.items():
    o.append(f'<rect x="886" y="{y-5}" width="20" height="10" fill="#d4af37"/>'); o.append(t(914,y+5,k,12,700,"#fff","start"))
o.append(t(1000,500,"the round 'eyes' face the visitors",11,400,"#6b7280"))
# --- wires
def w(pts,col,num,tag,dash=False):
    d="M"+" L".join(f"{x},{y}" for x,y in pts)
    o.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="4" stroke-linejoin="round" {"stroke-dasharray=\"10 6\"" if dash else ""}/>')
    tx,ty=tag
    o.append(f'<circle cx="{tx}" cy="{ty}" r="13" fill="#fff" stroke="{col}" stroke-width="2.5"/>'+t(tx,ty+5,str(num),13,700,col))
x2,y2=pin(2); w([(x2+13,y2),(330,y2),(330,100),(860,100),(860,260),(886,260)],RED,1,(600,100))
x6,y6=pin(6); w([(x6+13,y6),(380,y6),(380,580),(840,580),(840,410),(886,410)],BLK,2,(600,580))
x16,y16=pin(16); w([(x16+13,y16),(400,y16),(400,600),(820,600),(820,310),(886,310)],BLU,3,(600,600))
w([(886,360),(800,360),(800,290),(714,290)],PUR,4,(840,360),dash=True)
x18,y18=pin(18); w([(x18+13,y18),(470,y18),(470,290),(506,290)],GRN,5,(470,560))
x4,y4=pin(4); w([(x4+13,y4),(310,y4),(310,140),(770,140),(770,330),(714,330)],RED,6,(600,140))
x1,y1=pin(1); w([(x1-13,y1),(104,y1),(104,115),(490,115),(490,330),(506,330)],ORG,7,(420,115))
x14,y14=pin(14); w([(x14+13,y14),(450,y14),(450,370),(506,370)],BLK,8,(405,446))
# --- list
rows=[("1","Sensor VCC","Pi pin 2 (5 V)",RED),("2","Sensor GND","Pi pin 6 (GND)",BLK),("3","Sensor Trig","Pi pin 16 (GPIO 23)",BLU),("4","Sensor Echo","Converter RXI (5 V side, top channel)",PUR),
      ("5","Converter RXO (3.3 V side, top ch.)","Pi pin 18 (GPIO 24)",GRN),("6","Converter HV","Pi pin 4 (5 V)",RED),("7","Converter LV","Pi pin 1 (3.3 V)",ORG),("8","Converter GND (3.3 V side)","Pi pin 14 (GND)",BLK)]
y0=740
for i,(n,a,b,c) in enumerate(rows):
    x=40+(i//4)*560; y=y0+(i%4)*30
    o.append(f'<circle cx="{x+12}" cy="{y-5}" r="12" fill="#fff" stroke="{c}" stroke-width="2.5"/>'+t(x+12,y,n,12,700,c))
    o.append(t(x+34,y,f"{a}  →  {b}",14,400,"#111827","start"))
o.append(t(40,y0+128,"Pin names from Jaycar's XC4486 datasheet, printed on the board. RXI to RXO is the one-way 5 V to 3.3 V channel, made for exactly this job. Speaker: Pi's 3.5 mm jack.",12,400,"#6b7280","start"))
o.append('</svg>')
open("set1-lion-pins.svg","w").write("\n".join(o))

# Pin-by-pin wiring sketch for the spaceship jet button: Pi 4 GPIO header, Jaycar SP0662 lit arcade button, ethernet to the grandMA2 desk
import html
W,H=1180,1010
o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">',
   f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="#fff" stroke="#d1d5db"/>']
def t(x,y,s,size=13,w=400,fill="#111827",anchor="middle"): return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}">{html.escape(s)}</text>'
o.append(t(28,40,"Spaceship jet (bs-rpi1): Pi and lit arcade button, pin by pin",22,700,anchor="start"))
o.append(t(28,64,"4 female-to-female jumpers · wire with the Pi unplugged · numbers on the wires match the list at the bottom · button drawn from the side, not to scale",13,400,"#6b7280","start"))
RED,BLK,BLU,GRY,CYN="#dc2626","#111827","#2563eb","#6b7280","#0891b2"
# --- Pi header, same layout as the lion sheet (pin 1 top-left)
def pin(n): r=(n+1)//2; return (210 if n%2 else 260), 170+(r-1)*46
o.append(f'<rect x="118" y="130" width="236" height="500" rx="10" fill="#2f7d4a" stroke="#14532d" stroke-width="2"/>')
o.append(f'<rect x="188" y="148" width="94" height="460" rx="4" fill="#111827"/>')
o.append(t(236,652,"Pi GPIO header (first 20 pins)",13,700))
use={4:("5V",RED),6:("GND",BLK),9:("GND",BLK),11:("GPIO 17",BLU)}
names={1:"3.3V",2:"5V",3:"GPIO2",4:"5V",5:"GPIO3",6:"GND",7:"GPIO4",8:"GPIO14",9:"GND",10:"GPIO15",11:"GPIO17",12:"GPIO18",13:"GPIO27",14:"GND",15:"GPIO22",16:"GPIO23",17:"3.3V",18:"GPIO24",19:"GPIO10",20:"GND"}
for n in range(1,21):
    x,y=pin(n); on=n in use
    o.append(f'<circle cx="{x}" cy="{y}" r="{13 if on else 9}" fill="{use[n][1] if on else "#b8a14a"}" stroke="#fff" stroke-width="{2 if on else 0}"/>')
    o.append(t(x,y+4,str(n),10,700,"#fff" if on else "#3f3f1a"))
    if n%2: o.append(t(182,y-12,names[n],10,700 if on else 400,"#ffffff" if on else "#c7e3cf","end"))
    else: o.append(t(288,y-12,names[n],10,700 if on else 400,"#ffffff" if on else "#c7e3cf","start"))
o.append(t(236,674,"Pin 1 = the corner pin at the end away",12,600,"#374151"))
o.append(t(236,690,"from the USB ports, inner row",12,600,"#374151"))
# --- arcade button, side view
o.append(f'<line x1="700" y1="236" x2="1150" y2="236" stroke="#9ca3af" stroke-width="8"/>')
o.append(t(700,226,"panel (25 mm hole)",11,400,"#6b7280","start"))
o.append(f'<rect x="852" y="180" width="96" height="52" rx="22" fill="#ef4444" stroke="#991b1b" stroke-width="2"/>')
o.append(f'<ellipse cx="900" cy="196" rx="30" ry="8" fill="#fecaca" opacity=".8"/>')
o.append(f'<rect x="832" y="226" width="136" height="10" rx="3" fill="#b91c1c"/>')
o.append(t(900,168,"Arcade button SP0662 (lit red)",14,700))
o.append(f'<rect x="862" y="240" width="76" height="90" fill="#fca5a5" opacity=".55" stroke="#991b1b"/>')
o.append(f'<rect x="846" y="244" width="108" height="14" rx="3" fill="#374151"/>')
o.append(t(700,256,"plastic nut",11,400,"#6b7280","start"))
# microswitch with COM / NO / NC tabs
o.append(f'<rect x="796" y="330" width="138" height="90" rx="4" fill="#1f2937"/>')
o.append(t(865,356,"microswitch",12,700,"#e5e7eb"))
o.append(t(865,374,"(click part)",11,400,"#9ca3af"))
TAB={"COM":(818,BLU,True),"NO":(865,BLK,True),"NC":(912,GRY,False)}
for k,(x,c,u) in TAB.items():
    o.append(f'<rect x="{x-7}" y="420" width="14" height="40" fill="{"#d4af37" if u else "#9ca3af"}"/>')
    o.append(t(x,410,k,11,700,"#fde68a" if u else "#9ca3af"))
o.append(t(912,476,"not used",10,400,"#9ca3af"))
# lamp holder with LED tabs
o.append(f'<rect x="940" y="330" width="90" height="70" rx="4" fill="#e5e7eb" stroke="#6b7280"/>')
o.append(t(985,352,"LED lamp",12,700,"#374151"))
for k,x in (("+",960),("−",1010)):
    o.append(f'<rect x="{x-6}" y="400" width="12" height="40" fill="#d4af37"/>')
    o.append(t(x,390,k,16,700,"#111827"))
# --- wires
def w(pts,col,num,tag,dash=False):
    d="M"+" L".join(f"{x},{y}" for x,y in pts)
    o.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="4" stroke-linejoin="round" {"stroke-dasharray=\"10 6\"" if dash else ""}/>')
    tx,ty=tag
    o.append(f'<circle cx="{tx}" cy="{ty}" r="13" fill="#fff" stroke="{col}" stroke-width="2.5"/>'+t(tx,ty+5,str(num),13,700,col))
x11,y11=pin(11); w([(x11-13,y11),(90,y11),(90,708),(818,708),(818,460)],BLU,1,(560,708))
x9,y9=pin(9); w([(x9-13,y9),(70,y9),(70,728),(865,728),(865,460)],BLK,2,(640,728))
x4,y4=pin(4); w([(x4+13,y4),(310,y4),(310,120),(1120,120),(1120,520),(960,520),(960,440)],RED,3,(700,120))
x6,y6=pin(6); w([(x6+13,y6),(330,y6),(330,140),(1095,140),(1095,500),(1010,500),(1010,440)],BLK,4,(760,140),dash=True)
# --- crimp steps (button end of each jumper)
o.append(t(410,214,"Button end of each jumper",14,700,anchor="start"))
steps=["cut the plastic plug off","strip 5 mm of insulation","fold the bare wire back on itself","crimp a 6.3 mm female spade on","push the spade onto the tab"]
for i,s in enumerate(steps):
    y=244+i*48
    o.append(f'<circle cx="422" cy="{y}" r="11" fill="#111827"/>'+t(422,y+5,str(i+1),12,700,"#fff"))
    o.append(t(442,y+5,s,13,400,"#374151","start"))
# little drawing: wire + spade
o.append(f'<line x1="440" y1="500" x2="560" y2="500" stroke="{BLU}" stroke-width="6"/>')
o.append(f'<rect x="560" y="492" width="22" height="16" fill="#9ca3af"/><rect x="582" y="488" width="56" height="24" rx="3" fill="#d4af37" stroke="#a16207"/>')
o.append(t(610,530,"6.3 mm female spade",11,400,"#6b7280"))
# --- network: Pi -> venue switch -> grandMA2 -> jet lights
NY=790
def nbox(x,w,title,sub,fill="#eef0f3",stroke="#9aa3ae"):
    o.append(f'<rect x="{x}" y="{NY}" width="{w}" height="64" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    o.append(t(x+w/2,NY+26,title,14,700)); o.append(t(x+w/2,NY+46,sub,11.5,400,"#4b5563"))
o.append(t(28,NY-16,"Network",15,700,anchor="start"))
nbox(28,200,"Pi ethernet port","next to the USB ports","#e8f5ec","#2f9e55")
nbox(318,220,"Venue network switch","any free port")
nbox(628,250,"grandMA2 desk","192.168.0.20 · telnet port 30000")
nbox(968,184,"Spaceship jet lights","Executor 130","#fff4e6","#e08a1e")
for a,b,lab in ((228,318,"ethernet cable"),(538,628,"venue network"),(878,968,"DMX")):
    o.append(f'<line x1="{a}" y1="{NY+32}" x2="{b}" y2="{NY+32}" stroke="{CYN}" stroke-width="4"/>'+t((a+b)/2,NY+24,lab,11,600,CYN))
# --- list
rows=[("1","Button microswitch COM","Pi pin 11 (GPIO 17)",BLU),("2","Button microswitch NO","Pi pin 9 (GND)",BLK),
      ("3","Button LED +","Pi pin 4 (5 V)",RED),("4","Button LED −","Pi pin 6 (GND)",BLK)]
y0=910
for i,(n,a,b,c) in enumerate(rows):
    x=40+(i//2)*560; y=y0+(i%2)*30
    o.append(f'<circle cx="{x+12}" cy="{y-5}" r="12" fill="#fff" stroke="{c}" stroke-width="2.5"/>'+t(x+12,y,n,12,700,c))
    o.append(t(x+34,y,f"{a}  →  {b}",14,400,"#111827","start"))
o.append(t(40,y0+68,"COM and NO, never NC. No resistor: the Pi's internal pull-up holds GPIO 17 high until the press joins it to GND. Button light stays dark? Swap wires 3 and 4.",12,400,"#6b7280","start"))
o.append('</svg>')
open("set2-jet-pins.svg","w").write("\n".join(o))

# Small wiring drawings for the 3 Raspberry Pi trigger sets (style matches the statue sheets)
import html
W, H = 1180, 470
C = dict(ac="#6b7280", dc5="#d97706", sig="#2563eb", i2c="#7c3aed", audio="#059669", net="#0891b2")
def box(x,y,w,h,title,lines,tag,kind):
    fill={"BUY":"#fff4e6","HAVE":"#e8f5ec","SITE":"#eef0f3"}[kind]
    stroke={"BUY":"#e08a1e","HAVE":"#2f9e55","SITE":"#9aa3ae"}[kind]
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
    s+=f'<text x="{x+12}" y="{y+24}" font-size="15" font-weight="700" fill="#1f2937">{html.escape(title)}</text>'
    for i,l in enumerate(lines):
        s+=f'<text x="{x+12}" y="{y+44+i*17}" font-size="12" fill="#4b5563">{html.escape(l)}</text>'
    if tag:
        tw=8*len(tag)+14
        s+=f'<rect x="{x+w-tw-6}" y="{y-10}" width="{tw}" height="20" rx="10" fill="{stroke}"/>'
        s+=f'<text x="{x+w-tw/2-6}" y="{y+4}" font-size="11" font-weight="700" fill="#fff" text-anchor="middle">{tag}</text>'
    return s
def wire(pts,col,label=None,lx=None,ly=None,dash=False):
    d="M"+" L".join(f"{a},{b}" for a,b in pts)
    s=f'<path d="{d}" fill="none" stroke="{col}" stroke-width="3" {"stroke-dasharray=\"7 5\"" if dash else ""}/>'
    if label:
        s+=f'<text x="{lx}" y="{ly}" font-size="11" font-weight="600" fill="{col}" text-anchor="middle">{html.escape(label)}</text>'
    return s
def legend():
    items=[("240 V AC",C["ac"]),("5 V USB-C",C["dc5"]),("button / GPIO",C["sig"]),("audio 3.5 mm",C["audio"]),("ethernet",C["net"])]
    s='<rect x="28" y="76" width="22" height="14" rx="3" fill="#e8f5ec" stroke="#2f9e55" stroke-width="2"/><text x="56" y="88" font-size="12" fill="#4b5563">GOT = bought at Jaycar 12 Nov</text>'
    s+='<rect x="236" y="76" width="22" height="14" rx="3" fill="#fff4e6" stroke="#e08a1e" stroke-width="2"/><text x="264" y="88" font-size="12" fill="#4b5563">BUY</text>'
    s+='<rect x="302" y="76" width="22" height="14" rx="3" fill="#eef0f3" stroke="#9aa3ae" stroke-width="2"/><text x="330" y="88" font-size="12" fill="#4b5563">on site</text>'
    x=400
    for n,c in items:
        s+=f'<line x1="{x}" y1="83" x2="{x+26}" y2="83" stroke="{c}" stroke-width="3"/><text x="{x+32}" y="88" font-size="12" fill="#4b5563">{n}</text>'
        x+=32+int(6.3*len(n))+18
    return s
def page(title,sub,body,notes,fname,H=H):
    s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">'
    s+=f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="#fff" stroke="#d1d5db"/>'
    s+=f'<text x="28" y="38" font-size="21" font-weight="700" fill="#111827">{html.escape(title)}</text>'
    s+=f'<text x="28" y="60" font-size="13" fill="#6b7280">{html.escape(sub)}</text>'
    s+=legend()+body
    top=H-20-18*len(notes)
    s+=f'<text x="28" y="{top-20}" font-size="14" font-weight="700" fill="#111827">Notes</text>'
    for i,n in enumerate(notes):
        b="  " if n.startswith("  ") else "• "
        s+=f'<text x="28" y="{top+i*18}" font-size="12" fill="#374151" xml:space="preserve">{b}{html.escape(n.strip())}</text>'
    s+='</svg>'
    open(fname,"w").write(s)

# Shared top row: wall socket -> Pi power supply -> Pi
def power_row():
    s=box(28,118,170,72,"Wall socket",["240 V venue outlet","(RCD at the venue)"],None,"SITE")
    s+=box(258,118,210,72,"Pi power supply",["official 5.1 V 3 A USB-C","Jaycar XC9122"],"GOT","HAVE")
    s+=wire([(198,154),(258,154)],C["ac"],"240 V",228,146)
    s+=box(528,110,240,120,"Raspberry Pi 4 in case",["Jaycar XC9100 (4 GB)","microSD 16–32 GB: system,","station.py, settings, mp3","pins · aux jack · ethernet"],"GOT","HAVE")
    s+=wire([(468,154),(528,154)],C["dc5"],"USB-C",498,146)
    return s

# Set 1: lion (Jaycar XC4442 ultrasonic + XC4486 level converter)
b=power_row()
b+=box(888,110,270,84,"Logic level converter",["Jaycar XC4486 (A$4.95)","turns the sensor's 5 V Echo","into 3.3 V for the Pi"],"BUY","BUY")
b+=wire([(768,130),(888,130)],C["dc5"],"5 V · 3.3 V · GND",828,122)
b+=wire([(768,175),(888,175)],C["sig"],"GPIO 24 (Echo)",828,192)
b+=box(888,262,270,72,"Ultrasonic sensor",["Jaycar XC4442 · in the lion base,","aimed at visitors · fires under 1 m"],"GOT","HAVE")
b+=wire([(1023,194),(1023,262)],C["sig"])+'<text x="1031" y="234" font-size="11" font-weight="600" fill="#2563eb">Echo (5 V)</text>'
b+=wire([(768,215),(840,215),(840,300),(888,300)],C["sig"])+'<text x="848" y="230" font-size="11" font-weight="600" fill="#2563eb">5 V · GND ·</text><text x="848" y="244" font-size="11" font-weight="600" fill="#2563eb">Trig GPIO 23</text>'
b+=box(528,290,240,64,"Speaker",["on site (manager has it), next to","the lion · plays lion_roar.mp3"],None,"SITE")
b+=wire([(648,230),(648,290)],C["audio"],"3.5 mm aux cable (on site)",585,266)
b+=box(258,290,210,64,"Wall socket",["speaker power","(or USB if it's a USB speaker)"],None,"SITE")
b+=wire([(468,322),(528,322)],C["ac"],"240 V",498,314)
pins=[("Sensor VCC","Pi 5 V (pin 2)"),("Sensor GND","Pi GND (pin 6)"),("Sensor Trig","Pi GPIO 23 (pin 16)"),("Sensor Echo","Converter HV1"),("Converter LV1","Pi GPIO 24 (pin 18)"),("Converter HV","Pi 5 V (pin 4)"),("Converter LV","Pi 3.3 V (pin 1)"),("Converter GND","Pi GND (pin 14)")]
b+='<text x="28" y="392" font-size="14" font-weight="700" fill="#111827">8 female-to-female jumpers: every end pushes onto a pin (Pi, sensor and converter all have pins), no crimps</text>'
for i,(f,t) in enumerate(pins):
    x=28+(i%4)*285; y=416+(i//4)*22
    b+=f'<text x="{x}" y="{y}" font-size="12" fill="#374151"><tspan font-weight="700">{i+1}.</tspan> {html.escape(f)} → {html.escape(t)}</text>'
page("Set 1 · Lion roar: wiring (ultrasonic sensor + speaker)",
     "Raspberry Pi 4 · Jaycar XC4442 ultrasonic · XC4486 level converter · speaker on site · no network needed · config-1-lion.json",
     b,["The sensor runs on 5 V and its Echo pin sends back 5 V. Pi pins only take 3.3 V, so Echo must go through the converter (or a 1k/2k resistor divider).",
        "Trig can go straight to the Pi: 3.3 V from the Pi is enough to fire the sensor.",
        "Person within 1 m → the speaker roars once; again only after they step away and 10 s have passed.",
        "Male-to-female jumpers are only for the backup plan: a 1k/2k resistor divider on a mini breadboard instead of the converter."],"set1-lion-wiring.svg",H=590)

def button_set(n,name,sub,notes,fname,udp):
    b=power_row()
    b+=box(888,110,270,72,"Arcade button, red, lit",["Jaycar SP0662 · 25 mm hole · spades","switch: COM + NO · light: 2 LED tabs"],"GOT","HAVE")
    b+=wire([(768,130),(888,130)],C["sig"],"GPIO 17 · pin 11",828,122)
    b+=wire([(768,150),(888,150)],"#111827")
    b+=wire([(768,170),(888,170)],C["dc5"])
    b+='<text x="828" y="188" font-size="11" font-weight="600" fill="#111827" text-anchor="middle">GND · pin 9</text>'
    b+='<text x="828" y="202" font-size="11" font-weight="600" fill="#d97706" text-anchor="middle">LED · pin 4 + pin 6</text>'
    b+=box(888,240,270,72,"Venue network switch",["light/sound system listens for","UDP: "+udp],None,"SITE")
    b+=wire([(700,230),(700,276),(888,276)],C["net"],"ethernet cable",790,268)
    b+=box(528,276,150,64,"(no speaker)",["aux jack unused","unless a sound is added"],None,"SITE")
    page(name,sub,b,notes,fname,H=510)

button_set(2,"Set 2 · Button: wiring (spaceship jet lights)",
     "Raspberry Pi 4 · lit arcade button · ethernet to the venue · no sound · settings file config-2-button.json",
     ["Press → the Pi sends one UDP message to the venue system, which changes the lights on the spaceship jet.",
      "Button wiring: 2 female-to-female jumpers. Pi end: push onto pin 11 (GPIO 17) and pin 9 (GND). Button end: cut off the plug, strip 5 mm,",
      "  fold the bare wire double, crimp a 6.3 mm female spade, push onto the microswitch's COM and NO tabs (not NC, not the 2 LED tabs). No resistor.",
      "Light: 2 more crimped jumpers from the LED tabs to pin 4 (5 V) and pin 6 (GND). Dark? swap them (LED has a + side). Too dim on 5 V?",
      "  Use a 12 V DC plug pack + DC-socket-to-screw-terminal adapter on the LED tabs instead (Pi pins stay as they are).",
      "UDP message, IP and port are placeholders until the venue tells us what its system listens for."],"set2-button-wiring.svg","SPACESHIP_JET_GO (placeholder)")
button_set(3,"Set 3 · Spare: wiring (set up as a button)",
     "Identical to set 2, ready to swap in or to become a third trigger · settings file config-3-spare.json",
     ["Wired exactly like set 2: 2 female-to-female jumpers onto pins 11 and 9, button end cut and crimped with 6.3 mm female spades.",
      "To swap in: for the button set copy config-2-button.json in as config.json; for the lion move the sensor, converter and jumpers across.",
      "Light: same as set 2, LED tabs to pin 4 (5 V) and pin 6 (GND), or a 12 V plug pack if 5 V is too dim.",
      "If a third trigger is wanted later, only its settings file changes (sound, UDP message or both)."],"set3-spare-wiring.svg","SPARE_BUTTON_GO (placeholder)")

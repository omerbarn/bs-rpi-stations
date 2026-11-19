# "How it works" sheets for the lion and the spaceship jet: a flow along the top and a timeline
# made by running station.py's trigger rules (same loop, 50 ms steps) on a made-up visit
import html, json
W=1180
def t(x,y,s,size=13,w=400,fill="#111827",anchor="middle"): return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}">{html.escape(s)}</text>'
def head(H,title,sub):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">',
            f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="#fff" stroke="#d1d5db"/>',
            t(28,40,title,22,700,anchor="start"),t(28,64,sub,13,400,"#6b7280","start"),
            '<defs><marker id="ar" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#6b7280"/></marker></defs>']
def flow(o,y,steps):
    # steps: (title, [lines], fill, stroke); equal boxes with arrows between
    n=len(steps); gap=34; bw=(W-56-gap*(n-1))/n; h=118
    for i,(title,lines,fill,stroke) in enumerate(steps):
        x=28+i*(bw+gap)
        o.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        o.append(f'<circle cx="{x+20}" cy="{y+22}" r="11" fill="{stroke}"/>'+t(x+20,y+27,str(i+1),12,700,"#fff"))
        o.append(t(x+38,y+27,title,14,700,anchor="start"))
        for j,l in enumerate(lines): o.append(t(x+14,y+52+j*17,l,12,400,"#374151","start"))
        if i<n-1: o.append(f'<line x1="{x+bw+4}" y1="{y+h/2}" x2="{x+bw+gap-4}" y2="{y+h/2}" stroke="#6b7280" stroke-width="2.5" marker-end="url(#ar)"/>')
def simulate(cfg,close_at,length,sound_s):
    # Same rules as station.py's main loop; returns the times fire() runs
    fires=[]; last_fire=last_close=last_done=-1e9; armed=True; play_end=-1; t_=0.0  # station.py starts at 0 on a clock of ~1.7e9 s
    while t_<length:
        close=close_at(t_); playing=t_<play_end
        if playing: last_done=t_
        if close:
            repeat=cfg.get("repeat_s",0)>0 and t_-last_done>cfg["repeat_s"]
            if (armed or repeat) and not playing and t_-last_fire>cfg["cooldown_s"]:
                last_fire=t_; fires.append(t_); armed=False
                if sound_s: play_end=t_+sound_s
            last_close=t_
        elif t_-last_close>cfg.get("clear_s",0.2): armed=True
        t_=round(t_+0.05,2)
    return fires

# ---------- Lion ----------
cfg=json.load(open("../config-1-lion.json")); ROAR=10.0; L=50
def dist(s):  # metres: visitor A walks up, stays ~28 s, leaves; visitor B walks up at 40 s
    if s<2: return 3.0
    if s<5: return 3.0-(s-2)*0.7
    if s<31: return 0.9+0.08*((s*7)%3)/3
    if s<34: return 0.9+(s-31)*0.7
    if s<39: return 3.0
    if s<42: return 3.0-(s-39)*0.7
    return 0.95
fires=simulate(cfg,lambda s: dist(s)*1000<cfg["distance_mm"],L,ROAR)
o=head(700,"Lion: how it works","Ultrasonic sensor in the lion base → Raspberry Pi → speaker · settings in config-1-lion.json · no network needed")
flow(o,92,[("Visitor walks up",["someone comes within","1.5 m of the lion"],"#eef0f3","#9aa3ae"),
           ("Sensor measures",["pings 20× a second, Echo","comes back through the","level converter (5 V → 3.3 V)"],"#e8f5ec","#2f9e55"),
           ("Pi decides",["station.py checks the rules","below: new visitor, still","roaring, waited long enough?"],"#e8f5ec","#2f9e55"),
           ("Lion roars",["lion_roar.mp3 (10 s) plays","from the 3.5 mm jack","to the speaker"],"#fff4e6","#e08a1e")])
# timeline
X0,X1,Y0,Y1=90,1150,262,452   # plot box; distance 0..3 m upward
sx=lambda s: X0+(X1-X0)*s/L; sy=lambda m: Y1-(Y1-Y0)*m/3
o.append(t(28,248,"Example: what the code does with two visitors",15,700,anchor="start"))
o.append(f'<rect x="{X0}" y="{Y0}" width="{X1-X0}" height="{Y1-Y0}" fill="#f9fafb" stroke="#e5e7eb"/>')
o.append(f'<rect x="{X0}" y="{sy(1.5)}" width="{X1-X0}" height="{Y1-sy(1.5)}" fill="#fef3c7" opacity=".6"/>')
for m in (0,1,1.5,2,3):
    o.append(t(X0-8,sy(m)+4,f"{m:g} m",11,400,"#6b7280","end"))
o.append(f'<line x1="{X0}" y1="{sy(1.5)}" x2="{X1}" y2="{sy(1.5)}" stroke="#d97706" stroke-width="2" stroke-dasharray="7 5"/>')
o.append(t(X1-6,sy(1.5)-6,"trigger line: distance_mm = 1500",11,700,"#d97706","end"))
pts=" ".join(f"{sx(i/10):.1f},{sy(dist(i/10)):.1f}" for i in range(0,L*10+1))
o.append(f'<polyline points="{pts}" fill="none" stroke="#2563eb" stroke-width="3"/>')
o.append(t(X0+6,Y0+16,"distance the sensor reads",11,700,"#2563eb","start"))
o.append(t(sx(18),sy(0.9)+24,"visitor A stands at the lion",11,600,"#2563eb"))
o.append(t(sx(45),sy(0.95)+24,"visitor B",11,600,"#2563eb"))
# roar bars
RY=480
o.append(t(X0-8,RY+16,"roar",11,700,"#e08a1e","end"))
for f in fires:
    o.append(f'<rect x="{sx(f)}" y="{RY}" width="{sx(min(f+ROAR,L))-sx(f)}" height="24" rx="5" fill="#f59e0b"/>')
    o.append(f'<line x1="{sx(f)}" y1="{Y0}" x2="{sx(f)}" y2="{RY}" stroke="#e08a1e" stroke-width="1.5" stroke-dasharray="3 3"/>')
gaps=[(fires[i]+ROAR,fires[i+1]) for i in range(len(fires)-1) if fires[i+1]-fires[i]-ROAR<6]
for a,b in gaps:
    o.append(t((sx(a)+sx(b))/2,RY+16,f"{b-a:.0f} s",11,700,"#92400e"))
for s in range(0,L+1,5):
    o.append(f'<line x1="{sx(s)}" y1="{RY+30}" x2="{sx(s)}" y2="{RY+35}" stroke="#9ca3af"/>'+t(sx(s),RY+48,f"{s} s",10,400,"#6b7280"))
rules=[("New visitor → roar straight away.","Someone counts as new once nobody has been inside 1.5 m for clear_s = 0.5 s (so one missed sensor reading doesn't count as leaving)."),
       ("Visitor stays → roar again.",f"Another roar repeat_s = {cfg['repeat_s']:g} s after the last one finishes, for as long as they stay."),
       ("Never two at once.",f"No new roar while one is playing, and at least cooldown_s = {cfg['cooldown_s']:g} s between the starts of two roars."),
       ("Walks away mid-roar →","the roar plays to the end; the next person gets a fresh roar as soon as the speaker is free.")]
for i,(a,b) in enumerate(rules):
    y=566+i*28
    o.append(f'<circle cx="38" cy="{y-5}" r="5" fill="#e08a1e"/>')
    o.append(f'<text x="52" y="{y}" font-size="13" fill="#374151"><tspan font-weight="700">{html.escape(a)}</tspan> {html.escape(b)}</text>')
o.append(t(28,684,"Timeline computed with the same rules and settings as station.py · roar length 10 s · live readings: set \"debug\": true in config.json and run journalctl -u station -f",11,400,"#9ca3af","start"))
o.append('</svg>'); open("how-lion.svg","w").write("\n".join(o))

# ---------- Spaceship jet ----------
cfg=json.load(open("../config-2-button.json")); L=20
presses=[(1,2.5),(4,4.3),(8,8.3),(9,9.2),(14.5,14.8)]
pressed=lambda s: any(a<=s<b for a,b in presses)
fires=simulate(cfg,pressed,L,0)
o=head(640,"Spaceship jet: how it works","Lit arcade button → Raspberry Pi → grandMA2 lighting desk → jet lights · settings in config-2-button.json · set the desk login with set-ma.sh")
flow(o,92,[("Visitor presses",["the lit red button","(its light is always on)"],"#eef0f3","#9aa3ae"),
           ("Pi sees the press",["microswitch joins GPIO 17","to GND · 50 ms debounce"],"#e8f5ec","#2f9e55"),
           ("Pi calls the desk",["telnet to 192.168.0.20:30000","login \"administrator\" \"…\"",f"{cfg['ma_command']}"],"#e8f5ec","#2f9e55"),
           ("grandMA2 desk",[f"toggles Executor {cfg['ma_command'].split()[-1]}","one press on,","the next press off"],"#eef0f3","#9aa3ae"),
           ("Jet lights change",["the spaceship jet","lighting cue runs"],"#fff4e6","#e08a1e")])
X0,X1=150,1150; sx=lambda s: X0+(X1-X0)*s/L
o.append(t(28,250,"Example: what the code does with five presses",15,700,anchor="start"))
BY,CY=272,330
o.append(t(X0-10,BY+18,"button held",11,700,"#2563eb","end"))
o.append(t(X0-10,CY+18,"command sent",11,700,"#e08a1e","end"))
o.append(f'<rect x="{X0}" y="{BY}" width="{X1-X0}" height="26" fill="#f9fafb" stroke="#e5e7eb"/>')
o.append(f'<rect x="{X0}" y="{CY}" width="{X1-X0}" height="26" fill="#f9fafb" stroke="#e5e7eb"/>')
for a,b in presses:
    o.append(f'<rect x="{sx(a)}" y="{BY+3}" width="{max(sx(b)-sx(a),6)}" height="20" rx="4" fill="#2563eb"/>')
state=False
for f in fires:
    state=not state
    o.append(f'<line x1="{sx(f)}" y1="{BY+26}" x2="{sx(f)}" y2="{CY}" stroke="#e08a1e" stroke-width="1.5" stroke-dasharray="3 3"/>')
    o.append(f'<rect x="{sx(f)}" y="{CY+3}" width="12" height="20" rx="3" fill="#f59e0b"/>')
    o.append(t(sx(f)+18,CY+18,f"Toggle → lights {'ON' if state else 'OFF'}",11,700,"#92400e","start"))
for a,b in presses:
    if not any(a<=f<b+0.1 for f in fires):
        o.append(t(sx(a)+4,BY+44,"ignored (cooldown)",10,600,"#9ca3af","start"))
o.append(t(sx(1.2),BY-6,"held 1.5 s: still one command",10,600,"#2563eb","start"))
for s in range(0,L+1,2):
    o.append(f'<line x1="{sx(s)}" y1="{CY+32}" x2="{sx(s)}" y2="{CY+37}" stroke="#9ca3af"/>'+t(sx(s),CY+50,f"{s} s",10,400,"#6b7280"))
rules=[("One press = one command.","Holding the button down doesn't repeat it; the button has to be let go first."),
       ("Cooldown.",f"Presses less than cooldown_s = {cfg['cooldown_s']:g} s after the last command are ignored, so kids hammering it can't flicker the lights."),
       ("Toggle.","The desk flips Executor 130 each time, so presses alternate the jet lights on and off."),
       ("Desk unreachable?","The Pi logs \"MA2 command failed\" and keeps listening for the next press; it never needs a restart.")]
for i,(a,b) in enumerate(rules):
    y=444+i*28
    o.append(f'<circle cx="38" cy="{y-5}" r="5" fill="#e08a1e"/>')
    o.append(f'<text x="52" y="{y}" font-size="13" fill="#374151"><tspan font-weight="700">{html.escape(a)}</tspan> {html.escape(b)}</text>')
o.append(t(28,578,"The command line is the same as the venue's existing MA button: log in, send one line, hang up. Change it with ./set-ma.sh, e.g. a Go+ instead of a Toggle.",12,400,"#6b7280","start"))
o.append(t(28,604,"Timeline computed with the same rules and settings as station.py · watch it live: ssh pi@bs-rpi1.local journalctl -u station -f",11,400,"#9ca3af","start"))
o.append('</svg>'); open("how-jet.svg","w").write("\n".join(o))
print("lion fires:",fires and "ok")

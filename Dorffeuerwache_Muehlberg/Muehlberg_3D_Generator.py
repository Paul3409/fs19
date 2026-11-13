"""Procedurally built interpretation of the user's 4-view Dorffeuerwache Mühlberg drawing.
Creates a valid Wavefront OBJ/MTL + PNG textures and portable GLB. Unit = meter.
This is an EXTERIOR visual model, not a ready-to-play LS19 placeable or engineered interior.
"""
import os, math, random, zipfile, collections
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import trimesh

OUT=os.path.join(os.getcwd(),'Dorffeuerwache_Muehlberg_Nach_Zeichnung')
os.makedirs(OUT,exist_ok=True)
random.seed(43)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(n,b=True):return ImageFont.truetype(BOLD if b else FONT,n)
def save(name,img):
    img.save(os.path.join(OUT,name+'.png'))
    return name+'.png'
def noisy(base,size=(512,512),sigma=3):
    a=np.zeros((size[1],size[0],3),np.uint8)
    noise=np.random.default_rng(20).normal(0,sigma,(size[1],size[0],1))
    for c in range(3):a[:,:,c]=np.clip(base[c]+noise[:,:,0],0,255)
    return Image.fromarray(a,'RGB')

def brick(name, base=(145,67,52), w=1024,h=1024):
    im=noisy((179,165,149),(w,h),2); d=ImageDraw.Draw(im)
    bh=42; bw=126; mortar=5
    for row,y in enumerate(range(0,h,bh)):
        shift=(row%2)*(bw//2)
        for x in range(-bw,w+bw,bw):
            xx=x+shift
            sh=random.randint(-20,22)
            color=tuple(int(max(1,min(255,v+sh))) for v in base)
            d.rectangle((xx+mortar,y+mortar,xx+bw-2,y+bh-2),fill=color)
            if random.random()<0.28:
                d.line((xx+10,y+bh-7,xx+bw-10,y+bh-7),fill=tuple(max(0,z-9) for z in color),width=1)
    save(name,im)
brick('klinker_rot',(143,65,48))
brick('klinker_dunkel',(104,55,48))
brick('klinker_schornstein',(130,65,49))
brick('naturstein',(174,156,131))
# dark brown tile roof with rows and subtle textured individual tiles
im=noisy((65,48,43),(1024,1024),3); d=ImageDraw.Draw(im)
for row,y in enumerate(range(-7,1050,52)):
    off=(row%2)*31
    for x in range(-100+off,1040,62):
        c=random.choice([(61,45,43),(69,50,46),(72,48,42),(80,53,46),(56,43,41),(84,58,48)])
        d.rounded_rectangle((x+2,y+2,x+60,y+50),radius=5,fill=c,outline=(45,36,34),width=2)
        d.line((x+7,y+9,x+55,y+9),fill=tuple(min(255,k+18) for k in c),width=2)
        d.arc((x+5,y+31,x+56,y+58),0,180,fill=(43,34,32),width=2)
save('dachziegel_dunkel',im)
# wood plank door: horizontal grain + seams
im=noisy((126,53,52),(1024,1024),4); d=ImageDraw.Draw(im)
for y in range(0,1024,128):
    d.rectangle((0,y+3,1024,y+121),fill=random.choice([(127,52,50),(131,56,53),(139,63,57),(117,47,46)]))
    d.line((0,y+1,1024,y+1),fill=(64,30,29),width=5)
    d.line((0,y+9,1024,y+9),fill=(167,75,70),width=2)
    for j in range(7):
        yy=y+random.randint(15,113)
        d.line((random.randint(0,100),yy,random.randint(850,1024),yy+random.randint(-3,3)),fill=(110,47,45),width=1)
save('holztor_ochsenblutrot',im)
# stained aged wood & metal / stone etc
for name,color in [('holz_alt',(121,86,55)),('rahmen_hell',(217,207,176)),('putz_hell',(212,195,170)),('blech_dunkel',(58,64,63)),('glas_blau',(78,113,127)),('fenster_weiss',(208,210,198)),('dachkupfer',(78,78,62)),('fenster_dunkel',(47,61,65)),('ziegel_fuge',(113,108,100)),('grau',(125,123,119)),('rasen',(85,101,70))]:
    im=noisy(color,(512,512),3)
    d=ImageDraw.Draw(im)
    if name=='holz_alt':
        for x in range(0,512,42):
            d.line((x,0,x,512),fill=(64,46,33),width=2)
            d.line((x+4,0,x+4,512),fill=(165,125,85),width=1)
    if name=='glas_blau':
        d.polygon([(0,480),(0,330),(380,0),(510,0)],fill=(110,143,151))
        for q in range(0,512,40):d.line((q,0,q+80,511),fill=(89,117,126),width=1)
    save(name,im)
# old paved apron
im=noisy((168,162,150),(1024,1024),2); d=ImageDraw.Draw(im)
for y in range(0,1024,98):
    for x in range(0,1024,118):
        shift=random.randint(-13,10)
        d.rounded_rectangle((x+3,y+4,x+114,y+94),radius=5,fill=(168+shift,162+shift,150+shift),outline=(121,119,111),width=3)
save('hofpflaster',im)
# herbals and brick for backside accents
im=noisy((46,81,41),(512,512),12); d=ImageDraw.Draw(im)
for i in range(1600):
    x=random.randint(0,511); y=random.randint(0,511)
    c=random.choice([(51,110,42),(76,108,52),(32,71,34),(90,126,57)])
    r=random.randint(1,7)
    d.ellipse((x-r,y-r,x+r,y+r),fill=c)
save('laubwerk',im)
# sign, precise German name, front sign 4:1 horizontal
im=Image.new('RGB',(2048,256),(226,219,187));d=ImageDraw.Draw(im)
d.rectangle((8,10,2040,245),outline=(85,70,60),width=9)
text='DORFFEUERWACHE  –  MÜHLBERG'
f=font(104)
b=d.textbbox((0,0),text,font=f);d.text(((2048-(b[2]-b[0]))/2,70),text,font=f,fill=(35,37,35))
save('schriftzug_muehlberg',im)
# Enameled heraldic badge with recognizable fire symbol
im=Image.new('RGB',(512,650),(57,50,43));d=ImageDraw.Draw(im)
d.polygon([(45,25),(467,25),(467,420),(256,605),(45,420)],fill=(162,35,34),outline=(236,218,175),width=17)
d.text((256,55),'FREIWILLIGE',font=font(44),fill=(246,220,176),anchor='ma')
d.text((256,105),'FEUERWEHR',font=font(51),fill=(246,220,176),anchor='ma')
d.ellipse((131,205,385,450),fill=(241,217,178),outline=(52,48,43),width=14)
d.ellipse((151,225,365,430),fill=(29,46,52))
# crossed axes and flame/helmet icon
d.line((185,265,322,389),fill=(211,193,155),width=20)
d.line((320,263,190,395),fill=(211,193,155),width=20)
d.polygon([(206,257),(160,235),(174,299)],fill=(205,213,218))
d.polygon([(304,260),(360,245),(346,309)],fill=(205,213,218))
d.text((256,477),'MÜHLBERG',font=font(36),fill=(248,214,169),anchor='mm')
save('wappen_feuerwehr',im)
# tower plaque (not on blueprint but subtle) no extra signage
MATS={k:k+'.png' for k in ['klinker_rot','klinker_dunkel','klinker_schornstein','naturstein','dachziegel_dunkel','holztor_ochsenblutrot','holz_alt','rahmen_hell','putz_hell','blech_dunkel','glas_blau','fenster_weiss','dachkupfer','fenster_dunkel','ziegel_fuge','grau','rasen','hofpflaster','laubwerk','schriftzug_muehlberg','wappen_feuerwehr']}

facets=[]
def tri(obj,mat,pts,uvs):
    if len(pts)!=3 or len(uvs)!=3:raise ValueError('tri')
    facets.append((obj,mat,pts,uvs))
def poly(obj,mat,points,uv=None,scale=1):
    points=[tuple(map(float,p)) for p in points]
    if uv is None:
        # project polygon to predominant plane with self-consistent UVs
        pa=np.array(points)
        n=np.cross(pa[1]-pa[0],pa[2]-pa[0]); ax=np.argmax(np.abs(n))
        if ax==0: uv=[(p[1]/scale,p[2]/scale) for p in points]
        elif ax==1:uv=[(p[0]/scale,p[2]/scale) for p in points]
        else:uv=[(p[0]/scale,p[1]/scale) for p in points]
    for i in range(1,len(points)-1):tri(obj,mat,[points[0],points[i],points[i+1]],[uv[0],uv[i],uv[i+1]])
def box(obj,mat,x0,x1,y0,y1,z0,z1,scale=1):
    if x1<=x0 or y1<=y0 or z1<=z0:return
    # Closed solid with outward-facing normals (essential in GIANTS/Blender).
    faces = [
        [(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)], # front -Y
        [(x1,y1,z0),(x0,y1,z0),(x0,y1,z1),(x1,y1,z1)], # back +Y
        [(x0,y1,z0),(x0,y0,z0),(x0,y0,z1),(x0,y1,z1)], # left -X
        [(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)], # right +X
        [(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)], # top +Z
        [(x0,y1,z0),(x1,y1,z0),(x1,y0,z0),(x0,y0,z0)]  # bottom -Z
    ]
    for face in faces: poly(obj,mat,face,scale=scale)

def linebox(obj,mat,a,b,th=.09,scale=1):
    """Beam between two points as rectangular prism."""
    a=np.array(a,float); b=np.array(b,float);v=b-a; ln=np.linalg.norm(v)
    if ln<1e-5:return
    v=v/ln
    up=np.array((0.,0.,1.))
    if abs(np.dot(v,up))>.93:up=np.array((0.,1.,0.))
    s=np.cross(v,up);s=s/np.linalg.norm(s)*th/2
    t=np.cross(v,s);t=t/np.linalg.norm(t)*th/2
    corners=[]
    for p in (a,b):corners +=[tuple(p-s-t),tuple(p+s-t),tuple(p+s+t),tuple(p-s+t)]
    for j in range(4):poly(obj,mat,[corners[j],corners[(j+1)%4],corners[(j+1)%4+4],corners[j+4]],scale=scale)
    poly(obj,mat,corners[:4],scale=scale);poly(obj,mat,corners[4:],scale=scale)

def gable_x(obj,mat,x,y0,y1,z_eave,z_peak,scale=1,outward=1):
    points=[(x,y0,z_eave),(x,y1,z_eave),(x,(y0+y1)/2,z_peak)]
    if outward<0:points.reverse()
    poly(obj,mat,points,scale=scale)
def roof_x(obj,x0,x1,ylo,yhi,eave,ridge,mat='dachziegel_dunkel',overhang=.35):
    # horizontal ridge in X; two roof planes and fascia on edges
    ymid=(ylo+yhi)/2
    poly(obj,mat,[(x0-overhang,ylo-overhang,eave),(x1+overhang,ylo-overhang,eave),(x1+overhang,ymid,ridge),(x0-overhang,ymid,ridge)],scale=.85)
    poly(obj,mat,[(x1+overhang,yhi+overhang,eave),(x0-overhang,yhi+overhang,eave),(x0-overhang,ymid,ridge),(x1+overhang,ymid,ridge)],scale=.85)
    linebox(obj+'_Traufe','blech_dunkel',(x0-overhang,ylo-overhang,eave),(x1+overhang,ylo-overhang,eave),.13)
    linebox(obj+'_Traufe','blech_dunkel',(x0-overhang,yhi+overhang,eave),(x1+overhang,yhi+overhang,eave),.13)
    linebox(obj+'_First','dachziegel_dunkel',(x0-overhang,ymid,ridge+.04),(x1+overhang,ymid,ridge+.04),.16)
    for x in (x0-overhang,x1+overhang):
        linebox(obj+'_Ortgang','blech_dunkel',(x,ylo-overhang,eave),(x,ymid,ridge),.14)
        linebox(obj+'_Ortgang','blech_dunkel',(x,ymid,ridge),(x,yhi+overhang,eave),.14)

def roof_y(obj,x0,x1,y0,y1,eave,ridge,mat='dachziegel_dunkel'):
    mid=(x0+x1)/2
    poly(obj,mat,[(x0-.25,y0-.3,eave),(mid,y0-.3,ridge),(mid,y1+.3,ridge),(x0-.25,y1+.3,eave)],scale=.75)
    poly(obj,mat,[(mid,y0-.3,ridge),(x1+.25,y0-.3,eave),(x1+.25,y1+.3,eave),(mid,y1+.3,ridge)],scale=.75)
    linebox(obj+'_First','blech_dunkel',(mid,y0-.3,ridge),(mid,y1+.3,ridge),.13)
    for x in (x0-.25,x1+.25):linebox(obj+'_Traufe','blech_dunkel',(x,y0-.3,eave),(x,y1+.3,eave),.1)
    for y in (y0-.3,y1+.3):
        linebox(obj+'_Giebel','blech_dunkel',(x0-.25,y,eave),(mid,y,ridge),.11)
        linebox(obj+'_Giebel','blech_dunkel',(mid,y,ridge),(x1+.25,y,eave),.11)

# FRONT / main structure, red brick with pier and high zone
box('Hauptbau_Gewaende','klinker_rot',4.00,24.0,0,10,0,6.15,1.4)
gable_x('Hauptbau_Giebel_rechts','klinker_rot',24.001,0,10,6.15,10.45,1.4)
gable_x('Hauptbau_Giebel_links','klinker_rot',3.999,0,10,6.15,10.45,1.4,outward=-1)
roof_x('Hauptbau_Ziegeldach',4.0,24.0,0,10,6.15,10.45)
# different colored foundation / decorative brick band
box('Hauptbau_Sockel','klinker_dunkel',4,24,-.12,10.14,0,.45,1.0)
for x0,x1 in [(4,5.07),(10.65,11.43),(17.03,17.81),(23.3,24)]:
    box('Hauptbau_Torpfeiler','klinker_rot',x0,x1,-.20,.01,.45,5.38,1.3)
box('Hauptbau_Torsturz','naturstein',4.85,23.45,-.25,0,4.79,4.93,1)
box('Hauptbau_Traufgesims','naturstein',4,24,-.29,.15,5.92,6.13,1)
# front red double-doors: explicit panels, diagonals, hinges and glass; not just dark rectangle
BAYS=[(5.14,10.61),(11.47,16.97),(17.84,23.26)]
for i,(a,b) in enumerate(BAYS,1):
    obj=f'Tor_{i:02d}_zweifluegelig'
    m=(a+b)/2; front=-.36
    # stone border around each entrance
    box(obj+'_Laibung','naturstein',a-.11,b+.11,front+.23,front+.34,.48,4.80,1.2)
    box(obj+'_Holz_Zargen','holz_alt',a-.07,b+.07,front-.065,front+.22,.55,4.65,1.0)
    for xx,zz,ww in [(a-.07,.45,.17),(b-.10,.45,.17)]:
        box(obj+'_Rahmen','holz_alt',xx,xx+ww,front-.17,front+.14,.47,4.7)
    box(obj+'_Rahmen','holz_alt',a-.03,b+.03,front-.20,front+.1,4.53,4.73)
    box(obj+'_Schwelle','naturstein',a-.09,b+.09,front-.4,front+.2,.38,.55)
    for x0,x1 in [(a+.10,m-.045),(m+.045,b-.1)]:
        box(obj+'_Holzfluegel','holztor_ochsenblutrot',x0,x1,front-.16,front-.07,.61,4.52,2.0)
        # recessed rectangular 3 lower panels
        for z0,z1 in [(.85,1.93),(2.02,3.08)]:
            box(obj+'_Rahmenleisten','holz_alt',x0+.14,x1-.14,front-.19,front-.16,z0,z0+.075)
            box(obj+'_Rahmenleisten','holz_alt',x0+.14,x1-.14,front-.19,front-.16,z1-.075,z1)
        # diagonal wood brace (X motif in lower part)
        linebox(obj+'_Diagonalstreben','holztor_ochsenblutrot',(x0+.15,front-.24,.8),(x1-.14,front-.24,3.18),.10)
        # glass upper panel(s), like reference 4 windows per full double door
        half=(x0+x1)/2
        for wa,wb in [(x0+.16,half-.07),(half+.07,x1-.16)]:
            box(obj+'_Fensterglas','glas_blau',wa,wb,front-.27,front-.20,3.45,4.27)
            for xx in (wa,wb):box(obj+'_Fensterrahmen','holz_alt',xx-.045,xx+.045,front-.30,front-.19,3.42,4.32)
            for zz in (3.43,4.27):box(obj+'_Fensterrahmen','holz_alt',wa,wb,front-.30,front-.19,zz-.047,zz+.047)
            box(obj+'_Fensterrahmen','holz_alt',wa,wb,front-.31,front-.19,3.79,3.84)
        # handles and wrought iron strap
        box(obj+'_Tuergriffe','blech_dunkel',m-.10,m-.045,front-.34,front-.24,2.12,2.24)
        box(obj+'_Scharniere','blech_dunkel',x0+.06,x0+.3,front-.32,front-.20,1.05,1.11)
    # short arched lintel lamps over bay
    box('Leuchten_Aussen','blech_dunkel',m-.15,m+.15,-.5,-.23,5.28,5.48)
    box('Leuchten_Glas','fenster_weiss',m-.11,m+.11,-.54,-.50,5.27,5.43)
# front sign sitting below eave, little plaque with proper real text
a,b=6.55,21.82
box('Schriftzug_Fassung','holz_alt',a-.14,b+.14,-.51,-.32,5.03,5.66)
poly('Schriftzug_DORFFEUERWACHE_MUEHLBERG','schriftzug_muehlberg',[(a,-.526,5.09),(b,-.526,5.09),(b,-.526,5.61),(a,-.526,5.61)],uv=[(0,0),(1,0),(1,1),(0,1)])
# roof mounted crest front pitch, approximate roof plane z=eave+(ridge-eave)*((y+.55)/5.55)
def roof_front_z(y):return 6.15+(10.45-6.15)*(y+.55)/5.55
# make shield a pitched plane, x 12.95..14.45 y=1.6..3.5
cx=13.9; yb=1.25; yt=3.12; zoffset=.065
poly('Wappen_Freiwillige_Feuerwehr_Muehlberg','wappen_feuerwehr',[(cx-.68,yb,roof_front_z(yb)+zoffset),(cx+.68,yb,roof_front_z(yb)+zoffset),(cx+.68,yt,roof_front_z(yt)+zoffset),(cx-.68,yt,roof_front_z(yt)+zoffset)],uv=[(0,0),(1,0),(1,1),(0,1)])

# fire hose tower left; proper brick walls from every angle
box('Schlauchturm_Klinker','klinker_rot',.28,3.93,-.62,3.91,0,14.4,1.4)
box('Schlauchturm_Sockel','klinker_dunkel',.20,4.03,-.73,4.03,0,.53,1.1)
box('Schlauchturm_Rahmengesims','naturstein',.15,4.10,-.75,4.09,13.97,14.17,1.2)
# tower hipped roof eave 14.4 ridge 16.45
base=[(.04,-.86,14.40),(4.14,-.86,14.40),(4.14,4.18,14.40),(.04,4.18,14.40)]
top=(2.09,1.67,16.48)
for k in range(4):poly('Schlauchturm_Walmdach','blech_dunkel',[base[k],base[(k+1)%4],top],scale=1.6)
box('Schlauchturm_Dachspitze','blech_dunkel',2.01,2.17,1.57,1.74,16.40,16.80)
# front tower entry and four windows in front

def window_front(obj,x,y,z,w=1.05,h=1.67,flower=False):
    # window mounted in plane y (front -Y)
    box(obj+'_Brustriegel','naturstein',x-.12,x+w+.12,y-.24,y+.09,z-.15,z+.02)
    box(obj+'_Fensterrahmen','fenster_weiss',x-.08,x+w+.08,y-.20,y+.08,z,z+h)
    box(obj+'_Fensterscheiben','glas_blau',x+.035,x+w-.035,y-.235,y-.20,z+.10,z+h-.08)
    for xx in [x,x+w,x+w/2]:box(obj+'_Sprossen','fenster_weiss',xx-.045,xx+.045,y-.28,y-.19,z+.05,z+h-.05)
    for zz in [z+.05,z+h-.05,z+h*.56]:box(obj+'_Sprossen','fenster_weiss',x-.035,x+w+.035,y-.29,y-.19,zz-.035,zz+.035)
    if flower:
        box(obj+'_Blumenkaesten','holz_alt',x-.11,x+w+.11,y-.41,y-.12,z-.29,z-.10)
        for q in range(9):
            px=x+.02+q*w/9
            box(obj+'_Grun','laubwerk',px,px+.095,y-.33,y-.15,z-.08,z+.10,scale=.5)

def window_side(obj,x,y,z,w=1.00,h=1.30,flower=False,frontside='right'):
    # mounted on x=constant side facing +X if right
    dir=1 if frontside=='right' else -1
    box(obj+'_Rahmen','fenster_weiss',x-.05,x+.05,y-.08,y+w+.08,z,z+h)
    xx=x+dir*.1
    box(obj+'_Glas','glas_blau',xx-.04,xx+.04,y+.03,y+w-.03,z+.09,z+h-.08)
    for yy in [y,y+w,y+w/2]:box(obj+'_Sprossen','fenster_weiss',xx-.10,xx+.10,yy-.035,yy+.035,z,z+h)
    for zz in [z+.05,z+h-.07,z+h*.52]:box(obj+'_Sprossen','fenster_weiss',xx-.10,xx+.10,y,y+w,zz-.03,zz+.03)
    if flower:
        box(obj+'_Blumenkasten','holz_alt',xx-.12,xx+.12,y-.09,y+w+.09,z-.24,z-.1)
        for q in range(8):
            yy=y+.04+q*w/9
            box(obj+'_Pflanzen','laubwerk',xx-.06,xx+.12,yy,yy+.12,z-.1,z+.12,scale=.4)

def louvers_front(obj,x,y,z,w=.8,h=.95):
    box(obj+'_Holz_Zarge','holz_alt',x-.05,x+w+.05,y-.16,y+.06,z-.05,z+h+.05)
    box(obj+'_Schatten','fenster_dunkel',x,x+w,y-.20,y-.16,z,z+h)
    for q in range(7):box(obj+'_Lamellen','holz_alt',x+.07,x+w-.07,y-.27,y-.18,z+.1+q*.115,z+.16+q*.115)
# front tower has paired louvres top, tall windows at z8 and entrance bottom
for x in (.71,2.16):
    louvers_front('Schlauchturm_Lueftung',x,-.65,12.05,w=.92,h=1.08)
    window_front('Schlauchturm_Fenster',x-.02,-.65,7.80,w=.96,h=2.00)
# door tower
box('Schlauchturm_Tuergewand','naturstein',1.05,2.32,-.95,-.62,.37,3.06)
box('Schlauchturm_Eingang','holz_alt',1.16,2.22,-1.00,-.94,.44,2.99)
box('Schlauchturm_Tuerfenster','glas_blau',1.35,2.08,-1.06,-1.00,2.25,2.78)
box('Schlauchturm_Tuerklinke','blech_dunkel',2.04,2.13,-1.10,-1.04,1.63,1.76)
box('Schlauchturm_Stufe','naturstein',.88,2.54,-1.35,-.67,.14,.34)
# side tower: windows look deliberate not black
for z in (3.0,9.3):window_side('Schlauchturm_Seitenfenster',3.95,1.02,z,.6,1.05,frontside='right')
for z in (3.5,10.0):window_side('Schlauchturm_Rueckfenster',.27,1.05,z,.58,.9,frontside='left')
# cast iron rain downpipes on sides
for x,y0 in [(4.1,-.42),(23.88,-.44)]:
    linebox('Fallrohre','blech_dunkel',(x,y0,6.05),(x,y0,.22),.085)

# right gable 6 windows with wood flower boxes; exact side motif
for y in (1.55,4.54,7.55):
    window_side('Rechte_Giebelseite_OG',24.04,y,6.27,1.22,1.15,flower=True,frontside='right')
    window_side('Rechte_Giebelseite_EG',24.04,y,2.05,1.22,1.55,flower=True,frontside='right')
# right side roof drain
linebox('Fallrohr_rechts','blech_dunkel',(24.15,9.45,6.08),(24.15,9.45,.15),.10)
# chimney red brick
box('Schornstein_Klinker','klinker_schornstein',19.3,20.25,6.76,7.60,7.85,11.52,.55)
box('Schornstein_Deckplatte','naturstein',19.12,20.43,6.60,7.74,11.44,11.65,.55)
box('Schornstein_Oeffnung','fenster_dunkel',19.44,20.1,6.85,7.48,11.66,11.70,.8)

# small bell turret on main ridge around x ~12, with wood supports, a small visible bell
BX=12.9; BY=5.0
box('Dachreiter_Sockel','holz_alt',BX-.56,BX+.56,BY-.53,BY+.53,10.28,11.26,.7)
for xx in (BX-.41,BX+.31):
    for yy in (BY-.42,BY+.32):box('Dachreiter_Holzpfeiler','holz_alt',xx,xx+.10,yy,yy+.10,11.23,12.44)
# arch above open bell, wood crossbars
for yy in (BY-.47,BY+.40):box('Dachreiter_Riegel','holz_alt',BX-.49,BX+.51,yy,yy+.09,12.27,12.44)
# bell and bell clapper
box('Dachreiter_Glocke','naturstein',BX-.28,BX+.29,BY-.24,BY+.24,11.55,12.12,.3)
linebox('Dachreiter_Kloeppel','blech_dunkel',(BX,BY,11.50),(BX,BY,11.33),.09)
# pointed small pyramid roof
sb=[(BX-.76,BY-.72,12.48),(BX+.76,BY-.72,12.48),(BX+.76,BY+.72,12.48),(BX-.76,BY+.72,12.48)]
for k in range(4):poly('Dachreiter_Ziegeldach','dachziegel_dunkel',[sb[k],sb[(k+1)%4],(BX,BY,14.27)],scale=.4)
# weather vane at top with horizontal swallow
linebox('Wetterfahne','blech_dunkel',(BX,BY,14.25),(BX,BY,14.91),.07)
linebox('Wetterfahne','blech_dunkel',(BX-.5,BY,14.72),(BX+.46,BY,14.72),.07)
poly('Wetterfahne','blech_dunkel',[(BX+.18,BY,14.66),(BX+.58,BY,14.78),(BX+.18,BY,14.86)])
# roof ridge details chimney not front

# rear annex building (back left) reference tall gable + two levels
box('Rueckanbau_Gewaende','klinker_rot',4.35,12.35,9.80,17.0,0,4.55,1.3)
# triangular end gables at Y = 17 (roof ridge oriented Y)
poly('Rueckanbau_Giebel','klinker_rot',[(12.35,17,4.55),(4.35,17,4.55),(8.35,17,7.63)],scale=1.3)
poly('Rueckanbau_Giebel','klinker_rot',[(4.35,9.8,4.55),(12.35,9.8,4.55),(8.35,9.8,7.63)],scale=1.3)
roof_y('Rueckanbau_Ziegeldach',4.35,12.35,9.8,17.0,4.55,7.63)
box('Rueckanbau_Sockel','klinker_dunkel',4.35,12.35,9.66,17.13,0,.42)
# back gable with upstairs windows and ground windows, door
for x in (5.62,9.67):
    window_front('Rueckanbau_Giebel_Fenster',x,17.05,5.19,1.1,1.15) # orientation signs slight internal but visible
# rear facing: y positive, separate window function

def window_rear(obj,x,y,z,w=1.16,h=1.55,flower=False):
    box(obj+'_Rahmen','fenster_weiss',x-.08,x+w+.08,y-.1,y+.12,z,z+h)
    box(obj+'_Glas','glas_blau',x+.02,x+w-.02,y+.12,y+.19,z+.07,z+h-.06)
    for xx in (x,x+w,x+w/2):box(obj+'_Sprossen','fenster_weiss',xx-.04,xx+.04,y+.12,y+.23,z,z+h)
    for zz in (z+.04,z+h-.04,z+.57*h):box(obj+'_Sprossen','fenster_weiss',x,x+w,y+.13,y+.23,zz-.04,zz+.04)
    box(obj+'_Fensterbank','naturstein',x-.14,x+w+.14,y-.1,y+.36,z-.16,z-.05)
    if flower:
        box(obj+'_Blumenkasten','holz_alt',x-.08,x+w+.08,y+.27,y+.47,z-.28,z-.12)
        for i in range(8):box(obj+'_Gruen','laubwerk',x+i*w/8,x+(i+.7)*w/8,y+.30,y+.48,z-.10,z+.08)
for x in (5.55,10.02):window_rear('Rueckanbau_Hinten_Fenster',x,17.05,2.19,1.12,1.55)
# door at rear gable center
box('Rueckanbau_Eingang_Zarge','naturstein',8.10,9.62,17.03,17.27,.34,2.76)
box('Rueckanbau_Holztuer','holz_alt',8.21,9.52,17.23,17.29,.45,2.64)
box('Rueckanbau_Tuerglas','glas_blau',8.48,9.29,17.28,17.35,2.12,2.52)
box('Rueckanbau_Griff','blech_dunkel',9.28,9.37,17.35,17.46,1.36,1.51)
box('Rueckanbau_Stufe','naturstein',7.95,9.80,17.22,17.75,.17,.33)
# back main facade doors windows and flower boxes (beyond annex)
for x in (13.22,17.82,21.34):window_rear('Hauptbau_Rueckfenster',x,10.05,2.26,1.32,1.45)
for x in (15.19,20.15):
    box('Hauptbau_Ruecktueren_Zargen','naturstein',x-.10,x+1.18,10.04,10.31,.32,2.74)
    box('Hauptbau_Ruecktueren_Holz','holz_alt',x,x+1.08,10.28,10.35,.41,2.64)
    box('Hauptbau_Ruecktueren_Glas','glas_blau',x+.18,x+.88,10.35,10.41,2.12,2.51)
    box('Hauptbau_Ruecktueren_Griffe','blech_dunkel',x+.88,x+.98,10.41,10.51,1.5,1.6)
for x in (14,20.7):window_rear('Hauptbau_Rueckfenster_oben',x,10.05,4.65,1.18,1.08)
# rear roof dormer towards y positive
box('Dachgaube_Wand','klinker_rot',16.24,19.03,7.67,9.65,8.02,8.85)
for x in (16.45,17.67):window_rear('Dachgaube_Fenster',x,9.70,8.24,1.04,.75)
# small gable roof on dormer ridge toward y, show rear
roof_y('Dachgaube_Dach',16.2,19.08,7.5,9.7,8.81,9.86)
# rectangular skylight on back pitch near x11.8
poly('Rueckdach_Fenster','glas_blau',[(12.2,7.76,8.39),(13.17,7.76,8.39),(13.17,8.67,7.63),(12.2,8.67,7.63)],scale=.45)
# ground details: pale stone front area, side compact step to rear
box('Hof_Flaeche_Pflaster','hofpflaster',3.4,24.4,-5.6,-.8,-.16,-.025,1.8)
box('Rueckanbau_Trittstein','hofpflaster',4.0,12.65,17.05,18.25,-.15,-.04,1.6)
# dividing slab seams embedded surface
for i in range(4):
    x=5.04+i*6.0
    box('Hof_Pflasterlaengsfugen','ziegel_fuge',x,x+.035,-5.6,-.9,-.023,-.020)
# stone workshop scene at back (log pile, green crates, ladder)
for i in range(9):
    r=i%3;c=i//3
    box('Rueckseite_Holzstapel','holz_alt',22.65+c*.23,22.86+c*.23,10.53+r*.13,10.78+r*.13,.1,.94)
for i in range(4):box('Rueckseite_Pflanzkuebel','holz_alt',13.1+i*.58,13.49+i*.58,10.65,11.04,.14,.63)
for i in range(12):
    px=13.05+i*.18
    box('Rueckseite_Begruenung','laubwerk',px,px+.17,10.71,11.11,.62,.93,scale=.4)
# ladder rests on rear facade right
for xx in (23.09,23.48):
    linebox('Anstellleiter_Seitenteil','holz_alt',(xx,11.44,.14),(xx,10.3,5.16),.08)
for j in range(12):
    z=.45+j*.36
    y=11.36-(z-.14)/(5.16-.14)*1.14
    linebox('Anstellleiter_Sprosse','holz_alt',(23.09,y,z),(23.48,y,z),.06)
# discreet side wall annex on right low lean-to as shown in side view
box('Seitenanbau_Putz','putz_hell',23.97,26.00,7.95,10.0,0,2.75,1.3)
poly('Seitenanbau_Pultdach','dachziegel_dunkel',[(23.9,7.82,3.18),(26.16,7.82,2.61),(26.16,10.2,2.61),(23.9,10.2,3.18)],scale=.8)
window_side('Seitenanbau_Fenster',26.0,8.45,1.19,.70,.97,frontside='right')

# small discrete paving around side/tower, boundary foundation
box('Turm_Vorplatz','hofpflaster',-.45,4.1,-2.45,-.75,-.14,-.04,1.5)
box('Rueckseite_Boden','hofpflaster',4.1,24.4,10.08,10.78,-.14,-.04,1.5)
# Export OBJ with strictly valid 1-based vertex and UV indices, per-object material batching
obj_path=os.path.join(OUT,'Dorffeuerwache_Muehlberg_nach_Zeichnung.obj')
mtl_path=os.path.join(OUT,'Dorffeuerwache_Muehlberg_nach_Zeichnung.mtl')
with open(mtl_path,'w',encoding='utf-8') as f:
    f.write('# Native external JPG/PNG materials for Blender 2.93 OBJ import\n')
    for key,filename in MATS.items():
        f.write(f'newmtl {key}\nKa 0.15 0.15 0.15\nKd 1.0 1.0 1.0\nKs 0.08 0.08 0.08\nNs 6.0\nd 1.0\nillum 2\nmap_Kd {filename}\n\n')
by_obj=collections.defaultdict(lambda:collections.defaultdict(list))
for obj,mat,pts,uvs in facets:by_obj[obj][mat].append((pts,uvs))
nv=0;nt=0
with open(obj_path,'w',encoding='utf-8',newline='\n') as f:
    f.write('# Dorffeuerwache Muehlberg from reference drawing\n# meters, Z up, main front faces negative Y\n')
    f.write('mtllib Dorffeuerwache_Muehlberg_nach_Zeichnung.mtl\n')
    for obj,mats in by_obj.items():
        f.write(f'o {obj}\n')
        for mat,geometry in mats.items():
            f.write('usemtl '+mat+'\n')
            for pts,uvs in geometry:
                for p in pts:f.write('v %.6f %.6f %.6f\n'%tuple(p))
                for uv in uvs:f.write('vt %.6f %.6f\n'%tuple(uv))
                f.write('f %d/%d %d/%d %d/%d\n'%(nv+1,nt+1,nv+2,nt+2,nv+3,nt+3))
                nv+=3;nt+=3
# Validator UV range + linked image references
with open(obj_path,encoding='utf-8') as f:
    counter=collections.Counter()
    for line in f:
        k=line.split(' ',1)[0];counter[k]+=1
        if k=='f':
            for token in line.split()[1:]:
                v,t=map(int,token.split('/'))
                assert v>0 and t>0
    assert counter['v']==counter['vt']==counter['f']*3
print('OBJ',len(by_obj),'objects,',len(facets),'triangles,',len(MATS),'textures',os.path.getsize(obj_path)//1024,'KiB')
# convert: keep file with embedded texture images, group geometry by material
try:
    scene=trimesh.load(obj_path,force='scene',process=False,maintain_order=True)
    assert len(scene.geometry)>0
    glb=os.path.join(OUT,'Dorffeuerwache_Muehlberg_nach_Zeichnung.glb')
    scene.export(glb)
    test=trimesh.load(glb,force='scene')
    print('GLB size',os.path.getsize(glb),'geometries',len(test.geometry),'bounds',test.bounds)
except Exception as e:
    print('GLB conversion error',str(e))
    raise
readme='''DORFFEUERWACHE MÜHLBERG - 3D-MODELL NACH DER VORLAGE
======================================================
Neu aufgebaute Außenansicht anhand der vom Nutzer bereitgestellten Zeichnung.

Enthalten:
- .obj + .mtl + PNG Texturen (Blender 2.93 Import)
- .glb mit eingebetteten Texturen (3D-Viewer / Blender glTF Import)

Maße in Metern, angenähert: Frontbreite ~24 m, Hauptbau bis Dachfirst ~10,5 m,
Schlauchturm ~16,5 m, rückwärtiger Anbau ~7,6 m hoch.

Geometrische und gestalterische Details: drei zweiflügelige rote Holztore mit
Glaseinsätzen, rote Klinkerfassade, seitlicher gemauerter Schlauchturm mit
Walmdach, Fenster mit Sprossen, braunes Dachziegelmuster, Dachreiter,
Dachwappen, Frontschriftzug, Fenster und Blumenkästen auf der rechten
Giebelseite, rückwärtiges zweigeschossiges Nebengebäude, Türen, Dachgaube.

BLENDER 2.93:
  Datei > Importieren > Wavefront (.obj) > ...nach_Zeichnung.obj
  oder Datei > Importieren > glTF 2.0 > ...nach_Zeichnung.glb
  Danach oben rechts die Materialvorschau einschalten.
  OBJ, MTL und alle PNGs beim Import zusammen im selben Ordner lassen.

GEGENÜBER DER ZEICHNUNG:
  Dies ist eine Interpretation anhand einer Illustration, KEINE exakte
  technische Rekonstruktion. Die Bemaßungen im Plan sind teils nicht
  eindeutig. Details sind angenähert und an mehreren Stellen ergänzt.
  Es gibt KEINE modellierten Innenräume, beweglichen Tore oder LS19-Kollisionen.

GIANTS EDITOR 8 / LS19:
  Dies ist KEINE fertige i3d und KEIN im Spiel platzierbarer Mod.
  Für I3D sind passender Blender-Exporter/FBX-Weg und Materialzuweisungen
  sowie später Kollisionen und XML für das Spiel erforderlich.

Rückseiten und Turmaußenwände sind jetzt mit eigenständigem Material versehen.
Die OBJ-Datei verwendet gültige, durchgängig 1-basierte UV-Indizes.
'''
with open(os.path.join(OUT,'BITTE_LESEN.txt'),'w',encoding='utf-8') as f:f.write(readme)
zip_path=os.path.join(os.getcwd(),'Dorffeuerwache_Muehlberg_Nach_Zeichnung_3D.zip')
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for filename in sorted(os.listdir(OUT)):
        z.write(os.path.join(OUT,filename),arcname='Dorffeuerwache_Muehlberg/'+filename)
print('ZIP',os.path.getsize(zip_path),zip_path)
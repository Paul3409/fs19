# LF 20 | Materialien und Zusatzdetails | Blender 2.93
# Ausfuehren: Scripting > Text Editor > Open > Run Script (Alt+P)
# Fuer das zuvor importierte LF20_MAN_LowPoly_3D_Vorschau.glb
import bpy
import math

COLLECTION_NAME = 'LF20_Zusatzdetails'
old = bpy.data.collections.get(COLLECTION_NAME)
if old:
    for ob in list(old.objects):
        bpy.data.objects.remove(ob, do_unlink=True)
    bpy.data.collections.remove(old)
col = bpy.data.collections.new(COLLECTION_NAME)
bpy.context.scene.collection.children.link(col)

def material(name, hexcolor, metal=0, rough=0.5, emission=0):
    mat = bpy.data.materials.get('LF20_'+name) or bpy.data.materials.new('LF20_'+name)
    code = hexcolor.lstrip('#')
    rgb = [int(code[i:i+2],16)/255 for i in (0,2,4)]
    def linear(v):
        return v/12.92 if v < 0.04045 else ((v+0.055)/1.055)**2.4
    rgba = tuple(linear(v) for v in rgb)+(1,)
    mat.diffuse_color = rgba
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = rgba
        bsdf.inputs['Metallic'].default_value = metal
        bsdf.inputs['Roughness'].default_value = rough
        if emission:
            bsdf.inputs['Emission'].default_value = rgba
            bsdf.inputs['Emission Strength'].default_value = emission
    return mat

m = {
    'rot':material('Feuerwehrrot','C5101B',0,.32),
    'rot_dunkel':material('Rot_Dunkel','9D1016',0,.4),
    'schwarz':material('Gummi_Schwarz','15191D',0,.86),
    'anthrazit':material('Kunststoff','292E32',0,.62),
    'fenster':material('Scheiben_Dunkel','253F51',.15,.15),
    'silber':material('Rolladen_Silber','A4AAB0',.6,.32),
    'chrom':material('Chrom','C7CED0',.8,.2),
    'weiss':material('Weiss','EDEDE9',0,.4),
    'gelb':material('Reflex_Gelb','F2DE37',0,.35),
    'blau':material('Blaulicht_Blau','125DFF',0,.19,.6),
    'orange':material('Blinker_Orange','F38A18',0,.21,.25),
    'ruecklicht':material('Ruecklicht_Rot','DF2019',0,.25,.2),
}

def match_material(name):
    n=name.lower()
    if 'roller' in n:
        return m['anthrazit'] if any(t in n for t in ('slat','bottom','handle')) else m['silber']
    if 'tire' in n: return m['schwarz']
    if 'lug' in n or 'hub' in n: return m['anthrazit']
    if 'rim' in n or 'ladder' in n or 'step' in n or 'badge' in n or 'trim' in n: return m['chrom']
    if 'window' in n or 'windshield' in n or 'glass' in n: return m['fenster']
    if 'yellow' in n: return m['gelb']
    if 'reflective' in n or 'headlight' in n: return m['weiss']
    if 'blue' in n: return m['blau']
    if 'marker' in n: return m['orange']
    if 'rear lamp' in n: return m['ruecklicht']
    if 'roof' in n and 'blue' not in n: return m['rot_dunkel']
    if any(t in n for t in ('grille','bumper','chassis','arch','mirror','arm','pillar','handle')): return m['anthrazit']
    if any(t in n for t in ('front cabin','body','door','skirt')): return m['rot']
    if 'feuerwehr' in n or 'rear 112' in n: return m['weiss']
    return None

changed=0
for obj in bpy.data.objects:
    if obj.type != 'MESH' or obj.name.startswith('LF20plus_'): continue
    mat=match_material(obj.name)
    if mat:
        obj.data.materials.clear()
        obj.data.materials.append(mat)
        changed+=1

def link_to_col(ob):
    for c in list(ob.users_collection): c.objects.unlink(ob)
    col.objects.link(ob)
    return ob

def cube(name,loc,scale,mat,bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    ob=link_to_col(bpy.context.object)
    ob.name='LF20plus_'+name
    ob.dimensions=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    ob.data.materials.append(mat)
    if bevel:
        mod=ob.modifiers.new('Weiche Kanten','BEVEL')
        mod.width=bevel; mod.segments=2
        ob.modifiers.new('Normals','WEIGHTED_NORMAL')
    return ob

def cyl(name,loc,radius,depth,mat,axis='Y',vertices=16):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth,location=loc)
    ob=link_to_col(bpy.context.object)
    ob.name='LF20plus_'+name
    if axis=='Y': ob.rotation_euler[0]=math.pi/2
    elif axis=='X': ob.rotation_euler[1]=math.pi/2
    ob.data.materials.append(mat)
    return ob

def label(name,text,loc,size,mat,side='front'):
    curve=bpy.data.curves.new('LF20_'+name,'FONT')
    curve.body=text; curve.align_x='CENTER'; curve.align_y='CENTER'
    curve.size=size; curve.extrude=.001
    ob=bpy.data.objects.new('LF20plus_'+name,curve)
    col.objects.link(ob); ob.location=loc
    if side=='front': ob.rotation_euler=(math.pi/2,0,-math.pi/2)
    elif side=='left': ob.rotation_euler=(math.pi/2,0,math.pi)
    elif side=='right': ob.rotation_euler=(math.pi/2,0,0)
    elif side=='rear': ob.rotation_euler=(math.pi/2,0,math.pi/2)
    ob.data.materials.append(mat)
    return ob

for side in (-1,1):
    cube('Trittstufe_'+str(side),(-1.72,side*1.32,1.08),(.52,.28,.09),m['anthrazit'],.025)
    for x in (-2.30,-1.43):
        cube('Griff_'+str(side)+'_'+str(x),(x,side*1.257,1.81),(.20,.035,.045),m['anthrazit'],.01)
    cube('Spiegelglas_'+str(side),(-3.18,side*1.523,2.48),(.145,.009,.29),m['chrom'],.015)
    for x in (-2.34,2.42):
        cyl('Radnabenring_'+str(side)+'_'+str(x),(x,side*1.445,.69),.195,.014,m['chrom'])
    for x in (-.6,1.55,3.28):
        cube('Marker_'+str(side)+'_'+str(x),(x,side*1.29,1.01),(.18,.028,.075),m['orange'],.012)
    for x in (-.45,1.0,2.45):
        cube('Kastenlicht_'+str(side)+'_'+str(x),(x,side*1.245,3.02),(.25,.04,.13),m['weiss'],.025)
    label('Schrift_Feuerwehr_'+str(side),'FEUERWEHR',(1.25,side*1.307,1.05),.18,m['weiss'],'right' if side<0 else 'left')
    label('Notruf_'+str(side),'112',(3.08,side*1.306,1.09),.16,m['weiss'],'right' if side<0 else 'left')

for z in (1.29,1.40,1.51,1.62):
    cube('Grillstrebe_'+str(z),(-3.418,0,z),(.026,1.37,.024),m['schwarz'])
for side in (-1,1):
    wiper=cube('Scheibenwischer_'+str(side),(-3.386,side*.48,1.88),(.035,.78,.025),m['schwarz'])
    wiper.rotation_euler[0]=side*.12
cube('Lichtbalken_Basis',(-2.67,0,3.18),(.40,2.02,.11),m['anthrazit'],.045)
for side in (-1,1):
    cube('Lichtbalken_Blitz_'+str(side),(-2.68,side*.73,3.27),(.34,.47,.18),m['blau'],.04)
    for i in range(3):
        cube('Lichtbalken_LED_'+str(side)+'_'+str(i),(-2.862,side*(.60+i*.13),3.27),(.015,.07,.09),m['weiss'])
    cyl('Martinshorn_'+str(side),(-2.55,side*.24,3.30),.10,.29,m['anthrazit'],axis='X')
cube('Dachkasten',(2.5,-.67,3.36),(.85,.43,.23),m['anthrazit'],.03)
for x in (.2,1.1,2.0):
    cube('Dachtritt_'+str(x),(x,.84,3.24),(.38,.28,.045),m['silber'])
label('Heck_Notruf','112',(3.725,0,2.25),.34,m['weiss'],'rear')
label('Front_Feuerwehr','FEUERWEHR',(-3.407,0,1.96),.24,m['weiss'],'front')
label('Front_MAN','MAN',(-3.452,0,1.45),.13,m['chrom'],'front')

for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        area.spaces.active.shading.type='MATERIAL'
print('LF20 fertig: %d bestehende Objekte eingefaerbt, %d Zusatzobjekte erstellt.'%(changed,len(col.objects)))

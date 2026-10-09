"""Regenerate all printable meshes and 3MF. Requires numpy, shapely, trimesh,
mapbox-earcut, manifold3d, scipy, matplotlib. Usage: python build.py --thickness 1.5
Units are millimetres. SCAD edits are independent; JSON is this builder's source.
"""
import argparse,json,csv,zipfile,hashlib,xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
import trimesh,manifold3d
from shapely.geometry import Polygon
from shapely.affinity import translate
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent.parent
NS='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
ET.register_namespace('',NS)
def elem(parent,tag,attrs=None):return ET.SubElement(parent,'{'+NS+'}'+tag,attrs or {})
def save_3mf(meshes,poses,path):
 model=ET.Element('{'+NS+'}model',{'unit':'millimeter','{http://www.w3.org/XML/1998/namespace}lang':'en-US'})
 elem(model,'metadata',{'name':'Title'}).text='RC Bionic Butterfly - reconstructed flat parts, 1.5 mm'
 resources=elem(model,'resources');build=elem(model,'build')
 for i,(name,m) in enumerate(meshes,1):
  obj=elem(resources,'object',{'id':str(i),'type':'model','name':name});mesh=elem(obj,'mesh');v=elem(mesh,'vertices');t=elem(mesh,'triangles')
  for p in m.vertices:elem(v,'vertex',dict(zip(('x','y','z'),[f'{x:.7f}' for x in p])))
  for f in m.faces:elem(t,'triangle',dict(zip(('v1','v2','v3'),map(str,f))))
  x,y=poses[i-1];elem(build,'item',{'objectid':str(i),'transform':f'1 0 0 0 1 0 0 0 1 {x} {y} 0'})
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
  z.writestr('[Content_Types].xml','<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
  z.writestr('_rels/.rels','<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
  z.writestr('3D/3dmodel.model',ET.tostring(model,encoding='utf-8',xml_declaration=True))
def svg(p,name):
 x0,y0,x1,y1=p.bounds
 rings=[p.exterior,*p.interiors]
 path=' '.join('M '+' L '.join(f'{x:.4f},{y1-y:.4f}' for x,y in ring.coords)+' Z' for ring in rings)
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="{x1:.4f}mm" height="{y1:.4f}mm" viewBox="0 0 {x1:.4f} {y1:.4f}"><title>{name}</title><path d="{path}" fill="#2b8c98" fill-rule="evenodd"/></svg>'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--thickness',type=float,default=1.5);ap.add_argument('--hole-clearance',type=float,default=0,help='total added cutout width; open slots excluded');a=ap.parse_args();assert a.thickness>0
 data=json.loads((ROOT/'cad/profiles.json').read_text());layout=json.loads((ROOT/'cad/layout.json').read_text());poses=layout['positions']
 meshes=[];polys=[];report=[];features=[]
 for idx,part in enumerate(data['parts']):
  outer=Polygon(part['outer']);holes=[Polygon(h).buffer(a.hole_clearance/2,join_style='mitre') if a.hole_clearance else Polygon(h) for h in part['holes']]
  p=outer
  for h in holes:p=p.difference(h)
  assert p.is_valid and p.geom_type=='Polygon' and len(p.interiors)==len(holes),'Cutouts invalid or split solid'
  m=trimesh.creation.extrude_polygon(p,a.thickness,engine='earcut');name=part['name'];target=ROOT/'stl'/f'{name}.stl';m.export(target)
  # Validate the actual serialized STL, not only the in-memory construction.
  m=trimesh.load_mesh(target,process=True)
  edge_counts=np.bincount(m.edges_unique_inverse);mn=manifold3d.Manifold(manifold3d.Mesh(np.asarray(m.vertices,dtype=np.float32),np.asarray(m.faces,dtype=np.uint32)))
  expected=p.area*a.thickness;err=abs(m.volume-expected)/expected
  assert m.is_watertight and m.is_winding_consistent and m.is_volume and np.all(edge_counts==2)
  assert len(m.split())==1 and np.min(m.area_faces)>1e-10 and err<1e-5
  assert str(mn.status())=='Error.NoError' and m.euler_number==2-2*len(holes)
  min_web=min(h.distance(outer.exterior) for h in holes);min_hh=min((h.distance(k) for i,h in enumerate(holes) for k in holes[i+1:]),default=None)
  for j,h in enumerate(holes):
   r=np.array(h.minimum_rotated_rectangle.exterior.coords);dims=np.linalg.norm(np.diff(r,axis=0),axis=1)
   features.append({'part':name,'hole_index':j,'center_x_mm':h.centroid.x,'center_y_mm':h.centroid.y,'short_extent_mm':min(dims),'long_extent_mm':max(dims),'area_mm2':h.area,'web_to_outer_mm':h.distance(outer.exterior)})
  report.append({'part':name,'size_mm':m.extents.tolist(),'holes':len(holes),'volume_mm3':float(m.volume),'watertight':bool(m.is_watertight),'winding_consistent':bool(m.is_winding_consistent),'single_connected_solid':True,'each_edge_two_faces':True,'manifold3d_status':str(mn.status()),'euler_characteristic':int(m.euler_number),'min_triangle_area_mm2':float(min(m.area_faces)),'volume_relative_error':float(err),'min_hole_to_outer_web_mm':min_web,'min_hole_to_hole_web_mm':min_hh})
  (ROOT/'profiles'/f'{name}.svg').write_text(svg(p,name));polys.append(p);meshes.append((name,m))
 save_3mf(meshes,poses,ROOT/'butterfly_plate.3mf')
 # Validate the archive's units, object names, mesh counts, transforms, and geometry after readback.
 with zipfile.ZipFile(ROOT/'butterfly_plate.3mf') as z:
  assert z.testzip() is None;model=ET.fromstring(z.read('3D/3dmodel.model'));assert model.attrib['unit']=='millimeter'
  objs=model.findall('{'+NS+'}resources/{'+NS+'}object');items=model.findall('{'+NS+'}build/{'+NS+'}item');assert len(objs)==len(items)==13
  for obj,item,(name,m),pos in zip(objs,items,meshes,poses):
   verts=np.array([[float(v.attrib[k]) for k in ['x','y','z']] for v in obj.findall('.//{'+NS+'}vertex')]);faces=np.array([[int(f.attrib[k]) for k in ['v1','v2','v3']] for f in obj.findall('.//{'+NS+'}triangle')]);rt=trimesh.Trimesh(verts,faces,process=True)
   assert obj.attrib['name']==name and rt.is_volume and rt.is_watertight and np.allclose(rt.extents,m.extents)
   assert list(map(float,item.attrib['transform'].split()))[-3:]==[*pos,0]
 placed=[translate(p,*pos) for p,pos in zip(polys,poses)];gap=min(p.distance(q) for i,p in enumerate(placed) for q in placed[i+1:]);assert gap>2.999
 bounds=[min(p.bounds[0] for p in placed),min(p.bounds[1] for p in placed),max(p.bounds[2] for p in placed),max(p.bounds[3] for p in placed)];assert bounds[2]<=220 and bounds[3]<=220
 validation={'units':'mm','thickness_mm':a.thickness,'enclosed_cutout_clearance_diameter_mm':a.hole_clearance,'parts':report,'build_plate':{'bed_mm':[220,220],'occupied_bounds_mm':bounds,'minimum_part_gap_mm':gap,'part_intersections':0,'3mf_readback_passed':True},'limits':['Static flat-profile geometry only; assembly locations and moving clearances absent from PDF.','No flight, strength, fatigue, or physical printer-fit validation.','Open edge slots are preserved; hole-clearance parameter does not change edge slots.']}
 (ROOT/'validation.json').write_text(json.dumps(validation,indent=2))
 with open(ROOT/'feature_measurements.csv','w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(features[0]));w.writeheader();w.writerows(features)
 fig,ax=plt.subplots(figsize=(9,9))
 for idx,p in enumerate(placed):
  ax.fill(*np.array(p.exterior.coords).T,color='#94d3d6',ec='#155d68',lw=.7)
  for h in p.interiors:ax.fill(*np.array(h.coords).T,color='white',ec='#155d68',lw=.7)
  c=p.representative_point();ax.text(c.x,c.y,str(idx+1),ha='center',fontsize=10,fontweight='bold')
 ax.set(xlim=(0,220),ylim=(0,220),xlabel='mm',ylabel='mm',title=f'13 separate parts | thickness {a.thickness:g} mm | 220 x 220 mm bed');ax.set_aspect('equal');ax.grid(alpha=.15);fig.tight_layout();fig.savefig(ROOT/'plate_preview.png',dpi=160);plt.close(fig)
 print(json.dumps({'parts':13,'holes_total':sum(x['holes'] for x in report),'all_meshes_valid':True,'bounds_mm':bounds,'min_plate_gap_mm':gap,'thickness_mm':a.thickness}))
if __name__=='__main__':main()

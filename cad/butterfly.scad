// RC Bionic Butterfly: editable vector reconstruction, not a verified assembly.
include <profiles.scad>

// Choose -1 to display all 13 parts, or a part index 0..12.
part_index = -1;
layout = "plate"; // "plate" or "source"
thickness = 1.5; // original drawing: 1.5 mm plywood
thickness_overrides = []; // example [[0,2.0],[1,2.0]]; [part index, mm]
scale_xy = [1,1]; // scales outlines AND feature positions
hole_clearance_diameter = 0; // adds this amount to cutout width, both sides total
hole_edits = []; // [part index,hole index,dx,dy,sx,sy], dimensions in mm
// Example hole_edits = [[7,0,0,0,1.2,1.2]]; scales one hole about its center.
// Open edge slots and integral tabs belong to outer_profiles in profiles.scad.
// Increasing thickness does NOT widen those edge slots automatically.
$fn = 96;
function th(i) = let(v=[for(a=thickness_overrides) if(a[0]==i) a[1]]) len(v)>0 ? v[0] : thickness;
function he(i,j) = let(v=[for(a=hole_edits) if(a[0]==i && a[1]==j) a]) len(v)>0 ? v[0] : [i,j,0,0,1,1];
module profile(i) {
 difference() {
  polygon(outer_profiles[i]);
  for(j=[0:len(hole_profiles[i])-1]) let(c=hole_centers[i][j],e=he(i,j))
   translate([c[0]+e[2],c[1]+e[3]]) scale([e[4],e[5]])
    offset(delta=hole_clearance_diameter/2) translate([-c[0],-c[1]]) polygon(hole_profiles[i][j]);
 }
}
module part(i) {
 assert(th(i)>0,"Thickness must be positive");
 scale([scale_xy[0],scale_xy[1],1]) linear_extrude(height=th(i),convexity=20) profile(i);
}
if(part_index>=0) {assert(part_index<13,"Index must be 0..12");part(part_index);}
else for(i=[0:12]) translate(layout=="source" ? source_origins[i] : plate_positions[i]) part(i);

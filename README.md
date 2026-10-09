# RC Bionic Butterfly - PDF profile reconstruction

13 separate STL parts, a generic millimetre-based 3MF build plate, and editable OpenSCAD source. Default thickness: **1.5 mm**, matching the drawing's material note. This package reconstructs the supplied flat cutting profiles; the functional mechanism and flight performance have not been verified.

## Downloads

- [Complete printable package](rc_bionic_butterfly_printable_files.zip): all 13 STLs, editable CAD, profiles, measurements, and validation.
- [Build plate 3MF](butterfly_plate.3mf)
- [Editable OpenSCAD model](cad/butterfly.scad) and [required profile data](cad/profiles.scad)
- [Individual STL files](stl/)
- [Validation report](validation.json)
- [Source profile map](source_profile_map.png) and [plate preview](plate_preview.png)

The complete ZIP preserves the original generated package. The unpacked files below are also available directly in this repository.

## Open the files

- `butterfly_plate.3mf`: 13 named objects, lying flat at Z=0 on a 220 x 220 mm bed. This is a standard geometry/build-layout 3MF, without proprietary slicer profiles or machine settings.
- `stl/`: one binary STL per separate source part, lower-left bounds at X=Y=0, base at Z=0. **Import STLs in millimetres**; STL itself has no units.
- `cad/butterfly.scad`: open in OpenSCAD alongside `profiles.scad`. `part_index=-1` displays all parts; indices 0..12 select one part for STL export. Indices are one less than the displayed part number.
- `cad/profiles.json`: editable polygon coordinates and feature positions used by the Python builder. Polygon vertices are a reconstruction of the vector contours, not fully dimension-constrained sketches.
- `profiles/`: separate millimetre-scale SVG profiles, with holes preserved.
- `source_profile_map.png`: numbered profile map with recovered geometry over the PDF's red vectors; numbers are visual labels only and are not embossed on the printable parts.
- `plate_preview.png`: numbered layout preview. `feature_measurements.csv`: local CAD coordinates, dimensions and web measurements for every enclosed cutout.
- `dimension_checks.csv`: all eight dimension labels compared to their source vector reference endpoints. `validation.json`: exported-mesh checks, plate checks, slit measurements and provenance.

## Source inspection and reconstruction

Source: `Dimension_Main_fram.pdf`, one A4 page, heading "RC Bionic Butterfly", attributed in the page to truongvansu91 / S-DiY channel. The PDF is a vector cutting layout on a dimensioned 145 x 175 mm sheet and says "1.5mm plywood". It contains no assembly drawing, part numbers, hardware list or kinematic instructions. Names such as body, mounting plate, bracket and fork are descriptive shape labels; they do not establish the manufacturer's intended function.

The eight printed dimensions are 145.00, 175.00, 41.64, 172.02, 24.20, 74.09, 48.92 and 26.23 mm. All vector reference measurements agree within 0.01 mm. Some dimensions refer to specific oblique stations or reference spans, **not maximum axis-aligned bounds**: the body is about 42.332 mm at its widest point although the indicated width station is 41.64 mm; the small plates' maximum Y extent is about 26.916 mm although the indicated span is 26.23 mm. The recovered contours are not rescaled to force these bounding boxes to match a differently defined dimension.

The calibrated scale is 0.352777711 mm/PDF point in X and 0.352777772 in Y. Red cutting vectors were extracted; title, text, blue dimensions and black sheet frame were excluded. Cubics were adaptively tessellated to 0.002 mm chord tolerance. Repeated and slightly drifting duplicate strokes were consolidated. Endpoints within 0.08 mm were clustered, with maximum actual endpoint movement 0.02891 mm. Adjacent duplicate-stroke slivers smaller than 0.3 mm^2 were merged into the external boundary; duplicate dangling strokes were excluded. Final outlines were simplified at 0.003 mm tolerance and rounded to 0.0001 mm coordinates. These are explicit cleanup assumptions, particularly at shared endpoints and tab edges; they are not a manufacturing tolerance guarantee.

The PDF's curves, undimensioned outlines and cutout positions were retained rather than replaced with guessed circles, ideal symmetry or invented missing assembly parts. Paired profiles remain separate and retain source differences. Y is flipped from page-down coordinates to CAD-up coordinates; X is unchanged, preserving handedness. Each outline was extruded normally through Z.

## Part inventory

All parts below are 1.5 mm thick. A quantity of one per outline is supplied, giving 13 parts in total; no hidden or additional copies are assumed.

| Map number | STL | XY bounds in mm | Enclosed cutouts |
| --- | --- | --- | --- |
| 01 | [01_body_profile.stl](stl/01_body_profile.stl) | 42.332 x 172.021 | 9 |
| 02 | [02_mounting_plate.stl](stl/02_mounting_plate.stl) | 46.212 x 74.093 | 10 |
| 03 | [03_fork_plain_right.stl](stl/03_fork_plain_right.stl) | 32.370 x 49.470 | 1 |
| 04 | [04_fork_plain_left.stl](stl/04_fork_plain_left.stl) | 32.370 x 49.470 | 1 |
| 05 | [05_fork_slotted_right.stl](stl/05_fork_slotted_right.stl) | 32.881 x 49.363 | 1 |
| 06 | [06_fork_slotted_left.stl](stl/06_fork_slotted_left.stl) | 32.881 x 49.363 | 1 |
| 07 | [07_side_bracket_lower.stl](stl/07_side_bracket_lower.stl) | 18.681 x 35.000 | 2 |
| 08 | [08_side_bracket_upper.stl](stl/08_side_bracket_upper.stl) | 18.681 x 35.000 | 2 |
| 09 | [09_three_hole_strip.stl](stl/09_three_hole_strip.stl) | 8.000 x 35.045 | 3 |
| 10 | [10_four_hole_plate_bottom_right.stl](stl/10_four_hole_plate_bottom_right.stl) | 10.175 x 26.916 | 4 |
| 11 | [11_four_hole_plate_top_left.stl](stl/11_four_hole_plate_top_left.stl) | 10.175 x 26.916 | 4 |
| 12 | [12_four_hole_plate_bottom_left.stl](stl/12_four_hole_plate_bottom_left.stl) | 10.175 x 26.916 | 4 |
| 13 | [13_four_hole_plate_top_right.stl](stl/13_four_hole_plate_top_right.stl) | 10.175 x 26.916 | 4 |

The body has four 1.6 x 4 mm rectangular slots, one 1.6 x 5 mm slot, two small elliptical holes and two longer elliptical cutouts. The broad plate has four oblong slots, an approximately 15.87 x 13.32 mm elliptical opening, four 1.6 x 4 mm slots and one 1.5 x 5 mm slot. The two brackets have integral tabs, a side semicircular notch and two approximately 1 mm holes each. The strip has end tabs and three oval holes. Each fork has a roughly 4 x 7 mm rectangular cutout; the two slotted forks additionally have four open edge slits each. Each small plate has a lateral tab and four approximately 1 mm holes at roughly 3 mm pitch. Exact sampled coordinates and individual measurements are in the source and CSV.

## Connections and clearances

Tab/slot joining is suggested by the integral tabs and narrow rectangular cutouts. Small round holes may be fastener or pivot holes; oval openings may be mounting or clearance features. These functions are **inferences from geometry**, not documented assembly instructions. The PDF does not establish which tab goes in which slot, which face is outward, or which hole is a moving joint.

- Enclosed narrow slots are approximately **1.5 or 1.6 mm wide**. Against a perpendicular 1.5 mm sheet these give nominal thickness clearances of **0 or +0.1 mm total**. Some 4 and 5 mm slot lengths equal corresponding tab spans, leaving essentially zero longitudinal clearance if those features are paired.
- All eight open edge slits in the two slotted forks measure approximately **1.4 mm**. If they receive 1.5 mm sheet material, nominal clearance is **-0.1 mm**, an interference fit. Their intended mate is unspecified: no widening is silently applied. Source plywood/laser-fit behavior cannot be assumed for printed plastic.
- A 2 mm thickness would produce nominal interference of **0.4-0.6 mm** against 1.4-1.6 mm openings unless mating geometry is revised.
- The smallest measured hole-to-outer web is **1.164 mm**, at a side-bracket hole. The smallest measured hole-to-hole web is **1.765 mm**, on the three-hole strip. These are planar distances between enclosed feature boundaries; they are not a proof of minimum ligament width everywhere in the outer outline or mechanical strength.
- Approximately 1 mm round holes are geometrically open but physical clearance depends on the printer and the unspecified hardware. Measure a trial print before selecting a pin or enlarging a hole.

Preserve nominal geometry for reference, then use fit trials before printing an assembly set. Optional enclosed-hole compensation is exposed in the CAD source. Open slits and tabs remain editable in the outline vertex arrays; no automatic slot-fit assumption is built in.

## Modify and regenerate

In `cad/butterfly.scad`, change `thickness`, `thickness_overrides`, `scale_xy`, `hole_clearance_diameter`, or `hole_edits`. `hole_clearance_diameter` adds the stated amount to the total width of enclosed cutouts. `hole_edits` changes individual cutout position/scale about its own center. For tab geometry or open edge-slit width, edit the corresponding points in `outer_profiles` in `profiles.scad`. The relevant long edge indices for each slit are in `validation.json`; move both slit walls by half of the required width increase while preserving the blind-end and mouth connections. Thickness changes do not update fit geometry automatically. CAD array coordinates are editable but do not infer constraints missing from the drawing.

For Python regeneration, install `numpy shapely trimesh mapbox-earcut manifold3d scipy matplotlib`, then run:

```sh
python cad/build.py --thickness 1.5
# Example: add 0.20 mm total width to enclosed cutouts only:
python cad/build.py --thickness 1.5 --hole-clearance 0.20
```

The builder reads `profiles.json`, not changes made in the SCAD files. It regenerates STLs, SVGs, 3MF, mesh validation and the preview; the README and source dimension checks describe this delivered nominal set. After editing SCAD export and revalidate the changed STL. Scaling XY also changes hole spacing and tab sizes; it is not a fit compensation control.

## Validation and printing limits

The **actual exported STL files** were reopened and checked for closed geometry, consistent winding, positive volume, one connected solid, two incident faces per edge, nondegenerate triangles, expected Euler characteristic for each hole count, and successful Manifold3D status. Mesh volume agrees with 2D profile area times 1.5 mm within 0.001%. The valid simple planar polygons and their nonoverlapping holes produce non-self-intersecting extrusions. This is a construction-based self-intersection check, not a swept assembly collision simulation.

The 3MF archive was reopened and checked for millimetre units, 13 named meshes, correct transforms, watertight positive-volume meshes and matching dimensions. All parts lie at Z=0, with no intersections on the plate and a minimum gap of **3.000 mm**. Occupied bounds are X=5.000..154.105 mm and Y=5.000..213.948 mm. The layout fits a 220 x 220 mm rectangular bed; account for your slicer's excluded regions, skirts or brims and rearrange as needed.

All solids have a flat bottom and constant nonzero thickness, so this orientation has no geometric need for supports. A 0.15 mm layer height gives ten nominal layers through 1.5 mm; final slicing settings, material, flow and hole compensation must be chosen for your printer. Narrow webs and small holes require inspection in the sliced preview. No physical printing, stiffness, fatigue, screw-bearing, weight or flight validation was performed. A printed polymer part cannot be presumed mechanically equivalent to the original plywood.

OpenSCAD source was generated from the same sampled polygons as the validated STLs; the OpenSCAD application itself was not available for independent rendering in this environment.

## Precisely what is missing for a functional RC assembly

1. An assembled or exploded view identifying all part connections, orientations and final XYZ positions, plus a bill of materials and confirmation of quantities.
2. Fastener, pivot pin, bearing/bushing and shaft diameters; fits, washers/spacers and stack heights; retention method and required axial/radial play.
3. Motor, gearbox/gears, crank and linkage specifications, including pivot-center distances, travel limits and timing. The four-hole arrays alone do not determine which pivot positions are used.
4. Wing planforms, spars, membrane material/thickness, attachments, hinges and flapping-axis geometry. Wing surfaces are not represented on this cutting sheet.
5. Electronics, battery and actuator envelope, mounting, mass distribution, target mass and center of gravity.
6. Assembly tolerances, adhesive/press-fit intent, acceptable flexibility, loads and strength requirements. Thickness and slot-width adaptation for FDM must be resolved experimentally or with specifications.

These omissions prevent verification of kinematics, moving clearances, collisions, hardware fit and flight. This package supplies all visible flat profiles and records uncertainty; it does not invent a working butterfly mechanism.

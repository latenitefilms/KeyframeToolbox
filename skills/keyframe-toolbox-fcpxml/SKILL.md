---
name: keyframe-toolbox-fcpxml
description: Create, inspect, or edit Final Cut Pro XML with editable Keyframe Toolbox graphs. Use for the Keyframe Toolbox, 360 Reframe, and Time Remap effects when authoring or modifying FCPXML.
---

# Keyframe Toolbox FCPXML

Write the requested curve as graph JSON, then use the bundled Python 3.9+ helper to encode it. The profiles in this skill match Keyframe Toolbox 2.1.0 (Build 61). The complete example targets FCPXML 1.15. [Graph IDs, units, timing and archive format](references/fcpxml-guide.md)

## Select the effect

- For a new project, adapt the [media-independent Counting project](assets/zoom-base.fcpxml). Create an `effect` resource using the intended template UID, then attach a `filter-video` referencing its document-local ID to the target clip. The guide lists all three UIDs and the allowed position of the filter within an `asset-clip`.
- For an existing export, run `python3 scripts/kt_graph.py inspect INPUT`. Match the project, clip, and effect. If the same effect appears more than once, use the reported `--instance N` on reads and edits. The occurrence is one-based within that effect type in document order.
- Read a graph with `python3 scripts/kt_graph.py read INPUT "Keyframe Toolbox" 104`. An omitted graph resolves to its factory curve. Add `--default` to inspect the reset value. A `.fcpxmld` input resolves to its `Info.fcpxml`.

## Author and verify the curve

1. Look up the **graph ID** and units for the selected effect. For example, `104` means Scale in percent on the regular effect and Field of View in degrees on 360 Reframe. For normal relative timing, place frame `i` of an `N`-frame clip at progress `i / N`.
2. Supply the top-level fields to change in a JSON object. Each point requires `progress`, `value`, and `handlesBroken`. For a one-point edit to an existing curve, update the decoded point and pass the full `points` array back. Preserve the handles, links, and timing references the user wants to keep. [Eased zoom example](assets/zoom-scale.json)
3. Apply the JSON with the helper. A video filter stores each graph in one custom `param`. The helper preserves its existing factory reset value. An existing bundle can contain other media and resources. Copy the bundle for a new deliverable and target the copy’s `Info.fcpxml`.
4. Validate against the DTD matching the root FCPXML version. `set --dtd PATH` runs `xmllint` before saving. Read the saved graph, then compare its points, handles, modes, and target clip with the request. Report which checks actually ran. Importing and re-exporting in Final Cut provides a separate host check.

Run the example from the repository root. For a standalone installation, set `skill` to the installed folder and run from the desired output directory.

```sh
skill="$PWD/.agents/skills/keyframe-toolbox-fcpxml"
mkdir -p Zoom.fcpxmld
python3 "$skill/scripts/kt_graph.py" set "$skill/assets/zoom-base.fcpxml" "Keyframe Toolbox" 104 \
  "$skill/assets/zoom-scale.json" Zoom.fcpxmld \
  --dtd "/Applications/Final Cut Pro.app/Contents/Frameworks/Interchange.framework/Versions/A/Resources/FCPXMLv1_15.dtd"
python3 "$skill/scripts/kt_graph.py" read Zoom.fcpxmld "Keyframe Toolbox" 104
```

The zoom reaches 125% at frame 25 and holds 150% from frame 50 to frame 99. For a different Toolbox release, compare a new Final Cut export with the [Build 61 reference filter in a portable project](references/build-61-example.fcpxml) before applying the same encoding.

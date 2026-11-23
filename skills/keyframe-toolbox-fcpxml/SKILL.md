---
name: keyframe-toolbox-fcpxml
description: Attach Keyframe Toolbox, 360 Reframe, or Time Remap effects in FCPXML, author editable graphs, change Inspector settings, and select a 360 projection. Use when generating or editing Final Cut Pro XML for these effects.
---

# Keyframe Toolbox FCPXML

Use the bundled Python 3.9+ helper to write Toolbox parameters. Keyframe Toolbox 2.0.1 (Build 60) and 2.1.0 (Build 61) share the same graph format. For Final Cut Pro 11.2, start from FCPXML 1.13. [Graph IDs, units, timing and compatibility](references/fcpxml-guide.md)

## Select the effect

- For a new project, choose the Counting starter for the target host. Both include the regular effect. [FCPXML 1.13 starter](assets/zoom-base-1.13.fcpxml) · [FCPXML 1.15 starter](assets/zoom-base.fcpxml)
- To add an effect, run `python3 scripts/kt_graph.py attach INPUT "Keyframe Toolbox" OUTPUT --clip "Shot A"`. Use `--project NAME` or `--clip-occurrence N` to select among clips with the same name. Running the same attachment twice produces one filter.
- For an existing export, run `python3 scripts/kt_graph.py inspect INPUT`. Match the project, clip, and effect. If the same effect appears more than once, use the reported `--instance N` on reads and edits. The occurrence is one-based within that effect type in document order.
- Read a graph with `python3 scripts/kt_graph.py read INPUT "Keyframe Toolbox" 104`. An omitted graph resolves to its factory curve. Add `--default` to inspect the reset value. A `.fcpxmld` input resolves to its `Info.fcpxml`.
- Read and edit Inspector settings with row `100`. For motion blur, pass `{"temporalBlurSettings":{"isEnabled":true}}` as the JSON file to `set`. Add `--reveal` to a **graph** edit to show that property in the Inspector. For 360 Reframe use `projection INPUT "Tiny Planet" OUTPUT` or read row `110`. [Settings and Projection examples](references/fcpxml-guide.md#edit-inspector-settings-and-projection)

## Author and verify the curve

1. Look up the **graph ID** and units for the selected effect. For example, `104` means Scale in percent on the regular effect and Field of View in degrees on 360 Reframe. For normal relative timing, place frame `i` of an `N`-frame clip at progress `i / N`.
2. Supply the top-level fields to change in a JSON object. Each point requires `progress`, `value`, and `handlesBroken`. For a one-point edit to an existing curve, update the decoded point and pass the full `points` array back. Preserve the handles, links, and timing references the user wants to keep. [Eased zoom example](assets/zoom-scale.json)
3. Apply the JSON with `set`. New FCPXML 1.13 rows use OZML 5.14 and new 1.15 rows use 5.15. An existing row keeps its wrapper version and reset value. Use `--ozml-version 5.14` or `5.15` to set the wrapper version on the rows written. For a separate deliverable from an existing bundle, copy the bundle and target the copy.
4. Pass `--dtd PATH` to any write command to validate against the DTD for the FCPXML root before saving. Read the saved rows and compare the target clip and decoded values with the request. Report a Final Cut import and re-export separately if performed.

Run the example from the repository root. For a standalone installation, set `skill` to the installed folder and run from the desired output directory.

```sh
skill="$PWD/.agents/skills/keyframe-toolbox-fcpxml"
mkdir -p Zoom.fcpxmld
python3 "$skill/scripts/kt_graph.py" set "$skill/assets/zoom-base-1.13.fcpxml" "Keyframe Toolbox" 104 \
  "$skill/assets/zoom-scale.json" Zoom.fcpxmld --reveal \
  --dtd "/Applications/Final Cut Pro.app/Contents/Frameworks/Interchange.framework/Versions/A/Resources/FCPXMLv1_13.dtd"
python3 "$skill/scripts/kt_graph.py" read Zoom.fcpxmld "Keyframe Toolbox" 104
```

The zoom reaches 125% at frame 25 and holds 150% from frame 50 to frame 99. The reference project contains four parameter values from a native Final Cut export. [Build 61 reference filter](references/build-61-example.fcpxml)

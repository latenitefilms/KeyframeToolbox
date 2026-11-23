# LLM Agents

This page is mainly for LLM agents - however, humans are welcome too! 🤖

---

## Download Skill

You can find the Keyframe Toolbox Skill on [GitHub](https://github.com/latenitefilms/KeyframeToolbox/tree/main/skills/keyframe-toolbox-fcpxml).

You can download it and use it in Claude, Codex or your preferred LLM. Need help? Ask you LLM.

---

## Generate FCPXML with Keyframe Toolbox effects

Use an `effect` resource to identify the installed Motion template, a `filter-video` to apply it to a clip, and one `param` per Toolbox graph you want to change. Each graph is a single custom FxPlug value. Its keyframes live in JSON inside that value. Final Cut’s `keyframeAnimation` element and `adjust-transform` control other kinds of animation.

This guide targets **Keyframe Toolbox v2.1.0 (Build 61)** and **FCPXML v1.15**. The worked example creates a four-second project with an editable Scale graph and Final Cut’s built-in Counting generator. It needs no external footage. The encoder uses Python 3.9+ and the standard library. To view the result, launch Keyframe Toolbox to install its Motion templates and open Final Cut Pro. [Run the zoom example](#generate-a-zoom-and-hold) · [Look up a graph ID](#choose-the-property-and-its-units)

---

### What Final Cut actually exports

The Build 61 export used one regular Keyframe Toolbox instance. Its `filter-video ref="r4"` pointed to a Motion template. Four direct `param` children had `name=""` and keys ending in `100` (inspector settings), `102` (Position X), `103` (Position Y), and `104` (Scale). The portable reference project retains these four original parameter values and uses the built-in Counting generator in place of the original media. A generator can omit untouched rows. The 360 Reframe and Time Remap mappings below come from their shipped templates and FxPlug registrations. [Build 61 reference project](build-61-example.fcpxml)

| Effect name | `resources/effect/@uid` for the standard user installation |
| --- | --- |
| Keyframe Toolbox | `~/Effects.localized/Keyframe Toolbox/Keyframe Toolbox/Keyframe Toolbox.moef` |
| Keyframe Toolbox 360 Reframe | `~/Effects.localized/Keyframe Toolbox/Keyframe Toolbox 360 Reframe/Keyframe Toolbox 360 Reframe.moef` |
| Keyframe Toolbox Time Remap | `~/Effects.localized/Keyframe Toolbox/Keyframe Toolbox Time Remap/Keyframe Toolbox Time Remap.moef` |

Keep the literal `~/` and spaces in the UID. The optional `src` in an export is a file URL for that Mac. Omit it when generating for a standard installation on another Mac. The UUID inside a `.moef` identifies its renderer. The template path above is the identifier that goes in FCPXML. [Template installer](../../../../Keyframe%20Toolbox/Wrapper%20Application/Code/ContentView.swift) · [Apple’s effect resource reference](https://developer.apple.com/documentation/professional-video-applications/effect)

Every Build 61 graph uses the full key **`9999/10003/10007/3/10021/20/<graph ID>`**. For example, regular Scale is `9999/10003/10007/3/10021/20/104`. The DTD requires a `name` attribute. These rows export it as `name=""`. Match the effect by resource UID and the parameter by its full key. Resource IDs such as `r4` are local to each document.

---

### Choose the property and its units

Each cell gives the property's authoring range and factory default. The **graph ID** is the last component of the FCPXML key. The **property ID** belongs in `propertyVisibility.visibleParameterIDs` if you edit inspector settings. Reused IDs take their meaning from the effect instance. [Graph definitions, defaults and normalization](../../../../Keyframe%20Toolbox/Plugin/Code/KeyframeParameterBridge.swift) · [FxPlug parameter registrations](../../../../Keyframe%20Toolbox/Plugin/Code/KeyframeToolboxPlugIn%2BParameters.swift)

| Graph ID | Property ID | Keyframe Toolbox | 360 Reframe | Time Remap |
| ---: | ---: | --- | --- | --- |
| 101 | 1 | Opacity 0–100%, default 100 | Same | — |
| 102 | 2 | Position X −8000…8000 px, default 0 | Pan −720…720°, default 0 | — |
| 103 | 3 | Position Y −8000…8000 px, default 0 | Tilt −720…720°, default 0 | — |
| 104 | 4 | Scale 0–2000%, default 100 | Field of View 1–360°, default 120 | — |
| 105 | 5 | Rotation Z −1440…1440°, default 0 | Roll −720…720°, default 0 | — |
| 106 | 6 | Blur 0–500 px, default 0 | Same | — |
| 107 | 7 | Rotation X −1440…1440°, default 0 | — | — |
| 108 | 8 | Rotation Y −1440…1440°, default 0 | — | — |
| 111 | 9 | — | Distortion offset −100…100, default 0 | — |
| 112 | 10 | Scale X 0–2000%, default 100 | — | — |
| 113 | 11 | Scale Y 0–2000%, default 100 | — | — |
| 114 | 12 | — | — | Time 0–100% of source, default ramp 0 → 100 |

- **Regular transforms.** A Scale value of `150` means 150%. Scale X and Y multiply the overall scale, so Scale `150` and Scale X `200` together give 300% width. A fixed pivot uses `anchorOffset` in pixels in the Position X and Position Y graph objects. Degrees are stored in the graph and converted at render time. [Transform evaluation](../../../../Keyframe%20Toolbox/Plugin/Code/KeyframeToolboxPlugIn%2BPluginState.swift)
- **360 Reframe.** Use equirectangular footage interpreted as **Rectangular** in Final Cut, a regular project, and Spatial Conform set to Fill. For a 90° pan, edit graph `102` from `0` to `90`. Projection is a separate static menu at leaf `110`. Its renderer indices are `0` Rectilinear, `1` Wide/Panini, `2` Fisheye, `3` Stereographic (default), and `4` Tiny Planet. To override the menu, copy its native `param` from an export with that projection selected. Each projection applies its own Field of View limits. [360 setup](../../../../Keyframe%20Toolbox/Plugin/Code/KeyframeInspectorHeader.swift) · [Projection definitions](../../../../Keyframe%20Toolbox/Plugin/Code/KeyframeToolboxPlugIn%2BRendering.swift)
- **Time Remap.** A value of `25` selects the source frame one-quarter of the way through the input. Equal values hold a frame and decreasing values reverse playback. For a freeze halfway through, use `(progress, value)` pairs `(0, 0), (0.5, 50), (1, 50)`. The effect requests video frames and leaves the timeline clip duration as authored. The separate Super Slow-Mo compound preparation writes a native `conform-rate` and `timeMap`. To keep the curve editable in Toolbox, write graph `114`. [Time Remap renderer](../../../../Keyframe%20Toolbox/Plugin/Code/KeyframeToolboxTimeRemapPlugIn.swift) · [Compound preparation](../../../../Keyframe%20Toolbox/Plugin/Code/TimeRemapFCPXMLService.swift)

---

### Write a graph

A `ParameterGraphStorage` object uses `version: 2`. Give each point a numeric `progress`, a numeric `value` in the property’s units, and a Boolean `handlesBroken`. Use `isUserEdited: true` for authored curves. Emit finite numbers, ascending progress in `[0, 1]`, and values within the table bounds. The plug-in merges points within `0.000001` progress. For a constant value, write two equal-valued points at `0` and `1`.

For normal **relative** timing on an `N`-frame clip, frame `i` (zero-based) starts at `i / N`. For example, frame 50 of a 100-frame clip begins at `0.5`. Progress `1` denotes the graph endpoint. To reach an exact value on the last displayed frame, put a point at `(N − 1) / N` and hold it. In the reference export, the clip is `10100/2500s` at 25 fps, or 101 frames. Its Position X and Y end at `0.9900990099009901` (`100/101`), while Scale has a point at `1`. Clip `start`, parent `offset`, and project timecode are separate FCPXML times. Keep those as rational seconds such as `1001/30000s`. [Render-time progress](../../../../Keyframe%20Toolbox/Plugin/Code/KeyframeToolboxPlugIn%2BPluginState.swift) · [Frame occupancy](../../../../Keyframe%20Toolbox/Plugin/Code/KeyframeParameterBridge.swift)

For a straight segment, omit the left point’s `outHandle` and the right point’s `inHandle`. For Bézier easing, each handle stores `timeOffset` in normalized graph time and `valueOffset` in property units, both **relative to their own point**. An outgoing handle extends to the right and an incoming handle to the left. Keep control times inside the segment and control values inside the property range. A horizontal handle has `valueOffset: 0`. Set `handlesBroken` when the two handles should be independently editable. A shared optional `linkedGroupID` UUID links coincident points across graphs in the same instance.

The optional `beforeFirstKeyframeMode` and `afterLastKeyframeMode` each accept `constant` (hold), `pingPong` (alternate direction), or `progressive` (repeat with a cumulative value offset). `displayLowerBound` and `displayUpperBound` set the graph’s display range. [Graph storage and extrapolation](../../../../Keyframe%20Toolbox/Plugin/Code/KeyframeParameterBridge.swift)

For new relative graphs, omit `timingReferenceTimelineStartSeconds` and `timingReferenceEffectiveDurationSeconds`. In absolute timing, the renderer uses these together to remap points after a trim. Its reference start is the host’s **input start** in seconds, and its effective duration is the input duration less one input frame, falling back to the input duration for very short clips. Preserve the pair when editing an absolute-timing graph. Time Remap always evaluates relative timing. Its optional `activeDurationFrames` limits the graph to the opening frames of a longer clip. For an active window of `A` frames, `1 < A < N`, the last active frame maps to progress `1` at frame `A − 1`. [Absolute timing](../../../../Keyframe%20Toolbox/Plugin/Code/KeyframeToolboxPlugIn%2BPluginState.swift) · [Active Duration mapping](../../../../Keyframe%20Toolbox/Plugin/Code/TimeRemapActiveDurationMapping.swift)

---

### Generate a zoom and hold

The starter is a complete four-second project using Final Cut’s built-in Counting generator with the regular Toolbox effect at its defaults. The accompanying JSON specifies three Scale points. Horizontal Bézier handles ease the zoom from 100% to 150% over two seconds. At 25 fps, the expected values are 100% on frame 0, 125% on frame 25, and 150% on frames 50 through 99. [Starter project](../assets/zoom-base.fcpxml) · [Scale edit](../assets/zoom-scale.json)

The commands below run from the repository root. For a standalone copy, set `skill` to the skill’s location. Pass a DTD file for the target FCPXML version to validate the output before saving. The path shown is from Final Cut Pro on macOS.

```sh
skill="$PWD/.agents/skills/keyframe-toolbox-fcpxml"
mkdir -p Zoom.fcpxmld
python3 "$skill/scripts/kt_graph.py" set "$skill/assets/zoom-base.fcpxml" "Keyframe Toolbox" 104 \
  "$skill/assets/zoom-scale.json" Zoom.fcpxmld \
  --dtd "/Applications/Final Cut Pro.app/Contents/Frameworks/Interchange.framework/Versions/A/Resources/FCPXMLv1_15.dtd"
python3 "$skill/scripts/kt_graph.py" read Zoom.fcpxmld "Keyframe Toolbox" 104
python3 "$skill/scripts/kt_graph.py" read Zoom.fcpxmld "Keyframe Toolbox" 104 --default
```

The first read returns the authored `points` and handles. The second returns two points at 100%, the factory reset value. For a new project using footage, place the `filter-video` on the target `asset-clip` or `video` and reference the `effect` resource’s local ID. On an `asset-clip`, video filters follow intrinsic adjustments, connected items, markers, and audio channel sources, and precede audio filters and metadata. Preserve the order of stacked filters. [Apple’s FCPXML document structure](https://developer.apple.com/documentation/professional-video-applications/creating-fcpxml-documents)

---

### Edit an existing export

Run `python3 "$skill/scripts/kt_graph.py" inspect INPUT` to list the clip path, timing, saved graph IDs, and occurrence of each effect. Use `--instance N` on `read` and `set` when multiple instances of the same effect are present. An absent graph reads as the factory curve. The helper accepts a plain FCPXML file, an existing `.fcpxmld` bundle, or its `Info.fcpxml`. To deliver a separate version of an existing bundle, copy the whole bundle, then target that copy. [Python helper](../scripts/kt_graph.py)

The JSON edit replaces only the supplied top-level fields. Supplying `points` replaces the entire point array. To move a single keyframe, read the graph, update that point in the returned JSON, and pass the complete array back. The helper preserves the existing OZML factory value and other parameter rows. For 360 Reframe and Time Remap, attach the corresponding template and pass its full effect name on the command line.

---

### Encode the custom parameter

From the outside in, Build 61 uses the following representations. The two Base64 alphabets have different jobs.

1. FCPXML `param/@value` is **standard Base64** of a complete UTF-8 `ozml` channel document. The supplied export uses OZML `5.15`. The inner `parameter/@id` equals the graph ID. Its `numberOfKeypoints` is `0` even on animated graphs.
2. `parameter/dataValue` is the current value. `defaultVal` holds the factory value used for reset. Preserve `defaultVal` when editing an existing row.
3. Motion’s alphabet is `*-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz` in index order. Decoding `dataValue` yields an eight-byte **big-endian** byte count, one type byte (`0x2A`), then exactly that many bytes of binary plist. Zero bytes at the end fill the last three-byte group. The length counts only the plist.
4. The outer plist is an `NSKeyedArchiver`. Its `$top.BlindDataObject` UID refers into `$objects` to the **bytes of a second binary keyed archive**. `$top.DataIsLegacy` refers to false. Inside, `$top["Custom Data"]` refers to the object of class `Keyframe_Toolbox_Renderer.ParameterGraphValue`. Its `storageData` UID refers to UTF-8 JSON **bytes**. Follow UID references when reading an export. [Production secure-coding class](../../../../Keyframe%20Toolbox/Plugin/Code/KeyframeParameterBridge.swift) · [Bundled Motion templates](../../../../Keyframe%20Toolbox/Wrapper%20Application/Resources/Motion%20Templates)

---

### Check the result

The generated zoom passed Apple’s 1.15 DTD. The production Swift decoder read the graph and the evaluator returned 100%, 125%, 150%, and 150% at the four specified frames. The factory graphs for all three effects were checked against their shipped Motion templates. A fresh Final Cut import and re-export is the remaining host check for the generated project.

1. **Check the document.** Match the root `version` to the DTD. The supplied export is 1.15. Every `id` must be unique, every `ref` must point to the right resource type, and clip durations and offsets must land on the intended frame boundaries. For real media, use accessible `media-rep/@src` URLs. Preserve unrelated resources, filters, clip timing, and any other files in an existing `.fcpxmld` bundle. For FCPXML 1.14 documents, use the repository’s [1.14 DTD](../../../../LLM%20References/FCPXMLv1_14.dtd).
2. **Decode the generated row.** Read `param/@value` with standard Base64, parse the resulting XML, and run `decode_storage` on `parameter/dataValue`. Compare its `points`, handles, and modes with the request. Decode `defaultVal` separately to check the reset behavior. DTD validation checks XML structure. It treats the encoded parameter as text and cannot detect a wrong graph ID, archive class, or packed value.
3. **Check it in Final Cut.** Use **File → Import → XML** and select `Zoom.fcpxmld`. Open *Editable Zoom*, select the Counting clip, and inspect the three Scale points. If Scale is hidden, enable it in the effect’s Settings. Scrub frames 0, 25, 50, and 99. Export XML again and decode graph `104`. Compare the decoded values and curve, since JSON key order, plist object order, and document-local resource IDs can change on export.

For edits to an existing project, the `100` row uses the same encoding with an `InspectorPanelSettings` JSON object. Decode that object, change only the requested setting, and preserve the other fields. For instance, adding property ID `10` to `propertyVisibility.visibleParameterIDs` exposes the regular Scale X graph (`112`). Rendering still evaluates a graph when it is hidden in the inspector. For an explicit per-instance settings change, set `isSeededDefault` to `false` and omit `seededDefaultRevision`. Leaf `109` is a transient refresh pulse and has no saved FCPXML value. [Inspector settings and rendering](../../../../Keyframe%20Toolbox/Plugin/Code/KeyframeToolboxPlugIn%2BPluginState.swift) · [Saved parameter flags](../../../../Keyframe%20Toolbox/Plugin/Code/KeyframeToolboxPlugIn%2BParameters.swift)

For a different Toolbox build, export a clip with an edited graph in the target effect. Compare its UID, full key, OZML wrapper, factory default, archive class, and decoded JSON before reusing this encoder.

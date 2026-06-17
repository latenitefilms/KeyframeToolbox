# Release Notes

### 1.4.0 (Build 5x)

**🎉 Released:**
- Coming soon...

**🔨 Improvements:**
- **Keyframe Toolbox 360 Reframe** has been added. Thanks for requesting, many people! Please read and follow the Quick Start instructions in the effect or shown below before using it.
  - To reframe 360° footage, you'll apply the new, dedicated effect. If you don't see it, please run the Keyframe Toolbox app, then restart FCP.
  - **QUICK START INSTRUCTIONS** — to work correctly, this effect needs to sidestep FCP's native 360° processing. To get started:
    1. Using your camera manufacturer's tools, process your original 360° camera footage into equirectangular (panoramic) format.
    2. Import the equirectangular clips into FCP, then select them in the Browser.
    3. In the Info Inspector, set the *Projection Mode* to *Rectangular* (not Equirectangular).
    4. Add your 360° clips to a regular (not 360º) timeline and set *Spatial Conform* to *Fill*.
    5. Add the Keyframe Toolbox 360 Reframe effect to your 360° timeline clips.

  - Standard Keyframe Toolbox graph controls can be used with a new set of properties, including Pan, Tilt, Field of View and Roll. Additionally, Opacity, Distortion and Blur can be added in Settings.
  - A new Projection button at the top switches between five ways to reframe your footage:
    - **Rectilinear** will never curve a straight line, but allows Field of View up to 180°.
    - **Wide/Panini** is a cylindrical view that allows a Field of View up to 220°.
    - **Fisheye** allows more distortion around the edges of frame, and allows a Field of View up to 360°.
    - **Stereographic** is the default projection, and it allows smooth transitions between a normal Field of View and (if Pan is adjusted down) a Tiny Planet-style view.
    - **Tiny Planet** is a stereographic projection with a Tilt and Field of View offset to make it easier to achieve this effect — it defaults to looking down, with a wider FOV.
    - In each Projection, Field of View is interpreted slightly differently, and each has different Distortion parameters behind the scenes too.
   - To animate smoothly between perspectives, choosing the Stereographic projection and recording keyframes on the Field of View property is usually enough. However, if you want more control, consider also animating the Distortion parameter. This graph is disabled by default, but can be enabled in Settings.
 
 - **New keyframes now maintain existing curves more closely**.
   - Previously, newly added keyframes defaulted to linear, unless Command was held. Now, if the new keyframe is along a curve, it will be created with handles that maintain that curve.
   - While creating a new keyframe in the OSC, you can still hold Command or Option to force new flat handles to be created.
   - If you want a linear keyframe, it's still easy to Command- or Option-click on a keyframe to remove its handles.

- **The Keyframe Toolbox effect now uses a more flexible height**.
  - The Inspector will always maintain enough space for all visible graphs to be shown at standard size. 
  - Graphs can still be minimized to make more room for larger graphs, but minimized graphs will be returned to standard size next time the effect is loaded. If any graphs are expanded, they will remain expanded.
  - To force the Inspector to update, simply select any other clip, then reselect a clip with Keyframe Toolbox.
  - In some rare situations, when most graphs were hidden and are then all made visible at once, there may not be enough space to show the header and the graphs in the limited space available. This is temporary. Simply select any other clip, then reselect the clip you want to work on, and the Inspector will return to normal.

**🐞 Bug Fixes:**
- An issue with incorrect Position values being shown in Better Performance mode has been fixed.
- Linking keyframes is now more reliable and resilient.
- Previous/next keyframe buttons in the OSC are more reliable.
- Keyframes now light up (when the playhead is over them) more reliably.
- Performance improvements have been made to the regular Keyframe Toolbox effect. If you ever experienced a delay when loading a timeline with multiple instances of Keyframe Toolbox, this has now been improved.
- Potential issues with very large images have been resolved. Note that Keyframe Toolbox is now limited to images no larger than 8500px across.

### 1.3.0 (Build 48)

**🎉 Released:**
- Coming soon...

**🔨 Improvements:**
- **On-Screen Controls (OSC) have been added.** Thanks for requesting, Dylan Bates and others!
  - Labels appear while the diamonds are dragged.
  - Position is in the centre, Rotation Z/X/Y are on spokes, Scale has a circle, Opacity is above and Blur is below.
  - Click or drag the colour-matched diamonds for any of the existing properties to create a new linear keyframe at the current time.
  - Command-click or drag an OSC diamond to create a new keyframe with easing handles applied.
  - Keyframe diamonds are now filled in if they are at the current playhead position, in the OSC and in the graphs.
  - Clicking a filled keyframe diamond in the OSC will delete that keyframe. (This doesn’t happen in the graph.)
  - Use the previous/next buttons around each keyframe to jump to the neighbouring keyframe on that property.
  - If you hold Shift while adjusting Position keyframes, you’ll constrain movement to only one dimension and only create a keyframe on that graph.
  - Motion paths are shown, using diamonds to indicate keyframe positions (on X, Y, or both) and white dots to indicate tweened frames.
  - On-screen controls can be instantly hidden by activating the Live/OSC mode, using Caps Lock. (Note that the Live Scrubbing button in the Inspector has been renamed.)
  - If you prefer not to see the OSC at all, it can be disabled in Settings.

- **Keyframes on different property graphs can be linked.** Thanks for requesting, Dylan Bates!
  - Two or more keyframes positioned at the same point in time can now be linked with the Link Keyframes command in the right-click or graph menus.
  - Linked keyframes are drawn with a thicker outline.
  - Handle direction, handle length and keyframe time positions are synced between linked keyframes.
  - Keyframes can be unlinked manually. Select one or more keyframes and choose “Unlink Keyframe(s)” in the menu. (When only one keyframe would remain linked, it is also unlinked.)
  - Keyframes are also unlinked if a preset or paste operation would affect a linked keyframe.

- **Keyframe timing is now frame-accurate in Absolute Mode.**
  - Previously, if you added an Oscillate preset to Position Y to create a bouncing animation, the lowest point of each bounce might not have been visible, because keyframes in the graph might not have landed exactly on real frames in the clip. This is only visible in moments where a very quick direction change occurs (like a bounce) but it’s been seen in Apple Motion and Adobe Animate too.
  - In Absolute Timing mode, keyframes are now snapped to real frames, so every keyframe in the graphs represents a real frame on-screen. Every bounce will land.
  - In Relative Timing mode, not every keyframe will end up exactly on a frame, because the graph needs to stretch to match any clip length. While this is rarely visible, switching to Absolute Timing mode will fix any issues. Alternatively, fix these issues manually with the OSC, by Shift-dragging the visible object position to the desired position.

- **Playhead Movement can be disabled in Settings to work around a storyline bug in FCP.**
  - **If possible, avoid using Keyframe Toolbox on clips in storylines.**
  - In a storyline, we recommend to uncheck Playhead Movement in Settings. This lets you use Keyframe Toolbox in storylines without unwanted playhead jumps. Why?
   - In a secondary storyline, the playhead cannot be moved reliably, as the clip's timecode is not accurately reported. We also can't reliably detect that a clip is in a secondary storyline and disable these features automatically. As a result, the playhead is likely to jump to near the start of your timeline instead of the correct position.
   - Playhead movement includes clicking in the graphs to move the playhead to a specific position, jumping to a keyframe position when editing a keyframe numerically, moving the playhead in the graphs when Live Scrubbing is active, and using the previous/next keyframe buttons in the OSC.

---

### 1.1.0 (Build 39)

**🎉 Released:**
- 23rd April 2026

**🔨 Improvements:**
- **Clicking the name of a property creates a keyframe at the current time**, maintaining the current graph shape.
- **Shift-clicking a property name creates a keyframe on all graphs.** Thanks for requesting, Honusan and others!
  - Related — clicking the name of a property while over a keyframe (or double-clicking the keyframe property name) opens that keyframe for numeric editing. Thanks for requesting, Honusan and others!
- **Graphs can now be zoomed horizontally.** Use two fingers on a trackpad or hold option while scrolling. Alternatively, double-click in empty space to zoom in to show just 25% of the graph width. When zoomed in, a scroll indicator at the bottom shows the visible part of the total graph. This can be dragged manually. Alternatively, you can scroll with a horizontal scroll on a trackpad or by holding shift while using a scroll wheel. Thanks for requesting, Jake, Honusan and others!
- **Presets can be saved**, using the new Save Preset option at the end of the Presets menu. When you apply one of your own presets, you’ll be able to control limits, scale handles up or down, and flip the preset as you can with the other presets. Thanks for requesting, cinestillsamurai, Honusan and others!
  - Use **Manage Presets**, in the same menu, to reveal a folder containing all your presets. Share presets with your friends if you wish!
  - Renaming presets renames them in the menu; deleting them removes them.
- **Easing has been added** to the graph menu and right-click menu, for Ease In, Ease Out, or Ease In+Out, for many common curve types (Linear, Sine, Quad, Cubic, Quart, Quint, Circ, Expo, Back). If you’re a fan of Easy Ease in After Effects, try Sine here. Note that selecting two or more keyframes applies easing to the curves between the presets, while selecting a single keyframe applies easing to the handles around that keyframe. Thanks for requesting something like this, Alex Gollner!
- **Clicking on a line connecting two keyframes selects both keyframes.** This makes it easier to apply easing to the graph between two keyframes. (Note that double-clicking on a line still creates a new linear keyframe.)
- **Settings can now be saved as default.** If you always want to use Motion Blur and Absolute Timing, set your preferred options, then press the new button at the bottom of the Settings panel. This affects new instances of Keyframe Toolbox. Thanks for requesting, Honusan!
- **In Absolute Timing mode, time is now shown in frames and timecode.** If a clip is less than a minute long, only seconds and frames are shown. Thanks for requesting, Honusan!
- Several improvements to numeric editing.
  - **When you double-click a keyframe, the playhead moves to that frame** so you can see your changes directly.
  - When editing values numerically, use up/down to change by 1, ⇧-up/down to change by 10, and (new!) ⌥-up/down to change by 100.
  - **Changing values with arrow keys now immediately updates** a keyframe or handle.
  - **Left and right arrow keys now switch to editing neighbouring keyframes** (and move the playhead) so you can easily edit all values in a graph numerically if you wish.
- If you wish, hold Command while using the scroll wheel to move the playhead.

**🐞 Bug Fixes:**
- Important: property changes now more closely follow extreme graph curves. Please check any existing animations to make sure they're still doing what you want; very minor tweaks may be needed.
- Scrolling behavior is more consistent.
- It's easier to select groups of keyframes.

---

### 1.0.0 (Build 31)

**🎉 Released:**
- 28th March 2026

This is the first release of **Keyframe Toolbox**. Woohoo!

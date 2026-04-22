# Release Notes

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
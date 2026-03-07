# How To Use

!!!tip Now in public beta! 🥳
KeyFrame Toolbox is currently in public beta.\
You can download it on Apple's [TestFlight](https://testflight.apple.com/join/YwzGCS6a).
!!!

Keyframe Toolbox is currently in **public beta** - so we are actively making changes and improvements based on YOUR feedback.

We will be constantly adding new builds to TestFlight as we add new features and fix any bugs reported.

Please add any and all feedback to our [GitHub Issues page](https://github.com/latenitefilms/KeyframeToolbox/issues).

---

## Installation

You can download Keyframe Toolbox from [Apple's TestFlight](https://testflight.apple.com/join/YwzGCS6a).

![](/static/test-flight-install.png)

Click **Install** then run the Keyframe Toolbox application, where you'll be prompted to install the **Motion Template**.

![](/static/wrapper-application.png)

After the Motion Template is installed you can launch Final Cut Pro.

You'll find Keyframe Toolbox in the **Effects Browser**.

![](/static/effects-browser.png)

You can then apply Keyframe Toolbox to any effect and away you go!

![](/static/keyframe-toolbox-hero.png)

---

## Using Keyframe Toolbox

This effect is built to let you use familiar beziér keyframes and handles to control common properties in Final Cut Pro. 

In the Keyframe Toolbox interface you'll see several graphs, each one controlling a separate parameter.

In the current effect, graphs include `Opacity`, `Position X`, `Position Y`, `Scale`, `Rotation Z`, `Rotation X`, `Rotation Y`,and `Blur`.
 - (Note that Rotation, in a 2D context, is actually Rotation around the Z axis.)

Because Final Cut Pro captures regular keystrokes before we can, we've made heavy use of modifier keys. Tooltips are present, so if you hover over an icon, menu or graph item, you'll be told what modifier keys do in that particular context. 

Right now, Option and Command are equivalent, to hopefully make it easier for users of both Motion and After Effects to work with handles. Shift is a constraining modifier, as usual, and Control-clicking a keyframe or handle deletes it, while right-clicking pops up a menu. (If you don't have the normal right-click behavior set up on your pointing device, you can use the menu above each graph instead of right-clicking.)

---

## An important note about still images and aspect ratios

If you're working with regular video clips in the same aspect ratio as your canvas, you won't have any problems. You also probably won't have any problems if you're working in a different aspect ratio, and have set Spatial Conform to Fill. If that's your plan, skip straight to the next section!

However, there's a specific situation, common in animation, which requires some special treatment. Because effects can only act on the clip they've been applied to, they are limited to the size of the frame the image takes up. It's not possible to move an image outside that area — it just clips off at the original border. Setting Spatial Conform to Fill does solve this problem, but can cause quality issues, as it can mean the image is scaled down and then scaled back up in some contexts.

To deal with this, the standard workflow for many animation plug-ins based on effects is to place each element in a compound clip, and that works here too. You can select any smaller elements and place them in a compound clip before applying Keyframe Toolbox. However, this can introduce some complexity around the sizing of compound clips and also timing.

As a better solution, we've added a feature to pad any still image with extra space, making it the same aspect ratio as the timeline the effect is placed in. This means you won't need to change Spatial Conform before applying Keyframe Toolbox, and you won't hit any scaling quality problems.

To use it, you'll need to have applied Keyframe Toolbox to a clip in your timeline — even on a temporary clip. With that in place, drag an image from the Browser to the logo at the top of the effect. (This image will need to be in the same Event as your current Project, due to how FCP works.)

Keyframe Toolbox will then send the new image back to a new event called "images with padding". The new image also has its new resolution as part of its name. You can now add this image to your timeline instead of your original image.
 
---

## Keyframe graph basics

Keyframes remembers values at points in time.

![](/static/basic-graph.png)

- Each graph starts with has a keyframe at the start (left) and end (right) and a line connecting them.
- **The graph width maps to the clip width**, while the **graph height maps to the values of the property**, within the limits shown to the right of that graph.
- Linear keyframes transition values directly, in a straight line, while non-linear keyframes have handles that influence curves, creating smoother transitions between values.
- At least two keyframes must remain in the graph, so the first and last keyframes cannot be deleted until other keyframes are added.
- However, the first and last keyframes can be moved horizontally, so the first keyframe can start later than 0% and the last keyframe can end before 100%.
- If the playhead is over the clip, **a line briefly indicates the position of the timeline playhead** in relation to the clip. The line will update to the correct position as you move keyframes around, to allow you to snap keyframes to the playhead.
- As you drag a keyframe, hold `SHIFT` to enable snapping to the playhead.
- **Opacity has a fixed 0..100 range**, while the other properties use defaults that should make sense, based on the clip properties. (Note that Position values are calculated based on the clip resolution, not the timeline resolution.
- **All other limits can be changed by dragging them**, horizontally or vertically. Hold `OPTION` as you drag to change both sides in opposite directions.
- **Press the button between the limits to fit the graph** to the current values within it, plus a small buffer.

---

## Resetting and scaling the graphs

Each graph can be reset, and shown in one of three sizes.

![](/static/graph-sizes.png)

- **Each property graph can be reset** using the reset button next to its name.
- **`SHIFT`-click any graph's reset button** to reset all graphs at once.
- To the right of the reset button, you'll see a three-position toggle displaying the current graph height: Minimised, Standard or Expanded.
- When Minimized, the "Fit" button within the upper and lower limits is not available. All other controls work in any size.
- **`SHIFT`-click on a toggle** to force all graphs to that size.
- **`OPTION`-click on a toggle** to set that graph to the chosen size and minimize all other graphs.
-- As it's not possible to show all graphs at larger sizes, when graphs move to Standard or Expanded size, other graphs may shrink.

---

## Adding and moving keyframes

Keyframes can be moved and new keyframes can be added.

![](/static/dragging-snapping-crop.png)

- **Double-click** on a graph line to add a linear keyframe and remember a value at a point in time.
- **Click and drag on a keyframe** to move it.
- During the drag, numbers will appear showing the keyfrane's value (above) and time (below).
- **`SHIFT`-drag on a keyframe** to lock movement to horizontal (time) or vertical (value) movement.
- If you move a keyframe on one graph to a position near a keyframe on another graph, a vertical line will appear.
- If `SHIFT` is now held down, the keyframe will snap to this line to align with keyframes on other properties.
- **Dragging a keyframe and adding `SHIFT` while dragging** will also snap to the line that indicates the playhead position, if present. This allows you to snap a keyframe to the current playhead position.
- Dragging a line connnecting two keyframes will move both keyframes together.

---

## Non-linear (smooth) keyframes

Handles connected to keyframes control the graph curve that controls how one value changes into another.

![](/static/simple-keyframes.png)

- **`OPTION`- or `COMMAND`-drag on a line** to add a non-linear keyframe, dragging out two symmetric handles to create a bezier curve.
- **`OPTION`- or `COMMAND`-drag on a keyframe** to add handles to a linear keyframe, or reset and redraw the handles on an existing non-linear keyframe.
- Optionally, hold `SHIFT` while doing this to lock the curve to horizontal (0°).
- **`OPTION`- or `COMMAND`-click on a keyframe** to remove handles and reset the keyframe to linear.
- **`OPTION`- or `COMMAND`-drag on a handle** to split a handle pair and make it asymmetric.
- **`SHIFT`-drag a handle** to maintain its current angle and only change distance.

---

## Deleting keyframes and handles

Keyframes and handles can be deleted.

![](/static/delete-keyframes.png)

- **`CONTROL`-click on a keyframe** to delete it.
- **Right-click on one or more selected keyframe and select Delete Keyframe(s)** to delete them.
- **`CONTROL`-click on a handle** to delete it. This operation only deletes one handle in a symmetric pair.
- **`COMNMAND`- or `OPTION`-click on a keyframe** to delete its handles and convert it to linear.
- The first and last keyframes can be deleted just like other keyframes, but at least two keyframes must remain — there must be a first and a last keyframe.

---

## Working with precision

Exact numbers can be entered for keyframes and handles.

![](/static/precision.png)

- **Double-click on any keyframe** to see its value (above) and time (below).
- **Double-click on any handle** to see its distance (above) and angle (below).
- In both these cases, **type in new values** to change them, then approve the change by presing `RETURN` or `ENTER`, or cancel the change with `ESCAPE`.
- Alternatively, use **up and down arrows** to change the values by 1, and **`SHIFT`-up and `SHIFT`-down arrows** to change the values by 10.

---

## Selecting, moving and scaling keyframes

Multiple keyframes can be selected and manipulated.

![](/static/multi-select.png)

- **Clicking a keyframe selects it**.
- **`SHIFT`-clicking** additional keyframes selects additional keyframes.
- **Drag from empty space across one or more keyframes** to create a selection marquee that selectes enclosed keyframes.
- **Hold `SHIFT` as you drag a selection box** to select additional keyframes.
- When multiple keyframes have been selected, a bounding box appears that allows the selected keyframes to be scaled and/or moved.
- **Drag one of the selected keyframes** to move them, or **drag the sides or corners of the bounding box** to move the contained keyframes proportionally to one another.
- **Hold `SHIFT` as you drag** one of multiple selected keyframes to constrain to horizontal or vertical movement.
- Right-click to delete, copy, or perform other operations on multiple keyframes at once.
- Click elsewhere in the graph to dismiss the bounding box.

---

## Using the graph menu

Each grpah has a menu that enables some advanced features. 

![](/static/opacity-graph-menu.png)

- The graph menu can be accessed by the menu to the right of the toggle buttons, or by right-clicking on the graph.
- Many of these menu options are context-sensitive. If you select one or more keyframes, those keyframes will be affected. If no keyframes are selected, the entire graph is affected.
- When a single keyframe is selected, use `Clone Value from Previous Keyframe` or `Clone Value from Next Keyframe` to simulate a Hold keyframe.
- If no keyframes are selected, an entire graph can be reversed in time by choosing `Time-Reverse Graph`, or flipped vertically by choosing `Invert Graph`.
- If two or more contiguous keyframes are selected, they can be reversed by choosing `Time-Reverse Keyframes`, or flipped vertically by choosing `Invert Keyframes`.
- Use `Copy Keyframes` or `Copy Graph` to copy keyframes from a graph.
- Use `Paste Keyframes` or `Paste Graph` to paste copied keyframes from one graph into another graph. One or more keyframes must be selected for Paste Keyframes to be available.
- `Clone Value from Previous Keyframe` and `Clone Value from Next Keyframe` change the value of the selected keyframe to a the value or a neighbouring keyframe. 

- **Presets** and **Before First Keyframe and After Last Keyframe** are discussed in the following sections.
---


## Presets

To create flexible keyframe graphs based on common animation patterns.

![](/static/opacity-expanded-graph.png)

- The graph menu and the right-click menu both contain a **Presets** submenu.
- Adjusting the controls on these presets allows many common animation patterns to be created, including bounces, fades up and down moves in and out, and more.
- If no keyframes are selected, these presets replace the entire graph.
- If two or more contiguous keyframes are selected, these presets apply within the selected keyframe range, using the width and height of the selected keyframes. This allows more than one preset to be used in the same graph.

![](/static/pos-y-oscillate-bounce.png)

- The presets include:
  - Oscillate (repeated movements up and down, with modes for bouncing)
  - Min, Max (move in one direction)
  - Min, Max, Min (move in one direction and then immediately back)
  - Min, Max, Hold, Min (move in one direction, pause, move back)
  - Min, Mid, Hold, Max (move halfway, pause, move further)
  - Note that all these presets include a toggle to invert the graph.
  - While it’s possible to control the upper and lower limits of any presets after choosing it, selecting multiple keyframes before choosing a preset sets the limits from keyframe values.
- In each case, when a preset is chosen, several draggable options appear underneath each graph, including some of:
  - Upper limit
  - Lower limit
  - Bend (handle size)
  - Wavelength
  - Phase
  - Decay
  - Graph type or Flip — use this to make a preset work in the opposite way, so _Min, Max_ becomes _Max, Min_.
- These options can be repeatedly changed until a keyframe is moved or the clip selection in FCP is changed.

![](/static/pos-x-oscillate-graph.png)

- In **Oscillate**, the options are:
  - Upper limit
  - Lower limit (hold `SHIFT` while dragging to change these quickly, but they cannot exceed current graph limits)
  - Wavelength
  - Phase
  - Bend (handle strength)
  - Decay
  - Oscillate mode, which cycles through a Sine wave, a bounce down and a bounce up
- In **Min, Max** and **Min, Max, Min**, the options are:
  - Upper limit
  - Lower limit
  - Bend (handle strength)
  - A toggle to flip the graph, reversing Min and Max
- In **Min, Max, Hold, Min** and **Min, Mid, Hold, Max**, the options are:
  - Upper limit
  - Lower limit
  - Bend (handle strength)
  - Hold duration (in %)
  - A toggle to flip the graph, reversing Min and Max
- Remember that when a single keyframe is adjusted, the controls disappear. Simply select the keyframes and choose the preset once more.

---

## Before First Keyframe and After Last Keyframe

To control a virtual keyframe graph beyond the first and last keyframes.

![](/static/before-first-after-last.png)

- If the first keyframe is moved to the right or the last keyframe is moved to the left, a dashed line displays the _virtual_ graph beyond the bounds of the _real_ graph.
- This strategy allows an animation to be repeated many times, if desired.
- By default, this graph is a constant line, but the graph and right-click menus allow two other options to be chosen:
  - **Ping-Pong**, which repeats the real graph backwards, then forwards, repeating while time permits.
  - **Progressive**, which repeats the real graph, but transposed so that the first virtual keyframe is positioned on the real final keyframe. This graph also repeats while time permits.
- You can create new keyframes on the _virtual_ graph in the standard ways.


---

## Settings

Settings gives access to advanced features.

![](/static/settings.png)

- Click the Settings button to pop up a panel with two sections: **Properties** and **Motion Blur**.
- **Properties** allows some graphs to be hidden by unchecking them. At least one graph must remain active.
  - Note that those graphs, if keyframes have been changed, will still have an effect if deactivated.
  - Currently, all graphs are activated by default.
- **Timing Mode**, which allows:
  - `Relative Timing (graph maps to clip)` which is appropriate when working with still images, or you want to create a movement that spans the clip length, with that animation automatically retiming if the clip length is adjusted.
  - `Absolute Timing (graph maps to time)` which is appropriate when specific animation moments must happen at particular moments in the video. If the source clip is trimmed in this mode, the graphs will be cropped, or extra space will be added around the first or last keyframes.
- **Motion Blur**, when active, creates blur on moving objects. Adjust the settings here to adjust the blur parameters.
- **Help**, which includes a global setting to disable tooltips, if they're bothering you.

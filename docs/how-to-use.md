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

![](/static/keyframe-toolbox-01.png)

---

## Using Keyframe Toolbox

This is a work in progress, and may change. However, here's a list of commands you can use to control keyframes and handles. Right now, option and command are equivalent, to hopefully make it easier for users of both Motion and After Effects to work with handles. This may change. Currently, control-clicking and right-clicking are not the same — right clicking doesn't do anything.

In the Keyframe Toolbox interface you'll see several graphs, each one controlling a separate parameter.

In the current effect, graphs include `Opacity`, `Position X`, `Position Y`, `Scale`, `Rotation`, and `Blur`.

---

## Keyframe graph basics

Each graph starts with has a keyframe at the start (left) and end (right) and a line connecting them.

- **These two keyframes cannot be removed**, but they can be moved horizontally.
- If the playhead is over the clip, **a line indicates the position of the timeline playhead** in relation to the clip.
- **The graph width maps to the clip width**, while the **graph height maps to the values of the property**, within the limits shown to the right of that graph.
- **Opacity has a fixed 0..100 range**, while the other properties use defaults that should make sense.
- **All other limits can be changed by dragging them**, horizontally or vertically. Hold **option** as you drag to change both sides in opposite directions.
- **Press the button between the limits to fit the graph** to the current values within it, plus a small buffer.

---

## Adding and moving keyframes

Keyframes can be moved and new keyframes can be added.

- **Double-click** on a graph line to add a linear keyframe and remember a value at a point in time.
- **Click and drag on a keyframe** to move it.
- During the drag, numbers will appear showing the keyfrane's value (above) and time (below).
- **`SHIFT` drag on a keyframe** to lock movement to horizontal (time) or vertical (value) movement.
- If you move a keyframe on one graph to a position near a keyframe on another graph, a vertical line will appear.
- If `SHIFT` is now held down, the keyframe will snap to this line to align with keyframes on other properties.
- **`SHIFT` dragging** a keyframe will also snap to the line that indicates the playhead position, if present.
- Dragging a line connnecting two keyframes will move both keyframes together.

---

## Smoothing keyframes

Handles connected to keyframes control the graph curve that controls how one value changes into another.

- **`OPTION` or `COMMAND` drag on a line** to add a non-linear keyframe, dragging out two symmetric handles to create a bezier curve.
- **`OPTION` or `COMMAND` drag on a keyframe** to add handles to a linear keyframe, or reset and redraw the handles on an existing non-linear keyframe.
- Optionally, hold `SHIFT` while doing this to lock the curve to horizontal (0°).
- **`OPTION` or `COMMAND` click on a keyframe** to remove handles and reset the keyframe to linear.
- **`OPTION` or `COMMAND` drag on a handle** to split a handle pair and make it asymmetric.
- **`SHIFT` drag a handle** to maintain its current angle and only change distance.

---

## Deleting keyframes and handles

Keyframes and handles can be deleted.

- **`CONTROL` click on a keyframe** to delete it.
- **`CONTROL` click on a handle** to delete it. This operation only deletes one handle in a symmetric pair.
- Though the first and last keyframes cannot be deleted, you can **`CONTROL` click on the first keyframe** to duplicate the value of the second keyframe, or **`CONTROL` click on the last keyframe** to duplicate the value of second-last keyframe.

---

## Working with precision

Exact numbers can be entered for keyframes and handles.

- **Double-click on any keyframe** to see its value (above) and time (below).
- **Double-click on any handle** to see its distance (above) and angle (below).
- In both these cases, **type in new values** to change them, then approve the change by presing `RETURN` or `ENTER`, or cancel the change with `ESCAPE`.
- Altenatively, use **up and down arrows** to change the values by 1, and **`SHIFT` up and `SHIFT` down arrows** to change the values by 10.

---

## Selecting, moving and scaling keyframes

Multiple keyframes can be selected and manipulated.

- **Clicking a keyframe selects it**.
- **`SHIFT` clicking** additional keyframes selects additional keyframes.
- **Drag from empty space across one or more keyframes** to create a selection marquee that selectes enclosed keyframes.
- **Hold `SHIFT` as you drag a selection box** to select additional keyframes.
- When multiple keyframes have been selected, a bounding box appears that allows the selected keyframes to be scaled and/or moved.
- **Drag one of the selected keyframes** to move them, or **drag the sides or corners of the bounding box** to move the contained keyframes proportionally to one another.
- **Hold `SHIFT` as you drag** one of multiple selected keyframes to constrain to horizontal or vertical movement.
- Click elsewhere in the graph to dismiss the bounding box.

---

## Using the reset button and the graph menu

Next to each graph's name is a reset button and a menu that enables some advanced features.

- **Each property graph can be reset** using the reset button next to its name.
- **`SHIFT` click any graph's reset button** to reset all graphs at once.
- Use `Copy Graph` to copy all keyframes from a graph.
- Use `Paste Graph` to paste copied keyframes from one graph into another graph.
- When a single keyframe is selected, use `Copy Value from Previous Keyframe` or `Copy Value from Next Keyframe` to do that.
- If no keyframes are selected, an entire graph can be reversed in time by choosing `Time-Reverse Graph`.
- If two or more contiguous keyframes are selected, they can be reversed by choosing `Time-Reverse Keyframes`.

---

## Settings

- This doesn't do anything yet.
- We do plan to add presets.
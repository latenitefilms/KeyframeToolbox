# Keyframe graph basics

Keyframes remember values at points in time.

![](/static/basic-graph.png)

- Each graph starts with a keyframe at the start (left) and end (right) and a line connecting them.
- **The graph width maps to the clip width**, while the **graph height maps to the values of the property**, within the limits shown to the right of that graph.
- Linear keyframes transition values directly, in a straight line, while non-linear keyframes have handles that influence curves, creating smoother transitions between values.
- At least two keyframes must remain in the graph, so the first and last keyframes cannot be deleted until other keyframes are added.
- However, the first and last keyframes can be moved horizontally, so the first keyframe can start later than 0% and the last keyframe can end before 100%.
- If the playhead is over the clip, **a line briefly indicates the position of the timeline playhead** in relation to the clip. The line will update to the correct position as you move keyframes around, to allow you to snap keyframes to the playhead.
- This **"mini playhead" can be moved by using the scroll wheel as you hold `COMMAND`** while the pointer is over a graph. You can also hold `COMMAND` while moving two fingers on a trackpad. `New in v1.1`
- Alternatively, activate **Live Scrubbing** with the button at the top, or press `CAPS LOCK` to toggle it. When Live Scrubbing is active, moving the mouse over a graph moves the playhead.
- As you drag a keyframe, hold `SHIFT` to enable snapping to the playhead.
- **Opacity has a fixed 0..100 range**, while the other properties use defaults that should make sense, based on the clip properties. (Note that Position values are calculated based on the clip resolution, not the timeline resolution.)
- **All other limits can be changed by dragging them**, horizontally or vertically. Hold `OPTION` as you drag to change both sides in opposite directions.
- **Press the button between the limits to fit the graph** to the current values within it, plus a small buffer.
- Tick marks underneath each graph indicate seconds, with an extra indication 5-second and 10-second intervals.

<div style="padding:100.00% 0 0 0;position:relative;"><iframe src="https://player.vimeo.com/video/1173533437?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479%2Fembed" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen="" frameborder="0" style="position:absolute;top:0;left:0;width:100%;height:100%;"></iframe></div>

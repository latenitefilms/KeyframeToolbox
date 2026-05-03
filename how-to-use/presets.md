# Presets

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
  - Lower limit (hold `SHIFT` while dragging to change limits quickly, but they cannot exceed current graph limits)
  - Bend (handle size/amount of smoothing)
  - Wavelength
  - Phase
  - Decay
  - Graph type or Flip — use this to make a preset work in the opposite way, so _Min, Max_ becomes _Max, Min_.
- A preset's options can be repeatedly changed **until a keyframe is moved** or the clip selection in FCP is changed.

![](/static/pos-x-oscillate-graph.png)

- In **Oscillate**, the options are:
  - Upper limit
  - Lower limit
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

<div style="padding:100% 0 0 0;position:relative;"><iframe src="https://player.vimeo.com/video/1173533497?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479" frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media; web-share" referrerpolicy="strict-origin-when-cross-origin" style="position:absolute;top:0;left:0;width:100%;height:100%;" title="KT 11 — Presets"></iframe></div><script src="https://player.vimeo.com/api/player.js"></script>

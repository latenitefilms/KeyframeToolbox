# Before First Keyframe and After Last Keyframe

To control a virtual keyframe graph beyond the first and last keyframes.

![](/static/before-first-after-last.png)

- If the first keyframe is moved to the right or the last keyframe is moved to the left, a dashed line displays the _virtual_ graph beyond the bounds of the _real_ graph.
- This strategy allows an animation to be repeated many times, if desired.
- By default, this graph is a constant line, but the graph and right-click menus allow two other options to be chosen:
  - **Ping-Pong**, which repeats the real graph backwards, then forwards, repeating while time permits.
  - **Progressive**, which repeats the real graph, but transposed so that the first virtual keyframe is positioned on the real final keyframe. This graph also repeats while time permits.
- You can create new keyframes on the _virtual_ graph in the standard ways.

<div style="padding:100.00% 0 0 0;position:relative;"><iframe src="https://player.vimeo.com/video/1173533435?h=120310bc90&amp;badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479%2Fembed" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen="" frameborder="0" style="position:absolute;top:0;left:0;width:100%;height:100%;"></iframe></div>

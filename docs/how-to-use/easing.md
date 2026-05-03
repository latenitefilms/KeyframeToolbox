# Easing

Allowing predictable curve patterns to be used across one or more keyframes. `New in v1.1`

![](/static/easing.png)

- The graph menu and the right-click menu both contain an **Easing** submenu. `New in v1.1`
- The Easing submenu can be used in two contexts: **referring to curves**, and **referring to handles on a keyframe**. To refer to curves, select two or more keyframes before choosing the Easing submenu; to refer to handles on a keyframe, select just one keyframe before choosing the Easing submenu.
- If two or more keyframes are selected, easing affects the **curves between the selected keyframes**, so any handle before the first selected keyframe or after the last selected keyframe will be ignored.
- In this mode, options include **Ease In+Out**, **Ease In** and **Ease Out**.
  - All options here affect the handles on both sides of each selected curve.
- However, if a single keyframe is selected, these menu items now refer to the handles around that keyframe. The submenu items change to reflect this, and now read **Ease Left+Right**, **Ease Left** and **Ease Right**.
  - Ease Left means the handle to the left of the keyframe and Ease Right means the handle to the right of the keyframe.
- Each submenu contains:
  - Linear
  - Sine
  - Quad
  - Cubic
  - Quart
  - Quint
  - Circ
  - Expo
  - Back
- For an illustration of how these graphs should appear, refer to https://easings.net.
  - Important: The easing curves shown here refer to the curve between two keyframes, not to the handles on a keyframe.


<div style="padding:100.00% 0 0 0;position:relative;"><iframe src="https://player.vimeo.com/video/1185344571?h=d20889ee60&amp;badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479%2Fembed" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen="" frameborder="0" style="position:absolute;top:0;left:0;width:100%;height:100%;"></iframe></div>

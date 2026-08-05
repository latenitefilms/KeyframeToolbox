# Introducing Keyframe Toolbox

This effect is built to let you use familiar Bezier keyframes and handles to control common properties in Final Cut Pro. `Updated in v1.5`

In the Keyframe Toolbox interface you'll see several graphs, each one controlling a separate parameter.

In the current effect, active graphs include `Opacity`, `Position X`, `Position Y`, `Scale`, `Rotation Z`, `Rotation X`, `Rotation Y`, and `Blur`.
 - (Note that Rotation, in a 2D context, is actually Rotation around the Z axis.)
 - Either or both of two additional graphs, `Scale X` and `Scale Y`, can be activated if needed. `New in v1.5`
   - In most circumstances, a single scale value is easiest to manage. For more complex animations, you can use any combination of these three graphs:
     - `Scale` with `Scale X` 
     - `Scale` with `Scale Y`
     - `Scale X` with `Scale Y`
     - `Scale` with `Scale X` and `Scale Y`
   - Note that `Scale X` and `Scale Y` are multiplied with the `Scale` value to produce a final value.
   - Remember: graphs are not deactivated when they are hidden. If you've used a graph and later decide not to, reset it before hiding it.

Because Final Cut Pro captures regular keystrokes before we can, we've made heavy use of modifier keys. Tooltips are present, so if you hover over an icon, menu or graph item, you'll be told what modifier keys do in that particular context.

Right now, `OPTION (⌥)`  and `COMMAND (⌘)` are equivalent, to hopefully make it easier for users of both Motion and After Effects to work with handles. `SHIFT (⇧)` is a constraining modifier, as usual, and `CONTROL (⌃)`-clicking a keyframe or handle deletes it, while right-clicking pops up a menu. (This means that `CONTROL (⌃)`-clicking does not pop up the right-click menu. If you don't have right-click behavior set up on your pointing device (such as a two-finger click on a trackpad) you can use the menu above each graph instead of right-clicking.)

<div style="padding:56.25% 0 0 0;position:relative;"><iframe src="https://player.vimeo.com/video/1173533501?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479" frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media; web-share" referrerpolicy="strict-origin-when-cross-origin" style="position:absolute;top:0;left:0;width:100%;height:100%;" title="KT 1 — Introducing Keyframe Toolbox"></iframe></div><script src="https://player.vimeo.com/api/player.js"></script>

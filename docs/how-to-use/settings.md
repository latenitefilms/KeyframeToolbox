# Settings

Settings gives access to advanced features.

![](/static/settings.png)

- Click the Settings button to pop up a panel with two sections: **Properties** and **Motion Blur**.
- **Properties** allows some graphs to be hidden by unchecking them. At least one graph must remain active.
  - Note that those graphs, if keyframes have been changed, will still have an effect if deactivated.
  - Currently, all graphs are activated by default.
- **Timing Mode**, which allows:
  - `Relative Timing (graph maps to clip)` which is appropriate when working with still images, or you want to create a movement that spans the clip length, with that animation automatically retiming if the clip length is adjusted.
  - `Absolute Timing (graph maps to time)` which is appropriate when specific animation moments must happen at particular moments in the video. If the source clip is trimmed in this mode, the graphs will be cropped, or extra space will be added around the first or last keyframes.
    - In Absolute Timing mode, time values are shown in frames and timecode. (If a clip is less than a minute long, only seconds and frames are shown.)
- **Motion Blur**, when active, creates blur on moving objects. Adjust the settings here to adjust the blur parameters.
- **Help**, which includes a global setting to disable tooltips, if they're bothering you.
- To save the currently chosen settings as the default for new instances of Keyframe Toolbox, press the button at the bottom of the panel: **Save Current Settings as Default**. `New in v1.1`

<div style="padding:100% 0 0 0;position:relative;"><iframe src="https://player.vimeo.com/video/1173533429?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479" frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media; web-share" referrerpolicy="strict-origin-when-cross-origin" style="position:absolute;top:0;left:0;width:100%;height:100%;" title="KT 13 — Settings"></iframe></div><script src="https://player.vimeo.com/api/player.js"></script>

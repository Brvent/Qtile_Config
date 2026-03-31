import os
import subprocess
from libqtile import hook
from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import re

alt = "mod1"
mod = "mod4"
terminal = guess_terminal()

keys = [
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn("alacritty"), desc="Launch terminal"),
    
    #Launch rofi  menu and rofi windown 
    Key([mod],"m", lazy.spawn("rofi -show drun -show-icons -b "), desc="open rofi menu"),
    Key([mod,"control"], "m", lazy.spawn("rofi -show window"), desc="rofi window"  ),
    
    #Jupyter-lab, ide 
    Key([mod,alt],"j", lazy.spawn("jupyter lab")),

# Toggle between different layouts as defined below
   Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
   Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
   Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    #Volume control
    Key([],"XF86AudioMute",lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),
    Key([],"XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([],"XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),

    #Screen brightness control
    Key([],"XF86MonBrightnessDown",lazy.spawn("brightnessctl set 10%-")), 
    Key([],"XF86MonBrightnessUp",lazy.spawn("brightnessctl set +10%")),
   
    #open whatsapp/zapzap (alternative for linux)
    Key([alt],"w", lazy.spawn("zapzap"), desc="open zapzap"),
    
    #open Telegram-Desktop
    Key([alt],"t", lazy.spawn("Telegram"), desc="open telegram"),

    #browsers
    Key([mod,alt],"f", lazy.spawn("firefox"), desc = "open firefox"),
    Key([mod,alt],"b", lazy.spawn("brave"), desc = "open brave"),
    
    #temperature 
    Key([alt,"shift"], "r", lazy.spawn("redshift -O 2800"),desc="Night"),
    Key([alt,"shift"], "d", lazy.spawn("redshift -x"), desc="Day default"), 

    #file manager
    Key([mod], "h",lazy.spawn("thunar"),desc = "open files"),

    #Screen Layout editor
    Key([mod], "F4",lazy.spawn("arandr"), desc = "monitor config"),

    #open openRGB (mouse)
    Key([mod],"F3", lazy.spawn("openrgb"),desc="open RGB config"),
    
    #screenshot and save config
    Key([mod], "s", lazy.spawn("scrot 'screenshot_%Y-%m-%d-%T_$wx$h.png' -e 'mkdir -p ~/Pictures/screenshots/full-screenshots/ | mv $f ~/Pictures/screenshots/full-screenshots/'")),
    Key([mod, "shift"],"s", lazy.spawn("scrot -s 'screenshot_%Y-%m-%d-%T_$wx$h.png' -e 'mkdir -p ~/Pictures/screenshots/area-screenshots/ | mv $f ~/Pictures/screenshots/area-screenshots/'")),
]

#switch to group (workspace)
groups = [Group(i) for i in "12345"]

for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
        ]
    )

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"],
                   border_width=1,
                   border_focus="#DEDEDE"),
    layout.Max(border_focus="#FFFFFF",border_width=0),
    # Try more layouts by unleashing below layouts.
     # layout.Stack(num_stacks=3),
    # layout.Bsp(),
    # layout.Matrix(border_focus="#208E63" , border_with=3),
    # layout.MonadTall(border_focus ="#239fb9",border_width=4),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    # layout.floating.Floating(),
]

widget_defaults = dict(
    font="sans",
    fontsize=16,
    padding=3,
)
extension_defaults = widget_defaults.copy()


def parse_window_name(text):
    if '@' in text and '~' in text:
        return re.split(r'@', text)[-1].split(' ~')[0].strip()  
    return re.split(r' — | - ',text)[-1].strip()  

#Bar config 2 Screens
#principal
screens = [
      Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.WindowName(parse_text=parse_window_name),
                widget.Spacer(),
                widget.Chord(
                    chords_colors={
                         "launch": ("#ff0000", "#ffffff"),
                     },
                     name_transform=lambda name: name.upper(),
                 ),
                widget.TextBox("Screen", name="personalizado"),
                widget.Systray(),
                widget.Battery(low_foreground='FF0000', low_percentage =0.1,empty_char="x",
                    charge_char="+",format='{char} {percent:2.0%} {hour:d}:{min:02d} {watt:.2f} W',update_interval=1),
                widget.Backlight(backlight_name="intel_backlight", fmt="☀︎ {}",step=5,
                    change_command="light -S {0:.0f}" ),
                widget.Clock(format=' %H:%M:%S | %d/%m/%y', update_interval=0.05),
                widget.CPUGraph(background= "#222222",border_color="000000",graph_color="186539",frequency=0.05,
                 core="all",fill_color="186539"),
                 widget.CPU(),
                 widget.ThermalSensor(threshold=50.0,foreground_alert='ff0000',metric=True,update_interval=0.1),
                 widget.CheckUpdates(custom_command="checkupdates",update_interval=1800, display_format="Updates:{updates}", padding = 10, execute="lxterminal -e pacman -Syu"),
            ],
            28,
             background ="#0a0a0a",
             opacity=0.8,
        ),
    ),

   Screen(
    top=bar.Bar(
             [

            widget.CurrentLayout(),
            widget.GroupBox(),
            widget.WindowName(parse_text=parse_window_name),
            widget.Spacer(),
            widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_trasform=lambda name: name.upper(),
                ),
            widget.TextBox("Screen 2", name="personalizado"),
            widget.Battery(low_foreground='FF0000', low_percentage =0.1,empty_char="x",
            charge_char="+",format='{char} {percent:2.0%} {hour:d}:{min:02d} {watt:.2f} W',update_interval=1
                ),
            widget.Clock(format=' %H:%M:%S | %d/%m/%y', update_interval=0.05),
            widget.CPUGraph(background= "#222222",border_color="000000",graph_color="186539",frequency=0.05,
            core="all",fill_color="186539"),
            widget.CPU(),
            widget.ThermalSensor(threshold=50.0,foreground_alert='ff0000',metric=True,update_interval=0.1),
            widget.CheckUpdates(custom_command="checkupdates",update_interval=1800, display_format="Updates:{updates}", padding = 10, execute="lxterminal -e pacman -Syu"),
            
            ],
             28,
             background ="#0a0a0a",
             opacity=0.8,
             ),
  ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

#3D non-reparenting WM

wmname = "LG3D"

#file config autostart.sh

@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.run([script])
 


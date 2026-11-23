#!/usr/bin/env python3
"""Attach Keyframe Toolbox effects and edit their FCPXML parameters (2.0.1/2.1.0)."""

import argparse
import base64
import json
import plistlib
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from uuid import UUID

STANDARD = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
MOTION = "*-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
CLASS = "Keyframe_Toolbox_Renderer.ParameterGraphValue"
PREFIX = "9999/10003/10007/3/10021/20/"
UID = plistlib.UID
GRAPHS = {  # Graph ID -> (minimum, maximum, default at progress 0).
    "Keyframe Toolbox": {
        101: (0, 100, 100), 102: (-8000, 8000, 0), 103: (-8000, 8000, 0),
        104: (0, 2000, 100), 105: (-1440, 1440, 0), 106: (0, 500, 0),
        107: (-1440, 1440, 0), 108: (-1440, 1440, 0), 112: (0, 2000, 100),
        113: (0, 2000, 100),
    },
    "Keyframe Toolbox 360 Reframe": {
        101: (0, 100, 100), 102: (-720, 720, 0), 103: (-720, 720, 0),
        104: (1, 360, 120), 105: (-720, 720, 0), 106: (0, 500, 0), 111: (-100, 100, 0),
    },
    "Keyframe Toolbox Time Remap": {114: (0, 100, 0)},
}
REFRAME = "Keyframe Toolbox 360 Reframe"
TIME_REMAP = "Keyframe Toolbox Time Remap"
EFFECT_UIDS = {name: f"~/Effects.localized/Keyframe Toolbox/{name}/{name}.moef" for name in GRAPHS}
PROPERTY_IDS = {101: 1, 102: 2, 103: 3, 104: 4, 105: 5, 106: 6, 107: 7, 108: 8,
                111: 9, 112: 10, 113: 11, 114: 12}
PROJECTIONS = ("Rectilinear", "Wide/Panini", "Fisheye", "Stereographic", "Tiny Planet")
VIDEO_FILTER_HOSTS = {"asset-clip", "clip", "ref-clip", "sync-clip", "video", "title", "live-drawing"}


def keyed_archive(top, objects):
    return plistlib.dumps({"$version": 100000, "$archiver": "NSKeyedArchiver",
                           "$top": top, "$objects": objects},
                          fmt=plistlib.FMT_BINARY, sort_keys=False)


def encode_storage(state):
    data = json.dumps(state, allow_nan=False, separators=(",", ":")).encode("utf-8")
    inner = keyed_archive({"Custom Data": UID(1)}, [
        "$null", {"storageData": UID(2), "$class": UID(3)}, data,
        {"$classname": CLASS, "$classes": [CLASS, "NSObject"]},
    ])
    outer = keyed_archive({"BlindDataObject": UID(1), "DataIsLegacy": UID(2)},
                          ["$null", inner, False])
    packet = len(outer).to_bytes(8, "big") + b"*" + outer
    packet += bytes(-len(packet) % 3)
    return base64.b64encode(packet).decode("ascii").translate(str.maketrans(STANDARD, MOTION))


def decode_storage(text):
    encoded = "".join(text.split()).translate(str.maketrans(MOTION, STANDARD))
    packet = base64.b64decode(encoded, validate=True)
    end = 9 + int.from_bytes(packet[:8], "big")
    if packet[8:9] != b"*" or len(packet) != end + (-end % 3) or any(packet[end:]):
        raise ValueError("Invalid Motion archive length, type or padding")
    outer = plistlib.loads(packet[9:end])
    objects = outer["$objects"]
    if objects[outer["$top"]["DataIsLegacy"].data] is not False:
        raise ValueError("Expected a nonlegacy Toolbox archive")
    inner = plistlib.loads(objects[outer["$top"]["BlindDataObject"].data])
    objects = inner["$objects"]
    obj = objects[inner["$top"]["Custom Data"].data]
    if objects[obj["$class"].data]["$classname"] != CLASS:
        raise ValueError("Unexpected FxPlug custom parameter class")
    return json.loads(objects[obj["storageData"].data])


def default_graph(name, leaf):
    if leaf not in GRAPHS.get(name, {}):
        raise ValueError(f"{name} has no graph {leaf}")
    start = GRAPHS[name][leaf][2]
    end = 100 if leaf == 114 else start
    return {"version": 2, "isUserEdited": False, "beforeFirstKeyframeMode": "constant",
            "afterLastKeyframeMode": "constant", "points": [
                {"progress": 0, "value": start, "handlesBroken": False},
                {"progress": 1, "value": end, "handlesBroken": False},
            ]}


def template_settings(name, tag):
    # These are the actual Motion header values, including Time Remap's saved visibility [1].
    visibility, velocity, revision = {
        "Keyframe Toolbox": ([1, 2, 3, 4, 5], True, 14),
        REFRAME: ([2, 3, 4, 5], True, 1),
        TIME_REMAP: ([1], False, 0),
    }[name]
    seeded = name != "Keyframe Toolbox" or tag == "defaultVal"
    state = {
        "timingMode": "relative", "isSolidOutputEnabled": False, "isSeededDefault": seeded,
        "propertyVisibility": {"visibleParameterIDs": visibility},
        "userInterfaceSettings": {"isOSCEnabled": True, "isVelocityGraphEnabled": velocity,
                                  "isPlayheadMovementEnabled": True},
        "temporalBlurSettings": {"isEnabled": False, "shutterDurationFrames": 1, "shutterBias": "centered",
                                 "sampleCount": 8, "weightCurve": "gaussian", "affectsPosition": True,
                                 "affectsRotation": True, "affectsScale": True, "maxBlurClampPixels": 300},
    }
    if seeded:
        state["seededDefaultRevision"] = revision
    return state


def in_range(value, low, high):
    return type(value) in (int, float) and low <= value <= high


def patch_settings(state, changes, name):
    """Merge only supplied keys. Existing export fields, including unknown fields, survive."""
    template = template_settings(name, "dataValue")
    options = {"timingMode": ("relative", "absolute"), "shutterBias": ("centered", "trailing", "leading"),
               "weightCurve": ("box", "triangle", "gaussian")}
    allowed_ids = {PROPERTY_IDS[leaf] for leaf in GRAPHS[name]}

    def merge(current, patch, schema):
        if not isinstance(patch, dict):
            raise ValueError("Inspector settings and their sections must be JSON objects")
        for key, value in patch.items():
            if key in ("isSeededDefault", "seededDefaultRevision") and current is state:
                continue  # The plug-in treats an explicitly edited header as instance-specific.
            if key not in schema:
                if key in current and current[key] == value:
                    continue
                raise ValueError(f"Unknown inspector setting {key}")
            expected = schema[key]
            if isinstance(expected, dict):
                # TemporalBlurSettings decodes all its members as required when the section exists.
                section = current.get(key)
                if section is None:
                    section = expected.copy() if key == "temporalBlurSettings" else {}
                    current[key] = section
                if not isinstance(section, dict):
                    raise ValueError(f"Expected an object for {key}")
                merge(section, value, expected)
                continue
            if type(expected) is bool:
                valid = type(value) is bool
            elif key in options:
                valid = value in options[key]
            elif key == "visibleParameterIDs":
                valid = (isinstance(value, list) and all(type(v) is int for v in value)
                         and (value == current.get(key) or
                              (bool(value) and set(value) <= allowed_ids and len(set(value)) == len(value))))
            elif key == "sampleCount":
                valid = type(value) is int and 2 <= value <= 32
            else:
                valid = in_range(value, 0, {"shutterDurationFrames": 8, "maxBlurClampPixels": 10000}[key])
            if not valid:
                raise ValueError(f"Invalid inspector setting {key}: {value!r}")
            current[key] = value

    merge(state, changes, template)
    state["isSeededDefault"] = False
    state.pop("seededDefaultRevision", None)
    if name == "Keyframe Toolbox" and state == template:
        # Build 61 treats this exact five-ID ordering as a template seed even with the flag cleared.
        # The Inspector displays graphs in definition order, so the same set in another order pins the edit.
        state["propertyVisibility"]["visibleParameterIDs"] = [2, 1, 3, 4, 5]


def check_curve(state, name, leaf):
    low, high, _ = GRAPHS[name][leaf]
    for field in ("beforeFirstKeyframeMode", "afterLastKeyframeMode"):
        if state.get(field, "constant") not in ("constant", "pingPong", "progressive"):
            raise ValueError(f"Unknown {field}")
    if not isinstance(state["points"], list) or not state["points"]:
        raise ValueError("Supply at least one graph point")
    for field in ("displayLowerBound", "displayUpperBound", "anchorOffset", "activeDurationFrames",
                  "timingReferenceTimelineStartSeconds", "timingReferenceEffectiveDurationSeconds"):
        if state.get(field) is not None and type(state[field]) not in (int, float):
            raise ValueError(f"{field} must be numeric")
    previous = -1
    for point in state["points"]:
        x, y = point["progress"], point["value"]
        if not in_range(x, 0, 1) or x - previous <= 1e-6 or not in_range(y, low, high):
            raise ValueError(f"Invalid point order, progress or {name} value at {point}")
        if type(point.get("handlesBroken")) is not bool:
            raise ValueError("Each point requires a Boolean handlesBroken")
        group = point.get("linkedGroupID")
        if group is not None and str(UUID(group)) != group.lower():
            raise ValueError("Use a hyphenated UUID for linkedGroupID")
        for key, min_dx, max_dx in [("inHandle", -x, 0), ("outHandle", 0, 1 - x)]:
            handle = point.get(key)
            if handle is not None and not (
                in_range(handle["timeOffset"], min_dx, max_dx)
                and in_range(handle["valueOffset"], low - y, high - y)
            ):
                raise ValueError(f"Invalid {key} at progress {x}")
        previous = x


def new_channel(name, leaf, state, version="5.15"):
    oz = ET.Element("ozml", version=version)
    factory = ET.SubElement(oz, "factory", id="1", uuid="6f69a722e95c4b7a870bfb0345c9f167")
    for tag, text in [("description", "Channel"), ("manufacturer", "Apple"), ("version", "1")]:
        ET.SubElement(factory, tag).text = text
    flags = "81621221392" if name == "Keyframe Toolbox" else "12901744656"
    channel = ET.SubElement(oz, "parameter", name="", id=str(leaf), flags=flags)
    ET.SubElement(channel, "flags").text = flags
    ET.SubElement(channel, "numberOfKeypoints").text = "0"
    ET.SubElement(channel, "defaultVal").text = encode_storage(state)
    ET.SubElement(channel, "dataValue")
    return oz


def unpack_channel(param, leaf):
    encoded = "".join(param.attrib["value"].split())
    ozml = ET.fromstring(base64.b64decode(encoded, validate=True))
    channel = ozml.find(f"./parameter[@id='{leaf}']")
    if channel is None:
        raise ValueError(f"OZML channel does not match parameter ID {leaf}")
    return ozml, channel


def channel_storage(channel, tag):
    value = channel.findtext(tag)
    if not value:
        raise ValueError(f"Missing {tag} in OZML channel {channel.get('id')}")
    return decode_storage(value)


def graph_param(instance, leaf):
    key = PREFIX + str(leaf)
    matches = instance.findall(f"param[@key='{key}']")
    if len(matches) > 1:
        raise ValueError(f"Duplicate parameter key {key}")
    return matches[0] if matches else None


def projection_index(value):
    if isinstance(value, str):
        for index, title in enumerate(PROJECTIONS):
            if value.casefold() == title.casefold():
                return index
        # FCP exports pop-ups as "index (title)". The numeric index also works with localized titles.
        match = re.fullmatch(r"([0-4])(?: \([^\n]*\))?", value)
        if match:
            return int(match[1])
    if type(value) is int and 0 <= value < len(PROJECTIONS):
        return value
    raise ValueError("Projection must be 0–4 or one of: " + ", ".join(PROJECTIONS))


def read_graph(instance, name, leaf, tag="dataValue"):
    if leaf == 110 and name == REFRAME:
        param = graph_param(instance, leaf)
        if param is None or tag == "defaultVal":
            return PROJECTIONS[3]
        return PROJECTIONS[projection_index(param.attrib["value"])]
    factory = template_settings(name, tag) if leaf == 100 else default_graph(name, leaf)
    param = graph_param(instance, leaf)
    if param is None:
        return factory
    _, channel = unpack_channel(param, leaf)
    return channel_storage(channel, tag)


def set_graph(instance, name, leaf, changes, *, fcpxml_version="1.15", ozml_version=None):
    param = graph_param(instance, leaf)
    if leaf == 110 and name == REFRAME:
        if ozml_version is not None:
            raise ValueError("Projection is a scalar menu with no OZML version")
        index = projection_index(changes)
        if param is None:
            param = ET.SubElement(instance, "param", name="Projection", key=PREFIX + "110")
        elif any(isinstance(child.tag, str) for child in param):
            raise ValueError("Expected a static Projection parameter")
        elif "value" in param.attrib:
            previous = param.attrib["value"]
            if projection_index(previous) == index:
                return
            if previous.isdecimal():
                param.set("value", str(index))
                return
        param.set("value", f"{index} ({PROJECTIONS[index]})")
        return
    if not isinstance(changes, dict):
        raise ValueError("Supply a JSON object for a graph or inspector edit")
    if leaf != 100 and leaf not in GRAPHS[name]:
        raise ValueError(f"{name} has no editable parameter {leaf}")
    if param is not None:
        oz, channel = unpack_channel(param, leaf)
        state = channel_storage(channel, "dataValue")
        if ozml_version is not None:
            oz.set("version", ozml_version)
    else:
        version = tuple(int(n) for n in fcpxml_version.split("."))
        new_version = ozml_version or ("5.14" if version <= (1, 14) else "5.15")
        state = template_settings(name, "dataValue") if leaf == 100 else default_graph(name, leaf)
        factory = template_settings(name, "defaultVal") if leaf == 100 else state
        oz = new_channel(name, leaf, factory, new_version)
        channel = oz.find("parameter")
    if leaf == 100:
        patch_settings(state, changes, name)
    else:
        if state.get("version", 2) != 2 or changes.get("version", 2) != 2:
            raise ValueError("Expected Toolbox graph storage version 2")
        state.update(changes)
        state["version"] = 2
        state["isUserEdited"] = True
        check_curve(state, name, leaf)
    channel.find("dataValue").text = encode_storage(state)
    prolog = b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE ozxmlscene>\n'
    encoded = base64.b64encode(prolog + ET.tostring(oz, encoding="utf-8")).decode("ascii")
    if param is None:
        param = ET.SubElement(instance, "param", name="", key=PREFIX + str(leaf))
    param.set("value", encoded)


def xml_file(path):
    path = Path(path)
    return path / "Info.fcpxml" if path.suffix == ".fcpxmld" else path


def parse_project(source):
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True, insert_pis=True))
    root = ET.parse(xml_file(source), parser=parser).getroot()
    if root.tag != "fcpxml":
        raise ValueError(f"Expected an fcpxml document, found {root.tag}")
    return root


def toolbox_instances(root):
    names = {uid: name for name, uid in EFFECT_UIDS.items()}
    resources = {e.attrib["id"]: names[e.get("uid")] for e in root.findall("./resources/effect")
                 if e.get("uid") in names}
    return [(resources[f.get("ref")], f) for f in root.iter("filter-video") if f.get("ref") in resources]


def attach_effect(root, name, clip_name, project_name=None, occurrence=None):
    scope = root
    if project_name is not None:
        projects = [p for p in root.iter("project") if p.get("name") == project_name]
        if len(projects) != 1:
            raise ValueError(f"Expected one project named {project_name!r}, found {len(projects)}")
        scope = projects[0]
    resource_names = {r.get("id"): r.get("name") for r in root.findall("./resources/*") if r.get("id")}
    clips = [clip for clip in scope.iter() if clip.tag in VIDEO_FILTER_HOSTS and
             (clip.get("name") or resource_names.get(clip.get("ref"))) == clip_name]
    if not clips:
        raise ValueError(f"No clip that accepts a video filter matched {clip_name!r}")
    if (occurrence is None and len(clips) != 1) or (occurrence is not None and not 1 <= occurrence <= len(clips)):
        raise ValueError(f"Found {len(clips)} clips named {clip_name!r}. Select --project or --clip-occurrence 1…{len(clips)}.")
    clip = clips[(occurrence or 1) - 1]

    resources = root.find("resources")
    if resources is None:
        resources = ET.Element("resources")
        options = root.find("import-options")
        root.insert(0 if options is None else list(root).index(options) + 1, resources)
    refs = [e.attrib["id"] for e in resources.findall("effect") if e.get("uid") == EFFECT_UIDS[name]]
    filters = clip.findall("filter-video") + clip.findall("./filter-video-mask/filter-video")
    if any(f.get("ref") in refs for f in filters):
        return
    if refs:
        ref = refs[0]
    else:
        used = {e.attrib["id"] for e in root.iter() if "id" in e.attrib}
        number = 1
        while f"r{number}" in used:
            number += 1
        ref = f"r{number}"
        ET.SubElement(resources, "effect", id=ref, name=name, uid=EFFECT_UIDS[name])
    # Every supported DTD puts video filters after markers/sources and before these trailing elements.
    index = next((i for i, child in enumerate(clip) if child.tag in ("filter-audio", "metadata", "reserved")), len(clip))
    clip.insert(index, ET.Element("filter-video", ref=ref, name=name))


def select_instance(root, name, number):
    matches = [effect for profile, effect in toolbox_instances(root) if profile == name]
    if number is None and len(matches) == 1:
        return matches[0]
    if number is not None and 1 <= number <= len(matches):
        return matches[number - 1]
    raise ValueError(f"Found {len(matches)} {name} instances. Use inspect to identify the clip and --instance to select it.")


def inventory(root):
    parents = {child: parent for parent in root.iter() for child in parent}
    counts = {}
    entries = []
    for name, effect in toolbox_instances(root):
        counts[name] = counts.get(name, 0) + 1
        clip = parents[effect]
        if clip.tag == "filter-video-mask":
            clip = parents[clip]
        ancestry = []
        ancestor = clip
        while ancestor in parents:
            if ancestor.get("name"):
                ancestry.append(ancestor.get("name"))
            ancestor = parents[ancestor]
        entries.append({
            "effect": name, "instance": counts[name], "path": list(reversed(ancestry)),
            "clip": {k: clip.get(k) for k in ("name", "start", "offset", "duration") if k in clip.attrib},
            "storedGraphs": [leaf for leaf in GRAPHS[name] if graph_param(effect, leaf) is not None],
            "storedSettings": graph_param(effect, 100) is not None,
        })
    return entries


def write_project(root, destination, dtd=None):
    prolog = b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n'
    document = prolog + ET.tostring(root, encoding="utf-8") + b"\n"
    if dtd:
        subprocess.run(["xmllint", "--nonet", "--noout", "--dtdvalid", Path(dtd).resolve().as_uri(), "-"],
                       input=document, check=True)
    destination = xml_file(destination)
    with tempfile.NamedTemporaryFile(dir=destination.parent, delete=False) as temp:
        staged = Path(temp.name)
        try:
            temp.write(document)
            temp.flush()
            if destination.exists():
                staged.chmod(destination.stat().st_mode & 0o777)
            staged.replace(destination)
        finally:
            staged.unlink(missing_ok=True)


def main(source, name, leaf, change_file, destination, *, number=None, dtd=None, ozml_version=None, reveal=False):
    root = parse_project(source)
    effect = select_instance(root, name, number)
    leaf = int(leaf)
    changes = json.loads(Path(change_file).read_text(encoding="utf-8"))
    versions = {"fcpxml_version": root.attrib["version"], "ozml_version": ozml_version}
    if reveal and leaf not in GRAPHS[name]:
        raise ValueError("--reveal applies to graph IDs listed for this effect")
    set_graph(effect, name, leaf, changes, **versions)
    if reveal:
        settings = read_graph(effect, name, 100)
        # An older header can omit propertyVisibility. Swift then uses regularParameters' default.
        visibility = settings.get("propertyVisibility") or {}
        visible = visibility.get("visibleParameterIDs", [1, 2, 3, 4, 5, 7, 8, 6])
        allowed = {PROPERTY_IDS[i] for i in GRAPHS[name]}
        visible = list(dict.fromkeys(i for i in visible if i in allowed))
        property_id = PROPERTY_IDS[leaf]
        if property_id not in visible:
            visible.append(property_id)
        set_graph(effect, name, 100, {"propertyVisibility": {"visibleParameterIDs": visible}}, **versions)
    write_project(root, destination, dtd)


def cli():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    inspect = commands.add_parser("inspect", help="List clips, Toolbox effects and stored graph IDs")
    inspect.add_argument("source")
    read = commands.add_parser("read", help="Read a graph, inspector settings (100), or 360 Projection (110) as JSON")
    write = commands.add_parser("set", help="Edit a graph, inspector settings (100), or 360 Projection (110)")
    attach = commands.add_parser("attach", help="Attach a Toolbox effect to a named clip")
    projection = commands.add_parser("projection", help="Set the static 360 Reframe Projection menu")
    for command in (read, write, attach, projection):
        command.add_argument("source", help="FCPXML file or .fcpxmld bundle")
    for command in (read, write, attach):
        command.add_argument("effect", choices=list(GRAPHS))
    for command in (read, write):
        command.add_argument("row", type=int, help="Parameter ID from the guide")
    for command in (read, write, projection):
        command.add_argument("--instance", type=int, help="One-based occurrence of this effect from inspect")
    read.add_argument("--default", action="store_true", help="Read the factory reset value")
    write.add_argument("changes", help="JSON file with graph fields, nested settings, or a Projection title/index")
    write.add_argument("--ozml-version", choices=("5.14", "5.15"), help="Set the OZML version of the custom rows written")
    write.add_argument("--reveal", action="store_true", help="Also show this graph in this instance's Inspector")
    attach.add_argument("--clip", required=True, help="Exact clip name (or its resource name when unnamed)")
    attach.add_argument("--project", help="Limit clip selection to one named project")
    attach.add_argument("--clip-occurrence", type=int, help="One-based occurrence among matching clips in document order")
    projection.add_argument("mode", help="0–4 or " + ", ".join(PROJECTIONS))
    for command in (write, attach, projection):
        command.add_argument("destination", help="Output file or existing output bundle")
        command.add_argument("--dtd", help="Validate with this FCPXML DTD before saving (requires xmllint)")
    arguments = sys.argv[1:]
    # Accept the original guide's five-positional-argument edit command as well.
    if arguments and not arguments[0].startswith("-") and arguments[0] not in commands.choices:
        arguments = ["set", *arguments]
    args = parser.parse_args(arguments)
    try:
        if args.command == "set":
            main(args.source, args.effect, args.row, args.changes, args.destination,
                 number=args.instance, dtd=args.dtd, ozml_version=args.ozml_version, reveal=args.reveal)
            return
        root = parse_project(args.source)
        if args.command == "attach":
            attach_effect(root, args.effect, args.clip, args.project, args.clip_occurrence)
            write_project(root, args.destination, args.dtd)
            return
        if args.command == "projection":
            set_graph(select_instance(root, REFRAME, args.instance), REFRAME, 110, args.mode)
            write_project(root, args.destination, args.dtd)
            return
        if args.command == "inspect":
            result = inventory(root)
        else:
            effect = select_instance(root, args.effect, args.instance)
            result = read_graph(effect, args.effect, args.row, "defaultVal" if args.default else "dataValue")
        print(json.dumps(result, indent=2, allow_nan=False))
    except (OSError, ValueError, KeyError, TypeError, AttributeError, IndexError, ET.ParseError,
            plistlib.InvalidFileException, subprocess.CalledProcessError) as error:
        parser.exit(1, f"{parser.prog}: {error}\n")


if __name__ == "__main__":
    cli()

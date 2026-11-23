#!/usr/bin/env python3
"""Read and edit Keyframe Toolbox graph storage in FCPXML (2.1.0, Build 61)."""

import argparse
import base64
import json
import plistlib
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
        raise ValueError("Expected a Build 61 nonlegacy archive")
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


def in_range(value, low, high):
    return type(value) in (int, float) and low <= value <= high


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


def new_channel(name, leaf, state):
    oz = ET.Element("ozml", version="5.15")
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
        raise ValueError(f"OZML channel does not match graph ID {leaf}")
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
        raise ValueError(f"Duplicate graph key {key}")
    return matches[0] if matches else None


def read_graph(instance, name, leaf, tag="dataValue"):
    factory = default_graph(name, leaf)
    param = graph_param(instance, leaf)
    if param is None:
        return factory
    _, channel = unpack_channel(param, leaf)
    return channel_storage(channel, tag)


def set_graph(instance, name, leaf, changes):
    if not isinstance(changes, dict):
        raise ValueError("Graph changes must be a JSON object")
    state = default_graph(name, leaf)
    param = graph_param(instance, leaf)
    if param is not None:
        oz, channel = unpack_channel(param, leaf)
        state = channel_storage(channel, "dataValue")
    else:
        oz = new_channel(name, leaf, state)
        channel = oz.find("parameter")
    if state.get("version", 2) != 2 or changes.get("version", 2) != 2:
        raise ValueError("Expected Build 61 graph storage version 2")
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
    names = {f"~/Effects.localized/Keyframe Toolbox/{name}/{name}.moef": name for name in GRAPHS}
    resources = {e.attrib["id"]: names[e.get("uid")] for e in root.findall("./resources/effect")
                 if e.get("uid") in names}
    return [(resources[f.get("ref")], f) for f in root.iter("filter-video") if f.get("ref") in resources]


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
        })
    return entries


def main(source, name, leaf, change_file, destination, *, number=None, dtd=None):
    root = parse_project(source)
    effect = select_instance(root, name, number)
    changes = json.loads(Path(change_file).read_text(encoding="utf-8"))
    set_graph(effect, name, int(leaf), changes)
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


def cli():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    inspect = commands.add_parser("inspect", help="List clips, Toolbox effects and stored graph IDs")
    inspect.add_argument("source")
    read = commands.add_parser("read", help="Decode one graph as JSON")
    write = commands.add_parser("set", help="Apply graph changes to a project")
    for command in (read, write):
        command.add_argument("source", help="FCPXML file or .fcpxmld bundle")
        command.add_argument("effect", choices=list(GRAPHS))
        command.add_argument("graph", type=int, help="Graph ID from the parameter table")
        command.add_argument("--instance", type=int, help="One-based occurrence of this effect from inspect")
    read.add_argument("--default", action="store_true", help="Read the factory reset value")
    write.add_argument("changes", help="Graph changes in JSON")
    write.add_argument("destination", help="Output file or existing output bundle")
    write.add_argument("--dtd", help="Validate with this FCPXML DTD before saving (requires xmllint)")
    arguments = sys.argv[1:]
    # Accept the original guide's five-positional-argument edit command as well.
    if arguments and not arguments[0].startswith("-") and arguments[0] not in commands.choices:
        arguments = ["set", *arguments]
    args = parser.parse_args(arguments)
    try:
        if args.command == "set":
            main(args.source, args.effect, args.graph, args.changes, args.destination,
                 number=args.instance, dtd=args.dtd)
            return
        root = parse_project(args.source)
        if args.command == "inspect":
            result = inventory(root)
        else:
            effect = select_instance(root, args.effect, args.instance)
            result = read_graph(effect, args.effect, args.graph, "defaultVal" if args.default else "dataValue")
        print(json.dumps(result, indent=2, allow_nan=False))
    except (OSError, ValueError, KeyError, TypeError, AttributeError, IndexError, ET.ParseError,
            plistlib.InvalidFileException, subprocess.CalledProcessError) as error:
        parser.exit(1, f"{parser.prog}: {error}\n")


if __name__ == "__main__":
    cli()

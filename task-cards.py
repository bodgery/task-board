#!/usr/bin/env python3

import csv
import os
import matplotlib.font_manager as fontman
from PIL import ImageFont
from sys import argv

INCSV = argv[1]
OUTDIR = argv[2]

###############################################################################
## A bunch of templates
###############################################################################

FONT = "Arial"

TASK_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
     width="612px" height="792px" viewBox="0 0 612 792" enable-background="new 0 0 612 792" xml:space="preserve">

<g>
    {BACKGROUND}
    <text transform="matrix(1 0 0 1 9.75 28.29)" font-family="'MyriadPro-Regular'" font-size="24">{TITLE}</text>
    <text transform="matrix(1 0 0 1 18 50)" font-family="'MyriadPro-Regular'" font-size="14">
    {DESC}
    </text>
    <text transform="matrix(1 0 0 1 9.75 186)" font-family="'MyriadPro-Regular'" font-size="20">More info? Contact: {CONTACT}</text>
    {LABEL}
    <rect x="193" y="105" fill="#FFFFFF" stroke="#000000" stroke-width="3" stroke-miterlimit="10" width="231" height="63"/>
    <text transform="matrix(1 0 0 1 198 116.52)" font-family="'MyriadPro-Regular'" font-size="12">Your name:</text>
    {TIME_EST}
    {AREA}
</g>

</svg>
"""

RED_GRADIENT = """
    <linearGradient id="SVGID_1_" gradientUnits="userSpaceOnUse" x1="218.0005" y1="195" x2="218.0005" y2="1.989520e-13">
        <stop  offset="0" style="stop-color:#EE3026"/>
        <stop  offset="1" style="stop-color:#F9BAB9"/>
    </linearGradient>
"""

YELLOW_GRADIENT = """
    <linearGradient id="SVGID_1_" gradientUnits="userSpaceOnUse" x1="218.0005" y1="195" x2="218.0005" y2="1.989520e-13">
        <stop  offset="0" style="stop-color:#FFE400"/>
        <stop  offset="1" style="stop-color:#FDF5A6"/>
    </linearGradient>
"""

GREEN_GRADIENT = """
    <linearGradient id="SVGID_1_" gradientUnits="userSpaceOnUse" x1="218.0005" y1="195" x2="218.0005" y2="1.989520e-13">
        <stop  offset="0" style="stop-color:#24B34B"/>
        <stop  offset="1" style="stop-color:#ACD480"/>
    </linearGradient>
"""

RED_STROKE = "#BE1E2D"
YELLOW_STROKE = "#FFF200"
GREEN_STROKE = "#009444"

URGENT_LABEL = """
    <path opacity="0.5" fill="#FFFFFF" stroke="#000000" stroke-width="3" stroke-miterlimit="10" d="M300,19c0,-6.627 5.373,-12 12,-12h105c 6.627,0 12,5.373 12,12v2c0,6.627,-5.373,12,-12,12h-105c-6.627,0,-12,-5.373,-12,-12v-2z"/>
    <text transform="matrix(1 0 0 1 305 27.54)" font-family="'MyriadPro-Regular'" font-size="24">\xa1URGENT!</text>
"""

NEEDED_SOON_LABEL = """
    <path opacity="0.5" fill="#FFFFFF" stroke="#000000" stroke-width="3" stroke-miterlimit="10" d="M275,19c0,-6.627 5.373,-12 12,-12h130c 6.627,0 12,5.373 12,12v2c0,6.627,-5.373,12,-12,12h-130c-6.627,0,-12,-5.373,-12,-12v-2z"/>
    <text transform="matrix(1 0 0 1 280 27.54)" font-family="'MyriadPro-Regular'" font-size="24">Needed soon</text>
"""

COOL_IF_LABEL = """
    <path opacity="0.5" fill="#FFFFFF" stroke="#000000" stroke-width="3" stroke-miterlimit="10" d="M300,19c0,-6.627 5.373,-12 12,-12h105c 6.627,0 12,5.373 12,12v2c0,6.627,-5.373,12,-12,12h-105c-6.627,0,-12,-5.373,-12,-12v-2z"/>
    <text transform="matrix(1 0 0 1 305 27.54)" font-family="'MyriadPro-Regular'" font-size="24">So cool if...</text>
"""

BACKGROUND_TEMPLATE = """
    {GRADIENT}
    <path fill="url(#SVGID_1_)" stroke="{STROKE_COLOR}" stroke-width="5" stroke-miterlimit="10" d="M436,183c0,6.627-5.373,12-12,12H12
        c-6.627,0-12-5.373-12-12V12C0,5.373,5.373,0,12,0h412c6.627,0,12,5.373,12,12V183z"/>
"""

TIME_ESTIMATE_TEMPLATE = """
    <text transform="matrix(1 0 0 1 9.75 128)"><tspan x="0" y="0" font-family="'MyriadPro-Regular'" font-size="16">Should take: {EST}</tspan></text>
"""

AREA_TEMPLATE = """
    <text transform="matrix(1 0 0 1 9.75 148)"><tspan x="0" y="0" font-family="'MyriadPro-Regular'" font-size="16" font-weight="bold">Area: {AREA}</tspan></text>
"""

FONT_CACHE={}
def find_font_file(query):
    global FONT_CACHE

    query = query.lower()

    if query in FONT_CACHE:
        return FONT_CACHE[query]

    matches = list(filter(lambda path: query in
        str(os.path.basename(path)).lower(), fontman.findSystemFonts()))

    if len(matches) == 0:
        if os.path.isfile("/mnt/c/Windows/Fonts/ARIALN.TTF"):
            FONT_CACHE[query] = "/mnt/c/Windows/Fonts/ARIALN.TTF"
        elif os.path.isfile("/Library/Fonts/Arial Unicode.ttf"):
            FONT_CACHE[query] = "/Library/Fonts/Arial Unicode.ttf"
        else:
            raise ValueError("Cannot find font: " + query)
    else:
        FONT_CACHE[query] = matches[0]

    return FONT_CACHE[query]

def text_width(text, size):
    fontfile = find_font_file(FONT)
    font = ImageFont.truetype(fontfile, size)
    return font.getsize(text)[0]

def make_wrapped_desc(desc):
    HEIGHT = 16 #px
    WIDTH = 320 #px

    if len(desc) == 0:
        return ""

    # break the text into lines by adding words until we are about to be too
    # wide for the card; then, we add a new line.
    words = list(desc.split())
    lines = [""]
    while len(words) > 0:
        next_word = words.pop(0)

        if text_width(lines[-1] + next_word, 14) + 1 <= WIDTH:
            if len(lines[-1]) > 0:
                lines[-1] += " "
            lines[-1] += next_word
        else:
            lines.append(next_word)

    out = ""
    for i, line in enumerate(lines):
        out += """<tspan x="0" y="%d">%s</tspan>""" % (i * HEIGHT, line)

        # really if i >= 4, but we only want to print once...
        if i == 4:
            print("Description is too long: " + desc)

    return out

def construct_svg(urgency, title, time_est, contact, area, desc):
    stroke = None
    grad = None
    label = None
    if urgency == "urgent":
        stroke = RED_STROKE
        grad = RED_GRADIENT
        label = URGENT_LABEL
    elif urgency == "soon":
        stroke = YELLOW_STROKE
        grad = YELLOW_GRADIENT
        label = NEEDED_SOON_LABEL
    elif urgency == "nice":
        stroke = GREEN_STROKE
        grad = GREEN_GRADIENT
        label = COOL_IF_LABEL
    else:
        print("Unknown urgency")

    if text_width(title, 24) > 240:
        print("Title is too long: " + title)

    bg = BACKGROUND_TEMPLATE.format(STROKE_COLOR=stroke, GRADIENT=grad)
    time = TIME_ESTIMATE_TEMPLATE.format(EST=time_est)
    area = AREA_TEMPLATE.format(AREA=area)

    desc = make_wrapped_desc(desc)

    return TASK_TEMPLATE.format(BACKGROUND=bg, TITLE=title,
                                DESC=desc, CONTACT=contact,
                                LABEL=label, TIME_EST=time,
                                AREA=area) \
                        .replace("MyriadPro-Regular", FONT)

###############################################################################
## Generate task SVGs
###############################################################################

tasks = []

# Read CSV and produce SVG for each
with open(INCSV, newline='') as csvf:
    r = csv.DictReader(csvf)

    for i, row in enumerate(r):
        svg = construct_svg(row["Urgency"], row["Title"], row["Time Estimate"],
                row["Contact"], row["Area"], row["Description"])

        with open(OUTDIR + ("/%d.svg" % i), "w") as outf:
            outf.write(svg)

print("Created %d task cards." % (i+1))

import os
import re
import xml.etree.ElementTree as ET
from PIL import Image
dofus_local_path = f"{os.getenv('LOCALAPPDATA')}{os.sep}Ankama{os.sep}zaap{os.sep}dofus{os.sep}content{os.sep}themes"
dofus_roaming_path = f"{os.getenv('APPDATA')}{os.sep}Dofus"
xml_path = f'{dofus_local_path}{os.sep}darkStone{os.sep}colors.xml'

images = {
    'icon_key.png': (255, 0, 255, 255),
    'icon_star_selected.png': (255, 0, 255, 255),
    'icon_star_normal.png': (255, 0, 255, 255),
    'bg_light.png': (255, 255, 255, 255),
    'window_separator_black_horizontal.png': (0, 0, 0, 0),
    'pin_mark_red.png': (255, 0, 255, 255)
}

xml_elements = {
    'chat.bgColor': '0xFFFFFF'
}

css = {
    "small2.css": {
        "grey_p": {
            "color": "#000000"
        },
        "green": {
            "color": "#000000",
            "font-size": "19"
        },
        "p": {
            "font-size": "20"
        }
    },
    "chat.css": {
        "p": {
            "color": "#000000"
        },
        "p10_p": {
            "color": "#000000"
        },
        "p11_p": {
            "color": "#000000"
        },
        "p14_p": {
            "color": "#000000"
        }
    },
    "special.css": {
        "coord": {
            "color": "#FFFFFF"
        }
    }
}

dat_files = {
    'Berilia_ui_positions.dat': b'\n\x0bA497031794414a552435f90151ac3b54b\x01',
    'dofus.dat': b'\n\x0bA497031794414a552435f90151ac3b54b\x1fcacheMapEnabled\x03#hdvBlockPopupType\x06\x13Sometimes\x19allowHitAnim\x03\x1dshowNewMailBox\x02)optimizeMultiAccount\x03%useNewTacticalMode\x02#allowSpellEffects\x03!mapFiltersSearch\x04\x82\x00\x1fshowFinishMoves\x03\x17resetColors\x03!zoomOnMouseWheel\x02#showEveryMonsters\x02\x15fullScreen\x03\x19flashQuality\x04\x02\x17showMapGrid\x02\x1ballowAnimsFun\x03\x17showMiniMap\x03AforceDefaultTacticalModeTemplate\x03\x1fshowMiniMapGrid\x02\x1fshowMovePreview\x02\x1fconfirmItemDrop\x03!itemTooltipDelay\x04\x001useAdvancedSpellTooltips\x02\x17turnPicture\x03#spellTooltipDelay\x04\x00!showMovementArea\x02\x19resetUIHints\x03#toggleEntityIcons\x02#notificationsMode\x04\x01\x19dofusQuality\x04\x03-showOmegaUnderOrnament\x02!hideDeadFighters\x029notificationsDisplayDuration\x04\x03\x1fautoConnectType\x04\x01-askForQualitySelection\x02)hideSummonedFighters\x03-notificationsMaxNumber\x04\x05!resetUIPositions\x02#showNotifications\x02\x15mapFilters\x04\x8f^+notificationsPosition\x04\x03%resetNotifications\x03/showEsportNotifications\x02\x1fsmallScreenFont\x02%mapFilters_miniMap\x04\x8f^%creaturesFightMode\x02\x1dforceRenderCPU\x03\x17showUIHints\x02\x1bbigMenuButton\x021warnOnGuildItemAgression\x02\x01',
    'tiphon.dat': b'\n\x0bA497031794414a552435f90151ac3b54b\x1dpointsOverhead\x04\x01\x1bcreaturesMode\x04\x00#animationsInCache\x042#useAnimationCache\x02\x11auraMode\x04\x00+alwaysShowAuraOnFront\x02\x01'
}

# ::::::::::: ::::    ::::      :::      ::::::::  :::::::::: ::::::::
#     :+:     +:+:+: :+:+:+   :+: :+:   :+:    :+: :+:       :+:    :+:
#     +:+     +:+ +:+:+ +:+  +:+   +:+  +:+        +:+       +:+
#     +#+     +#+  +:+  +#+ +#++:++#++: :#:        +#++:++#  +#++:++#++
#     +#+     +#+       +#+ +#+     +#+ +#+   +#+# +#+              +#+
#     #+#     #+#       #+# #+#     #+# #+#    #+# #+#       #+#    #+#
# ########### ###       ### ###     ###  ########  ########## ########


def open_image(name):
    for root, dirs, files in os.walk(dofus_local_path):
        for file in files:
            if file == name:
                file_path = os.path.join(root, file)
                image = Image.open(file_path)
                return image, file_path


def paint_image(image, color: tuple):
    pixels = image.load()
    if color[3] == 255:
        color = color[:3]
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixels[i,j] = color


def resize_image(image_path: str, final_size):
    actual_size = os.path.getsize(image_path)
    if actual_size > final_size:
        raise Exception(f"Can't adjust image file size of {image_path.split(os.sep)[-1]}!! Please repair your Dofus files")
    with open(image_path, 'a') as image_file:
        image_file.write(" "*(final_size - actual_size))


def change_image(image_name: str, color: tuple):
    image, image_path = open_image(image_name)
    original_size = os.path.getsize(image_path)
    if color[3] == 255:
        image = Image.new(mode="RGB", size=image.size)
    else:
        image = Image.new(mode="RGBA", size=image.size)
    paint_image(image=image, color=color)
    image.save(image_path)
    resize_image(image_path=image_path, final_size=original_size)


def change_all_images():
    for image_name, color in images.items():
        change_image(image_name, color)


# :::    ::: ::::    ::::  :::
# :+:    :+: +:+:+: :+:+:+ :+:
#  +:+  +:+  +:+ +:+:+ +:+ +:+
#   +#++:+   +#+  +:+  +#+ +#+
#  +#+  +#+  +#+       +#+ +#+
# #+#    #+# #+#       #+# #+#
# ###    ### ###       ### ##########


def change_xml_colors():
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True, insert_pis=True))
    tree = ET.parse(xml_path, parser)
    root = tree.getroot()
    for entry in root.findall("entry"):
        key = entry.get('key')
        if key in xml_elements:
            entry.text = xml_elements.get(key)
    tree.write(xml_path, encoding="UTF-8", xml_declaration=True)


#  ::::::::   ::::::::   ::::::::
# :+:    :+: :+:    :+: :+:    :+:
# +:+        +:+        +:+
# +#+        +#++:++#++ +#++:++#++
# +#+               +#+        +#+
# #+#    #+# #+#    #+# #+#    #+#
#  ########   ########   ########

def open_css(name):
    for root, dirs, files in os.walk(dofus_local_path):
        for file in files:
            if file == name:
                file_path = os.path.join(root, file)
                css = open(file_path, 'r')
                return css, file_path


def edit_css(css_name):
    begin_rule_regex = re.compile(r'([\d\w]+)(?:\s+)?{')
    end_rule_regex = re.compile(r'(})')
    element_key_regex = re.compile(r'(?:\s+)?(.+)(?:\s+)?:')
    element_value_regex = re.compile(r':(?:\s+)?(.+)(?:\s+)?;')
    css_rules = css.get(css_name)
    css_file, css_path = open_css(css_name)
    css_lines = css_file.readlines()
    line_number = 0
    current_rule = None
    elements_to_change = None
    for line in css_lines:
        begin_rule = begin_rule_regex.search(line)
        end_rule = end_rule_regex.search(line)
        if end_rule:
            current_rule = None
            elements_to_change = None
        if begin_rule:
            current_rule = begin_rule.group(1)
            if current_rule in css_rules:
                elements_to_change = css_rules.get(current_rule)
        if current_rule in css_rules:
            element_key = element_key_regex.search(line)
            element_value = element_value_regex.search(line)
            if element_key and element_value:
                element_key = element_key.group(1)
                element_value = element_value.group(1)
                if element_key in elements_to_change:
                    css_lines[line_number] = line.replace(element_value, elements_to_change.get(element_key))
                    # print('replacing:',element_value,elements_to_change.get(element_key), current_rule, element_key, css_name)
        line_number += 1
    new_css_file = open(css_path, 'w')
    new_css_file.writelines(css_lines)


def change_css_files():
    for css_file in css:
        edit_css(css_file)


# :::::::::      ::: :::::::::::
# :+:    :+:   :+: :+:   :+:
# +:+    +:+  +:+   +:+  +:+
# +#+    +:+ +#++:++#++: +#+
# +#+    +#+ +#+     +#+ +#+
# #+#    #+# #+#     #+# #+#
# #########  ###     ### ###


def change_dat_files():
    for file_name, data in dat_files.items():
        with open(f'{dofus_roaming_path}{os.sep}{file_name}', 'wb') as dat_file:
            dat_file.write(data)


def replace_files():
    print('Changing images...', end='\r')
    change_all_images()
    print('Changing images   Ok')
    print('Changing xml files...', end='\r')
    change_xml_colors()
    print('Changing xml files   Ok')
    print('Changing css files...', end='\r')
    change_css_files()
    print('Changing css files   Ok')
    print('Changing dat files...', end='\r')
    change_dat_files()
    print('Changing dat files   Ok')


if __name__ == '__main__':
    replace_files()
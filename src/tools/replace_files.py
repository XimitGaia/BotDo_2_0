import os
import re
import xml.etree.ElementTree as ET
from PIL import Image

dofus_local_path = f"D:{os.sep}Ankama{os.sep}Dofus{os.sep}content{os.sep}themes"
# dofus_local_path = f"{os.getenv('LOCALAPPDATA')}{os.sep}Ankama{os.sep}zaap{os.sep}dofus{os.sep}content{os.sep}themes"
dofus_roaming_path = f"{os.getenv('APPDATA')}{os.sep}Dofus"
xml_path = f"{dofus_local_path}{os.sep}darkStone{os.sep}colors.xml"

images = {
    "icon_key.png": (255, 0, 255, 255),
    "icon_star_selected.png": (255, 0, 255, 255),
    "icon_star_normal.png": (255, 0, 255, 255),
    "bg_light.png": (255, 255, 255, 255),
    "window_separator_black_horizontal.png": (0, 0, 0, 0),
    "pin_mark_red.png": (255, 0, 255, 255),
    "pin_mark_yellow.png": (255, 0, 255, 255),
    "icon_bin_normal.png": (255, 0, 255, 255),
    "icon_hud_creature_mode.png": (0, 255, 255, 255),
    "background_info_enemy.png": (255, 255, 255, 255)
}

xml_elements = {"chat.bgColor": "0xFFFFFF"}

css = {
    "small2.css": {
        "grey_p": {"color": "#000000"},
        "green": {"color": "#000000", "font-size": "19"},
        "p": {"font-size": "20"},
    },
    "chat.css": {
        "p": {"color": "#000000"},
        "p10_p": {"color": "#000000"},
        "p11_p": {"color": "#000000"},
        "p14_p": {"color": "#000000"},
    },
    "special.css": {"coord": {"color": "#FFFFFF"}},
}

dat_files = {
    "Berilia_ui_positions.dat": b'\n\x0bA497031794414a552435f90151ac3b54bUexternalActionBar_0##pos##mainCtr##default\n#A7bf6e8b80251f468368b7225e05a69d1\x03x\x03y\x04\x00\x04\x007chat##pos##mainCtr##default\n\x05\x04\xff\xff\xfe\xf2\x04\x86w9chat##size##mainCtr##default\n\x05\x04\x85"\x04sUexternalActionBar_1##pos##mainCtr##default\n\x05\x04\x00\x04\x00UexternalActionBar_2##pos##mainCtr##default\n\x05\x04\x00\x04\x00UexternalActionBar_3##pos##mainCtr##default\n\x05\x04\x00\x04\x00\x01',
    "dofus.dat": b'\n\x0bA497031794414a552435f90151ac3b54b%useNewTacticalMode\x02\x1dshowNewMailBox\x02!hideDeadFighters\x02\x15mapFilters\x04\x8f^\x15fullScreen\x03/showEsportNotifications\x02\x1fsmallScreenFont\x02%mapFilters_miniMap\x04\x8f^-showOmegaUnderOrnament\x02\x1dforceRenderCPU\x03-notificationsMaxNumber\x04\x05\x1bbigMenuButton\x02\x1fcacheMapEnabled\x03#hdvBlockPopupType\x06\x13Sometimes\x17resetColors\x03\x17showUIHints\x02)optimizeMultiAccount\x03%creaturesFightMode\x03!mapFiltersSearch\x04\x82\x00+notificationsPosition\x04\x03\x1fautoConnectType\x04\x01\x17turnPicture\x03\x17showMiniMap\x03\x19dofusQuality\x04\x03#showEveryMonsters\x02\x19flashQuality\x04\x02\x17showMapGrid\x021warnOnGuildItemAgression\x02\x1ballowAnimsFun\x03#spellTooltipDelay\x04\xff\xff\xff\xffAforceDefaultTacticalModeTemplate\x03\x1fshowMiniMapGrid\x02#showNotifications\x02\x1fconfirmItemDrop\x03!zoomOnMouseWheel\x021useAdvancedSpellTooltips\x02#toggleEntityIcons\x02!showMovementArea\x02!itemTooltipDelay\x04\xff\xff\xff\xff\x1fshowMovePreview\x02%resetNotifications\x03#notificationsMode\x04\x01\x1fshowFinishMoves\x03!resetUIPositions\x02\x19allowHitAnim\x03\x19resetUIHints\x039notificationsDisplayDuration\x04\x03-askForQualitySelection\x02#allowSpellEffects\x03)hideSummonedFighters\x03\x01',
    "tiphon.dat": b"\n\x0bA497031794414a552435f90151ac3b54b\x1dpointsOverhead\x04\x01\x1bcreaturesMode\x04\x00#animationsInCache\x042#useAnimationCache\x02\x11auraMode\x04\x00+alwaysShowAuraOnFront\x02\x01",
    "chat.dat": b"\n\x0bA497031794414a552435f90151ac3b54b\x1bchannelColor0\x04\x00\x1dchannelColor10\x04\x00#smileysAutoclosed\x03\x1dchannelColor11\x04\x82\xbb\xff\x00\x1dchannelColor14\x04\x82\xbd\xc7\x9d!currentChatTheme\x06\x13darkStone'letLivingObjectTalk\x02\x13tabsNames\t\t\x01\x04\x00\x06\x031\x06\x032\x06\x033\x1bchannelColor1\x04\x83\xfe\x80l\x1bchannelColor5\x04\x82\xe6\xf8>\x1bchannelColor9\x04\x81\xfd\xc3\xff\x1bchannelColor4\x04\x83\xc9\x7f\x1bchannelColor3\x04\x83\xff\xadB\x1dchannelColor12\x04\x83\xde\xba>\x1bchannelColor8\x04\x83\xfe\x80\xff\x19chatFontSize\x04\x12\x1bchannelColor7\x04\x83\xa7\xaa\x07\x19filterInsult\x02\x1bchannelColor6\x04\x83\xc9\xa0\xd5\x1bchannelColor2\x04\x00\x1dchannelColor13\x04\x83\xe2\xe3\x92\x01",
    "atouin.dat": b'\n\x0bA497031794414a552435f90151ac3b54b#elementsIndexPath\x06Afile://content/maps/elements.ele#mapPictoExtension\x06\x07png\x19elementsPath\x06Cpak://content/gfx/world/gfx0.d2p|\x15jpgSubPath\x06\x07jpg!allowAnimatedGfx\x02!allowParticlesFx\x023tacticalModeTemplatesPath\x06_file://content/maps/tactical_mode_templates.bin)particlesScriptsPath\x06Afile://content/scripts/emitters/\x15pngSubPath\x06\x08\x1fgroundCacheMode\x04\x01\x1fhideBlackBorder\x02\x11mapsPath\x06;pak://content/maps/maps0.d2p|\x1fpngPathOverride\x06\x01\x0fswfPath\x065!config.gfx.path.world.swf\x01',
    "ComputerModule_Ankama_GameUiCore.dat": b'\n\x0bA497031794414a552435f90151ac3b54b)currentMainCtrHeight\x04\x82*+currentChatHeightMode\x04\x00\x01',
    "Module_Ankama_GameUiCore.dat": b"\n\x0bA497031794414a552435f90151ac3b54b'tacticModeActivated\x03\x01baTchatHistory\t\x1f_nHistoryIndex \x04`AbannerSpellsPageIndex41643475146\x04\x00\x01"
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
            pixels[i, j] = color


def resize_image(image_path: str, final_size):
    actual_size = os.path.getsize(image_path)
    if actual_size > final_size:
        raise Exception(
            f"Can't adjust image file size of {image_path.split(os.sep)[-1]}!! Please repair your Dofus files"
        )
    with open(image_path, "a") as image_file:
        image_file.write(" " * (final_size - actual_size))


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
        key = entry.get("key")
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
                css = open(file_path, "r")
                return css, file_path


def edit_css(css_name):
    begin_rule_regex = re.compile(r"([\d\w]+)(?:\s+)?{")
    end_rule_regex = re.compile(r"(})")
    element_key_regex = re.compile(r"(?:\s+)?(.+)(?:\s+)?:")
    element_value_regex = re.compile(r":(?:\s+)?(.+)(?:\s+)?;")
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
                    css_lines[line_number] = line.replace(
                        element_value, elements_to_change.get(element_key)
                    )
                    # print('replacing:',element_value,elements_to_change.get(element_key), current_rule, element_key, css_name)
        line_number += 1
    new_css_file = open(css_path, "w")
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
        with open(f"{dofus_roaming_path}{os.sep}{file_name}", "wb") as dat_file:
            dat_file.write(data)


def replace_files():
    print("Changing images...", end="\r")
    change_all_images()
    print("Changing images   Ok")
    print("Changing xml files...", end="\r")
    change_xml_colors()
    print("Changing xml files   Ok")
    print("Changing css files...", end="\r")
    change_css_files()
    print("Changing css files   Ok")
    print("Changing dat files...", end="\r")
    change_dat_files()
    print("Changing dat files   Ok")


if __name__ == "__main__":
    replace_files()

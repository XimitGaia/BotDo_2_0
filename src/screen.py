from tools.search import Search
import numpy as np
from PIL import Image
from PIL import ImageGrab
import time
import os
import pytesseract
import pyautogui
import win32gui


#proportioon Widht_screen/width_action_screen = 1.415
#proportion width_sction_screen/high_action_scrren = 1.255


class Screen:

    def __init__(self,mode = None):
        self.base_local_path = os.path.dirname(os.path.realpath(__file__))
        self.markers_path = f'{self.base_local_path}{os.sep}screen_markers{os.sep}'
        self.screen_size = None
        self.get_screen_size()
        self.game_active_screen = None
        self.get_game_active_screen()
        self.bottom_region = (0,
            round(0.65*self.screen_size[1]),
            self.screen_size[0],
            self.screen_size[1]
            )
        self.chat_input = None


    def get_screen_size(self):
        self.screen_size = ImageGrab.grab('').size

    def filter_markers_points(
        self,
        marker_size:tuple,
        match_list:list
    ):
        if len(match_list) == 0:
            return match_list
        posto = 0
        match_list = match_list
        for match in match_list[1:]:
            if abs(match_list[posto][0] - match[0]) < marker_size[0] and abs(match_list[posto][1] - match[1]) < marker_size[1]:
                match_list.remove(match)
            else:
                posto +=1
        return match_list
    
    def get_marked_area_or_points(
        self,
        marker_number:int,
        screen = '',
        marker:str = ''
    )->tuple:
        marker = Image.open(f'{self.markers_path}{marker}.png')
        screen = screen
        matches = self.filter_markers_points(
            marker_size=marker.size,
            match_list=Search.search_image(
                image=marker,
                screen=screen,
                match_tolerance=0.01,
                validator_group_porcentage=1,
                saturation_tolerance=0.01,
                bright_tolerance=0.01,          
            )
        )
        if len(matches) <= 1 and marker_number == 2:
            print('Marker not found')
            return None
        if marker_number == 1:
            if screen != '':
                return [(screen[0]+match[0],screen[1]+match[1]) for match in matches]
            return matches
        marked_area = (
            matches[0][0],
            matches[0][1],
            matches[-1][0],
            matches[-1][1]
        )
        if screen != '':
            marked_area = (
                marked_area[0]+screen[0],
                marked_area[1]+screen[1],
                marked_area[2]+screen[0], 
                marked_area[3]+screen[1] 
            )
        return marked_area
    

    def get_game_active_screen(self):#(x1,y1,x2,y2)
        screen_proportion = 0.704
        action_screen_proportion = 0.709
        width = self.screen_size[0]*screen_proportion
        X = (self.screen_size[0] - width)/2
        high = action_screen_proportion * width
        self.game_active_screen = (
            round(X),
            0,
            round(X+width),
            round(0+high)
        )

    def get_chat_input(self):
        region = self.get_marked_area_or_points(screen=self.bottom_region,marker_number=2,marker='chat_input_marker')
        central_point = ((region[0]+region[2])/2 , (region[1]+region[3])/2)
        self.chat_input = central_point
        
    # bring_character_to_front
    def window_enum_handler(self,hwnd, resultList):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != '':
            resultList.append((hwnd, win32gui.GetWindowText(hwnd)))

    def get_app_list(self,handles=[]):
        mlst=[]
        win32gui.EnumWindows(self.window_enum_handler, handles)
        for handle in handles:
            mlst.append(handle)
        return mlst

    def bring_character_to_front(self, name:str):
        appwindows = self.get_app_list()
        for i in appwindows:
            if name in i[1].lower():
                win32gui.SetForegroundWindow(i[0])


###################################################################################################
#  ________  ________  _________  _________  ___       _______           _____ ______   ________  ________  _______      
# |\   __  \|\   __  \|\___   ___\\___   ___\\  \     |\  ___ \         |\   _ \  _   \|\   __  \|\   ___ \|\  ___ \     
# \ \  \|\ /\ \  \|\  \|___ \  \_\|___ \  \_\ \  \    \ \   __/|        \ \  \\\__\ \  \ \  \|\  \ \  \_|\ \ \   __/|    
#  \ \   __  \ \   __  \   \ \  \     \ \  \ \ \  \    \ \  \_|/__       \ \  \\|__| \  \ \  \\\  \ \  \ \\ \ \  \_|/__  
#   \ \  \|\  \ \  \ \  \   \ \  \     \ \  \ \ \  \____\ \  \_|\ \       \ \  \    \ \  \ \  \\\  \ \  \_\\ \ \  \_|\ \ 
#    \ \_______\ \__\ \__\   \ \__\     \ \__\ \ \_______\ \_______\       \ \__\    \ \__\ \_______\ \_______\ \_______\
#     \|_______|\|__|\|__|    \|__|      \|__|  \|_______|\|_______|        \|__|     \|__|\|_______|\|_______|\|_______|
##################################################################################################

                                                                                                          
#################################### talvez obsoletos ########################################
    def get_timeline_marker(self,marker:str):
        non_filtred_markers = self.get_marked_area_or_points(marker_number=1,screen=self.timeline_region,marker= marker)
        filtred_markers = [position for position in non_filtred_markers if non_filtred_markers[0][0] == position[0] or abs(non_filtred_markers[0][0]-position[0]) > 5]
        filtred_markers.sort(key=lambda tup: tup[1])
        return filtred_markers
   
    def get_timeline_changed_position(self):
        positions_blue = self.get_timeline_marker(marker='timeline_enemy_marker')
        positions_red = self.get_timeline_marker(marker='timeline_ally_marker')
        all_positions = positions_blue + positions_red
        all_positions.sort(key=lambda tup: tup[1])
        max_position = max(all_positions,key=lambda tup: tup[0])
        if max_position[0] == min(all_positions,key=lambda tup: tup[0])[0]:
            return 'invocation'
        elif max_position in positions_blue:
            return all_positions.index(max_position),'blue'
        return all_positions.index(max_position), 'red'

    def get_fight_markers_regions(self)->dict:
            return {
                'res_region': self.get_marked_area_or_points(marker='res_marker',screen=self.bottom_region),
                'name_region': self.get_marked_area_or_points(marker='name_marker',screen=self.bottom_region),
                'hp_ap_mp_region': self.get_marked_area_or_points(marker='hp_ap_mp_marker',screen=self.bottom_region)
            }

    def text_res_table_on_screen(self,table_region:tuple)->str:
        region_image = ImageGrab.grab(table_region)
        return pytesseract.image_to_string(region_image,config='--psm 4 -c tessedit_char_whitelist=-%0123456789')



##################################### fim talvez obsoletos ########################################




    def text_hp_ap_mp_list_on_screen(self,region:tuple)->str:
        region_image = ImageGrab.grab(region)
        return pytesseract.image_to_string(region_image,config='--psm 6 -c tessedit_char_whitelist=-/0123456789')

    def get_timeline_region(self):
        return (self.game_active_screen[2],0,self.screen_size[0],self.screen_size[1])
####################################   Battle map_info #########################################
    def get_action_screen_y_step(self):
        return (self.game_active_screen[3]-self.game_active_screen[1])/41
    
    def get_action_screen_x_step(self):
        return (self.game_active_screen[2]-self.game_active_screen[0])/14.5

    def get_comparation_group(self,point: tuple)->list: #point = (x,y)
        comparation_group = []
        for y in range(point[1]-1,point[1]+2):
            for x in range(point[0]-1,point[0]+2):
                comparation_group.append((x,y))
        return comparation_group

    def get_battle_map_info(self):
        #variables to return
        team = None
        cells = []
        walls = []
        holes = []
        start_positions = []
        timeline_region = self.get_timeline_region()
        #end of variables
        #define step and get the screen image to compare
        step_x = self.get_action_screen_x_step()
        step_y = self.get_action_screen_y_step()
        y_start = step_y * 0.5 # make the poinst match 1/4 of the high of the losangle
        action_screen = ImageGrab.grab(self.game_active_screen)
        action_screen = np.array(action_screen)
        position_number = 0 # number of the cell
        self.y_range = list(np.arange(y_start,len(action_screen)-step_y,step_y))
        self.x_range_black = list(
            np.arange(
                step_x * 0.5,
                len(action_screen[0]),
                step_x
            )
        )
        self.x_range_white = list(
            np.arange(
                step_x,
                len(action_screen[0]),
                step_x
            )
        )
        x_range_color = self.x_range_black # start difference between withe losangle and black losangle
        for y in self.y_range:
            for x in x_range_color:
                comparation_group = self.get_comparation_group((round(x),round(y)))
                pixels = []
                for xcoord,ycoord in comparation_group:
                    pixels.append(list(action_screen[ycoord][xcoord]))
                #define the group of the cell
                if pixels[1:] == pixels[:-1]:# if all pixels are equal
                    if pixels[0] == [142, 134, 94] or pixels[0] == [150, 142, 103]:
                        cells.append(position_number)
                    elif pixels[0] == [0, 0, 0]:
                        holes.append(position_number)
                    elif pixels[0] == [88, 83, 58]:
                        walls.append(position_number)
                    elif pixels[0] == [221, 34, 0]:
                        cells.append(position_number)
                        team = 'red'
                        start_positions.append(position_number)
                    elif pixels[0] == [0, 34, 221]:
                        cells.append(position_number)
                        team = 'blue'
                        start_positions.append(position_number)
                    else:# enemy start positions
                        cells.append(position_number)
                else:
                    cells.append(position_number)
            #change the index of the position and the translation of the row
                position_number += 1
            if x_range_color == self.x_range_black:
                x_range_color = self.x_range_white
            else:
                x_range_color = self.x_range_black
        
        return {
            'cells': cells,
            'walls': walls,
            'holes': holes,
            'start_positions': start_positions,
            'team': team,
            'timeline_region': timeline_region
        }

    def map_to_screen(self, cell_number:int):
        ycoord = (cell_number//14)
        xcoord = cell_number - (ycoord*14)
        translation_x = self.game_active_screen[0]
        translation_y = self.game_active_screen[1]
        if ycoord%2 == 0:
            return (round(self.x_range_black[xcoord]+translation_x),round(self.y_range[ycoord]+translation_y))
        return (round(self.x_range_white[xcoord]+translation_x),round(self.y_range[ycoord]+translation_y))

    def get_occupied_cells(self):
        screen = ImageGrab.grab('')
        occupied_cells = []
        for cell in self.cells:
            point = self.map_to_screen(cell)
            if screen.getpixel(point) != (142, 134, 94) and screen.getpixel(point) != (150, 142, 103):
                occupied_cells.append(cell)
        return occupied_cells
################################### End of Battle map_info #######################################


# ad = time.time()
s = Screen()
print(s.get_marked_area_or_points())
# print(s.get_timeline_changed_position())
# print(time.time()-ad)
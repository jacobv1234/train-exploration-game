from tkinter import *
from time import sleep, perf_counter


# third party modules
# try-except no longer needed due to nuitka
# keep it in anyway for development purposes
try:
    from PIL import Image
    from pygame import mixer
except ModuleNotFoundError:
    print('You are missing required third-party Python extensions needed for the game to run.')
    choice = input('Install? (y/n) ')
    if choice == 'y':
        from os import system
        system('python -m pip install pillow pygame')
    else:
        exit()


# import objects
from lib.helper import Popup, get_unlocked_lines, get_bought_items, get_pos_save, save_pos, get_map_manifest
from lib.map import Map
from lib.train import Train
from lib.speedtracker import SpeedTracker
from lib.junction_choice import JunctionChoice
from lib.space_to_enter import PressSpaceToEnter
from lib.station_display import StationDisplay
from lib.mapnamedisplay import MapNameDisplay
from lib.passengers import Passengers
from lib.station_shop import ShopStation
from lib.homepage import Homepage
from lib.skin_select import SkinSelect
from lib.zoomed_map import ZoomedMap
from lib.audio import AudioHandler


window = Tk()
game_running = True
def close_program():
    global game_running
    game_running = False
window.protocol("WM_DELETE_WINDOW", close_program)

window.iconbitmap('icon.ico')
window.title('Untitled Train Game')

screen_width = window.winfo_screenwidth() - 10
screen_height = window.winfo_screenheight() - 75

window.state('zoomed')

# load map manifest for premade saves
map_manifest = get_map_manifest()


skin = 'Classic - Yellow'

# audio setup
print('Sounds licensed for free from zapsplat.com')
audiohandler = AudioHandler()
audiohandler.next_bg_music()

# homepage
save_path = 'savedata'
homepage = Homepage(window, screen_width, screen_height, skin)
choice = ''
while game_running:
    sleep(0.017)
    window.update()
    if choice != 'How to Play':
        homepage.update_cursor()
    if homepage.space_pressed:
        homepage.space_pressed = False
        choice = homepage.get_choice()
        if choice == 'Continue':
            # valid existing save
            if len(get_pos_save(save_path)) == 6:
                break
            else:
                choice = 'New Game'
        if choice == 'New Game':
            homepage.save_selection(map_manifest, screen_width, screen_height)
        elif choice == 'Back':
            homepage.remove()
            del homepage
            homepage = Homepage(window, screen_width, screen_height, skin)
        elif choice == 'How to Play':
            homepage.go_to_how_to_play()
        else:
            save_path = f'map/premade_saves/{choice}'
            break
homepage.remove()
del homepage


# skin selection
skin_selector = SkinSelect(window, screen_width, screen_height)
while game_running:
    sleep(0.017)
    window.update()
    if skin_selector.space_pressed:
        skin_selector.space_pressed = False
        skin = skin_selector.get_selected()
        break
skin_selector.remove()
del skin_selector

# within if to avoid crash when closed
if game_running:
    c = Canvas(window, width = screen_width, height = screen_height, bg = 'lightblue', xscrollincrement=1, yscrollincrement=1)
    c.place(x=4,y=0)

    # get savedata
    unlocked_lines = get_unlocked_lines(save_path)
    bought = get_bought_items(save_path)
    startx, starty, startdir, start_map, start_line, points = get_pos_save(save_path)
    points = int(points)

    # called area cause map is a function
    area = Map(start_map, c, unlocked_lines)
    
    # hud
    speedtracker = SpeedTracker(window,screen_width,screen_height)

    # train
    train = Train(int(startx), int(starty), int(startdir), start_line, c, skin)

    # center on screen
    c.xview_scroll(int(startx) - (round(screen_width / 2)), 'units')
    c.yview_scroll(int(starty) - (round(screen_height / 2)), 'units')

    # initialise certain variables
    junc = False
    press_space = False
    space_pressed = False
    in_station = False
    mapnamecounter = -1
    mapnamedisplay = False
    popup = False
    zoomed_map = False
    force_space = False
    chooser = False


    # passenger display
    passengers = Passengers(window, screen_height, save_path)


# functions that work better in main than in lib.helper
def pressed_space(event):
    global space_pressed
    space_pressed = True

def HandleMapNameCounter():
    global mapnamecounter, mapnamedisplay
    if mapnamecounter >= 0:
        mapnamecounter -= 1
        if mapnamecounter == 0:
            mapnamedisplay.remove()
            mapnamedisplay = False

def openMap(event):
    global zoomed_map
    train.disable_speed_controls(c)
    train.speed = 0
    zoomed_map = ZoomedMap(window, screen_width, screen_height, area, train.x, train.y, area.water_coords, area.scroll_boundary, passengers)
    c.unbind_all('<m>')
    c.bind_all('<m>', closeMap)
    c.unbind_all('<space>')

def closeMap(event):
    global zoomed_map
    zoomed_map.close()
    zoomed_map = False
    train.enable_speed_controls(c)
    c.unbind_all('<m>')
    c.bind_all('<m>', openMap)
    if chooser:
        chooser.re_enable_controls()
    if press_space:
        c.bind_all('<space>', pressed_space)

if game_running:
    c.bind_all('<m>', openMap)


# loop
while game_running:
    start = perf_counter()
    if not in_station:
        train.move_train(c)

        # check collisions with objects
        if train.speed != 0:
            corner = area.check_corners(train.x, train.y, train.line)
            if corner != 0:
                train.corner(corner)

        if junc != False:
            if junc['coords'][0] == train.x and junc['coords'][1] == train.y:
                train.junction(junc, chooser.options[chooser.choice])
                junc = False
                chooser.close()
                chooser = False
        
        stop = area.check_stops(train.x,train.y,train.line)
        if stop != 0 and not zoomed_map:
            train.stop(stop, c)

        junction = area.check_j_approach(train.x,train.y,train.direction, train.line)
        if junction != 0:
            chooser = JunctionChoice(junction,window,screen_width)
            junc = junction

        # loading zones
        lz = area.check_lz(train.x, train.y, train.direction)
        if lz != 0:
            area.unload(c)
            area = Map(lz['map'], c, unlocked_lines)
            # move train and camera
            # dir
            train.direction = lz['new_dir']
            # coords
            current_x = train.x
            current_y = train.y
            train.x = lz['new_pos'][0]
            train.y = lz['new_pos'][1]
            # camera
            scroll_x = train.x - current_x
            scroll_y = train.y - current_y
            c.xview_scroll(scroll_x, 'units')
            c.yview_scroll(scroll_y, 'units')
            # object
            c.move(train.object,scroll_x, scroll_y)
            c.tag_raise(train.object)
            # line
            train.line = lz['new_line']

            # name popup
            mapnamedisplay = MapNameDisplay(area.name, area.size, window, screen_height)
            mapnamecounter = 45
    

        # station entry
        station = area.check_stations(train.x, train.y, train.line)
        if station != 0 and train.speed == 0 and not press_space and not zoomed_map:
            press_space = PressSpaceToEnter(window, screen_width, screen_height)
            c.bind_all('<space>', pressed_space)
        elif train.speed != 0 and press_space:
            press_space.remove()
            c.unbind_all('<space>')
            del press_space
            press_space = False
        
        # initialise the station menu (in_station)
        if space_pressed:
            space_pressed = False
            train.disable_speed_controls(c)
            c.unbind_all('<m>')

            points_obtained = passengers.remove(f'{area.internal_name}/{station.name}')
            if points_obtained > 0:
                points += points_obtained
                plural = 's'
                if points_obtained == 1:
                    plural = ''

            if station.shop:
                in_station = ShopStation(window, screen_width, screen_height, station, points, unlocked_lines, bought, skin)
            else:
                in_station = StationDisplay(window, screen_width, screen_height, station, points, unlocked_lines, bought, skin) 
            
            if points_obtained > 0:
                if popup:
                    popup.remove()
                    popup = False
                popup = Popup(window, screen_width, f'Passenger{plural} Delivered!', f'You got {points_obtained} point{plural}!', 100)

    
    # handle station choices
    elif space_pressed and in_station:
        space_pressed = False
        result = in_station.select_current()
        if result[0] == 'Exit':
            # exit and move the train
            # dir
            out = station.exits[result[1]]
            if str(type(out)) == "<class 'int'>":
                train.direction = out
            else:
                train.direction = out[0]
                if out[1] != '':
                    train.line = out[1]
            # coords
            current_x = train.x
            current_y = train.y
            train.x = station.pos[0]
            train.y = station.pos[1]

            # special coords
            if str(type(out)) != "<class 'int'>":
                if len(out) >= 4:
                    train.x = out[2]
                    train.y = out[3]

                    # map change
                    if len(out) == 5:
                        area.unload(c)
                        area = Map(out[4],c,unlocked_lines)
                        mapnamedisplay = MapNameDisplay(area.name, area.size, window, screen_height)
                        mapnamecounter = 45
                        c.tag_raise(train.object)
                        passengers.remove('ALL')

            # camera
            scroll_x = train.x - current_x
            scroll_y = train.y - current_y
            c.xview_scroll(scroll_x, 'units')
            c.yview_scroll(scroll_y, 'units')

            # object
            c.move(train.object,scroll_x, scroll_y)

            # save
            with open('savedata/bought.txt', 'w') as f:
                [f.write(f'{obj}\n') for obj in bought]

            with open('savedata/unlocked_lines.txt', 'w') as f:
                [f.write(f'{obj}\n') for obj in unlocked_lines]

            save_pos(train.x,train.y,train.direction,area.internal_name,train.line,points)

            passengers.save()

            # exit the menu
            in_station.close()
            del in_station
            in_station = False
            train.enable_speed_controls(c)
            c.bind_all('<m>', openMap)
        
        elif result[0] == 'Passengers':
            if result[1] != 0:
                in_station.passenger = passengers.add(result[1])
            else:
                in_station.passenger = 1
            in_station.change_tab()

        elif result[0] == 'Shop':
            purchase = in_station.station.shop[result[1]]
            if purchase['cost'] > points:
                if popup:
                    popup.remove()
                    popup = False
                popup = Popup(window, screen_width, f'Too expensive!', f'You can\'t afford that...', 100)
            
            else:
                # take points
                points -= purchase['cost']

                # add to lists
                bought.append(purchase['unique_name'])
                [unlocked_lines.append(section) for section in purchase['unlock'] if section not in unlocked_lines]
                station.reload_exits(unlocked_lines)
                
                # reload map and close station screen - originally reloaded but doesn't anymore to fix the Amelia Underground Crash
                area.unload(c)
                area = Map(area.internal_name, c, unlocked_lines)

                in_station.close()
                del in_station
                in_station = False
                train.enable_speed_controls(c)
                c.bind_all('<m>', openMap)
                
                # train layering
                c.tag_raise(train.object)

                # force a space input to re-open the station window - effectively a reload
                force_space = True


                # success popup
                if popup:
                    popup.remove()
                    popup = False
                popup = Popup(window, screen_width, f'Route Unlocked!', f'New track has been built.', 150)

                # save
                with open('savedata/bought.txt', 'w') as f:
                    [f.write(f'{obj}\n') for obj in bought]

                with open('savedata/unlocked_lines.txt', 'w') as f:
                    [f.write(f'{obj}\n') for obj in unlocked_lines]

                save_pos(train.x,train.y,train.direction,area.internal_name,train.line,points)

                passengers.save()



    # update HUD
    match train.speed:
        case 0:
            destination = 280
        case 1:
            destination = 200
        case 2:
            destination = 120
        case 4:
            destination = 40
    speedtracker.update(destination)

    try:
        chooser.update()
    except: pass

    if in_station:
        if in_station.cursor:
            in_station.update_cursor()

    if popup:
        timer = popup.countdown()
        if timer == 0:
            popup = False

    # forced space input
    if force_space:
        space_pressed = True
        force_space = False


    HandleMapNameCounter()
    window.update()
    
    end = perf_counter()
    diff = end - start
    if diff < 0.017:
        sleep(0.017 - diff)
import numpy as np
import math

def main(obj, map_size=11, screen_size=[1080, 1920]):
    '''
    1920*1080: 175*99
    0:無物件
    1:地板
    2:繩子
    3:玩家
    4:怪物
    '''
    # 繪製地圖
    def drawing_map(map, objs):
        if len(objs)<=0: # 判斷是否有該物件
            return map
        # 繪製
        for obj in objs:
            #取得與矯正數值
            label = obj['label'] 
            coordinates = obj['coordinates'] 
            y1, x1, y2, x2 = coordinates
            y1, x1, y2, x2 = math.ceil(y1/map_size), math.ceil(x1/map_size), math.ceil(y2/map_size), math.ceil(x2/map_size)
            #繪製
            map[x1:x2, y1:y2] = 1 if label.find('Ground')!=-1 else 2

        return map

    # 繪製生物
    def drawing_obj(map, objs):
        if len(objs)<=0: # 判斷是否有該物件
            return map
        # 繪製
        for obj in objs:
            #取得與矯正數值
            label = obj['label'] 
            coordinates = obj['center'] 
            if label == '0':
                continue
            y, x = coordinates
            y, x  = math.ceil(y/map_size), math.ceil(x/map_size)+1

            #繪製
            map[x, y] = 3 if label.find('Player')!=-1 else 4

        return map


    #
    Monster = obj['Monster']
    Player = obj['Player']
    Ground = obj['Ground']
    Ladder = obj['Ladder']
    # 初始化地圖
    corrent_map = np.zeros((math.ceil(screen_size[0]/map_size), 
                            math.ceil(screen_size[1]/map_size))).astype('uint8')
    # 繪製地圖
    corrent_map = drawing_map(corrent_map, Ground)
    corrent_map = drawing_map(corrent_map, Ladder)
    corrent_map = drawing_obj(corrent_map, Monster)
    corrent_map = drawing_obj(corrent_map, Player)

    return corrent_map



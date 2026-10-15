import math
def main(obj):
    '''
    用於整理Yolo取得的標籤
    Input:
    obj: list with dict, Yolo的檢測結果，dict結構為{'label(string)': 'label', 'coordinates(float)': [x1, y1, x2, y2]}
    Output:
    dict: dict 
    '''
    def process_label(obj):
        '''
        用於整理Yolo取得的標籤
        Input:
        obj: list with dict, Yolo的檢測結果，dict結構為{'label(string)': 'label', 'coordinates(float)': [x1, y1, x2, y2]}
        Output:
        processed_obj: list with dict 
        '''
        # 處理邏輯：保留 Player 和 Ground，其餘的 label 轉為 monster
        processed_obj = []
        for item in obj:
            label = item['label']
            if label.startswith('Player') or label.startswith('Ground') or label.startswith('Ladder'):
                processed_obj.append(item)
                continue
            # 將其他標籤改為 monster
            confidence = label.split()[-1]  # 提取置信度
            item['label'] = f"Monster {confidence}"
            processed_obj.append(item)
        
        return processed_obj

    def get_center(obj):
        '''
        計算各個物件之中心點
        Input:
        obj: list with dict, Yolo的檢測結果，dict結構為{'label(string)': 'label', 'coordinates(float)': [x1, y1, x2, y2]}
        Output:
        center_obj: list with dict 
        '''
        center_obj = []
        for i in obj:
            coordinate = i['coordinates']
            center_y = (coordinate[0]+coordinate[2])/2
            center_x = (coordinate[1]+coordinate[3])/2
            center_obj.append({'label': i['label'],
                            'center': (center_y, center_x),
                            'coordinates': i['coordinates'],})
        return center_obj

    def find_item(obj, target, pop=True): # Pop是否要將找到的目標移除，Treu:移除
        '''
        計算各個物件之中心點
        Input:
        obj: list with dict, Yolo的檢測結果，dict結構為{'label(string)': 'label', 'coordinates(float)': [x1, y1, x2, y2]}
        target: string, 檢測目標之標籤
        pop: boolean, 檢測到指定目標時，是否要在結束時將目標從obj中移除，True: 移除(預設), False: 不移除
        Output:
        obj: list with dict 
        list_target: list with dict, target檢測目標
        '''
        list_target = []
        target_index = []
        len_obj = len(obj)
        for i in range(0, len_obj):
            if not obj[i]['label'].startswith(target): # 檢測目標
                continue
            list_target.append(obj[i])
            target_index.append(i)
        if pop:
            target_index.reverse()
            for i in target_index:
                obj.pop(i)
        return obj, list_target

    def cal_distance(obj_player, obj_moster):
        '''
        計算各個物件之中心點
        Input:
        obj_player: list with dict, 玩家資料，當有多個玩家時，只判定第一位玩家
        obj_moster: string, 怪物資料
        Output:
        distance: list with dict 
        '''
        #
        distance = [{'label':'0',
                     'distance': 99999,
                     'center': [0, 0],
                     'coordinates':'0'}]
        #

        if len(obj_moster)<1:
            return distance
        if len(obj_player)<1:
            return distance
        #
        x_p, y_p = obj_player[0]['center']
        for i in obj_moster:
            x, y = i['center']
            corrent_distance = math.sqrt(pow(y_p-y, 2)+pow(x_p-x, 2))
            if corrent_distance>distance[0]['distance']: # 檢查是否為最近的怪物
                continue
            distance[0] = ({'label':i['label'],
                            'distance': math.sqrt(pow(y_p-y, 2)+pow(x_p-x, 2)),
                            'center':i['center'],
                            'coordinates':i['coordinates']})

        return distance

    # 處理標籤格式
    processed_obj = process_label(obj)
    # 取得各個物件中心點
    center_obj = get_center(processed_obj)
    # 分類物件類別
    center_obj, list_player = find_item(obj=center_obj, target='Player', pop=True)
    center_obj, list_ground = find_item(obj=center_obj, target='Ground', pop=True)
    center_obj, list_ladder = find_item(obj=center_obj, target='Ladder', pop=True)
    # 計算怪物距離
    monster_distance = cal_distance(list_player, center_obj)            


    return {'Monster':monster_distance,
            'Player':list_player,
            'Ground':list_ground,
            'Ladder':list_ladder,}

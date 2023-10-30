import cv2
import numpy as np
from PIL import Image
import sys

TATE = 0
YOKO = 0 

color2 = {
    '\U0001F7E5':[248, 49, 47], #red
    '\U0001F7E6':[0, 166, 237], #blue
    '\U0001F7E7':[255, 103, 35],#orange
    '\U0001F7E8':[255, 176, 46],#yelllow
    '\U0001F7E9':[0, 210, 106], #green
    '\U0001F7EA':[199, 144, 241],#purple
    '\U0001F7EB':[165, 105, 83],#brown
    '\U00002B1B':[0, 0, 0],#black
    '\U00002B1C':[255, 255, 255],#white
}

color3 = {
    (248, 49, 47):'\U0001F7E5',
    (0, 166, 237):'\U0001F7E6',
    (255, 103,35):'\U0001F7E7',
    (255, 176,46):'\U0001F7E8',
    (0, 210, 106):'\U0001F7E9',
    (199,144,241):'\U0001F7EA',
    (165, 105,83):'\U0001F7EB',
    (0, 0, 0   ):'\U00002B1B',
    (255,255,255):'\U00002B1C',
}

color4: dict[str, list[int]] = {
    '\U0001F7E5':[47, 49, 248], #red
    '\U0001F7E6':[237, 166, 0], #blue
    '\U0001F7E7':[35, 103,255 ],#orange
    '\U0001F7E8':[46, 176, 255],#yelllow
    '\U0001F7E9':[106, 210, 0], #green
    '\U0001F7EA':[241, 144, 199],#purple
    '\U0001F7EB':[83, 105, 165],#brown
    '\U00002B1B':[0, 0, 0],#black
    '\U00002B1C':[255, 255, 255],#white
}

color5 = {
    (47, 49, 248):'\U0001F7E5',
    ( 237, 166,0):'\U0001F7E6',
    (35, 103,255):'\U0001F7E7',
    (46, 176,255):'\U0001F7E8',
    (106, 210, 0):'\U0001F7E9',
    (241,144,199):'\U0001F7EA',
    (83, 105,165):'\U0001F7EB',
    (0, 0, 0   ):'\U00002B1B',
    (255,255,255):'\U00002B1C',
}


# 新しい辞書を作成し、各値をndarrayに変換
color2_as_numpy = {k: np.array(v) for k, v in color4.items()}

def split_image_into_grid(image, n):
    height, width, _ = image.shape
    base_grid_num = n
    scaled_image = image
    height_grid_num = 0
    width_grid_num = 0
    
    print(height,width)
    
    scaling_factor = 10
    scaled_image = cv2.resize(scaled_image, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_CUBIC)
    height, width, _ = scaled_image.shape

    if(width>height):
        height_grid_num = base_grid_num
        grid_size = height // base_grid_num
        width_grid_num = width // grid_size
    
    else:
        width_grid_num = base_grid_num
        grid_size = width // base_grid_num
        height_grid_num = height // grid_size

    print(grid_size,height_grid_num,width_grid_num)

    grid_images = []
    for i in range(height_grid_num):
        for j in range(width_grid_num):
            x1, y1 = j * grid_size, i * grid_size
            x2, y2 = (j + 1) * grid_size, (i + 1) * grid_size
            grid = scaled_image[y1:y2, x1:x2]
            grid_images.append(grid)

    print(grid_size,height_grid_num,width_grid_num)

    global TATE 
    global YOKO

    TATE = height_grid_num
    YOKO = width_grid_num

    return grid_images

def get_average_color(image):
    return np.mean(image, axis=(0, 1))

def find_closest_emoji(average_color, emoji_list):
    
    closest_emoji = None
    min_distance = float('inf')

    for rgb in emoji_list.values():
        distance = np.linalg.norm(average_color - rgb)

        if distance < min_distance:
            min_distance = distance
            closest_emoji = rgb

    return closest_emoji

def make_emoji_list(grid_images):
    result = []
    for grid in grid_images:
        average_color = get_average_color(grid)
        closest_emoji = find_closest_emoji(average_color, color2_as_numpy)
        result.append(closest_emoji)

    result_emoji = []
    for a in result:
        result_emoji.append(color5[tuple(a)])
    return result_emoji

def output_emoji(args, result_emoji_list):
    output_path = output_path = r'C:\Users\kanae\Desktop\hobbyprogram\image2emojisquare'+"\\" + args[1] + '.txt'
    with open(output_path, 'w', encoding='utf-8') as file:
        sys.stdout = file
        print_emoji(result_emoji_list)
    sys.stdout = sys.__stdout__

def print_emoji(result_emoji):
    
    for i in range(TATE*YOKO):
        print(result_emoji[i],end="")
        if((i+1)%YOKO==0):
            print("")

def image2emoji(image):
    grid_size = 100  

    # 画像を読み込む
    # PillowのImageオブジェクトをNumPyの配列に変換
    image_np = np.array(image)
    # NumPyの配列をcv2で読み込む
    cv2_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)  # カラー画像の場合
    # image = cv2.imread(args[1], cv2.IMREAD_UNCHANGED)

    #画像をgridに切り分ける
    grid_images = split_image_into_grid(cv2_image, grid_size)

    # 各格子に対して最も近い絵文字を選択
    result_emoji_list = make_emoji_list(grid_images)

    return result_emoji_list

    # emojistring =  "".join(result_emoji_list)

    # return jsonify({'result': emojistring})
    # return jsonify({'result': "aaa"})


#==================================

def main ():
    
    args = args = sys.argv
    grid_size = 100  

    # 画像を読み込む
    image = cv2.imread(args[1], cv2.IMREAD_UNCHANGED)

    #画像をgridに切り分ける
    grid_images = split_image_into_grid(image, grid_size)

    # 各格子に対して最も近い絵文字を選択
    result_emoji_list = make_emoji_list(grid_images)

    #結果の絵文字のtxtを出力
    output_emoji(args, result_emoji_list)



if __name__ == "__main__":
    args = args = sys.argv
    main()
    print(color2)

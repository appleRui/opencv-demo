import cv2

def draw_number_near_rectangle(image, rectangle_coords, number, color, font_scale=1, thickness=2):
    """
    画像に四角形の中心に数字を描きます。

    Parameters:
    image (np.ndarray): 画像データ。
    rectangle_coords (tuple): 四角形の座標 (x, y, w, h)。
    number (str): 描画する数字。
    color (tuple): 数字の色 (B, G, R)。
    font_scale (float): フォントのスケール。
    thickness (int): 数字の太さ。

    Returns:
    np.ndarray: 数字が描かれた画像データ。
    """
    x, y, w, h = rectangle_coords
    # 四角形の中心座標を計算
    center_x = x + w // 2
    center_y = y + h // 2
    
    # フォントの種類
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # 文字列のサイズを取得
    text_size, _ = cv2.getTextSize(number, font, font_scale, thickness)
    text_width, text_height = text_size
    
    # 文字列を描画するための位置を調整
    text_x = center_x - text_width // 2
    text_y = center_y + text_height // 2
    
    # 画像に数字を描く
    cv2.putText(image, number, (text_x, text_y), font, font_scale, color, thickness)
    
    return image

def draw_rectangle_on_image(image, rectangles, color, thickness):
    """
    画像に複数の四角形の線を描き、それぞれの近くにループの数に応じた数字を描きます。

    Parameters:
    image (np.ndarray): 画像データ。
    rectangles (list): 複数の四角形の座標のリスト [(x, y, w, h)]。
    color (tuple): 線の色 (B, G, R)。
    thickness (int): 線の太さ。

    Returns:
    np.ndarray: 四角形の線が描かれた画像データ。
    """
    for index, rectangle_coords in enumerate(rectangles, start=1):
        x, y, w, h = rectangle_coords
        # 四角形の線を描く
        cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)
        # 四角形の近くにループの数に応じた数字を描く
        draw_number_near_rectangle(image, rectangle_coords, str(index), color)
    return image

def process_image(image, rectangles, color, thickness):
    """
    複数の四角形の線を引いた画像を処理します。

    Parameters:
    image (np.ndarray): 画像データ。
    rectangles (list): 複数の四角形の座標のリスト [(x, y, w, h)]。
    color (tuple): 線の色 (B, G, R)。
    thickness (int): 線の太さ。

    Returns:
    np.ndarray: 処理された画像データ。
    """
    return draw_rectangle_on_image(image, rectangles, color, thickness)

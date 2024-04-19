import cv2

def crop_image(image, rectangle_coords):
    """
    画像を指定された四角形の座標に基づいてクロップします。

    Parameters:
    image (np.ndarray): 画像データ。
    rectangle_coords (tuple): 四角形の座標 (x, y, w, h)。

    Returns:
    np.ndarray: クロップされた画像データ。
    """
    x, y, w, h = rectangle_coords
    # 画像のクロップ
    cropped_image = image[y:y + h, x:x + w]
    return cropped_image

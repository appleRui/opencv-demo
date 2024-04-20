/* eslint-disable */
import { ChangeEvent, useState } from 'react';

// APIリクエストデータを作成
const rectangles = [
    [50, 247, 100, 50],  // 四角形1 (x, y, w, h)
    [178, 256, 100, 50],  // 四角形2 (x, y, w, h)
    [310, 254, 100, 50],  // 四角形3 (x, y, w, h)
    [460, 261, 100, 50],  // 四角形4 (x, y, w, h)
    // 必要に応じて他の四角形座標を追加できます
];

export default function Home() {
    const [image, setImage] = useState<string | null>(null);
    const [resultImage, setResultImage] = useState(null);
    const [croppedImages, setCroppedImages] = useState<string[] | null>([]); // 複数のクロップされた画像のリスト

    
    const handleImageChange = (e: ChangeEvent<HTMLInputElement>): void => {
        const file = e.target.files?.[0];
        if (file) {
            // 画像を読み込むためのFileReaderを作成
            const reader = new FileReader();
            reader.onloadend = async () => {
                if (typeof reader.result === 'string') {
                    // 画像データをbase64形式で取得
                    const imageData = reader.result;

                    // リサイズされた画像データを取得
                    const resizedImage = await resizeImage(imageData);

                    // リサイズされた画像データをセット
                    setImage(resizedImage);
                }
            };
            reader.readAsDataURL(file);
        }
    };

    // 画像をリサイズする関数
    const resizeImage = async (imageData: string): Promise<string> => {
        // <img> 要素を作成
        const img = new Image();
        img.src = imageData;

        // <img> 要素がロードされるのを待つ
        await new Promise((resolve) => {
            img.onload = resolve;
        });

        // 元の画像の幅と高さを取得
        const originalWidth = img.width;
        const originalHeight = img.height;

        // 目標とする横幅
        const targetWidth = 720;

        // アスペクト比を保持しつつ目標とする高さを計算
        const targetHeight = (originalHeight / originalWidth) * targetWidth;

        // <canvas> 要素を作成
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');

        // <canvas> のサイズを設定
        canvas.width = targetWidth;
        canvas.height = targetHeight;

        // 画像を <canvas> に描画
        ctx?.drawImage(img, 0, 0, targetWidth, targetHeight);

        // リサイズされた画像データを base64 形式で取得
        return canvas.toDataURL('image/png');
    };

    // クロップAPIにリクエストを送信する処理
    const handleCropSubmit = async (): Promise<void> => {
        if (image) {
            // 画像データのエンコード部分を取り除く（data:image/png;base64, の部分）
            const base64Image = image.split(',')[1];

            // APIリクエストデータを作成
            const data = {
                image_base64: base64Image,
                rectangle_coords: rectangles,
            };

            // APIリクエストを送信
            const myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");
            const response = await fetch('http://localhost:8000/image/crop', {
                method: 'POST',
                headers: myHeaders,
                body: JSON.stringify(data),
                redirect: "follow",
            });
            if (response.ok) {
                // APIレスポンスの取得
                const responseData = await response.json();
                // 複数のクロップされた画像をセット
                setCroppedImages(responseData.cropped_images_base64);
            }else {
                setCroppedImages(null)
            }

        }
    };

    // APIにリクエストを送信して結果を取得する処理
    const handleProcessSubmit = async (): Promise<void> => {
        if (image) {
            // 画像データのエンコード部分を取り除く（data:image/png;base64, の部分）
            const base64Image = image.split(',')[1];

            const data = {
                image_base64: base64Image,
                rectangle_coords: rectangles,
                color: [0, 0, 255], // 色 (B, G, R)
                thickness: 2 // 太さ
            };

            // APIリクエストを送信
            const myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");
            const response = await fetch('http://localhost:8000/image/draw', {
                method: 'POST',
                headers: myHeaders,
                body: JSON.stringify(data),
                redirect: "follow",
            });

            // APIレスポンスの取得
            const responseData = await response.json();
            setResultImage(responseData.processed_image_base64);
        }
    };

    return (
        <div>
            <h1>画像アップロードデモ</h1>
            <input type="file" accept="image/*" onChange={handleImageChange} />
            <button onClick={handleProcessSubmit}>Draw Grid Lines</button>
            <button onClick={handleCropSubmit}>Crop Images</button>

            <h2>切り取りサイズを指定するための四角形の座標:</h2>
            <ul>
                {rectangles.map((rectangle, index) => (
                    <li key={index}>
                        <p>四角形{index + 1} (x, y, w, h): {rectangle.join(', ')}</p>
                    </li>
                ))}
            </ul>
            
            {image && (
                <div>
                    <h2>元の画像:</h2>
                    <img src={image} alt="Uploaded" />
                </div>
            )}

            {resultImage && (
                <div>
                    <h2>処理された画像:</h2>
                    <img src={`data:image/png;base64,${resultImage}`} alt="Processed" />
                </div>
            )}

            {
                croppedImages == null ? (
                    <div>
                        <h2>クロップされた画像:</h2>
                        <p>リクエストに失敗しました</p>
                    </div>
                ) : croppedImages.length > 0 ? (
                    <div>
                        <h2>クロップされた画像:</h2>
                        {croppedImages.map((croppedImage, index) => (
                            <div key={index}>
                                <img src={`data:image/png;base64,${croppedImage}`} alt={`Cropped ${index}`} />
                            </div>
                        ))}
                    </div>
                ) : <></>
            }
        </div>
    );
}

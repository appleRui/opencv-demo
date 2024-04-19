# Python公式イメージを基にする
FROM python:3.9

# 作業ディレクトリを設定
WORKDIR /app

# OpenCVをインストール
RUN apt -y update && apt -y upgrade
RUN apt -y install libopencv-dev

# 必要なパッケージをインストール
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションファイルを作業ディレクトリにコピー
COPY app.py /app/

# FastAPIアプリケーションを実行
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

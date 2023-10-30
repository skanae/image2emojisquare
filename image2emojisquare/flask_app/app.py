from flask import Flask, request, render_template, jsonify
from PIL import Image
import io
import image2emoji

app = Flask(__name__)

def insert_newlines(emojistring, n):
    result = ''
    for i, char in enumerate(emojistring, start=1):
        result += char
        if i % n == 0:
            result += '\n'
    return result

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    # リクエストから画像ファイルを取得
    image_file = request.files.get('image')

    if image_file is None:
        return jsonify({'error': 'No image provided'})

    try:
        # 画像をPillowのImageオブジェクトに変換
        image = Image.open(io.BytesIO(image_file.read()))

        # ここで画像処理を行う
        result_emoji_list = image2emoji.image2emoji(image)

        # return jsonify({'result': processed_image.decode('latin1')})
        emojistring =  "".join(result_emoji_list)
        # print(image2emoji.YOKO)
        emojistring = insert_newlines(emojistring,image2emoji.YOKO)
        # return jsonify({'result': emojistring})
        # print(emojistring)
        return render_template('emoji.html', generated_string=emojistring)
    

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
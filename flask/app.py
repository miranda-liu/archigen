from flask import Flask, render_template, request, session
from PIL import Image
from rembg import remove
import requests
import json
import base64
import io

app = Flask(__name__)

app.secret_key = 'wetooplaya'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/prompt', methods=['POST'])
def post_prompt():
    if request.method == 'POST':
        session['img_bytes'] = None
        prompt = request.form['prompt']

        api_base_url = 'http://127.0.0.1:7860/sdapi/v1/txt2img'
        payload = {
            'prompt': 'floorplan ' + prompt,
            'steps': 10,
            "width": 512,
            "height": 512,
            "cfg_scale": 7.0,
            # "enable_hr": false,
            # "denoising_strength": 0,
            # "firstphase_width": 0,
            # "firstphase_height": 0,
            # "hr_scale": 2.0,
            # "hr_upscaler": null,
            # "hr_second_pass_steps": 0,
            # "hr_resize_x": 0,
            # "hr_resize_y": 0,
            # "styles": null,
            # "seed": -1,
            # "subseed": -1,
            # "subseed_strength": 0,
            # "seed_resize_from_h": -1,
            # "seed_resize_from_w": -1,
            # "sampler_name": null,
            # "batch_size": 1,
            # "n_iter": 1,

            # "restore_faces": false,
            # "tiling": false,
            # "do_not_save_samples": false,
            # "do_not_save_grid": false,
            # "negative_prompt": null,
            # "eta": null,
            # "s_churn": 0.0,
            # "s_tmax": null,
            # "s_tmin": 0.0,
            # "s_noise": 1.0,
            # "override_settings": null,
            # "override_settings_restore_afterwards": true,
            # "script_args": [],
            # "sampler_index": "Euler",
            # "script_name": null,
            # "send_images": true,
            # "save_images": false,
            # "alwayson_scripts": {}
        }
        response = requests.post(api_base_url, json=payload)

        if response.status_code == 200:
            response_json = json.loads(response.content)
            for i in response_json['images']:
                img_bytes = io.BytesIO(base64.b64decode(i.split(",",1)[0]))
                image = Image.open(img_bytes)
                removed_bg_img = remove(image)

            data = io.BytesIO()
            removed_bg_img.save(data, "png")
            b64_encoded_image = base64.b64encode(data.getvalue()).decode('utf-8')
        else:
            raise Exception('Error: ' + str(response.status_code))

        return render_template('index.html', img_data=b64_encoded_image, prompt=prompt)


if __name__ == '__main__':
    app.run(debug=True)

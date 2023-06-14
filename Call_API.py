from datetime import datetime
import os
import requests
from PIL import Image

def resize_image(image_path):
    # 打开图像文件
    image = Image.open(image_path)

    # 获取图像原始尺寸
    width, height = image.size

    # 计算缩放后的尺寸
    target_width = min(width, height  // 4 * 3)
    target_height = min(height, width // 4 * 3)

    # 缩放图像
    resized_image = image.resize((target_width, target_height))

    # 保存缩放后的图像
    resized_image_path = image_path.replace('.jpg', '_resized.jpg')
    resized_image_path = resized_image_path.replace('.jpeg', '_resized.jpeg')
    resized_image_path = resized_image_path.replace('.png', '_resized.png')
    resized_image.save(resized_image_path)

    return resized_image_path

def upload_images_from_folder(url, folder_path):
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y%m%d%H%M%S")
        # 检查文件是否为图片文件
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            # 构建图像文件的完整路径
            image_path = os.path.join(folder_path, filename)
            # 等比例缩小图像
            resized_image_path = resize_image(image_path)
            # 打开缩小后的图像文件
            with open(resized_image_path, 'rb') as file:
                # 读取图像数据
                image_data = file.read()

            # 构建请求参数
            payload = {
                'time': formatted_time,
                'name_image': filename
            }

            # 使用元组指定文件名和文件对象
            files = {
                'image': (filename, image_data),
            }

            # 发送POST请求
            response = requests.post(url, data=payload, files=files)

            # 打印上传结果
            print(f"Uploaded {filename}: {response.status_code}")

            # 删除缩小后的图像文件
            os.remove(resized_image_path)

api_url = 'http://iotadmin.onrender.com/API/upload_image/'
image_folder = './abc'
upload_images_from_folder(api_url, image_folder)

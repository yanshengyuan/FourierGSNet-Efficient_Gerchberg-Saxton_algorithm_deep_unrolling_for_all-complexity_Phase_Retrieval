from PIL import Image
import os

def crop_center_square_by_ratio(input_path, output_path, ratio):
    """
    从中心裁剪一个正方形区域，边长为原图尺寸乘以 ratio。

    :param input_path: 输入图像路径（要求为正方形图像）
    :param output_path: 输出裁剪图像路径
    :param ratio: 裁剪区域相对于原图尺寸的比例（0 < ratio <= 1）
    """
    # 打开图像
    img = Image.open(input_path)
    width, height = img.size

    # 检查图像是否为正方形
    if width != height:
        raise ValueError("输入图像必须是正方形")

    # 计算裁剪区域尺寸
    crop_size = int(width * ratio)

    # 计算中心点
    center = width // 2

    # 计算裁剪框（正方形）
    left = center - crop_size // 2
    upper = center - crop_size // 2
    right = center + crop_size // 2
    lower = center + crop_size // 2

    # 裁剪图像
    cropped_img = img.crop((left, upper, right, lower))

    # 保存裁剪图像
    cropped_img.save(output_path, format='PNG')
    print(f"裁剪完成，保存至: {output_path}")

# 示例使用
if __name__ == "__main__":
    image_names=os.listdir("36vis")
    
    for name in image_names:
        input_image_path = "36vis/" + name        # 输入图像路径
        output_image_path = name+"_cropped.png"      # 输出图像路径
        ratio = 3/4                          # 裁剪比例（例如 0.5 表示剪一半大小的正方形）

        crop_center_square_by_ratio(input_image_path, output_image_path, ratio)

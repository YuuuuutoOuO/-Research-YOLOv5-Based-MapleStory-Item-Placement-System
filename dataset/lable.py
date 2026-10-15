import os

def generate_yolo_labels(image_folder, output_folder):
    """
    根據資料夾中的影像自動生成 YOLO 標籤文件。
    :param image_folder: 包含各類別影像的資料夾（每個類別一個子資料夾）
    :param output_folder: 保存標籤文件的資料夾
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍歷每個類別的資料夾
    for class_id, class_name in enumerate(os.listdir(image_folder)):
        class_folder = os.path.join(image_folder, class_name)
        if not os.path.isdir(class_folder):
            continue  # 忽略非資料夾項目

        print(f"正在處理類別: {class_name} (ID: {class_id})")
        for file_name in os.listdir(class_folder):
            if not file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue  # 忽略非影像文件

            # 原始影像路
            image_path = os.path.join(class_folder, file_name)

            # 創建對應的標籤文件路徑
            label_file_name = os.path.splitext(file_name)[0] + ".txt"
            label_file_path = os.path.join(output_folder, label_file_name)

            # YOLO 標籤內容 (假設整張圖片是物件)
            label_content = f"{class_id} 0.5 0.5 1.0 1.0\n"

            # 保存標籤文件
            with open(label_file_path, "w") as label_file:
                label_file.write(label_content)
            
            print(f"已生成標籤文件: {label_file_path}")

# 使用範例
image_folder = "./dataset/training/"  # 資料夾路徑，包含每個類別的子資料夾
output_folder = "./dataset/labels"  # 標籤文件輸出路徑
generate_yolo_labels(image_folder, output_folder)

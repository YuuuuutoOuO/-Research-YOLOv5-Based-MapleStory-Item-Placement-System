import os
from PIL import Image

def extract_gif_frames(input_folder, output_folder):
    """
    將資料夾中的所有 GIF 文件分解為 PNG 文件。
    
    :param input_folder: 包含 GIF 文件的資料夾路徑
    :param output_folder: 保存 PNG 文件的資料夾路徑
    """
    # 確保輸出資料夾存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    

    # 遍歷資料夾中的所有文件
    for file_name in os.listdir(input_folder):
        print(file_name)
        if file_name.lower().endswith('.gif'):  # 確保只處理 .gif 文件
            gif_path = os.path.join(input_folder, file_name)
            gif_name = os.path.splitext(file_name)[0]  # 去掉文件擴展名

            try:
                # 打開 GIF 文件
                with Image.open(gif_path) as gif:
                    frame_index = 0
                    while True:
                        # 將當前幀保存為 PNG 文件
                        frame_output_path = os.path.join(
                            output_folder, f"{gif_name}_frame{frame_index}.png"
                        )
                        gif.save(frame_output_path, format="PNG")
                        print(f"保存幀: {frame_output_path}")
                        
                        frame_index += 1
                        gif.seek(frame_index)  # 移動到下一幀
            except EOFError:
                # 到達 GIF 的最後一幀時退出
                print(f"完成分解 GIF: {file_name}")
            except Exception as e:
                print(f"處理 GIF 時出錯: {file_name}, 錯誤: {e}")

# 設定資料夾路徑
input_folder = "./dataset/"  # 替換為包含 GIF 的資料夾路徑
output_folder = "./dataset/training/"  # 替換為保存 PNG 的資料夾路徑

# 執行提取
extract_gif_frames(input_folder, output_folder)

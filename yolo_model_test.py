from yolov5.models.common import DetectMultiBackend
import torch

# 載入模型
model_path = "./model/weights.pt"  # 替換為你的權重路徑
model = DetectMultiBackend(model_path)

# 提取類別名稱與數量
if hasattr(model, 'names'):
    class_names = model.names
    print(f"總共有 {len(class_names)} 個類別")
    print("類別名稱:", class_names)

# 提取訓練相關信息
if hasattr(model, '^train') and model.trainer:
    trainer_info = model.trainer.opt
    print("訓練相關資訊:")
    print(f"  Epoch 數量: {trainer_info.get('epochs', '未知')}")
    print(f"  Batch size: {trainer_info.get('batch_size', '未知')}")
    print(f"  初始學習率: {trainer_info.get('lr0', '未知')}")
else:
    print("訓練相關資訊不可用（可能未保存於模型中）。")

# 儲存模型資訊
'''
with open("model_info.txt", "w", encoding="utf-8") as file:
    # 基本資訊
    file.write("=== 模型基本資訊 ===\n")
    file.write(f"Model Path: {model_path}\n")
    file.write(f"Device: {model.device}\n")
    file.write(f"DNN Backend: {model.dnn}\n")
    file.write(f"Stride: {model.stride}\n")
    file.write(f"Input Shape: {model.pt if model.pt else 'Unknown'}\n")
    
    # 模型類別資訊
    if hasattr(model, "names"):
        file.write("\n=== 模型類別資訊 ===\n")
        for idx, name in enumerate(model.names):
            file.write(f"Class {idx}: {name}\n")
    
    # 模型結構
    file.write("\n=== 模型結構 ===\n")
    file.write(str(model.model))
    
    # 其他參數
    file.write("\n=== 其他參數 ===\n")
    if hasattr(model, "cfg"):
        file.write(f"Config: {model.cfg}\n")
    if hasattr(model, "nc"):
        file.write(f"Number of Classes: {model.nc}\n")
    if hasattr(model, "opt"):
        file.write(f"Options: {model.opt}\n")
    if hasattr(model, "trainer"):
        file.write(f"Trainer Info: {model.trainer.opt}\n")
    file.write(f"{model}\n")
'''
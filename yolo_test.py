from ultralytics import YOLO
import cv2

def train1():
    # 加載預訓練的 YOLOv8 模型
    model = YOLO('./runs/detect/train2/weights/best.pt')  # 可以替換成 yolov8s.pt 或其他模型

    # 測試圖片路徑
    image_path = "./dataset/Original img/image copy 4.png"

    # 使用模型進行檢測
    results = model.predict(source=image_path, save=False, conf=0.5)  # save=False 不保存文件

    # 讀取原始圖片
    image = cv2.imread(image_path)

    # 繪製檢測結果框框
    for box in results[0].boxes:
        # 提取邊界框座標
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # xyxy 是左上角和右下角的座標
        cls = int(box.cls[0])  # 物件類別 ID
        conf = box.conf[0]  # 置信度

        # 獲取類別名稱（預訓練模型有 80 類，COCO 的名稱）
        label = f"{model.names[cls]} {conf:.2f}"
        print(label)

        # 繪製邊界框
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 綠色框
        # 繪製標籤
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 顯示圖片
    cv2.imshow("Detection Results", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

import torch
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.dataloaders import LoadImages
from yolov5.utils.general import non_max_suppression, scale_boxes, xyxy2xywh
from yolov5.utils.plots import Annotator
import cv2

class Train2():
    def __init__(self):
        # 加載 YOLOv5 模型
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = DetectMultiBackend('./model/weights.pt', device=self.device)  # 替換成你的 YOLOv5 權重路徑
        self.stride, self.names, self.pt = self.model.stride, self.model.names, self.model.pt

    # 測試圖片路徑
    
    def load_image(self, image_path):
    # 加載圖片
        dataloader = LoadImages(image_path, img_size=640, stride=self.stride, auto=self.pt)
        for path, img, im0s, vid_cap, s in dataloader:
            img = torch.from_numpy(img).to(self.device)
            img = img.half() if self.model.fp16 else img.float()  # 如果支持 FP16，轉為半精度
            img /= 255.0  # 歸一化到 [0, 1]
            if len(img.shape) == 3:
                img = img[None]  # 添加一個 batch 維度

            # 推理
            pred = self.model(img, augment=False, visualize=False)

            # 非極大值抑制（NMS）
            pred = non_max_suppression(pred, conf_thres=0.5, iou_thres=0.45, classes=None, agnostic=False)

            # 繪製檢測結果
            for i, det in enumerate(pred):  # 每張圖片的檢測結果
                im0 = im0s.copy()

                annotator = Annotator(im0, line_width=2, example=str(self.names))
                if len(det):
                    # 將邊界框大小調整回原始圖片
                    det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], im0.shape).round()

                    # 遍歷每個檢測到的物件
                    for *xyxy, conf, cls in reversed(det):
                        label = f"{self.names[int(cls)]} {conf:.2f}"  # 類別名稱和置信度
                        print(label)

                        # 繪製邊界框和標籤
                        annotator.box_label(xyxy, label, color=(0, 255, 0))

                # 顯示圖片
                im0 = annotator.result()
        return im0
list_img = [
    '遊戲畫面',
    '維多利亞港',
    '勇士之村',
    '墮落城市',
    '弓箭手村',
    '沙漠',
    '魔法森林2',
]
if __name__ == "__main__":
    yolo = Train2()
    for img in list_img:
        image_path = f"./dataset/ILT/{img}.png"
        im0 = yolo.load_image(image_path)

        cv2.imshow("Detection Results", im0)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
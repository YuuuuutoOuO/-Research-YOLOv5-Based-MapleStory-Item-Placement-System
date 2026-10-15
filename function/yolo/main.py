import torch
import cv2
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.general import non_max_suppression, scale_boxes
from yolov5.utils.plots import Annotator
from yolov5.utils.augmentations import letterbox
import numpy as np
import time
class Main():
    def __init__(self):
        # 加載 YOLOv5 模型
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = DetectMultiBackend('./model/weights.pt', device=self.device)  # 替換成你的 YOLOv5 權重路徑
        self.stride, self.names, self.pt = self.model.stride, self.model.names, self.model.pt

    def load_image(self, img):
        result = [] # 紀錄檢測結果
        im0 = img.copy()
        
        # letterbox處理 (縮放、填充使得圖片符合 YOLO 模型輸入要求)
        img, ratio, dwdh = letterbox(img, 640, stride=self.stride, auto=self.pt)
        # img 此時為 (H, W, C) 格式，且是 RGB 
        # 若 letterbox 函數保留原本順序為 BGR，要自行轉 RGB；若無特別註明，此處皆為 BGR，因此需轉成 RGB
        # 但 YOLOv5 模型預設以 RGB 為輸入，所以要先將 im0(BGR) -> RGB
        # 若要保留顯示 im0 在後面標註時維持 BGR 可，只需要在推論前轉 img 為 RGB 即可
        # 下面程式碼假設 letterbox 只是縮放，未改變通道順序，所以我們先轉 RGB:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # 轉成張量並調整維度： (H, W, C) -> (C, H, W)
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(self.device)
        img = img.permute(2, 0, 1)  # (H, W, C) -> (C, H, W)
        img = img.half() if self.model.fp16 else img.float()  # FP16 或 FP32
        img /= 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)  # [C, H, W] -> [1, C, H, W]

        # 推理
        pred = self.model(img, augment=False, visualize=False)

        # 非極大值抑制（NMS）
        pred = non_max_suppression(pred, conf_thres=0.5, iou_thres=0.45, classes=None, agnostic=False)

        # 繪製檢測結果
        for _, det in enumerate(pred):
            annotator = Annotator(im0, line_width=2, example=str(self.names))
            if len(det):
                # 將邊界框從縮放後大小還原到原圖大小
                det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], im0.shape).round()

                for *xyxy, conf, cls in reversed(det):
                    label = f"{self.names[int(cls)]} {conf:.2f}"
                    x1, y1, x2, y2 = [coord.item() for coord in xyxy]
                    result.append({'label': label,
                                   'coordinates': [x1, y1, x2, y2]})
                    annotator.box_label(xyxy, label, color=(0, 255, 0))

            im0 = annotator.result()

        result = np.array(result)
        return im0, result

if __name__ == "__main__":
    yolo = Main()
    image_path = "./dataset/Original img/image copy 4.png"
    img = cv2.imread(image_path)  # BGR 格式
    time_start = time.time()

    im0, result = yolo.load_image(img)
    #
    print(f'檢測時間: {time.time()-time_start}')
    # print(result)
    # cv2.imshow("Detection Results", im0)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

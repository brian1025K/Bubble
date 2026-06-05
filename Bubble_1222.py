import torch
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection import FasterRCNN_ResNet50_FPN_Weights
from torchvision.transforms import functional as F
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickfile as pf
from pathlib import Path
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor

def load_model(model_path, num_classes, max_detections = 1000):
    weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn_v2(weights=weights)
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    
    model.roi_heads.detections_per_img = max_detections

    # 載入權重
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    
    print(f"模型已載入")
    return model, device

#推論函數
def predict_image(model, device, img_path, threshold):
    """
    對圖片進行推論
    """
    # 讀取圖片
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    tensor = F.to_tensor(img_rgb).to(device)
    img_height, img_width, _ = img_rgb.shape
    
    # 推論
    with torch.no_grad():
        prediction = model([tensor])
    
    # 定義類別
    class_names = {1: 'Bubble'}
    class_colors = {1: (0, 255, 255)}
    
    x_widths = []

    # 輸出預測結果
    print("=" * 50)
    print(f"檢測到 {len(prediction[0]['boxes'])} 個物體")
    for i, (box, score, label) in enumerate(zip(prediction[0]['boxes'], 
                                                prediction[0]['scores'], 
                                                prediction[0]['labels'])):
        if score > threshold:
            label_id = label.item()
            x1, y1, x2, y2 = box.int().tolist()
            x_width = x2 - x1  # 計算X方向的長度
            x_widths.append(x_width)
            
            print(f"物體 {i+1}: {class_names.get(label_id, f'未知{label_id}')} "
                  f"(信心分數: {score:.4f}, X方向長度: {x_width} pixels)")
    print("=" * 50)
    
    # 計算平均X方向長度

    if x_widths:
        avg_x_width = np.mean(x_widths)
        actual_size_cm = (avg_x_width * 3) / img_width

        #各別氣泡存成excel
        actual_sizes_list = [(x_width * 3 * 10000) / img_width for x_width in x_widths]
        df = pd.DataFrame({
            '序號': range(1, len(x_widths) + 1),
            'X方向長度(pixels)': x_widths,
            '實際尺寸(uM)': actual_sizes_list
        })

        excel_filename = f"{Path(img_path).stem}_bubble_measurements.xlsx"
        df.to_excel(excel_filename, index=False, sheet_name='氣泡測量')

        print("-" * 50)
        print(f"所有檢測框的X方向長度: {x_widths}")
        print(f"平均X方向長度: {avg_x_width:.2f} pixels")
        print(f"Bubble 尺寸為 {10000*actual_size_cm:.4f} uM")
    else:
        print("沒有檢測到符合閾值的物體")
        avg_x_width = 0
        actual_size_cm = 0
        actual_sizes_list = []
        excel_filename = None
    
    print("=" * 50)

    # 畫框
    output = img_rgb.copy()
    for i, (box, score, label) in enumerate(zip(prediction[0]['boxes'], 
                                                 prediction[0]['scores'], 
                                                 prediction[0]['labels'])):
        if score > threshold:
            label_id = label.item()
            color = class_colors.get(label_id, (255, 0, 0))
            
            x1, y1, x2, y2 = box.int().tolist()
            x_width = x2 - x1
            
            # 畫框
            cv2.rectangle(output, (x1, y1), (x2, y2), color, 1)
    
    return output, prediction, x_widths, avg_x_width, img_width, actual_size_cm, excel_filename

if __name__ == "__main__":
    # 載入模型
    model, device = load_model("./bubble_260604-2.pth", num_classes=2, max_detections=1000)
    
    # 對圖片進行推論
    img_paths = pf.pick_files()        # GUI 選多張圖片
    print(f"\n共選取 {len(img_paths)} 張圖片\n")
 
    for img_path in img_paths:
        output, prediction, x_widths, avg_x_width, img_width, actual_size_cm, excel_filename = predict_image(model, device, img_path, threshold=0.6)
 
        # 顯示每張結果
        plt.figure(figsize=(12, 8))
        plt.title(Path(img_path).name)
        plt.imshow(output)
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(f"{Path(img_path).stem}_measurement.png", bbox_inches='tight', pad_inches=0)
        plt.show()
        

# 服務於CPLab計算氣泡尺寸
## 使用步驟:
### 搭建環境(For新電腦或沒使用過pytorch的電腦):
1. 安裝python，網址: https://www.python.org/downloads/windows/

   (安裝時記得勾選加入path，重要!!)
   
2. 建立運行環境，打開終端機(在 windows 圖標點右鍵 -> 終端機):
   1. 安裝pytorch (如果有nvidia顯卡)及環境依賴
  
      Pytorch安裝(選自己電腦的cuda版本): https://pytorch.org/get-started/locally/

      再安裝程式庫:
      ```
      pip install opencv-python numpy matplotlib pandas tkinter openpyxl
      ```

   2. 無nvidia顯卡，直接運行以下命令:
  
      ```
      pip install torch torchvision torchaudio opencv-python numpy matplotlib pandas tkinter openpyxl
      ```

### 環境皆已搭建完成(For已經跑過這個項目的電腦)
1. 從 Release 裡下載 Source code (zip)並解壓縮

2. 在 Release 裡有 bubble_260604-2_best.pth 模型檔案，將它放到與此專案相同的資料夾內

3. 雙擊 Start.bat 檔案即可

## 注意
1. 程式會將圖片的X方向當作3公分，進model前請務必先裁好圖片
   
3. 如果不知道怎麼安裝pytorch，直接運行"無nvidia顯卡"那條指令就行

## 更新日誌
2026/5/5 新增多照片的批次處理功能

2026/5/11 新增.bat及自動儲存照片

2026/5/19 用一些相機的data訓練新模型，可於NAS中自行替換

2026/6/5 優化模型全重，調整訓練參數，並投入使用，模型檔名:bubble_260604-2_best.pth

# 服務於CPLab計算氣泡尺寸
## 使用步驟:
### 搭建環境(For新電腦或沒使用過pytorch的電腦):
1. 安裝python，網址: https://www.python.org/downloads/windows/

   (安裝時記得勾選加入path)
2. 安裝Microsoft VS code ，網址: https://code.visualstudio.com/

   (需要在extension介面安裝python拓展)
   
3. 建立運行環境，打開終端機:
   1. 安裝pytorch (如果有nvidia顯卡)及環境依賴
  
      Pytorch安裝(選自己電腦的cuda版本): https://pytorch.org/get-started/locally/

      再安裝程式庫:
      ```
      pip install opencv-python numpy matplotlib pandas
      ```

   2. 無nvidia顯卡，直接運行以下命令:
  
      ```
      pip install torch torchvision torchaudio opencv-python numpy matplotlib pandas
      ```

### 環境皆已搭建完成(For已經搭建好環境的電腦)
1. 在 NAS/Guan/Bubble AI 裡有兩個檔案，一個.py一個.pth，將整個Bubble AI資料夾複製到桌面

2. 用VScode打開後綴是.py的檔案，修改第117行

   ```
   img_path = "C:\\Users\\User\\Pictures\\Screenshots\\螢幕擷取畫面 2025-12-22 172658.png"
   ```

   在" "內放入要處理的照片路徑

3. 最後，點擊上方 RUN -> Run Without Debugging -> Python debugger 即可看到辨識結果

# 轉換webm至mp4的腳本

這個Python腳本旨在將指定目錄中的所有.webm文件轉換為.mp4格式。它使用FFmpeg工具進行轉換，並支持重新編碼為H.264並調整分辨率。

## 如何使用

1. **安裝依賴**

   請確保你的系統上已安裝了FFmpeg。你可以通過訪問[FFmpeg官方網站](https://ffmpeg.org/download.html)來獲取安裝指南。

2. **下載腳本**

   下載本存儲庫中的`convert_webm_to_mp4.py`文件。

3. **指定目錄**

   打開腳本文件，將`directory`變量設置為包含.webm文件的目錄的路徑。

4. **執行腳本**

   在終端或命令提示符中運行腳本：

   ```bash
   python convert_webm_to_mp4.py
   ```

   該腳本將遍歷指定目錄中的所有.webm文件，將其轉換為.mp4格式，並將轉換後的文件保存在相同目錄中。在轉換過程中，腳本會打印每個文件的轉換進度。


import os
import subprocess

# 定義一個函數，將指定目錄中的所有.webm文件轉換為.mp4格式
def convert_webm_to_mp4(directory):
    # 切換目錄到包含影片的文件夾
    os.chdir(directory)
    
    # 遍歷目錄中的所有文件
    for file in os.listdir():
        # 如果文件以“.webm”結尾
        if file.endswith(".webm"):
            # 定義新的文件名，保留原名但更改為.mp4擴展名
            mp4_file = file[:-5] + ".mp4"

            # 構建ffmpeg命令以轉換文件，重新編碼為H.264並調整分辨率
            command = (
                f"ffmpeg -i '{file}' "  # 輸入文件為原.webm文件
                "-vf 'scale=trunc(iw/2)*2:trunc(ih/2)*2' "  # 調整分辨率，確保為偶數
                "-c:v libx264 -preset fast -crf 23 "  # 使用libx264編碼器，快速預設，品質設置為23
                "-r 30 "  # 設定幀率為每秒30幀
                "-c:a aac "  # 使用aac音頻編碼器
                f"'{mp4_file}'"  # 輸出文件為新的.mp4文件
            )

            # 執行命令
            subprocess.run(command, shell=True)
            print(f"Converted {file} to {mp4_file}")  # 打印轉換成功消息

# 指定包含.webm文件的目錄
directory = "./"
convert_webm_to_mp4(directory)  # 呼叫函數開始轉換


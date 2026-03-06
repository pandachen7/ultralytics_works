本專案用於ultralytics的快速說明與建構方式

ultralytics作為框架, 主要就是可以用來訓練跟推測  
只要dataset的圖片很多樣化, 就能夠訓練出不錯的偵測器  
然後再透過infer的方式來推測並定位目標物的位置與分類  

ultralytics有很多種task, 通常都是yolo model, 其中最常用的就是Object Detection(會有Bounding Box)跟Segmentation(會有像素級的定位與分類)

建議用uv或python venv來安裝  
以免跟其他專案的python pkg(python package, 即lib)相衝突  
不同的環境也容易與ultralytics衝突  

# 專案中的檔案名稱
infer開頭的都是可以測試(預測, 偵測)  
train開頭的都是用來訓練model的  
這邊都只是範例, 詳細你可以任意改, 達到你的目的即可

# 準備環境 - nvidia
你需要nvidia的顯卡, 安裝nvidia driver(驅動)  
如果你只想使用pytorch, 或是你想用anaconda, 那麼CUDA(平行運算平台以及API)以及cuDNN(lib) 就不用裝  
ultralytics預設用pytorch, 所以要先準備好環境

Windows版應該已經能夠自動更新nvidia driver  
Ubuntu版有時需要用指令下載安裝特定版本的nvidia driver  
之後使用`nvidia-smi`可看到對應的版本, e.g.  
```bash
> nvidia-smi
Wed Dec 25 22:08:15 2024
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 551.86                 Driver Version: 551.86         CUDA Version: 12.4     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                     TCC/WDDM  | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 4060 ...  WDDM  |   00000000:01:00.0 Off |                  N/A |
| N/A   41C    P8              3W /   60W |       0MiB /   8188MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+
```
建議windows使用 `Power Shell` 或 `git bash`, 純文字CLI介面的支援度較高

## uv - python 虛擬環境
選擇一種版本來使用, 網路上或許有更新的安裝方式, 請先google `uv install`
```sh
# ubuntu
curl -LsSf https://astral.sh/uv/install.sh | sh

# windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
然後到一個ws下開創一個專案資料夾, 例如`my_project`, 專案路徑就以 `./ws/my_project` 為主  
```sh
uv python install 3.12
uv venv --python 3.12

# ubuntu
source .venv/bin/activate

# windows
./.venv/bin/activate.bat
```
在這裡你就已經進入venv的虛擬環境了, 所有安裝的python pkg都只會影響這個venv

# 準備訓練影像資料
## RoboFlow
RoboFlow為線上可用於dataset準備, 訓練, infer測試的平台  
但如果沒有付錢訂閱的話, 上傳多媒體檔案會被無償公開, 因此重要的資料請勿上傳到RoboFlow  

RoboFlow可自動畫框, 影像argument, 雲端訓練等等  
官網註冊就能使用  

免費版的credit很少, 自動畫框跟推測只有1000/month, 雲端訓練只有3/month   
但付費版的自動畫框跟推測也只有10000/month, 訓練10/month  
如果要再加購的話, 一個框約0.75~0.9台幣[2024.4.10當下]  

網站最大的好處就是基於分享的觀念, 可以下載別人畫好的圖片標籤檔dataset  
直接下載通常就能訓練, 很適合拿來練習  

## RoboFlow - Export
從RoboFlow下載訓練資料圖片跟標記檔, 通常就能夠直接拿來訓練  
但要注意的是, 有的dataset的設定檔 data.yaml會多一個path  
導致訓練時被引導到錯誤的路徑, 因此必須把路徑註解掉, 例如將  
`path: ../datasets/roboflow`  
變為  
`# path: ../datasets/roboflow`  
這樣, 訓練者如ultralytics就會去抓相對路徑而不被誤導

# 安裝lib
## 好用的yaml工具, 回存時可保留原本設定檔順序 以及註解
```
pip install ruamel.yaml
```
注意bool中的True/False會變成小寫, 但不影響ruamel.yaml的使用

# ultralytics
可用yolo v3 ~ v12, 26 [2026.3.5 當下]  
有Nvidia顯卡, 就要先裝gpu版本, 以免ultralytics因相依直接裝cpu版本的  
到 `https://pytorch.org/get-started/locally/` 選擇要下載安裝的方式  
注意新的ultralytics版本才能使用新的yolo版, 例如2024.5 yolov10才推出, 就要下載更之後的 ultralytics  
如果不知道如何安裝, 請參考我的筆記  
[PyTorch安裝方式](https://www.notion.so/PyTorch-30936ed5d3d680ceb0e1ed1dc8c2c7bf?source=copy_link)

## ultralytics - 設定
有時候訓練過後, 搬移或改名datasets路徑會導致設定檔的路徑不同步, 導致無法訓練  
這時可到  
`/home/${USER}/.config/Ultralytics/settings.yaml`  
或是  
`C:\Users\[USER_ID]\AppData\Roaming\Ultralytics`  
然後將內容的`datasets_dir`, 指定到特定資料夾路徑, 建議直接使用絕對路徑  
幸運的是win版的路徑用斜線`/`也是可行的, 不然python容易把`\`視為跳脫符號

## ultralytics - 多線程運作錯誤
比較奇妙的情形, 當簡單的訓練語法的main沒有加上 `if __name__ == "__main__":`(if-clause protection)  
就會導致以下錯誤  
```
An attempt has been made to start a new process before the
current process has finished its bootstrapping phase.
```
看了一下console居然跑了兩個net, 很神奇的是加了if-clause protection之後, 就不會再出現錯誤  
但有些電腦似乎沒有這種限制, 目前是在RTX2070 SUPER有看到  

## ultralytics - 訓練硬體規格需求
你可以選其中一種size的model: [yolo26n, yolo26s, yolo26m, yolo26l, yolo26x]  
RTX2060-6GB only can use yolo26n and yolo26s with batch=16, but yolo26m with batch=8  
看起來在batch=8時:  
 - yolo26m, 會用掉4GB左右的記憶體    
 - yolo26l, 會用掉5.6GB左右的記憶體  

batch=16時:  
 - yolo26x會用掉13.3GB  

可作為硬體規格以及需求參考  
如果訓練過程中記憶體不足OOM Killer(Out of Memory Killer), 那就降低batch試試  

更多細節請參考各個不同的train**.py檔案

# 舊資訊
[Nvidia安裝版本](./doc/old_info.md)

import cv2
import os

PATH_RECORDED = "./record"

if not os.path.isdir(PATH_RECORDED):
  os.makedirs(PATH_RECORDED)

cap = cv2.VideoCapture(0)

# 設定擷取影像的尺寸大小
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

reso_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
reso_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 使用 XVID 編碼
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# 建立 VideoWriter 物件，輸出影片至 output.avi
# FPS 值為 20.0，解析度為 640x360
out = cv2.VideoWriter(f'{PATH_RECORDED}/output.avi', fourcc, 20.0, (reso_width, reso_height))

while cap.isOpened():
  ret, frame = cap.read()
  if ret == True:
    # 寫入影格
    out.write(frame)

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
  else:
    break

# 釋放所有資源
cap.release()
out.release()
cv2.destroyAllWindows()

## 建立在 opencv & tkinter 上的 剪刀石頭布 AI ##
> 使用 opencv 進行即時手部辨識的剪刀石頭布 AI 遊戲
>
> dataset 來源:
> 最初使用 tensorflow rock_paper_scissors dataset: https://www.tensorflow.org/datasets/catalog/rock_paper_scissors
> 自己與團隊利用 opencv 影像擷取圖像取得的手部影像(使用 image_catch.py)
>
----------
>
> 在 opencv 上實現並利用 python 內建 GUI tkinter 展示
> 為了檢視效果，目前版本設定只要影像進入 user 辨識用 frame 範圍，會不斷辨識， computer 端則是設置每 30 次辨識後（我自己使用約是 5~8 秒完成 30 次），隨機變換手勢
> 
----------
> 使用方法:
> 確認攝影機沒有問題後，運行 scissor_rock_paper 後，呈現 tkinter GUI，按鈕選擇"猜拳比賽"，開始進行遊戲，需要暫時關閉可以按鈕選擇"結束比賽"或按鍵盤"q"鍵，需要關閉整個 GUI 直接右上角"X"離開或是按鈕選擇"關閉視窗"即可。

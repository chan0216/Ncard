# Ncard
### 本網站參考社群網站Dcard，主要功能有發文留言、抽卡配對聊天。


Demo
---
網站網址：https://ncard.website/
<br>
測試帳號
<br>
帳號：test@test.com
<br>
密碼：test

使用技術
--
- Python Flask
- 使用 Docker 部屬。
- 支援 Google OAuth 實現第三方登入。
- 使用 Socket.io 支援即時互動聊天室。
- 使用 Nginx 作為反向代理，並支援 HTTPS 的建置。
- 使用 AWS S3 儲存使用者上傳的圖片與頭貼，並利用 Cloudfront 建立 CDN 。
- 使用 AWS RDS 建構 MySQL 資料庫。

系統架構圖
--
<img width="800" alt="image" src="https://user-images.githubusercontent.com/94737861/173253578-e1ce1571-55e1-4c46-be38-bf397c1ff2c0.png">


主要功能
---
### 撰寫貼文及留言
使用者在登入/註冊系統後，需先填寫基本資料，即可發文留言。

<img width="800" alt="image" src="https://user-images.githubusercontent.com/94737861/173251768-e2c3fb42-af8e-4f90-b9e9-a52b03ced638.png">

<img width="800" alt="image" src="https://user-images.githubusercontent.com/94737861/173252072-3307f887-31e1-4cde-981c-8e2efa122822.png">

<img width="800" alt="image" src="https://user-images.githubusercontent.com/94737861/173252115-368b019f-d232-4f95-926d-df6ca47acd75.png">

### 抽卡配對
- 使用者填完自我介紹後，即可參與抽卡。
- 每到午夜12點，便可在網站瀏覽到當日配對到的對象，抽過的卡將不再配對到。
- 若兩人都送出交友邀請，即可成為好友聊天。

<img  width="800" alt="image" src="https://user-images.githubusercontent.com/94737861/173252389-a7f129c5-5d7b-4f0b-b910-bde66a20dcff.png">

### 聊天系統
- 成為卡友的兩人即可及時送信聊天，左側的好友欄也會隨訊息更新順序。

<img width="800" alt="image" src="https://user-images.githubusercontent.com/94737861/173274922-75d3bf7f-dd00-4a05-874d-2e0d1b5c6223.png">

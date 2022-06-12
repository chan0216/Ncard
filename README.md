# Ncard
### 本網站參考社群網站Dcard，主要功能有發文留言、抽卡配對聊天。


Demo
---
網站網址：https://ncard.website/
<br>
測試帳號：
<br>
User：test@test.com
<br>
Password：test

使用技術
---
- python Flask
- 支援 Google OAuth 實現第三方登入
- 使用 Docker部屬
- 使用 Socket.io 支援即時互動的聊天室
- 使用 Nginx 作為 Reverse Proxy 並支援 HTTPS 的建置
- 使用 AWS S3儲存使用者上傳的圖片與及頭貼，並利用Cloudfront建立CDN 
- 使用 AWS RDS 建構 MySQL資料庫

系統架構圖
---
<img width="432" alt="image" src="https://user-images.githubusercontent.com/94737861/173253333-55741748-b054-4ac6-9fe0-b30cbb916ced.png">


主要功能
---
### 撰寫貼文及留言
使用者在登入/註冊系統後，需先填寫基本資料，即可發文留言。

<img width="800" alt="image" src="https://user-images.githubusercontent.com/94737861/173251768-e2c3fb42-af8e-4f90-b9e9-a52b03ced638.png">

<img width="800" alt="image" src="https://user-images.githubusercontent.com/94737861/173252072-3307f887-31e1-4cde-981c-8e2efa122822.png">

<img width="800" alt="image" src="https://user-images.githubusercontent.com/94737861/173252115-368b019f-d232-4f95-926d-df6ca47acd75.png">

### 抽卡配對及聊天
- 使用者填完自我介紹後，即可參與抽卡。
- 每到午夜12點，便可在網站瀏覽到當日配對到的對象，抽過的卡將不再配對到。
- 若兩人都送出交友邀請，即可成為好友聊天。

<img  width="800" alt="image" src="https://user-images.githubusercontent.com/94737861/173252389-a7f129c5-5d7b-4f0b-b910-bde66a20dcff.png">

<img width="800" alt="image" src="https://user-images.githubusercontent.com/94737861/173252423-230ac23c-8b71-4de9-98dc-cbdfa05c7ef6.png">


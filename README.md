# Ncard

Dcard as a reference, users can post comments, share ideas, meet new friends, match with someone, and start a conversation.

## Demo

Website URL : https://ncard.website/

Test Account

Email：test@test.com

Password：test

## Technique

### Backend

- Python Flask for server framework.
- Creating a real-time chat with Socket.io.
- Using AWS S3 to store the images and CloudFront CDN to serve images fast.
- Using RDS for MySQL database to store data.
- Using indexes to improve MySQL query performance.
- Using Nginx as A Reverse Proxy with SSL.
- Deploying web applications with Docker.
- Support Google login with OAuth 2.0.
- Setting a crontab to run Ncard matching and write to a database.
- Design web APIs follow REST.

### Frontend

- HTML
- CSS
- JavaScript

## System Architecture


![](./ncard/static/image/Diagram.jpg)

## Introduction


### Browse Articles

- Homepage showing the latest articles.

<img width="900" alt="image" src="https://user-images.githubusercontent.com/94737861/183302281-1a84e928-79eb-4396-b0b9-399fca1901a3.png">

### Share Ideas

- After registration and filling out basic information, users can write an article and post comments.

  ![](ncard/static/image/ncard_post.png)

  ![](ncard/static/image/Ncard_comment.png)

### Match-making

- Every midnight, users would be paired up with a stranger randomly assigned.
- Users will only meet each person one time, once the opportunity has passed, it is gone forever.
- As long as both users hit the button and agree to meet each other they can be friends.

![](ncard/static/image/ncard_match.png)

### Chat

- After users become friends, they can start a conversation and exchange information.

![ncard_chat_](https://user-images.githubusercontent.com/94737861/176986984-711ef07f-30b9-42f9-b11f-d1031a8d1cdb.gif)



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
- Using RDS for MySQL database to store data and normalize a database structure in 3NF.
- Using Nginx as A Reverse Proxy with SSL.
- Deploying web applications with Docker.
- Support Google login with OAuth 2.0.
- Setting a crontab to run Ncard matching and write to a database.
- Design web APIs follow REST.

### Frontend

- HTML
- CSS
- JavaScript
- Bootstrap 

## System Architecture


<img width="800" alt="image" src="https://user-images.githubusercontent.com/94737861/184095340-4c512e69-3fe9-4bd7-aeff-692686c91a1d.png">

## Database Schema

<img width="800" alt="image" src="https://user-images.githubusercontent.com/94737861/184921021-16f43f97-7ede-45c4-b598-c11885aa4407.png">

## Introduction


### Browse Articles

- Display the latest article on a homepage.

<img width="800" alt="image" src="https://user-images.githubusercontent.com/94737861/183302387-a8a571bb-5151-468c-8867-723e228669e8.png">

### Share Ideas

- After registration and filling out basic information, users can write an article and post comments.

<img width="800" alt="image" src="https://user-images.githubusercontent.com/94737861/183302981-424ba62b-be2f-4f38-808d-2ae57252f30a.png">

<img width="800" alt="image" src="https://user-images.githubusercontent.com/94737861/183303591-53c65ef0-aa35-4184-859d-ecb99337d6ea.png">

### Match-making

- Every midnight, users would be paired up with a stranger randomly assigned.
- Users will only meet each person one time, once the opportunity has passed, it is gone forever.
- As long as both users hit the button and agree to meet each other they can be friends.

<img width="800" alt="image" src="https://user-images.githubusercontent.com/94737861/183303544-f84896e8-03b5-4002-bd07-d80ca8bfa6b7.png">

### Chat

- After users become friends, they can start a conversation and exchange information.
<img width="800" alt="image" src="https://user-images.githubusercontent.com/94737861/176986984-711ef07f-30b9-42f9-b11f-d1031a8d1cdb.gif">


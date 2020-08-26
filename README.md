This project help me to improve my practice skills in Python. 
For creating Telegram bot I used Python v.3.8 and library pyTelegramBotAPI. 
Also, for continuous operation of the bot I deploy it to remote server. For creating and
testing new functions I used Test-Bot which I launch locally. When new functions
have been tested and all bugs have been fixed, I deploy a stable version of bot with
help my CI/CD to remote server.
<h2>Experience on this project</h2>
<img src="https://github.com/hansholz/game-bot/blob/master/readmeimg/technologies.jpeg?raw=true" alt="Experience on this project" width="400">
<ul>
  <li>Google Cloud Platform</li>
  <li>Docker</li>
  <li>Jenkins</li>
  <li>GitHub</li>
  <li>SQLite</li>
  <li>Python v.3.8</li>
</ul>
<h2>Bot usage</h2>
Telegram Bot @SheldonGameFlagsBot works in private and public chats for
playing a simply and funny game - guessing the flags of different countries. For
start playing user must to send command “/start” and after that bot will send image
with some flag:
<img src="/readmeimg/start.jpeg" alt="Experience on this project" width="400">
If user don’t know what flag it is, he can give up and press appropriate button.
After that bot will sent correct answer with link to Wikipedia:
<img src="/readmeimg/wronganswer.jpeg" alt="Experience on this project" width="400">
For start a new round user must to press button “Next”.<br>
Message, when user answered a correct:
<img src="/readmeimg/correctanswer.jpeg" alt="Experience on this project" width="400">
Message, when user answered a wrong:
<img src="/readmeimg/wronganswer2.jpeg" alt="Experience on this project" width="400">
Also has been added battle mode, which will start when some user send a
command “/battle”:
<img src="/readmeimg/battle.jpeg" alt="Experience on this project" width="400">
Another peoples in chat can accept or reject the battle-call press appropriate
buttons:<br>
Message, when user accept the battle-call:
<img src="/readmeimg/joinbattle.jpeg" alt="Experience on this project" width="400">
Message, when user reject the battle-call:
<img src="/readmeimg/declinebattle.jpeg" alt="Experience on this project" width="400">
<h2>Development usage</h2>
For this project was implemented the concept of CI/CD, which help make certain
changes to the code of this bot in one click. How it’s works? I have GitHub-
repository with code of this project. Suppose I made some changes in code and
push it to repository, which is configured to send webhooks after push to Jenkins.<br>
This webhook automatically launch a Job in Jenkins. Job contain five stages:
<ol>
  <li>Pull code from GitHub</li>
  <li>Build Docker-image (for better review: <a href="https://github.com/hansholz/game-bot/blob/master/Dockerfile">Dockerfile</a>)</li>
  <li>Push Docker-image to Docker Registry</li>
  <li>Deploy artifact on remote server (with help Jenkins addon Public over SSH)</li>
  <li>Post-build action (Send a notification about Jenkins-build to Slack)</li>
</ol>
For better review: <a href="https://github.com/hansholz/game-bot/blob/master/Jenkinsfile">Jenkinsfile</a>

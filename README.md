 Dating Telegram Bot WebApp 2.0 <img width=32 src="https://github.com/AlexanderLukash/Dating-Telegram-Bot-Webapp/blob/main/assets/logo.png?raw=true">

![GitHub License](https://img.shields.io/github/license/AlexanderLukash/dating-telegram-bot-webapp)
![GitHub watchers](https://img.shields.io/github/watchers/AlexanderLukash/dating-telegram-bot-webapp)
<img src="https://github.com/AlexanderLukash/Dating-Telegram-Bot-Webapp/blob/main/assets/cover.png?raw=true">
![Python](https://img.shields.io/badge/-Python-070404?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/-Fastapi-070404?style=for-the-badge&logo=fastapi)
![Aiogram](https://img.shields.io/badge/-Aiogram-070404?style=for-the-badge&logo=telegram)
![Docker](https://img.shields.io/badge/-Docker-070404?style=for-the-badge&logo=docker)
![TypeScript](https://img.shields.io/badge/-typescript-070404?style=for-the-badge&logo=typescript)
![Next.JS](https://img.shields.io/badge/-next.Js-070404?style=for-the-badge&logo=nextdotjs)
![nextui](https://img.shields.io/badge/-nextui-070404?style=for-the-badge&logo=nextui)
![MongoDB](https://img.shields.io/badge/-mongoDB-070404?style=for-the-badge&logo=mongodb)

This project is Dating Telegram Bot WebApp, which combines the capabilities of a dating Telegram bot with a WebApp for
easy use.

## Description of the project

Dating Telegram Bot WebApp allows users to meet through the Telegram bot, as well as use a convenient web interface to
view profiles, send messages and manage interactions with other users.

## Requirements

Before using this project, make sure you have the following components installed:

- Docker
- Docker Compose
- GNU Make

## Installation and launch

After cloning the repository, follow these steps:
1. Create a `.env` file based on `.env.example` and specify the necessary environment variables.
2. Use [Ngrok](https://ngrok.com/) or [localtunnel](https://theboroer.github.io/localtunnel-www/) to open the https
   tunnels of our apps.
3. Open a terminal and navigate to the project's root directory.
4. Use the command `make all` to build all Docker containers and start the project.
5. Open your browser and go to `http://localhost:8000/api/docs` to view the project.

## Implemented Commands

- `make all`: Start the project.
- `make app`: Start the api project.
- `make app-logs`: Follow the logs in api container.
- `make test`: Run the test.
- `make frontend`: Start front-end project.
- `make storages`: Start MongoDB with UI on `28081` port.


## License

This project is distributed under the MIT License. See the `LICENSE` file for additional information.
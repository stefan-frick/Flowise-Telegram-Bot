# Local AI Telegram Bot with Flowise and Ollama

This guide walks you through setting up a fully private, locally-hosted AI Telegram bot using Flowise, Docker, and Ollama.

### 📥 Alternative: Interactive Manual with Screenshots

If you prefer a visual guide, which includes full step-by-step screenshots, you can download an interactive HTML version of this manual from the link below:

**⚠️ Important Viewing Instructions:**

1. Download the ZIP file from the link below.
2. **You must completely extract (unzip) the file** to a new folder on your computer.
3. Open the HTML file **Flowise Telegram Bot Setup Guide.html** from inside the *extracted* folder using your web browser.

*Note: If you attempt to open the HTML file directly from within the compressed ZIP archive without extracting it first, the images will not load correctly.*

[Download Flowise Telegram Bot Setup Guide](https://drive.google.com/drive/folders/1lrEi2DyZu1MANOd5jTPFtsKWEqpGpM5F)

---

## PHASE 0: Your Variables Cheat Sheet

Gather these values before you start. You will use these exact bracketed placeholders (like `[volume]`) throughout the files and commands below.

| Variable | Example | Source |
| --- | --- | --- |
| `[folder_path]` | `D:\progs\Flowise\telegram-flowise-project` | Defined by you |
| `[volume]` | `telegram_extended_flowise` | Defined by you |
| `[telegram_token]` | `123456789:AkboRksiTTkQkqklbirokaRfj` | Retrieved from Telegram app |
| `[telegram_user_id]` | `8111111111` | Retrieved from Telegram app |
| `[flowise_username]` | `L83r2#d1_2t?prka` | Defined by you |
| `[flowise_password]` | `%aB*,s#neS7sV.GQISeXXQ4*fv4o8o?` | Defined by you |
| `[chatflow_id]` | `3cb9c5ec-7967-4e3f-b4cc-6dd365c3838c` | Retrieved from Flowise Agentflow |
| `[flowise_api_key]` | `FOJnTNwjXhRu22JdZYh0_fp41bGlUhPT7mfNBShtaKs` | Retrieved from Flowise API settings |

> **Security Advisory:** The examples above are fictional and illustrate what the values might look like. Your Flowise dashboard represents the administrative backend of your AI architecture. It is imperative to secure it using strong, cryptographically complex strings for both your username and password. **Under no circumstances should you use default or easily compromised credentials** such as `Admin`, `123456`, or `QWERTY`. Do not use the examples above; create your own. You can use tools like KeePass to store these passwords in an encrypted container.

---

## PHASE 1: Prerequisites

1. **Download and install Docker Desktop** (available for Windows, Mac, or Linux - [Docker Desktop](https://www.docker.com/)).
2. **Start Docker Desktop** and ensure the engine is running (the whale icon in your system tray should be green or say "Docker Desktop Running").
3. **Install Ollama:** Go to [Ollama.com](https://ollama.com) and download the installer for your operating system. Run the installer.
4. **Download and Run the AI Model:** Open a terminal and run the following command to start the latest **llama3.2** model:

   `ollama run llama3.2:latest`
   
*Note: This is a lightweight model that runs smoothly on most systems. Larger models generally offer better performance for complex tasks. If your system has sufficient memory, you can use larger models — ensure they fit within your available VRAM or unified memory (on macOS). The first time you run this, Ollama will download the model files. Depending on your internet speed, this may take a few minutes.*

5. **Verify it is Working:** Once the download finishes, you will see a `>>> Send a message` prompt in your terminal. Type `Hello` and press Enter. If the AI replies, your local model is working perfectly!

---

## PHASE 2: Create the Database Volume

We are going to tell Docker to carve out a permanent, protected space on your hard drive to save your Flowise database and AI memory.

1. Open the Terminal in Docker.
2. Enter the following command and press enter (you can choose any name; in this example, the volume is named **telegram_extended_flowise**):
   
`docker volume create telegram_extended_flowise`

3. Ensure that the volume was created successfully under "Volumes" in your Docker Desktop dashboard.

---

## PHASE 3: Create Your Project Files

Create a new folder on your computer, e.g., `D:\progs\Flowise\telegram-flowise-project`. We will reference this folder as `[folder_path]`. Inside this folder, create two files:

### 1. docker-compose.yml

Download the [`docker-compose.yml`](https://github.com/stefan-frick/Flowise-Telegram-Bot/blob/main/src/docker-compose.yml) from the repository `/src` into `[folder_path]`.

**Open the folder in a code editor (e.g. Visual Studio Code) and replace the following variables in the file:**

* `Flowise` section:
  
  a) `[volume]` with the name of the `[volume]` you created in **Phase 2** (i.e. `telegram_extended_flowise`)
  
  b) `[flowise_username]` with your chosen username, ensure to store it safely
  
  c) `[flowise_password]` with your chosen password, ensure to store it safely
  
* `volumes` section:
  
  a) `[volume]` with the name of the `[volume]` you created in **Phase 2** (i.e. `telegram_extended_flowise`)
  
* `telegram-bot` section:
  
  a) Ignore the variables in this section of the file for now — you will fill them in later.

* Save the file.

### 2. bot.py

Download the [`bot.py`](https://github.com/stefan-frick/Flowise-Telegram-Bot/blob/main/src/bot.py) from the repository `/src` into `[folder_path]`. 

**No variables need to be changed inside this file** — it reads everything from the YAML environment.

---

## PHASE 4: Boot Flowise & Get Your API Info

We need to start Flowise so we can generate your API Key and retrieve your Chatflow ID.

1. Go to the Terminal in Docker and navigate to your folder:
`cd [folder_path]`
2. Run this command to start the Flowise container:
`docker compose up -d flowise`
3. Wait for some seconds until the status indicator of the docker contrainer turns green indicating that the container has booted up correctly. 
4. Open your web browser and go to `http://localhost:4000`. Enter your `[flowise_username]` and `[flowise_password]` into the setup fields. *(For the administrator account, enter a username, email address, and password. These are stored locally in the Docker volume).*

### Create Your Local Agentflow:

1. In the left menu, click **Agentflows**.
2. Ensure **V2** is selected, then click **Add New**.
3. Click the **Save** icon, enter an agent name (e.g., `Telegram Agent`), and confirm with **Save**.
4. Click the **+** button. Drag and drop an **Agent** node into the workspace.
5. Connect the Start node to the Agent node.
6. Double-click the Agent node to open its settings and configure the model:
* Select **ChatOllama**
* Set Base URL to `http://host.docker.internal:11434`
* Enter the model name, e.g., `llama3.2:latest`
* Leave all other parameters unchanged.


7. Click **OK**, then save the workflow.
8. Click the chat icon to test a conversation with your local Ollama model to verify it works.

### Retrieve Keys:

1. Return to the Flowise home screen and navigate to **API Keys**.
2. Click **+ Create Key** to generate the API Key (`[flowise_api_key]`). Name it `telegram_bot`, select all **AGENTFLOWS** checkboxes, and click **Add**.
3. Click **Copy** to copy the generated API Key. Open `docker-compose.yml` and replace `[flowise_api_key]` with this key.
4. Return to your `Telegram Agent` agentflow. Click the **API Endpoint** button (`</>` icon).
5. Open the Python tab and select the `telegram_bot` authorization key created earlier.
6. Copy the `chatflow_id` — it is the last segment of the API URL after `http://localhost:4000/api/v1/prediction/`.
7. Open `docker-compose.yml` and replace `[chatflow_id]` with the copied ID.

---

## PHASE 5: Gather Your Telegram Credentials

Before launching the bot, we need your two unique Telegram keys to connect and restrict access.

1. **Get your Bot Token (`[telegram_token]`):**
* Open the Telegram app and search for **@BotFather**.
* Send the command `/newbot`.
* Follow the prompts to give your bot a display name and a unique username (it must end in `bot`).
* BotFather will reply with your HTTP API Token. Copy this string and replace `[telegram_token]` in `docker-compose.yml`.


2. **Get your User ID (`[telegram_user_id]`):**
* *This acts as the "bouncer" so the bot only responds to you.*
* Search for **@userinfobot** (or **@getmyid_bot**) in Telegram and send `/start`.
* Copy the numeric `Id` it replies with and replace `[telegram_user_id]` in `docker-compose.yml`.



---

## PHASE 6: Finalize, Launch, and Monitor

1. Open `docker-compose.yml` one last time. Verify all variables in the `telegram-bot` environment section are filled. Save the file.
2. Run this command to flush the cache and apply your newest settings:
`docker compose up -d --force-recreate`
3. Verify in Docker Desktop that no errors occurred, the service `flowise-telegram-bot` has been added, and all status indicators are green.
4. To monitor your bot in real-time, run this log command:
`docker logs -f --tail 10 flowise-telegram-bot`
*(Press `Ctrl + C` to exit the live log view.)*

**Start Chatting:** Open Telegram, search for the bot username you created in Phase 5, and send it a message. You are now talking to your fully private, locally-hosted AI!

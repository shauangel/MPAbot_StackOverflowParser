# Stack Overflow Parser

This is a web parsing service for Stack Overflow.

---

# Preconditions

Before deployment, make sure Docker and Docker compose are installed on your computer.

You can use the following commands to check if Docker is installed:

```bash
node -v
npm -v
```

If not installed,...

---
# Deployment

```bash
# Clone this project
git clone https://github.com/shauangel/MPAbot_StackOverflowParser.git

# Navigate to the project directory
cd MPAbot_StackOverflowParser

# build image
docker compose build

# start deploy the service 
docker compose up -d

```

---
# API Interfaces
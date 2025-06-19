#!/bin/bash

echo "🚀 Starting Arbitrage Bot setup..."

apt update && apt upgrade -y
apt install -y git python3 python3-pip screen

echo "📥 Cloning arbitrage bot repository..."
git clone https://github.com/vinny-jpi/arbitrage-bot.git /opt/arbitrage-bot

cd /opt/arbitrage-bot || { echo "❌ Failed to enter bot directory"; exit 1; }

echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

echo "🖥️ Launching bot in new screen session..."
screen -dmS arbitrage-bot python3 main.py

echo "✅ Arbitrage Bot installed and running in background."
echo "Use 'screen -r arbitrage-bot' to view the session."

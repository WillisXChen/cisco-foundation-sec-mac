#!/bin/bash
# This script adds powermetrics to /etc/sudoers.d/ to allow execution without a password.
# This allows Chainlit to collect Apple Silicon power data in the background without
# needing to run the entire server as root.

echo "Adding powermetrics to the sudoers NOPASSWD list..."
echo "Requesting administrator privileges..."

sudo bash -c "echo \"${USER} ALL=(ALL) NOPASSWD: /usr/bin/powermetrics\" > /etc/sudoers.d/powermetrics-nopasswd"
sudo chmod 0440 /etc/sudoers.d/powermetrics-nopasswd

echo "✅ Setup complete! Chainlit can now access ASITOP power data in real-time."

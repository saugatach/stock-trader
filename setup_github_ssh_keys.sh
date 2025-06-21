#!/bin/bash

# === CONFIGURATION ===
PERSONAL_EMAIL="saugata.ch@gmail.com"
BUSINESS_EMAIL="tensorllcaz@gmail.com"

# Filenames
PERSONAL_KEY="$HOME/.ssh/id_ed25519_personal"
BUSINESS_KEY="$HOME/.ssh/id_ed25519_business"
SSH_CONFIG="$HOME/.ssh/config"

# === 1. Generate SSH Keys ===
echo "Generating personal SSH key..."
ssh-keygen -t ed25519 -C "$PERSONAL_EMAIL" -f "$PERSONAL_KEY" -N ""

echo "Generating business SSH key..."
ssh-keygen -t ed25519 -C "$BUSINESS_EMAIL" -f "$BUSINESS_KEY" -N ""

# === 2. Add to SSH agent ===
eval "$(ssh-agent -s)"
ssh-add "$PERSONAL_KEY"
ssh-add "$BUSINESS_KEY"

# === 3. Update ~/.ssh/config ===
echo "Writing SSH config..."

cat <<EOF >> "$SSH_CONFIG"

# Personal GitHub
Host github.com-personal
  HostName github.com
  User git
  IdentityFile $PERSONAL_KEY

# Business GitHub
Host github.com-business
  HostName github.com
  User git
  IdentityFile $BUSINESS_KEY
EOF

# === 4. Output public keys for copy-paste to GitHub ===
echo
echo "=== Personal public key ==="
cat "${PERSONAL_KEY}.pub"
echo
echo "Add this to your PERSONAL GitHub account at: https://github.com/settings/keys"
echo

echo "=== Business public key ==="
cat "${BUSINESS_KEY}.pub"
echo
echo "Add this to your BUSINESS GitHub account at: https://github.com/settings/keys"
echo

# === 5. Reminder to update remote URL ===
echo "✅ DONE. Now run this in your repo:"
echo "  git remote set-url origin git@github.com-business:your-business-username/your-repo.git"


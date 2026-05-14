#!/usr/bin/env bash
# .devcontainer/setup.sh
# Runs once after the container is created (postCreateCommand).
# Sets up all tools and dependencies required by the migrator.
set -euo pipefail

WORKSPACE_ROOT="/workspaces"
MIGRATOR_DIR="${WORKSPACE_ROOT}/genrevive-migrator-swing2angular"
GENREVIVE_DIR="${WORKSPACE_ROOT}/genrevive"

echo "========================================"
echo " GenRevive Migrator – Dev Container Setup"
echo "========================================"

# ── 1. Angular CLI v17 ────────────────────────────────────────────────────────
echo "[1/5] Installing Angular CLI v17..."
npm install -g @angular/cli@17.0.0

# ── 2. OpenAPI Generator CLI ──────────────────────────────────────────────────
echo "[2/5] Installing OpenAPI Generator CLI..."
npm install -g @openapitools/openapi-generator-cli

# ── 3. Poetry ─────────────────────────────────────────────────────────────────
echo "[3/5] Installing Poetry via pipx..."
pipx install poetry
# Ensure Poetry creates the venv inside the project folder
poetry config virtualenvs.in-project true

# ── 4. Clone genrevive sibling repository ────────────────────────────────────
# In Codespaces only this migrator repo is cloned by default.
# The genrevive core library must sit at ../genrevive relative to this repo,
# which maps to /workspaces/genrevive inside the container.
echo "[4/5] Cloning genrevive dependency..."
if [ ! -d "${GENREVIVE_DIR}" ]; then
  # Use the feature branch referenced in README.md
  git clone \
    --depth 1 \
    --branch feature/updated \
    https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive.git \
    "${GENREVIVE_DIR}" || {
      echo "WARNING: Could not clone genrevive automatically."
      echo "  Please clone it manually into ${GENREVIVE_DIR} and run:"
      echo "  cd ${MIGRATOR_DIR} && poetry install"
    }
else
  echo "  genrevive directory already exists, skipping clone."
fi

# ── 5. Patch pyproject.toml genrevive reference ─────────────────────────────
echo "[5/7] Patching pyproject.toml genrevive path..."
sed -i 's|^genrevive = .*|genrevive = { path = "../genrevive/genrevive-1.14.0.tar.gz", develop = false }|' "${MIGRATOR_DIR}/migrator/pyproject.toml"

# ── 6. Create logs directory and logfile ─────────────────────────────────────
echo "[6/7] Creating logs/logfile.log..."
mkdir -p "${MIGRATOR_DIR}/logs"
touch "${MIGRATOR_DIR}/logs/logfile.log"

# ── 7. Create target-project directory ───────────────────────────────────────
echo "[7/7] Creating target-project directory..."
mkdir -p "${WORKSPACE_ROOT}/target-project"

# ── Install Python dependencies ───────────────────────────────────────────────
echo "Installing Python dependencies via Poetry..."
cd "${MIGRATOR_DIR}"
poetry lock --no-update 2>/dev/null || true
poetry install

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Copy .env.template to .env and fill in your Azure OpenAI credentials."
echo "  2. Copy activities/target_code_generator/.env.template"
echo "       to activities/target_code_generator/.env  (default values are fine)."
echo "  3. Place your Java Swing MVP input project at the path set in ORIGIN_PROJECT_PATH."
echo "  4. Run: python main.py"

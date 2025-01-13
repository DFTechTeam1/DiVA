#!/bin/sh

# Define the source and target paths
SOURCE_DIR="/home/dfactory/Project/utils/diva/client_preview"
TARGET_DIR="/home/dfactory/Project/DiVA/assets"

# Show usage information
show_help() {
  echo "Usage: sh $0 [ --link | --unlink | --help ]"
  echo ""
  echo "Options:"
  echo "--link       Create a symbolic link from the source directory to the target directory."
  echo "--unlink     Remove the symbolic link from the target directory."
  echo "--help       Show this help message."
  echo ""
  echo "Source Directory: $SOURCE_DIR"
  echo "Target Directory: $TARGET_DIR"
}

# Check command-line arguments
if [ "$1" = "--help" ] || [ -z "$1" ]; then
  show_help
  exit 0
fi

# Parse arguments
case "$1" in
  --link)
    echo "Creating symbolic link..."
    if [ ! -L "$TARGET_DIR" ]; then
      ln -s "$SOURCE_DIR" "$TARGET_DIR"
      echo "Symlink created: $TARGET_DIR -> $SOURCE_DIR"
    else
      echo "Symlink already exists: $TARGET_DIR"
    fi
    ;;
  --unlink)
    echo "Removing symbolic link..."
    if [ -L "$TARGET_DIR" ]; then
      unlink "$TARGET_DIR"
      echo "Symlink removed: $TARGET_DIR"
    else
      echo "No symlink to remove at: $TARGET_DIR"
    fi
    ;;
  *)
    echo "Invalid option: $1"
    show_help
    exit 1
    ;;
esac

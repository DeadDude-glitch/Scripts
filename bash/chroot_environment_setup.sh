#!/bin/bash

# Check if an argument was provided for the chroot directory
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <chroot_directory>"
  exit 1
fi

# Get the chroot directory path from the command-line argument
CHROOT_DIR="$1"

# Check if the chroot directory exists
if [ ! -d "$CHROOT_DIR" ]; then
  echo "Chroot directory not found: $CHROOT_DIR"
  exit 1
fi

# Bind essential directories to the chroot environment
mount --bind /proc "$CHROOT_DIR/proc"
mount --bind /sys "$CHROOT_DIR/sys"
mount --bind /dev "$CHROOT_DIR/dev"
mount --bind /dev/pts "$CHROOT_DIR/dev/pts"
mount --bind /dev/shm "$CHROOT_DIR/dev/shm"
mount --bind /run "$CHROOT_DIR/run"
mount --bind /tmp "$CHROOT_DIR/tmp"

# Copy resolv.conf and hostname files for network configuration
cp /etc/resolv.conf "$CHROOT_DIR/etc/resolv.conf"
cp /etc/hostname "$CHROOT_DIR/etc/hostname"

# Chroot into the target directory
chroot "$CHROOT_DIR" /bin/bash

# When you exit the chroot environment, unmount the directories
umount "$CHROOT_DIR/proc"
umount "$CHROOT_DIR/sys"
umount "$CHROOT_DIR/dev/pts"
umount "$CHROOT_DIR/dev/shm"
umount "$CHROOT_DIR/run"
umount "$CHROOT_DIR/tmp"

# Optionally, remove copied files
rm "$CHROOT_DIR/etc/resolv.conf"
rm "$CHROOT_DIR/etc/hostname"

echo "Chroot environment exited."

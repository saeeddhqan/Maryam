#!/bin/bash

echo "Please run this as sudo"

rm -rv /usr/local/lib/python3.8/dist-packages/maryam*
pip uninstall requirements

read -p "Would you like to remove all project directories and files? (y/N) " user_choice
if [ "$user_choice" == 'y' ] || [ "$user_choice" == 'Y' ]; then
  echo "Proceeding to delete Maryam"

  curr_folder=$(pwd)
  echo "Removing $curr_folder"
  rm -rfv "$curr_folder"
  exit 1

else
    echo "Maryam Files and Directory kept intact"
    echo "Exiting Script"
    exit 1
fi

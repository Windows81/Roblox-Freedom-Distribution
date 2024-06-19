#!/bin/bash

# Display a whiptail menu with two options
CHOICE=$(whiptail --title "Menu" --menu "Choose an option:" 15 50 2 \
"1" "Host" \
"2" "Join" 3>&1 1>&2 2>&3)

# Exit status of whiptail
EXIT_STATUS=$?

# Check the exit status
if [ $EXIT_STATUS = 0 ]; then
    case $CHOICE in
        1)
            # Execute host.sh
            ./host.sh
            ;;
        2)
            # Execute join.sh
            ./join.sh
            ;;
        *)
            # Handle unexpected input
            echo "Invalid option"
            ;;
    esac
else
    echo "You chose Cancel."
fi


#!/bin/sh

FILE_NAME="CSGv3.rbxmx"
dir_name="BinaryStrings_"$FILE_NAME
mkdir $dir_name

awk -v d="$dir_name" '
BEGIN {
    toggle = 0;
    output = "";
}

/<SharedString/ {
    toggle = 1;
}

/<\/SharedString>/ {
    # After the end of this iteration, `toggle` will be reset to 0.
    toggle = 2;
}

{
    # Skips this line if `toggle` is not set.
    if (!toggle) next;

    # Removes leading and trailing whitespace.
    gsub(/^[ \t]+|[ \t]+$/, "", $0);

    # Appends the cleaned line to output.
    output = output $0;

    # Toggles between 1 and 0.
    toggle = toggle % 2;

    # If toggle is back to 0, print the accumulated output.
    if (!toggle) {
        # Gets the substring excluding XML tags.
        match(output, /<SharedString[^>]*>([^<]*)<\/SharedString>/, a);

        # Decode the base64 string
        cmd = "echo -n \"" a[1] "\" | base64 --decode"
    cmd | getline decoded_line
    close(cmd)

    # Write to a file with leading zeros
    filename = sprintf("%s/%03d.bin", d, NR)
	print filename
    print decoded_line > filename

        # Resets output for the next cycle.
        output = "";
}
}
' $FILE_NAME

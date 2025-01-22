If you make a union in 2025E Studio, it will not show in 2021E or 2018M versions of Rōblox.

Rōblox's CSG system works differently between modern versions of Rōblox and the ones that RFD uses.

If you want to get the binary strings of `CSGv3.rbxmx`, you can use the following command:

```sh
cat "./CSGv3.rbxmx" | awk '
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

		# Prints the captured string inside.
        print a[1];

		# Resets output for the next cycle.
        output = "";
    }
}
'
```

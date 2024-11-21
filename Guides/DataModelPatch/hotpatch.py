from assets.serialisers import rbxl as parser
read_file_name = r"C:\Users\USERNAME\Documents\Projects\FilteringDisabled\Roblox\v463\DataModelPatch.rbxm"
write_file_name = r"C:\Users\USERNAME\Documents\Projects\FilteringDisabled\Roblox\v463\Player\Content\Models\DataModelPatch\DataModelPatch.rbxm"

read_data = open(read_file_name, 'rb').read()
write_data = parser.parse(read_data)
open(write_file_name, 'wb').write(write_data)

from assets.serialisers import rbxl as parser
import util.resource
import util.versions
import unittest


class TestPatchDataModelPatch(unittest.TestCase):
    def test_patch_data_model_patch(self) -> None:
        '''
        Tests that the DataModelPatch can be patched.
        '''
        read_file_name = util.resource.retr_rōblox_full_path(
            util.versions.rōblox.v463,
            util.resource.bin_subtype.PLAYER,
            'Content', 'Models', 'DataModelPatch', 'DataModelPatch.rbxm',
        )
        write_file_name = util.resource.retr_rōblox_full_path(
            util.versions.rōblox.v463,
            util.resource.bin_subtype.PLAYER,
            'Content', 'Models', 'DataModelPatch', '_DataModelPatch.rbxm',
        )

        read_data = open(read_file_name, 'rb').read()
        write_data = parser.parse(read_data)
        open(write_file_name, 'wb').write(write_data)

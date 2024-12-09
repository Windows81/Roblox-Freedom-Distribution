from assets.serialisers import rbxl, mesh
import assets.extract
import unittest


class TestAssets(unittest.TestCase):
    '''
    Tests for the asset extraction module.
    '''

    def test_place_load(self) -> None:
        '''
        Tests that the data can be loaded and parsed by the parser.
        Asserts that the data has been loaded at all, then checks if it can be
        parsed by the RBXL parser.
        '''
        data = assets.extract.download_rōblox_asset(1818)
        self.assertIsNotNone(data)
        assert data is not None
        self.assertTrue(rbxl.check(data))

    def test_audio_load(self) -> None:
        '''
        Tests that audio data can be loaded and parsed by the parser.
        Asserts that the data has been loaded at all,
        then checks if it is either an OGG or a WAVE audio file.
        '''
        data = assets.extract.download_rōblox_asset(12222084)
        self.assertIsNotNone(data)
        assert data is not None
        self.assertRegex(data, b'(OggS|RIFF)')

    def test_image_load(self) -> None:
        '''
        Tests that specific image data can be loaded and is in the PNG format.
        '''
        data = assets.extract.download_rōblox_asset(270995247)
        # Asserts that the data has been loaded at all.
        self.assertIsNotNone(data)
        assert data is not None
        # Asserts that the data starts with the PNG header, indicating it is a valid PNG image.
        self.assertTrue(data.startswith(b'PNG'))

    def test_mesh_load(self) -> None:
        '''
        Tests that mesh data can be loaded and parsed by the parser.
        Asserts that the data has been loaded at all, then checks if it can be
        parsed by the `mesh` parser.
        '''
        data = assets.extract.download_rōblox_asset(120627289)
        self.assertIsNotNone(data)
        assert data is not None
        parsed_data = mesh.parse(data)
        self.assertRegex(parsed_data, rb'^version')

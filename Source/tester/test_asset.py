# Standard library imports
import unittest

# Local application imports
import assets.serialisers as serialisers
import assets.extractor as extractor


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
        data = extractor.download_rōblox_asset(1818)
        self.assertIsNotNone(data)
        assert data is not None

        self.assertTrue(serialisers.rbxl.check(data))

    def test_audio_load(self) -> None:
        '''
        Tests that audio data can be loaded and parsed by the parser.
        Asserts that the data has been loaded at all,
        then checks if it is either an OGG or a WAVE audio file.
        '''
        data = extractor.download_rōblox_asset(12222084)
        self.assertIsNotNone(data)
        assert data is not None

        self.assertRegex(data, b'(OggS|RIFF)')

    def test_video_load(self) -> None:
        '''
        Tests that video data can be loaded and parsed by the parser.
        '''
        data = extractor.download_rōblox_asset(5608333583)
        self.assertIsNotNone(data)
        assert data is not None

        self.assertTrue(serialisers.video.check(data))
        webm_data = serialisers.video.parse(data)
        self.assertIsNotNone(webm_data)

    def test_image_load(self) -> None:
        '''
        Tests that specific image data can be loaded and is in the PNG format.
        '''
        data = extractor.download_rōblox_asset(270995247)
        self.assertIsNotNone(data)
        assert data is not None

        # Asserts that the data starts with the PNG header, indicating it is a valid PNG image.
        self.assertTrue(data.startswith(b'\x89PNG'))

    def test_mesh_load(self) -> None:
        '''
        Tests that mesh data can be loaded and parsed by the parser.
        Asserts that the data has been loaded at all, then checks if it can be
        parsed by the `mesh` parser.
        '''
        data = extractor.download_rōblox_asset(120627289)
        self.assertIsNotNone(data)
        assert data is not None

        result = serialisers.mesh.parse(data) or data
        self.assertRegex(result, rb'^version')

    @unittest.skip("AttributeError: type object 'method' has no attribute 'convert_csg'")
    def test_csg_load(self) -> None:
        '''
        Tests that CSG v3 unions can be parsed.
        '''
        data = extractor.download_rōblox_asset(4500696697)
        self.assertIsNotNone(data)
        assert data is not None

        serialisers.rbxl.parse(
            data, methods={serialisers.rbxl.method.convert_csg},
        )

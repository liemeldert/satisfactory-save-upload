import unittest
import objects


class TestObjects(unittest.TestCase):
    def test_read_save(self):
        save = objects.GameSave("test_save.sav")
        assert save.header_version == 8
        assert save.save_version == 25
        assert save.build_version == 159365
        assert save.world_type == "Persistent_Level"
        assert save.world_properties == "?startloc=Grass Fields?sessionName=123?Visibility=SV_FriendsOnly"
        assert save.session_name == "123"
        assert save.play_time == 6605
        assert save.save_date == 637621495663610000
        assert save.session_visibility is True
        assert save.editor_object_version == 38
        assert save.mod_metadata is None
        assert save.mod_flags == 0

    def test_game(self):
        game = objects.Game("sdjkfjhkjhsadfkjdfsdkljhhk", "")
        assert game.state is False
        assert game.saves == [objects.GameSave("test_save.sav")]
        assert game.get_latest_save() == objects.GameSave("test_save.sav")


if __name__ == '__main__':
    unittest.main()

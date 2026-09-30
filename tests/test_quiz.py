import sys
import types
import unittest
from unittest.mock import MagicMock, patch


class Session(dict):
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value


streamlit = types.ModuleType("streamlit")
streamlit.session_state = Session()
streamlit.progress = MagicMock()
streamlit.subheader = MagicMock()
streamlit.write = MagicMock()
streamlit.link_button = MagicMock()
streamlit.error = MagicMock()
streamlit.expander = MagicMock()
streamlit.expander.return_value.__enter__ = MagicMock()
streamlit.expander.return_value.__exit__ = MagicMock(return_value=False)
streamlit.button = MagicMock(return_value=False)
sys.modules.setdefault("streamlit", streamlit)

from services.ujian_siswa_app import UjianSiswaApp  # noqa: E402


class QuizTest(unittest.TestCase):
    def setUp(self):
        streamlit.session_state.clear()
        streamlit.link_button.reset_mock()

    def test_three_questions_and_reward_only_for_perfect_result(self):
        ujian = UjianSiswaApp()
        self.assertTrue(ujian.siapkan_sesi())
        self.assertEqual(len(streamlit.session_state.soal_list), 3)

        with patch("services.ujian_siswa_app.ambil_link_daget", return_value="https://example.com"):
            for benar in range(3):
                streamlit.session_state.jumlah_benar = benar
                ujian.tampilkan_hasil_web()
                streamlit.link_button.assert_not_called()

            streamlit.session_state.jumlah_benar = 3
            ujian.tampilkan_hasil_web()
            streamlit.link_button.assert_called_once_with(
                "Buka link daget", "https://example.com"
            )


if __name__ == "__main__":
    unittest.main()

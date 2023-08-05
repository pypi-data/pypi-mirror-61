import os
from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat, TreeChord
from musicscore.musictree.treechordflags2 import FingerTremoloFlag2
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        xml_path = path + '_test_1.xml'
        durations = [2, 2, 2]
        midis = [60, 62, 63]
        sf = SimpleFormat(durations=durations, midis=midis)
        for chord in sf.chords:
            chord.add_flag(FingerTremoloFlag2(tremolo_chord=TreeChord(midis=[67])))

        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_2(self):
        xml_path = path + '_test_2.xml'
        durations = [1.5, 1.5, 1.5]
        midis = [60, 62, 63]
        sf = SimpleFormat(durations=durations, midis=midis)
        for chord in sf.chords:
            chord.add_flag(FingerTremoloFlag2(tremolo_chord=TreeChord(midis=[67])))

        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_3(self):
        xml_path = path + '_test_3.xml'
        durations = [0.25]
        midis = [60]
        sf = SimpleFormat(durations=durations, midis=midis)
        for chord in sf.chords:
            chord.add_flag(FingerTremoloFlag2(tremolo_chord=TreeChord(midis=[67])))

        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        # TestScore().assert_template(xml_path)

    def test_4(self):
        xml_path = path + '_test_4.xml'
        durations = [0.2, 0.8, 1]
        midis = [60, 62, 63]
        sf = SimpleFormat(durations=durations, midis=midis)
        for chord in sf.chords:
            chord.add_flag(FingerTremoloFlag2(tremolo_chord=TreeChord(midis=[67])))

        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        # TestScore().assert_template(xml_path)


import os
import demucs.separate
from pedalboard import Pedalboard, load_plugin
import soundfile as sf


def separate_vocals(input_file, mp3_bitrate=320):
    demucs.separate.main(
        [
            "-d",
            "cuda",
            "--mp3",
            "--mp3-bitrate",
            mp3_bitrate,
            "--two-stems",
            "vocals",
            "-n",
            "htdemucs",
            input_file,
        ]
    )


def apply_vst(input_file, output_file):
    c2_vst_path = "vsts\FabFilter Pro-C 2.vst3"
    c2_plugin = load_plugin(c2_vst_path)
    c2_plugin.active = True
    c2_plugin.parameters["Ratio"].value = 4.0
    c2_plugin.parameters["Threshold"].value = -24.0
    c2_plugin.parameters["Attack"].value = 0.1
    c2_plugin.parameters["Release"].value = 60.0
    c2_plugin.parameters["Auto Release"].value = False
    c2_plugin.parameters["Knee"].value = 2.0
    c2_plugin.parameters["Lookahead"].value = 10.0
    c2_plugin.parameters["Hold"].value = 0.0
    c2_plugin.parameters["Auto Gain"].value = True

    board = Pedalboard([c2_plugin])
    audio, sample_rate = sf.read(input_file)


# separate_vocals("extracted_audio.mp4")
apply_vst("inputs\extracted_audio.mp4", "outputs\output.wav")

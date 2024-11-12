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


def prepere_c2_plugin():
    c2_vst_path = "vsts\FabFilter Pro-C 2.vst3"
    c2_plugin = load_plugin(c2_vst_path)
    c2_plugin.active = True
    c2_plugin.parameters["ratio"].value = 4.0
    c2_plugin.parameters["threshold"].value = -24.0
    c2_plugin.parameters["attack"].value = 0.1
    c2_plugin.parameters["release"].value = 60.0
    c2_plugin.parameters["auto_release"].value = False
    c2_plugin.parameters["knee"].value = 2.0
    c2_plugin.parameters["lookahead"].value = 10.0
    c2_plugin.parameters["hold"].value = 0.0
    c2_plugin.parameters["auto_gain"].value = True
    return c2_plugin


def apply_vst(input_file, output_path):
    c2_plugin = prepere_c2_plugin()

    board = Pedalboard([c2_plugin])
    audio, sample_rate = sf.read(input_file)
    processed_audio = board(audio, sample_rate)

    sf.write(
        output_path,
        processed_audio,
        sample_rate,
        format="MP3",
        subtype="PCM_16",
        bitrate="320k",
    )


# separate_vocals("extracted_audio.mp4")
apply_vst("inputs\extracted_audio.mp3", "outputs\output.mp3")

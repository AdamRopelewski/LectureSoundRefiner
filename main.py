import demucs.separate
from pedalboard import Pedalboard, load_plugin
import soundfile as sf
import pyloudnorm as pyln


def separate_vocals(input_file, mp3_bitrate=320):
    demucs.separate.main(
        [
            "-d",
            "cuda",
            "--mp3",
            "--mp3-bitrate",
            str(mp3_bitrate),
            "--two-stems",
            "vocals",
            "-n",
            "htdemucs",
            input_file,
        ]
    )


def read_and_normalize_audio(input_path, target_lufs=-22):
    audio, sample_rate = sf.read(input_path)
    meter = pyln.Meter(sample_rate)
    loudness = meter.integrated_loudness(audio)
    normalized_audio = pyln.normalize.loudness(audio, loudness, target_lufs)

    return normalized_audio, sample_rate


def prepere_c2_plugin():
    c2_vst_path = "vsts\FabFilter Pro-C 2.vst3"
    c2_plugin = load_plugin(c2_vst_path)
    c2_plugin.active = True
    c2_plugin.parameters["ratio"].value = 4.0
    c2_plugin.parameters["threshold"].value = -26.0
    c2_plugin.parameters["attack"].value = 0.1
    c2_plugin.parameters["release"].value = 60.0
    c2_plugin.parameters["auto_release"].value = False
    c2_plugin.parameters["knee"].value = 2.0
    c2_plugin.parameters["lookahead"].value = 10.0
    c2_plugin.parameters["hold"].value = 0.0
    c2_plugin.parameters["auto_gain"].value = True
    return c2_plugin


def normlize_peaks(audio, sample_rate):
    meter = pyln.Meter(sample_rate)
    normalized_audio = pyln.normalize.peak(audio, -1.0)
    return normalized_audio


def save_processed(output_path, processed_audio, sample_rate):
    sf.write(output_path, processed_audio, sample_rate)


def apply_vst(input_file, output_path):
    audio, sample_rate = read_and_normalize_audio(input_file)

    c2_plugin = prepere_c2_plugin()

    board = Pedalboard([c2_plugin])

    processed_audio = board(audio, sample_rate)
    audio_to_save = normlize_peaks(processed_audio, sample_rate)
    save_processed(output_path, audio_to_save, sample_rate)


# separate_vocals("inputs\extracted_audio.mp4")
print("Separation finished")
apply_vst(r"separated\\htdemucs\\extracted_audio\\vocals.mp3", "outputs\output.mp3")
print("Processing finished")

import demucs.separate
from pedalboard import Pedalboard, load_plugin
import soundfile as sf
import pyloudnorm as pyln
import os


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
    c2_plugin.ratio = "4.00:1"
    c2_plugin.threshold = -26.0
    c2_plugin.attack = 0.1
    c2_plugin.release = 60.0
    c2_plugin.auto_release = False
    c2_plugin.knee = 2.0
    c2_plugin.lookahead = 10.0
    c2_plugin.hold = 0.0
    c2_plugin.auto_gain = True
    c2_plugin.oversampling = "2x"

    return c2_plugin


def prepare_q3_plugin():
    q3_vst_path = "vsts\FabFilter Pro-Q 3.vst3"
    q3_plugin = load_plugin(q3_vst_path)
    q3_plugin.active = True

    q3_plugin.band_1_used = "Used"
    q3_plugin.band_1_enabled = True
    q3_plugin.band_1_gain = 1.0
    q3_plugin.band_1_frequency = 155.0
    q3_plugin.band_1_q = 1.0
    q3_plugin.band_1_shape = "Bell"
    q3_plugin.band_1_slope = "12 dB/oct"

    q3_plugin.band_2_used = "Used"
    q3_plugin.band_2_enabled = True
    q3_plugin.band_2_gain = -5.5
    q3_plugin.band_2_frequency = 490.0
    q3_plugin.band_2_q = 1.0
    q3_plugin.band_2_shape = "Bell"
    q3_plugin.band_2_slope = "12 dB/oct"

    q3_plugin.band_3_used = "Used"
    q3_plugin.band_3_enabled = True
    q3_plugin.band_3_gain = 3.0
    q3_plugin.band_3_frequency = 2560.0
    q3_plugin.band_3_q = 1.0
    q3_plugin.band_3_shape = "Bell"
    q3_plugin.band_3_slope = "12 dB/oct"

    q3_plugin.band_4_used = "Used"
    q3_plugin.band_4_enabled = True
    q3_plugin.band_4_gain = 6.0
    q3_plugin.band_4_frequency = 6900.0
    q3_plugin.band_4_q = 1.0
    q3_plugin.band_4_shape = "Bell"
    q3_plugin.band_4_slope = "12 dB/oct"

    q3_plugin.band_5_used = "Used"
    q3_plugin.band_5_enabled = True
    q3_plugin.band_5_gain = 0.0
    q3_plugin.band_5_frequency = 100.0
    q3_plugin.band_5_q = 2.0
    q3_plugin.band_5_shape = "Low Cut"
    q3_plugin.band_5_slope = "36 dB/oct"

    q3_plugin.band_6_used = "Used"
    q3_plugin.band_6_enabled = True
    q3_plugin.band_6_gain = 0.0
    q3_plugin.band_6_frequency = 15000.0
    q3_plugin.band_6_q = 1.0
    q3_plugin.band_6_shape = "High Cut"
    q3_plugin.band_6_slope = "36 dB/oct"

    return q3_plugin


def prepeare_l2_plugin():
    l2_vst_path = "vsts\FabFilter Pro-L 2.vst3"
    l2_plugin = load_plugin(l2_vst_path)
    l2_plugin.active = True

    l2_plugin.gain = 11.0
    l2_plugin.output_level = -1.0
    l2_plugin.oversampling = "2x"
    l2_plugin.true_peak_limiting = True
    # print(l2_plugin.parameters)

    return l2_plugin


def normlize_peaks(audio):
    normalized_audio = pyln.normalize.peak(audio, -1.0)
    return normalized_audio


def save_processed(output_path, processed_audio, sample_rate):
    sf.write(output_path, processed_audio, sample_rate)


def apply_vst(input_file, output_path):
    audio, sample_rate = read_and_normalize_audio(input_file)

    c2_plugin = prepere_c2_plugin()
    q3_plugin = prepare_q3_plugin()
    l2_plugin = prepeare_l2_plugin()

    board = Pedalboard([c2_plugin, q3_plugin, l2_plugin])

    processed_audio = board(audio, sample_rate)
    # audio_to_save = normlize_peaks(processed_audio)
    audio_to_save = processed_audio

    save_processed(output_path, audio_to_save, sample_rate)


def main(input_file, output_path):
    separate_vocals(input_file)
    dir_name = os.path.splitext(os.path.basename(input_file))[
        0
    ]  # get the name of the file without extension
    print("Separation finished")
    apply_vst(rf"separated\htdemucs\{dir_name}\vocals.mp3", output_path)
    print("Processing finished")


if __name__ == "__main__":
    main("inputs\extracted_audio.mp4", "outputs\output.mp3")

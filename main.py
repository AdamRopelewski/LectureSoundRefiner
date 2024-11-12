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
    c2_plugin.parameters["oversampling"].value = "2x"
    return c2_plugin


def prepare_q3_plugin():
    q3_vst_path = "vsts\FabFilter Pro-Q 3.vst3"
    q3_plugin = load_plugin(q3_vst_path)
    q3_plugin.active = True

    q3_plugin.parameters["band_1_enabled"].value = True
    q3_plugin.parameters["band_1_gain"].value = 2.0
    q3_plugin.parameters["band_1_frequency"].value = 155.0
    q3_plugin.parameters["band_1_q"].value = 1.0
    q3_plugin.parameters["band_1_shape"].value = "Bell"
    q3_plugin.parameters["band_1_slope"].value = "12 dB/oct"

    q3_plugin.parameters["band_2_enabled"].value = True
    q3_plugin.parameters["band_2_gain"].value = -4.5
    q3_plugin.parameters["band_2_frequency"].value = 490.0
    q3_plugin.parameters["band_2_q"].value = 1.0
    q3_plugin.parameters["band_2_shape"].value = "Bell"
    q3_plugin.parameters["band_2_slope"].value = "12 dB/oct"

    q3_plugin.parameters["band_3_enabled"].value = True
    q3_plugin.parameters["band_3_gain"].value = 2.0
    q3_plugin.parameters["band_3_frequency"].value = 2560.0
    q3_plugin.parameters["band_3_q"].value = 1.0
    q3_plugin.parameters["band_3_shape"].value = "Bell"
    q3_plugin.parameters["band_3_slope"].value = "12 dB/oct"

    q3_plugin.parameters["band_4_enabled"].value = True
    q3_plugin.parameters["band_4_gain"].value = 5.0
    q3_plugin.parameters["band_4_frequency"].value = 6900.0
    q3_plugin.parameters["band_4_q"].value = 1.0
    q3_plugin.parameters["band_4_shape"].value = "Bell"
    q3_plugin.parameters["band_4_slope"].value = "12 dB/oct"

    q3_plugin.parameters["band_5_enabled"].value = True
    q3_plugin.parameters["band_5_gain"].value = 0.0
    q3_plugin.parameters["band_5_frequency"].value = 100.0
    q3_plugin.parameters["band_5_q"].value = 1.0
    q3_plugin.parameters["band_5_shape"].value = "Low Cut"
    q3_plugin.parameters["band_5_slope"].value = "36 dB/oct"

    q3_plugin.parameters["band_6_enabled"].value = True
    q3_plugin.parameters["band_6_gain"].value = 0.0
    q3_plugin.parameters["band_6_frequency"].value = 15000.0
    q3_plugin.parameters["band_6_q"].value = 1.0
    q3_plugin.parameters["band_6_shape"].value = "High Cut"
    q3_plugin.parameters["band_6_slope"].value = "36 dB/oct"

    return q3_plugin


def prepeare_l2_plugin():
    l2_vst_path = "vsts\FabFilter Pro-L 2.vst3"
    l2_plugin = load_plugin(l2_vst_path)
    l2_plugin.active = True

    l2_plugin.parameters["output_level"].value = -1.0
    l2_plugin.parameters["style"].value = "Safe"
    l2_plugin.parameters["oversampling"].value = "2x"
    l2_plugin.parameters["true_peak_limiting"].value = True
    l2_plugin.parameters["gain"].value = 8.0

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
    audio_to_save = normlize_peaks(processed_audio)

    save_processed(output_path, audio_to_save, sample_rate)


separate_vocals("inputs\extracted_audio.mp4")
print("Separation finished")
apply_vst(r"separated\\htdemucs\\extracted_audio\\vocals.mp3", "outputs\output.mp3")
print("Processing finished")

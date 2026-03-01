from Codes.Pipeline import pipeline


def test_call_compress_prefers_stabilized_file(monkeypatch):
    runner = pipeline()
    main_file = "sample.mov"
    captured = {}

    def fake_exists(candidate):
        return candidate == "sample_Stabilized.mp4"

    def fake_video_compression(filename, new_filename):
        captured["filename"] = filename
        captured["new_filename"] = new_filename
        return True

    monkeypatch.setattr("Codes.Pipeline.path.exists", fake_exists)
    monkeypatch.setattr("Codes.Pipeline._load_video_compression", lambda: fake_video_compression)

    runner.callCompress(main_file)

    assert captured["filename"] == "sample_Stabilized.mp4"
    assert captured["new_filename"] == "sample_Compressed.mp4"


def test_call_face_detect_prefers_compressed_file(monkeypatch):
    runner = pipeline()
    main_file = "sample.mov"
    captured = {}

    def fake_exists(candidate):
        return candidate in {"sample_Compressed.mp4", "sample_Stabilized.mp4"}

    def fake_face_extraction(filename, new_filename, correction_factor):
        captured["filename"] = filename
        captured["new_filename"] = new_filename
        captured["correction_factor"] = correction_factor

    monkeypatch.setattr("Codes.Pipeline.path.exists", fake_exists)
    monkeypatch.setattr("Codes.Pipeline._load_face_extraction", lambda: fake_face_extraction)

    runner.callFaceDetect(main_file, 30)

    assert captured["filename"] == "sample_Compressed.mp4"
    assert captured["new_filename"] == "sample_FaceDetector.mp4"
    assert captured["correction_factor"] == 30


def test_call_lip_extract_prefers_face_detector_file(monkeypatch):
    runner = pipeline()
    main_file = "sample.mov"
    captured = {}

    def fake_exists(candidate):
        return candidate in {"sample_FaceDetector.mp4", "sample_Compressed.mp4", "sample_Stabilized.mp4"}

    def fake_lip_extraction(filename, new_filename, correction_factor):
        captured["filename"] = filename
        captured["new_filename"] = new_filename
        captured["correction_factor"] = correction_factor

    monkeypatch.setattr("Codes.Pipeline.path.exists", fake_exists)
    monkeypatch.setattr("Codes.Pipeline._load_lip_extraction", lambda: fake_lip_extraction)

    runner.callLipExtraction(main_file, 30)

    assert captured["filename"] == "sample_FaceDetector.mp4"
    assert captured["new_filename"] == "sample_LipDetector.mp4"
    assert captured["correction_factor"] == 30


def test_call_tongue_track_uses_lip_file_and_updates_excel(monkeypatch):
    runner = pipeline()
    main_file = "sample.mov"
    captured = {}

    def fake_exists(candidate):
        return candidate == "sample_LipDetector.mp4"

    def fake_frequency_calc(filename, threshold, thresh_iterations, visual_area, disp, time_slice, model):
        captured["frequency_input"] = (
            filename,
            threshold,
            thresh_iterations,
            visual_area,
            disp,
            time_slice,
            model,
        )
        return 10, 1, 4, 5, 2, 25, time_slice

    def fake_excel_updater(timestamp, filename, time_slice, frequency_total, errors, sweeps_mode, time_mode,
                          sweeps_mean, time_mean, stdev):
        captured["excel"] = (
            filename,
            time_slice,
            frequency_total,
            errors,
            sweeps_mode,
            time_mode,
            sweeps_mean,
            time_mean,
            stdev,
        )

    monkeypatch.setattr("Codes.Pipeline.path.exists", fake_exists)
    monkeypatch.setattr("Codes.Pipeline._load_frequency_calculation", lambda: fake_frequency_calc)
    monkeypatch.setattr(runner, "excelUpadter", fake_excel_updater)

    runner.callTongueTrack(main_file, 40, 2, False, 0, 5, model="m", save_in_excel=True)

    assert captured["frequency_input"][0] == "sample_LipDetector.mp4"
    assert captured["excel"][0] == "sample_LipDetector.mp4"
    assert captured["excel"][5] == 16
    assert captured["excel"][7] == 20


def test_cui_calls_steps_in_order(monkeypatch):
    runner = pipeline()
    call_order = []

    monkeypatch.setattr(runner, "callStabilize", lambda *args, **kwargs: call_order.append("stabilize"))
    monkeypatch.setattr(runner, "callCompress", lambda *args, **kwargs: call_order.append("compress"))
    monkeypatch.setattr(runner, "callFaceDetect", lambda *args, **kwargs: call_order.append("face"))
    monkeypatch.setattr(runner, "callLipExtraction", lambda *args, **kwargs: call_order.append("lip"))
    monkeypatch.setattr(runner, "callTongueTrack", lambda *args, **kwargs: call_order.append("frequency"))

    runner.CUI(
        "sample.mov",
        True,
        True,
        True,
        True,
        True,
        40,
        2,
        0,
        False,
        30,
        30,
        True,
        5,
        model="m",
        SMOOTHING_RADIUS=50,
    )

    assert call_order == ["stabilize", "compress", "face", "lip", "frequency"]


def test_call_perform_all_forwards_correct_arguments(monkeypatch):
    runner = pipeline()
    captured = {}

    def fake_cui(*args):
        captured["args"] = args

    monkeypatch.setattr(runner, "CUI", fake_cui)
    runner.callPerformAll("sample.mov", 50, 40, 2, 0, False, 30, 30, model="m", save_in_excel=True, time_slice=5)

    assert captured["args"][0] == "sample.mov"
    assert captured["args"][6] == 40
    assert captured["args"][13] == 5
    assert captured["args"][14] == "m"
    assert captured["args"][15] == 50

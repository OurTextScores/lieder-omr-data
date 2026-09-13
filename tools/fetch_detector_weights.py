#!/usr/bin/env python3
"""Fetch the detector weights the vendored runtime needs before detection runs.

Only `.py` sources are vendored, so the segmentation and staff-detection ONNX graphs are
not in `vendor/homr-stage2`. HOMR fetches them through its own pinned downloader, and
nothing in the build triggered that - so every page raised "model file doesn't exist"
inside `detect_score`'s per-page `try/except`, which exists to skip title pages and blank
leaves. All 215 scores reported "OK: 0 page(s), 0 system(s)" and the build went on to
produce 0 pairs.

Run as a module so it uses the vendored HOMR on PYTHONPATH, not any other checkout.
"""

from homr.main import download_weights


def main() -> None:
    """Fetch both segnet precisions, because the CPU can end up loading either.

    `detect_imslp_systems` builds its Segnet with GPU inference requested. With no GPU
    execution provider present that path does not fall back to the fp32 graph - it prints
    "running on the CPU instead" and loads the **fp16** one, which
    `download_weights(segnet_use_gpu=False)` never fetches. Asking for both is one HTTP
    request more and removes the coupling between which device is requested, which is
    available, and which file happens to be on disk.
    """
    for segnet_use_gpu in (False, True):
        download_weights(
            segnet_use_gpu=segnet_use_gpu, transformer_use_gpu=False, coreml_encoder=False
        )
    print("detector weights present")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Set, Tuple

from google.cloud.speech_v1.types import SpeechRecognitionAlternative, SpeechRecognitionResult, WordInfo


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Segment:
    speaker: Optional[int]
    text: str
    start: float
    end: float

    def to_dict(self) -> dict:
        return {
            "speaker": self.speaker,
            "text": self.text,
            "start": self.start,
            "end": self.end,
        }


def _time_to_seconds(time_info: WordInfo) -> Tuple[float, float]:
    def _convert(maybe) -> float:
        if maybe is None:
            return 0.0
        return maybe.seconds + maybe.nanos / 1_000_000_000

    return _convert(time_info.start_time), _convert(time_info.end_time)


class DiarizationProcessor:
    def __init__(self, logs_dir: Path) -> None:
        self._seen_keys: Set[Tuple[Optional[int], float, float, str]] = set()
        self._log_path = Path(logs_dir) / "diarization_latest.json"

    def build_segments(self, result: SpeechRecognitionResult) -> List[Segment]:
        if not result.alternatives:
            return []

        alternative = result.alternatives[0]
        text = alternative.transcript.strip()
        if not text:
            return []

        segments = self._segments_from_words(alternative)
        if not segments:
            segments = [Segment(speaker=None, text=text, start=0.0, end=0.0)]

        unique_segments = self._deduplicate(segments)
        self._write_log(unique_segments)
        return unique_segments

    def _segments_from_words(self, alternative: SpeechRecognitionAlternative) -> List[Segment]:
        words = getattr(alternative, "words", [])
        if not words:
            return []

        segments: List[Segment] = []
        current_words: List[str] = []
        current_speaker: Optional[int] = None
        current_start: Optional[float] = None
        current_end: Optional[float] = None

        for word in words:
            speaker_tag = word.speaker_tag or None
            word_start, word_end = _time_to_seconds(word)

            if current_speaker != speaker_tag and current_words:
                segments.append(
                    Segment(
                        speaker=current_speaker,
                        text=self._finalize_text(current_words),
                        start=current_start or 0.0,
                        end=current_end or word_end,
                    ),
                )
                current_words = []
                current_start = None

            current_words.append(word.word)
            current_speaker = speaker_tag
            current_start = current_start or word_start
            current_end = word_end

        if current_words:
            segments.append(
                Segment(
                    speaker=current_speaker,
                    text=self._finalize_text(current_words),
                    start=current_start or 0.0,
                    end=current_end or 0.0,
                ),
            )

        return segments

    @staticmethod
    def _finalize_text(words: Iterable[str]) -> str:
        text = " ".join(words)
        return text.replace("  ", " ").strip()

    def _deduplicate(self, segments: Iterable[Segment]) -> List[Segment]:
        deduped: List[Segment] = []
        for segment in segments:
            key = (
                segment.speaker,
                round(segment.start, 2),
                round(segment.end, 2),
                segment.text,
            )
            if key in self._seen_keys:
                continue
            self._seen_keys.add(key)
            deduped.append(segment)
        return deduped

    def _write_log(self, segments: Iterable[Segment]) -> None:
        try:
            payload = [segment.to_dict() for segment in segments]
            self._log_path.parent.mkdir(parents=True, exist_ok=True)
            self._log_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as exc:  # pragma: no cover - logging only
            logger.debug("Failed to write diarization log: %s", exc)

import os
import re
from dataclasses import dataclass
from datetime import timedelta


TIMESTAMP_PATTERN = re.compile(
    r'(?P<start>\d{1,2}:\d{2}:\d{2},\d{3})\s+-->\s+(?P<end>\d{1,2}:\d{2}:\d{2},\d{3})'
)


@dataclass
class SubtitleEntry:
    index: int
    start: timedelta
    end: timedelta
    text: str


def _parse_timestamp(timestamp: str) -> timedelta:
    hours, minutes, rest = timestamp.split(':')
    seconds, milliseconds = rest.split(',')
    return timedelta(
        hours=int(hours),
        minutes=int(minutes),
        seconds=int(seconds),
        milliseconds=int(milliseconds),
    )


def _format_timestamp(value: timedelta) -> str:
    total_milliseconds = int(value.total_seconds() * 1000)
    hours, remainder = divmod(total_milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, milliseconds = divmod(remainder, 1000)
    return f'{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}'


def _parse_srt(srt_text: str) -> list[SubtitleEntry]:
    blocks = re.split(r'\n\s*\n', srt_text.strip())
    entries = []

    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue

        if len(lines) < 2:
            raise ValueError(f'Invalid subtitle block: {block!r}')

        if lines[0].isdigit():
            index = int(lines[0])
            timing_line = lines[1]
            text_lines = lines[2:]
        else:
            index = len(entries) + 1
            timing_line = lines[0]
            text_lines = lines[1:]

        match = TIMESTAMP_PATTERN.fullmatch(timing_line)
        if match is None:
            raise ValueError(f'Invalid subtitle timing line: {timing_line!r}')

        text = ' '.join(part.strip() for part in text_lines if part.strip())
        entries.append(
            SubtitleEntry(
                index=index,
                start=_parse_timestamp(match.group('start')),
                end=_parse_timestamp(match.group('end')),
                text=text,
            )
        )

    return entries


def _group_entries_by_gap(entries: list[SubtitleEntry], gap_threshold: timedelta) -> list[list[SubtitleEntry]]:
    if not entries:
        return []

    groups = [[entries[0]]]
    for entry in entries[1:]:
        previous_entry = groups[-1][-1]
        if entry.start - previous_entry.end > gap_threshold:
            groups.append([entry])
            continue
        groups[-1].append(entry)

    return groups


def text_from_srt(srt_text: str, gap_threshold_seconds: float = 0.0) -> str:
    entries = _parse_srt(srt_text)
    groups = _group_entries_by_gap(entries, timedelta(seconds=max(gap_threshold_seconds, 0.0)))
    paragraphs = [' '.join(entry.text for entry in group if entry.text) for group in groups]
    return '\n\n'.join(paragraph for paragraph in paragraphs if paragraph)


def _build_srt(entries: list[SubtitleEntry]) -> str:
    blocks = []
    for index, entry in enumerate(entries, start=1):
        blocks.append(
            f'{index}\n'
            f'{_format_timestamp(entry.start)} --> {_format_timestamp(entry.end)}\n'
            f'{entry.text}\n'
        )
    return '\n'.join(blocks)


def write_gap_segments(
    srt_text: str,
    output_dir: str,
    base_name: str = 'subtitles',
    gap_threshold_seconds: float = 0.0,
) -> list[str]:
    entries = _parse_srt(srt_text)
    groups = _group_entries_by_gap(entries, timedelta(seconds=max(gap_threshold_seconds, 0.0)))
    created_files = []

    for index, group in enumerate(groups, start=1):
        segment_path = os.path.join(output_dir, f'{base_name}_part_{index:02}.srt')
        with open(segment_path, 'w', encoding='utf-8') as segment_file:
            segment_file.write(_build_srt(group))
        created_files.append(segment_path)

    return created_files


def main(
    srt_path: str | None = None,
    gap_threshold_seconds: float = 0.0,
    create_gap_files: bool = False,
) -> str:
    if srt_path is None:
        srt_path = os.path.join(os.path.dirname(__file__), 'subtitles.srt')

    with open(srt_path, 'r', encoding='utf-8') as subtitle_file:
        srt_text = subtitle_file.read()

    restored_text = text_from_srt(srt_text, gap_threshold_seconds=gap_threshold_seconds)
    output_dir = os.path.dirname(srt_path)
    base_name = os.path.splitext(os.path.basename(srt_path))[0]
    text_output_path = os.path.join(output_dir, f'{base_name}.txt')

    with open(text_output_path, 'w', encoding='utf-8') as text_file:
        text_file.write(restored_text)

    if create_gap_files:
        write_gap_segments(
            srt_text,
            output_dir=output_dir,
            base_name=base_name,
            gap_threshold_seconds=gap_threshold_seconds,
        )

    return restored_text



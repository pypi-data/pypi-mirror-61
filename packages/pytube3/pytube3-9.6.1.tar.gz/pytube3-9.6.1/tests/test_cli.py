# -*- coding: utf-8 -*-
import argparse
from unittest import mock
from unittest.mock import MagicMock, patch

import pytest

from pytube import cli, StreamQuery, Caption, CaptionQuery

parse_args = cli._parse_args


@mock.patch("pytube.cli.YouTube")
def test_download_when_itag_not_found(youtube):
    youtube.streams = mock.Mock()
    youtube.streams.all.return_value = []
    youtube.streams.get_by_itag.return_value = None
    with pytest.raises(SystemExit):
        cli.download_by_itag(youtube, 123)
    youtube.streams.get_by_itag.assert_called_with(123)


@mock.patch("pytube.cli.YouTube")
@mock.patch("pytube.Stream")
def test_download_when_itag_is_found(youtube, stream):
    stream.itag = 123
    youtube.streams = StreamQuery([stream])
    with patch.object(
        youtube.streams, "get_by_itag", wraps=youtube.streams.get_by_itag
    ) as wrapped_itag:
        cli.download_by_itag(youtube, 123)
        wrapped_itag.assert_called_with(123)
    youtube.register_on_progress_callback.assert_called_with(cli.on_progress)
    stream.download.assert_called()


@mock.patch("pytube.cli.YouTube")
@mock.patch("pytube.Stream")
def test_display_stream(youtube, stream):
    stream.itag = 123
    stream.__repr__ = MagicMock(return_value="")
    youtube.streams = StreamQuery([stream])
    with patch.object(youtube.streams, "all", wraps=youtube.streams.all) as wrapped_all:
        cli.display_streams(youtube)
        wrapped_all.assert_called()
        stream.__repr__.assert_called()


@mock.patch("pytube.cli.YouTube")
def test_download_caption_with_none(youtube):
    caption = Caption(
        {"url": "url1", "name": {"simpleText": "name1"}, "languageCode": "en"}
    )
    youtube.captions = CaptionQuery([caption])
    with patch.object(
        youtube.captions, "all", wraps=youtube.captions.all
    ) as wrapped_all:
        cli.download_caption(youtube, None)
        wrapped_all.assert_called()


@mock.patch("pytube.cli.YouTube")
def test_download_caption_with_language_found(youtube):
    youtube.title = "video title"
    caption = Caption(
        {"url": "url1", "name": {"simpleText": "name1"}, "languageCode": "en"}
    )
    caption.download = MagicMock(return_value="file_path")
    youtube.captions = CaptionQuery([caption])
    cli.download_caption(youtube, "en")
    caption.download.assert_called_with(title="video title", output_path=None)


@mock.patch("pytube.cli.YouTube")
def test_download_caption_with_language_not_found(youtube):
    caption = Caption(
        {"url": "url1", "name": {"simpleText": "name1"}, "languageCode": "en"}
    )
    youtube.captions = CaptionQuery([caption])
    with patch.object(
        youtube.captions, "all", wraps=youtube.captions.all
    ) as wrapped_all:
        cli.download_caption(youtube, "blah")
        wrapped_all.assert_called()


def test_display_progress_bar(capsys):
    cli.display_progress_bar(bytes_received=25, filesize=100, scale=0.55)
    out, _ = capsys.readouterr()
    assert "25.0%" in out


@mock.patch("pytube.Stream")
@mock.patch("io.BufferedWriter")
def test_on_progress(stream, writer):
    stream.filesize = 10
    cli.display_progress_bar = MagicMock()
    cli.on_progress(stream, "", writer, 7)
    cli.display_progress_bar.assert_called_once_with(3, 10)


def test_parse_args_falsey():
    parser = argparse.ArgumentParser()
    args = cli._parse_args(parser, ["http://youtube.com/watch?v=9bZkp7q19f0"])
    assert args.url == "http://youtube.com/watch?v=9bZkp7q19f0"
    assert args.build_playback_report is False
    assert args.itag is None
    assert args.list is False
    assert args.verbosity == 0


def test_parse_args_truthy():
    parser = argparse.ArgumentParser()
    args = cli._parse_args(
        parser,
        [
            "http://youtube.com/watch?v=9bZkp7q19f0",
            "--build-playback-report",
            "-c",
            "en",
            "-l",
            "--itag=10",
        ],
    )
    assert args.url == "http://youtube.com/watch?v=9bZkp7q19f0"
    assert args.build_playback_report is True
    assert args.itag == 10
    assert args.list is True


@mock.patch("pytube.cli.YouTube", return_value=None)
def test_main_download_by_itag(youtube):
    parser = argparse.ArgumentParser()
    args = parse_args(parser, ["http://youtube.com/watch?v=9bZkp7q19f0", "--itag=10"])
    cli._parse_args = MagicMock(return_value=args)
    cli.download_by_itag = MagicMock()
    cli.main()
    youtube.assert_called()
    cli.download_by_itag.assert_called()


@mock.patch("pytube.cli.YouTube", return_value=None)
def test_main_build_playback_report(youtube):
    parser = argparse.ArgumentParser()
    args = parse_args(
        parser, ["http://youtube.com/watch?v=9bZkp7q19f0", "--build-playback-report"]
    )
    cli._parse_args = MagicMock(return_value=args)
    cli.build_playback_report = MagicMock()
    cli.main()
    youtube.assert_called()
    cli.build_playback_report.assert_called()


@mock.patch("pytube.cli.YouTube", return_value=None)
def test_main_display_streams(youtube):
    parser = argparse.ArgumentParser()
    args = parse_args(parser, ["http://youtube.com/watch?v=9bZkp7q19f0", "-l"])
    cli._parse_args = MagicMock(return_value=args)
    cli.display_streams = MagicMock()
    cli.main()
    youtube.assert_called()
    cli.display_streams.assert_called()


@mock.patch("pytube.cli.YouTube", return_value=None)
def test_main_download_caption(youtube):
    parser = argparse.ArgumentParser()
    args = parse_args(parser, ["http://youtube.com/watch?v=9bZkp7q19f0", "-c"])
    cli._parse_args = MagicMock(return_value=args)
    cli.download_caption = MagicMock()
    cli.main()
    youtube.assert_called()
    cli.download_caption.assert_called()


@mock.patch("pytube.cli.YouTube", return_value=None)
@mock.patch("pytube.cli.download_by_resolution")
def test_download_by_resolution_flag(youtube, download_by_resolution):
    parser = argparse.ArgumentParser()
    args = parse_args(parser, ["http://youtube.com/watch?v=9bZkp7q19f0", "-r", "320p"])
    cli._parse_args = MagicMock(return_value=args)
    cli.main()
    youtube.assert_called()
    download_by_resolution.assert_called()


@mock.patch("pytube.cli.Playlist")
def test_download_with_playlist(playlist):
    cli.safe_filename = MagicMock(return_value="safe_title")
    parser = argparse.ArgumentParser()
    args = parse_args(parser, ["https://www.youtube.com/playlist?list=PLyn"])
    cli._parse_args = MagicMock(return_value=args)
    cli.main()
    playlist.assert_called()


@mock.patch("pytube.cli.YouTube")
@mock.patch("pytube.StreamQuery")
@mock.patch("pytube.Stream")
def test_download_by_resolution(youtube, stream_query, stream):
    stream_query.get_by_resolution.return_value = stream
    youtube.streams = stream_query
    cli._download = MagicMock()
    cli.download_by_resolution(youtube=youtube, resolution="320p", target="test_target")
    cli._download.assert_called_with(stream, target="test_target")


@mock.patch("pytube.cli.YouTube")
@mock.patch("pytube.StreamQuery")
def test_download_by_resolution_not_exists(youtube, stream_query):
    stream_query.get_by_resolution.return_value = None
    youtube.streams = stream_query
    cli._download = MagicMock()
    with pytest.raises(SystemExit):
        cli.download_by_resolution(
            youtube=youtube, resolution="DOESNT EXIST", target="test_target"
        )
    cli._download.assert_not_called()

from __future__ import annotations

import argparse
import sys
import unittest
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from src.stream_capture import main as stream_capture_main
from src.stream_capture import StreamCapture


class TestStreamCapture(TestCase):
    """
    Tests for the StreamCapture class.
    """

    def setUp(self) -> None:
        """Set up a StreamCapture instance for use in tests."""
        # Initialise StreamCapture instance with a presumed stream URL
        self.stream_capture: StreamCapture = StreamCapture(
            'http://example.com/stream',
        )

    @patch('cv2.VideoCapture')
    async def test_initialise_stream_success(
        self,
        mock_video_capture: MagicMock,
    ) -> None:
        """
        Test that the stream is successfully initialised.

        Args:
            mock_video_capture (MagicMock): Mock for cv2.VideoCapture.
        """
        # Mock VideoCapture object's isOpened method to
        # return True, indicating the stream opened successfully
        mock_video_capture.return_value.isOpened.return_value = True

        # Call initialise_stream method to initialise the stream
        await self.stream_capture.initialise_stream(
            self.stream_capture.stream_url,
        )

        # Assert that the cap object is successfully initialised
        self.assertIsNotNone(self.stream_capture.cap)

        # Verify that VideoCapture was called correctly
        mock_video_capture.assert_called_once_with(
            self.stream_capture.stream_url,
        )

        # Release resources
        await self.stream_capture.release_resources()

    @patch('cv2.VideoCapture')
    @patch('time.sleep', return_value=None)
    async def test_initialise_stream_retry(
        self,
        mock_sleep: MagicMock,
        mock_video_capture: MagicMock,
    ) -> None:
        """
        Test that the stream initialisation retries if it fails initially.

        Args:
            mock_sleep (MagicMock): Mock for time.sleep.
            mock_video_capture (MagicMock): Mock for cv2.VideoCapture.
        """
        # Mock VideoCapture object's isOpened method to
        # return False on the first call and True on the second
        instance = mock_video_capture.return_value
        instance.isOpened.side_effect = [False, True]

        # Call initialise_stream method to simulate retry mechanism
        await self.stream_capture.initialise_stream(
            self.stream_capture.stream_url,
        )

        # Assert that the cap object is eventually successfully initialised
        self.assertIsNotNone(self.stream_capture.cap)

        # Verify that sleep method was called once to wait before retrying
        mock_sleep.assert_called_once_with(5)

    async def test_release_resources(self) -> None:
        """
        Test that resources are released correctly.
        """
        # Initialise StreamCapture instance and mock cap object
        stream_capture: StreamCapture = StreamCapture('test_stream_url')
        stream_capture.cap = MagicMock()

        # Call release_resources method to release resources
        await stream_capture.release_resources()

        # Assert that cap object is set to None
        self.assertIsNone(stream_capture.cap)

    @patch('cv2.VideoCapture')
    @patch('cv2.Mat')
    @patch('time.sleep', return_value=None)
    async def test_execute_capture(
        self,
        mock_sleep: MagicMock,
        mock_mat: MagicMock,
        mock_video_capture: MagicMock,
    ) -> None:
        """
        Test that frames are captured and returned with a timestamp.

        Args:
            mock_sleep (MagicMock): Mock for time.sleep.
            mock_video_capture (MagicMock): Mock for cv2.VideoCapture.
        """
        # Mock VideoCapture object's read method to
        # return a frame and True indicating successful read
        mock_video_capture.return_value.read.return_value = (True, mock_mat)
        mock_video_capture.return_value.isOpened.return_value = True

        # Execute capture frame generator and get the first frame and timestamp
        generator = self.stream_capture.execute_capture()
        frame, timestamp = await generator.__anext__()

        # Assert that the captured frame is not None
        # and the timestamp is a float
        self.assertIsNotNone(frame)
        self.assertIsInstance(timestamp, float)

        # Release resources
        await self.stream_capture.release_resources()

    @patch('speedtest.Speedtest')
    def test_check_internet_speed(self, mock_speedtest: MagicMock) -> None:
        """
        Test that internet speed is correctly checked and returned.

        Args:
            mock_speedtest (MagicMock): Mock for speedtest.Speedtest.
        """
        # Mock Speedtest object's download and upload methods
        # to return download and upload speeds
        mock_speedtest.return_value.download.return_value = 50_000_000
        mock_speedtest.return_value.upload.return_value = 10_000_000

        # Check internet speed and assert that
        # the returned speeds are correct
        download_speed, upload_speed = (
            self.stream_capture.check_internet_speed()
        )
        self.assertEqual(download_speed, 50.0)
        self.assertEqual(upload_speed, 10.0)

    @patch('streamlink.streams')
    def test_select_quality_based_on_speed_high_speed(
        self,
        mock_streams: MagicMock,
    ) -> None:
        """
        Test that the highest quality stream is selected
        for high internet speed.

        Args:
            mock_streams (MagicMock): Mock for streamlink.streams.
        """
        # Mock streamlink to return different quality streams
        mock_streams.return_value = {
            'best': MagicMock(url='http://best.stream'),
            '1080p': MagicMock(url='http://1080p.stream'),
            '720p': MagicMock(url='http://720p.stream'),
            '480p': MagicMock(url='http://480p.stream'),
        }

        # Mock internet speed check result
        with patch.object(
            self.stream_capture,
            'check_internet_speed',
            return_value=(20, 5),
        ):
            # Select the best stream quality based on internet speed
            selected_quality = (
                self.stream_capture.select_quality_based_on_speed()
            )
            self.assertEqual(selected_quality, 'http://best.stream')

    @patch('streamlink.streams')
    def test_select_quality_based_on_speed_medium_speed(
        self,
        mock_streams: MagicMock,
    ) -> None:
        """
        Test that an appropriate quality stream is selected
        for medium internet speed.

        Args:
            mock_streams (MagicMock): Mock for streamlink.streams.
        """
        # Mock streamlink to return medium quality streams
        mock_streams.return_value = {
            '720p': MagicMock(url='http://720p.stream'),
            '480p': MagicMock(url='http://480p.stream'),
            '360p': MagicMock(url='http://360p.stream'),
        }

        # Mock internet speed check result
        with patch.object(
            self.stream_capture,
            'check_internet_speed',
            return_value=(7, 5),
        ):
            # Select the appropriate stream quality based on internet speed
            selected_quality = (
                self.stream_capture.select_quality_based_on_speed()
            )
            self.assertEqual(selected_quality, 'http://720p.stream')

    @patch('streamlink.streams')
    def test_select_quality_based_on_speed_low_speed(
        self,
        mock_streams: MagicMock,
    ) -> None:
        """
        Test that a lower quality stream is selected for low internet speed.

        Args:
            mock_streams (MagicMock): Mock for streamlink.streams.
        """
        # Mock streamlink to return low quality streams
        mock_streams.return_value = {
            '480p': MagicMock(url='http://480p.stream'),
            '360p': MagicMock(url='http://360p.stream'),
            '240p': MagicMock(url='http://240p.stream'),
        }

        # Mock internet speed check result
        with patch.object(
            self.stream_capture,
            'check_internet_speed',
            return_value=(3, 5),
        ):
            # Select the lower quality stream based on internet speed
            selected_quality = (
                self.stream_capture.select_quality_based_on_speed()
            )
            self.assertEqual(selected_quality, 'http://480p.stream')

    @patch('streamlink.streams', return_value={})
    @patch.object(StreamCapture, 'check_internet_speed', return_value=(20, 5))
    def test_select_quality_based_on_speed_no_quality(
        self,
        mock_check_speed: MagicMock,
        mock_streams: MagicMock,
    ) -> None:
        """
        Test that None is returned if no suitable stream quality is available.

        Args:
            mock_check_speed (MagicMock): Mock for check_internet_speed method.
            mock_streams (MagicMock): Mock for streamlink.streams.
        """
        # Mock internet speed and stream quality check result to be empty
        selected_quality = self.stream_capture.select_quality_based_on_speed()
        self.assertIsNone(selected_quality)

    @patch(
        'streamlink.streams', return_value={
            'best': MagicMock(url='http://best.stream'),
            '720p': MagicMock(url='http://720p.stream'),
            '480p': MagicMock(url='http://480p.stream'),
        },
    )
    @patch.object(StreamCapture, 'check_internet_speed', return_value=(20, 5))
    @patch('cv2.VideoCapture')
    @patch('time.sleep', return_value=None)
    async def test_capture_generic_frames(
        self,
        mock_sleep: MagicMock,
        mock_video_capture: MagicMock,
        mock_check_speed: MagicMock,
        mock_streams: MagicMock,
    ) -> None:
        """
        Test that generic frames are captured and returned with a timestamp.

        Args:
            mock_sleep (MagicMock): Mock for time.sleep.
            mock_video_capture (MagicMock): Mock for cv2.VideoCapture.
            mock_check_speed (MagicMock): Mock for check_internet_speed method.
            mock_streams (MagicMock): Mock for streamlink.streams.
        """
        # Mock VideoCapture object's behaviour
        mock_video_capture.return_value.read.return_value = (True, MagicMock())
        mock_video_capture.return_value.isOpened.return_value = True

        # Execute capture frame generator
        generator = self.stream_capture.capture_generic_frames()
        frame, timestamp = await generator.__anext__()

        # Verify the returned frame and timestamp
        self.assertIsNotNone(frame)
        self.assertIsInstance(timestamp, float)

        # Release resources
        await self.stream_capture.release_resources()

    def test_update_capture_interval(self) -> None:
        """
        Test that the capture interval is updated correctly.
        """
        # Update capture interval and verify
        self.stream_capture.update_capture_interval(20)
        self.assertEqual(self.stream_capture.capture_interval, 20)

    @patch('argparse.ArgumentParser.parse_args')
    async def test_main_function(
        self,
        mock_parse_args: MagicMock,
    ) -> None:
        """
        Test that the main function correctly initialises
        and executes StreamCapture.

        Args:
            mock_parse_args (MagicMock):
                Mock for argparse.ArgumentParser.parse_args.
        """
        # Mock command line argument parsing
        mock_parse_args.return_value = argparse.Namespace(
            url='test_stream_url',
        )

        # Mock command line argument parsing
        mock_capture_instance = MagicMock()
        with patch(
            'src.stream_capture.StreamCapture',
            return_value=mock_capture_instance,
        ):
            with patch.object(
                sys, 'argv', ['stream_capture.py', '--url', 'test_stream_url'],
            ):
                await stream_capture_main()
            mock_capture_instance.execute_capture.assert_called_once()

    @patch('cv2.VideoCapture')
    @patch('time.sleep', return_value=None)
    @pytest.mark.asyncio
    async def test_execute_capture_failures(
        self,
        mock_sleep: MagicMock,
        mock_video_capture: MagicMock,
    ) -> None:
        """
        Test that execute_capture handles multiple failures before success.

        Args:
            mock_sleep (MagicMock): Mock for time.sleep.
            mock_video_capture (MagicMock): Mock for cv2.VideoCapture.
        """
        # Mock VideoCapture object's multiple failures and one success read
        instance: MagicMock = mock_video_capture.return_value
        instance.read.side_effect = [(False, None)] * 5 + [(True, MagicMock())]
        instance.isOpened.return_value = True

        # Mock capture_generic_frames method and execute
        with patch.object(
            self.stream_capture,
            'capture_generic_frames',
            return_value=iter([(MagicMock(), 1234567890.0)]),
        ) as mock_capture_generic_frames:
            generator = self.stream_capture.execute_capture()
            frame, timestamp = await generator.__anext__()
            self.assertIsNotNone(frame)
            self.assertIsInstance(timestamp, float)

            # Verify that capture_generic_frames method was called
            mock_capture_generic_frames.assert_called_once()

        # Release resources
        await self.stream_capture.release_resources()


if __name__ == '__main__':
    unittest.main()

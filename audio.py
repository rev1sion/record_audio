import audioop
import contextlib
import time

import pyaudio
import wave


class Audio:
    _CHUNK = 1024
    _WIDTH = 2
    _CHANNELS = 2

    _pa = ''
    _stream = ''
    _command_stop = ''

    def __init__(self,
                 input_device_index=None,  # None - get default by OS
                 output_device_index=None,
                 rate=44100,
                 audio_format="paInt16",
                 min_seconds=5,
                 max_seconds=10,
                 volume=2,
                 filename='record.wav'):
        self._INPUT_DEVICE = input_device_index
        self._OUTPUT_DEVICE = output_device_index
        self._RATE = rate
        self._FORMAT = self.audio_format(audio_format)
        self._MIN_RECORD_SECONDS = min_seconds
        self._MAX_RECORD_SECONDS = max_seconds
        self._VOLUME_LEVEL = volume
        self._WAVE_OUTPUT_FILENAME = filename
        self._pa = pyaudio.PyAudio()
        self._stream = self.init_stream()

    def init_stream(self, play=True):
        return self._pa.open(
            format=self._FORMAT,
            channels=self._CHANNELS,
            rate=self._RATE,
            frames_per_buffer=self._CHUNK,
            input=True,
            output=play,
            input_device_index=self._INPUT_DEVICE,
            output_device_index=self._OUTPUT_DEVICE
        )

    def record(self):
        """
        Записывать пока команда не стоп и время не больше установленого
        :return: array audio data, binaries
        """
        time_start = time.time()
        frames = []
        while self._command_stop != 'stop':
            for i in range(0, int(self._RATE / self._CHUNK * self._MIN_RECORD_SECONDS)):
                data = self._stream.read(self._CHUNK)
                if i >= 100:
                    data = audioop.mul(data, self._WIDTH, self._VOLUME_LEVEL)

                self._stream.write(data, self._CHUNK)
                frames.append(data)
            if time.time() - time_start >= self._MAX_RECORD_SECONDS:
                self._command_stop = 'stop'

        self.write_to_file(frames)
        return frames

    def stop_recording(self):
        self._command_stop = 'stop'

    def close_stream(self):
        self._stream.stop_stream()
        self._stream.close()
        self._pa.terminate()

    def write_to_file(self, frames):
        """
        Write audio data to file
        path

        :param frames: array audio data
        :return: string 'Success'
        """
        wf = wave.open(self._WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self._CHANNELS)
        wf.setsampwidth(self._pa.get_sample_size(self._FORMAT))
        wf.setframerate(self._RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        with contextlib.closing(wave.open(self._WAVE_OUTPUT_FILENAME, 'r')) as f:
            frames = f.getnframes()
            duration = round(frames / float(self._RATE))
            print('Записано: %s секунд' % duration)

    @staticmethod
    def audio_format(f):
        if f == 'paInt8':
            return pyaudio.paInt8
        elif f == 'paInt24':
            return pyaudio.paInt24
        elif f == 'paInt32':
            return pyaudio.paInt32
        else:
            return pyaudio.paInt16

# info = p.get_default_input_device_info()
# info = p.get_default_output_device_info()
# z = ''

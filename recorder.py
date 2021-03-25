import argparse
import json
import sys
import threading

from audio import Audio


def arg_parser():
    """
    Создание аргументов запуска скрипта
    Пример: 'python recorder.py -p '/mypath/record.wav'

    :return: parser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', default='record.wav')

    return parser


def record_audio(audio):
    """
    Record audio
    :param audio: instance Audio
    :return: None
    """
    print("* recording\n")
    audio.record()
    print("* stop recording")
    audio.stop_recording()


def stop_handler(a):
    """
    Stop recording audio from console

    :param a: instance Audio
    :return: None
    """
    command = input('Введите stop, чтобы остановить запись\n')
    if command == 'stop':
        a.stop_recording()


def main(path):
    settings = json.load(open('settings.json'))
    a = Audio(
        filename=path,
        input_device_index=settings['audio']['input_device_index'],
        output_device_index=settings['audio']['output_device_index'],
        rate=settings['audio']['rate'],
        audio_format=settings['audio']['audio_format'],
        min_seconds=settings['audio']['min_seconds'],
        max_seconds=settings['audio']['max_seconds'],
        volume=settings['audio']['volume']
    )

    record_thread = threading.Thread(target=record_audio, args=(a,), daemon=True)
    record_thread.start()
    threading.Thread(target=stop_handler, args=(a,), daemon=True).start()
    record_thread.join()
    a.close_stream()

    sys.exit(1)


if __name__ == '__main__':
    parser = arg_parser()
    namespace = parser.parse_args(sys.argv[1:])

    # if namespace.path.replace("'", ""):  # todo validate path
    #     pass

    ss = input("Чтобы запустить запись введите 'start'\n")

    if ss == 'start':
        try:
            main(namespace.path.replace("'", ""))
        except Exception as e:
            print(e)
    else:
        print('wrong command')

import argparse
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


def record_audio(event, audio):
    print("* recording\n")
    data = audio.record()
    print("* stop recording")
    # audio.write_to_file(data)
    audio.stop_recording()

    # while not event.wait(1):
    #     data += audio.record()
    #     print(event.wait(1))
    #     print('wait')
    # audio.stop_recording()
    # print("* stop recording")
    # audio.write_to_file(data)


def stop_handler(event, a):
    """
    Stop recording audio from console

    :param event: threading event
    :param a: instance Audio
    :return: None
    """
    command = input('Введите stop, чтобы остановить запись\n')
    if command == 'stop':
        a.stop_recording()
        # print("* stop recording")


def main(path):
    a = Audio(filename=path)

    thread_event = threading.Event()
    record_thread = threading.Thread(target=record_audio, args=(thread_event, a), daemon=True)
    record_thread.start()
    threading.Thread(target=stop_handler, args=(thread_event, a), daemon=True).start()
    record_thread.join()
    a.close_stream()

    sys.exit(1)


#
# def main(path):
#     a = Audio(path)
#
#     thread_event = threading.Event()
#     record_thread = threading.Thread(target=record_audio, args=(thread_event, a), daemon=True)
#     record_thread.start()
#
#     if input('Введите stop, чтобы остановить запись\n') == 'stop':
#         thread_event.set()
#         a.stop_recording()
#     record_thread.join()
#     a.close_stream()


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

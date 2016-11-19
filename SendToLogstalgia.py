import os
import argparse
import sys
import subprocess
from _operator import sub


class SendingToLogstalgia:
    def fill_dict(self):
        # logfile, fullscreen, window_size, background, fullscreen, simulation_speed,
        # pitch_speed, update_rate, group_name, paddle_mode, paddle_position, sync, from_time,
        # to_time, start_position, stop_position, no_bounce, hide_response_code, hide_paddle,
        # hide_paddle_tokens, hide_url_prefix, disable_auto_skip, disable_progress, disable_glow,
        # font_size, glow_duration, glow_multiplier, glow_intensity, output_ppm_stream, output_framerate,
        # load_config, save_config):
        self.namespace = self.parser.parse_args()  # sys.argv[1:])
        self.params = {
            'logfile': self.namespace.logfile,
            'fullscreen': self.namespace.f,
            'window-size': self.namespace.WxH,
            'background': self.namespace.b,
            'full-request': self.namespace.x,
            'simulation-speed': self.namespace.s,
            'pitch-speed': self.namespace.p,
            'update-rate': self.namespace.u,
            'group-name': self.namespace.g,
            'paddle-mode': self.namespace.paddle_mode,
            'paddle-position': self.namespace.paddle_position,
            'sync': self.namespace.sync,
            'from-time': self.namespace.from_time,
            'to-time': self.namespace.to_time,
            'start-position': self.namespace.start_position,
            'stop-position': self.namespace.stop_position,
            'no-bounce': self.namespace.no_bounce,
            'hide-response-code': self.namespace.hide_response_code,
            'hide-paddle': self.namespace.hide_paddle,
            'hide-paddle-tokens': self.namespace.hide_paddle_tokens,
            'hide-url-prefix': self.namespace.hide_url_prefix,
            'disable-auto-skip': self.namespace.disable_auto_skip,
            'disable-progress': self.namespace.disable_progress,
            'disable-glow': self.namespace.disable_progress,
            'font-size': self.namespace.font_size,
            'glow-duration': self.namespace.glow_duration,
            'glow-multiplier': self.namespace.glow_multiplier,
            'glow-intensity': self.namespace.glow_intensity,
            'output-ppm-stream': self.namespace.o,
            'output-framerate': self.namespace.r,
            'load-config': self.namespace.load_config,
            'save-config': self.namespace.save_config
        }

    def createParser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', action='store_true', help='fullscreen on')
        parser.add_argument('-WxH', help='window size')
        parser.add_argument('-b', help='background colour in HEX')
        parser.add_argument('-x', help='show full request ip/hostname')
        parser.add_argument('-s', help='simulation speed')
        parser.add_argument('-p', help='speed balls travel')
        parser.add_argument('-u', help='summary update speed', default=5)
        parser.add_argument('-g', help='creates a new named summarizer group')
        parser.add_argument('--paddle-mode', help='paddle mode(pid, vhost, pid)', default='single')
        parser.add_argument('--paddle-position', help='Paddle position as a fraction of the view width (0.25 - 0.75)')
        parser.add_argument('--sync')
        parser.add_argument('--from-time')
        parser.add_argument('--to-time')
        parser.add_argument('--start-position', help='begin at the some position in log file(between 0.0 and 1.0)')
        parser.add_argument('--stop-position', help='stop at some position')
        parser.add_argument('--no-bounce', help='no bouncing')
        parser.add_argument('--hide-response-code')
        parser.add_argument('--hide-paddle')
        parser.add_argument('--hide-paddle-tokens')
        parser.add_argument('--hide-url-prefix')
        parser.add_argument('--disable-auto-skip')
        parser.add_argument('--disable-progress')
        parser.add_argument('--disable-glow')
        parser.add_argument('--font-size', help='Font size (10-40)')
        parser.add_argument('--glow-duration')
        parser.add_argument('--glow-multiplier')
        parser.add_argument('--glow-intensity')
        parser.add_argument('-o', help='writes frames as PPM to a file')
        parser.add_argument('-r', help='framerate of output')
        parser.add_argument('--load-config', help='load a config file')
        parser.add_argument('--save-config', help='save a config file with the current options')
        parser.add_argument('--logfile', help='file with logs')
        self.parser = parser

    def start_logstalgia(self):
        options = []
        print(self.params)
        for key in self.params:
            if (self.params[key] != None):
                options.append('--' + str(key) + ' ' + str(self.params[key]) + ' ')

        command = ['Logstalgia/logstalgia.exe',]
        #process = subprocess.Popen(command + options, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        # subprocess.call(command + options)
        #stdout, stderr = process.communicate()

    def call_subprocess_fullscreen(self, filename):
        subprocess.call('Logstalgia/logstalgia -f ' + str(filename))
    def call_subprocess_glow_off(self, filename):
        subprocess.call('Logstalgia/logstalgia --disable-glow ' + str(filename))
    def call_subprocess_make_ppm_file(self, filename):
        subprocess.call('Logstalgia/logstalgia ' + str(filename) + ' -f -r 30 -1280x720 -o log.ppm', )
    def call_subprocess_convert_to_video(self, filename):
        subprocess.call('ffmpeg/bin/ffmpeg -y -r 30 -f image2pipe -vcodec ppm -i ' + str(filename) + ' -vcodec libx264 -pix_fmt yuv420p -crf 1 -threads 0 -bf 0 log_video.x264.avi')

if __name__ == '__main__':
    send = SendingToLogstalgia()
    send.createParser()
    send.fill_dict()
    send.start_logstalgia()
    # use fullscreen mode
    #send.call_subprocess_fullscreen('log.txt')
    # do not using glowing
    send.call_subprocess_glow_off('80.access.log')
    # uncomment and use this to make ppm file
    #send.call_subprocess_make_ppm_file('log.txt')
    # uncomment this for conversion ppm to videofile. Videoformats may be changed: mp4 or avi.
    # log.ppm is very big, near 5GiB, so use it after creating log.ppm
    #send.call_subprocess_convert_to_video('log.ppm')
  
#!/usr/bin/env python3
# encoding: utf-8
# The original author of this program, Danmaku2ASS, is StarBrilliant.
# This file is released under General Public License version 3.
# You should have received a copy of General Public License text alongside with
# this program. If not, you can obtain it at http://gnu.org/copyleft/gpl.html .
# This program comes with no warranty, the author will not be resopnsible for
# any damage or problems caused by this program.

# You can obtain a latest copy of Danmaku2ASS at:
#   https://github.com/m13253/danmaku2ass
# Please update to the latest version before complaining.

def ASSEscape(s):
    def ReplaceLeadingSpace(s):
        sstrip = s.strip(' ')
        slen = len(s)
        if slen == len(sstrip):
            return s
        else:
            llen = slen-len(s.lstrip(' '))
            rlen = slen-len(s.rstrip(' '))
            return ''.join(('\u2007'*llen, sstrip, '\u2007'*rlen))
    return '\\N'.join((ReplaceLeadingSpace(i) or ' ' for i in str(s).replace('\\', '\\\\').replace('{', '\\{').replace('}', '\\}').split('\n')))

def ConvertTimestamp(timestamp):
    timestamp = round(timestamp*100.0)
    hour, minute = divmod(timestamp, 360000)
    minute, second = divmod(minute, 6000)
    second, centsecond = divmod(second, 100)
    return '%d:%02d:%02d.%02d' % (int(hour), int(minute), int(second), int(centsecond))

def WriteASSHead(f, width, height, fontface, fontsize, alpha, styleid):
    f.write(
'''[Script Info]
; Script generated by Danmaku2ASS
; https://github.com/m13253/danmaku2ass
Script Updated By: Danmaku2ASS (https://github.com/m13253/danmaku2ass)
ScriptType: v4.00+
PlayResX: %(width)d
PlayResY: %(height)d
Aspect Ratio: %(width)d:%(height)d
Collisions: Normal
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: %(styleid)s, %(fontface)s, %(fontsize).0f, &H%(alpha)02XFFFFFF, &H%(alpha)02XFFFFFF, &H%(alpha)02X000000, &H%(alpha)02X000000, 0, 0, 0, 0, 100, 100, 0.00, 0.00, 1, %(outline).0f, 0, 7, 0, 0, 0, 0

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
''' % {'width': width, 'height': height, 'fontface': fontface, 'fontsize': fontsize, 'alpha': 255-round(alpha*255), 'outline': max(fontsize/25.0, 1), 'styleid': styleid}
    )


def WriteComment(f, text, start_t, row, width, duration_marquee, styleid):
    text = ASSEscape(text)
    styles = []
    styles.append('\\move(%(width)d, %(row)d, %(neglen)d, %(row)d)' % {'width': width, 'row': row, 'neglen': -len(text) * 15})
    duration = duration_marquee
    f.write('Dialogue: 2,%(start)s,%(end)s,%(styleid)s,,0000,0000,0000,,{%(styles)s}%(text)s\n' % {'start': ConvertTimestamp(start_t), 'end': ConvertTimestamp(start_t+duration), 'styles': ''.join(styles), 'text': text, 'styleid': styleid})


def main():
    width = 1280
    height = 720
    fontface = "SimHei"
    fontsize = 24
    alpha = 0.7
    styleid = "test"
    f = open("test.ass", "w")
    WriteASSHead(f, width=width,height=height,fontface=fontface,fontsize=fontsize,alpha=alpha,styleid=styleid)
    s = "我是测试弹幕"
    for i in range(10):
        WriteComment(f, s, i, i * 10, width, 10, styleid)
    f.close()

if __name__ == "__main__":
    main()

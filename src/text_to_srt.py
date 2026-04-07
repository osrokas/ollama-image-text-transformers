# importing integrated modules
import os
import re
from datetime import timedelta

# initializing subtitle length in seconds
WORDSPERSEC = 3

def text_to_srt(text: str, dursec: int = 3) -> str:
    # Split the text into lines for each 5 seconds of speech
    words = text.split()
    dursec = max(dursec, 1)  # Ensure duration is at least 1 second
    words_per_subtitle = WORDSPERSEC * dursec
    subtitles = [' '.join(words[i:i + words_per_subtitle]) for i in range(0, len(words), words_per_subtitle)]
    text = '\n\n'.join(subtitles)

    # splitting paragraphs into list items with regex
    par = re.split('\n{2,}', text)

    # pulling number of paragraphs in a text doc
    npar = len(par)

    # initializing starting subtitle and subtitile duration
    tdstart = timedelta(hours=0, seconds=-dursec)
    tddur = timedelta(seconds=dursec)

    # creating a list of timedeltas
    tdlist = []
    for i in range(npar+1):
        tdstart = tdstart + tddur
        tdlist.append(tdstart)

    # combining created list into a string in accordance with .srt formatting
    lcomb = []
    for i in range(npar):
        lcomb.append(str(i+1) + '\n' + str(tdlist[i]) + ',000 --> ' + str(
            tdlist[i+1]) + ',000' + '\n' + par[i] + '\n')

    # converting the list into a string with the delimiter '\n'
    srtstring = '\n'.join(lcomb)

    # adding '0' to single digit hours
    pat = r'^(\d:)'
    repl = '0\\1'
    srtstring2 = re.sub(pat, repl, srtstring, 0, re.MULTILINE)

    return srtstring2


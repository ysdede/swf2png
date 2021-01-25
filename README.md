# swf2png
Flash swf file to png renderer using ffmpeg python &amp; native flash player

How to install:

- Download flash player binary from macromedia site and copy it to util folder. Flash player download URL given in util folder. Flash Player title name hardcoded in source code. If you use another version of flash player please replace _flashplayertitle_ variable value with your window title name.
- Make sure ffmpeg is installed and ffmpeg/bin folder added to your system (or user) path. See [issue153@ffmpeg-python](https://github.com/kkroening/ffmpeg-python/issues/153#issuecomment-448472878 "issue153@ffmpeg-python")
- Install python requirements.
- Run main.py. It will check swf directory for swf files and copy the results to png folder.

[![](https://j.gifs.com/q7KvDR.gif)]

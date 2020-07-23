ffm
ffmpeg -i isaac.mp4 -vf "eq=contrast=10:gamma=1.0:saturation=2,edgedetect=mode=colormix,fps=10,scale=18:-1:flags=lanczos,crop=10:15:4:7,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -r 15   isaac.gif

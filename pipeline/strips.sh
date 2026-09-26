#!/bin/bash
# strips.sh — tira fina (N quadros/s) de cada janela candidata, com o tempo de origem gravado
cd /root/reels; mkdir -p strips
TM="zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:desat=0,zscale=t=bt709:m=bt709:r=pc,format=gbrp16le"
one() { s=$1 a=$2 b=$3 f=$4; n=$(python3 -c "print(max(1,round(($b-$a)*$f)))"); cols=8; rows=$(( (n+cols-1)/cols ))
  ffmpeg -v error -y -ss $a -t $(python3 -c "print($b-$a)") -i src/$s.MOV -an -vf "fps=$f,scale=180:320:flags=area,$TM,scale=out_color_matrix=bt709,format=yuv420p,drawtext=fontfile=/usr/share/fonts/opentype/inter/Inter-Bold.otf:text='%{pts\:flt\:$a}':x=4:y=4:fontsize=18:fontcolor=yellow:box=1:boxcolor=black,tile=${cols}x${rows}" -frames:v 1 -q:v 3 strips/${s}_${a}-${b}.jpg; }
export -f one; export TM
cat <<LIST | xargs -P 2 -L 1 bash -c 'one $0 $1 $2 $3'
IMG_8443 1 7 4
IMG_8443 26 30 4
IMG_8443 33 37 4
IMG_8441 0 8 3
IMG_8441 16 21 4
IMG_8444 24 32 3
IMG_8469 0 2.6 8
IMG_8451 0 3.3 6
IMG_8453 33 40 2
IMG_8460 0 8 2
IMG_8460 12 20 2
IMG_8470 8 20 2
IMG_8472 8 16 2
IMG_8472 32 38 2
IMG_8446 0 8 2
IMG_8445 2 12 2
IMG_8468 0 6 2
IMG_8459 0 6 4
IMG_8447 0 3.4 4
LIST
ls strips | wc -l

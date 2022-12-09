#!/usr/bin/env bash

head_x=0
head_y=0
tail_x=0
tail_y=0

while read direction distance; do
  for i in $(seq $distance); do
    case $direction in
      U) (( head_y += 1 )) ;;
      D) (( head_y -= 1 )) ;;
      R) (( head_x += 1 )) ;;
      L) (( head_x -= 1 )) ;;
    esac
    
    ver_gap=$(( head_y - tail_y ))
    hor_gap=$(( head_x - tail_x ))
  
    if [[ $ver_gap == *2 ]]; then
      tail_x=$head_x
      tail_y=$(( tail_y + (ver_gap / 2) ))
    elif [[ $hor_gap == *2 ]]; then
      tail_y=$head_y
      tail_x=$(( tail_x + (hor_gap / 2) ))
    fi

    echo $head_x $head_y $tail_x $tail_y $ver_gap $hor_gap
  done
  echo "---"
done # | sort | uniq | wc -l
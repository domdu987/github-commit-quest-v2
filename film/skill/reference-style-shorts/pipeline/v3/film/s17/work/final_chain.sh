F=__PROJ__/v3/film
for t in s17 s18 s25; do
  cd $F/$t && python3 shot.py render > work/render.log 2>&1 && python3 shot.py post > work/post.log 2>&1 && python3 shot.py contact >> work/post.log 2>&1 && python3 shot.py qa > work/qa.log 2>&1
  echo "$t done $(date)" >> $F/s17/work/final_chain.status
done

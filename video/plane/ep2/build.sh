W=../plane1   # in the repo the world parts live in video/plane/lib (copy them into the plane1 workspace)
cat helpers.part kit.part kit2.part hands.part kit3.part cut.part rich.part sinkui.part $W/plane.part $W/planecast.part $W/planeui.part body.part > shots.part && cat head.part sigcard.part shots.part foot.part > ep.tmpl.html && python3 make.py

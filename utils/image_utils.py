import cv2

def draw_boxes_and_save(frame, dets, out_path):
    img = frame.copy()
    for cls, conf, (x1,y1,x2,y2) in dets:
        cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
        cv2.putText(img, f'{cls} {conf:.2f}', (x1,y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
    cv2.imwrite(out_path, img)

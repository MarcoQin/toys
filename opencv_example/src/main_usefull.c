#include <cv.h>
#include <highgui.h>
#include <stdio.h>
#include <sys/time.h>
#include "osc.h"

int movement_detect(int current_frame_pixels, int nb_pixels, int threshold) {
    int percent = current_frame_pixels * 100 / nb_pixels;
    int moved = 0;
    if (percent >= threshold) {
        moved = 1;
        fprintf(stderr, "something moved!!\n");
    }
    return moved;
}

struct timeval tv;
long int last_t = 0;
long int now = 0;
double total = 500; //ms
double used = 0;  // ms
int r_max = 200;
int left = 0;
double datetime_diff_ms;

long int last_send_t = 0;

int draw_circle(CvMat* new, int radius, CvPoint point, int restart) {
    if (restart) {
        last_t = 0;
        used = 0;
    }
    /* fprintf(stderr, "input restart: %d\n", restart); */
    /* fprintf(stderr, "input radius: %d\n", radius); */
    gettimeofday(&tv,NULL);
    now = tv.tv_usec + tv.tv_sec * 1000000L;
    if (last_t != 0) {
        datetime_diff_ms = (now - last_t) / 1000.;
        /* fprintf(stderr, "timediff: %f\n", datetime_diff_ms); */
        used += datetime_diff_ms;
        if (used >= total) {
            radius = r_max;
        } else {
            left = r_max - radius;
            radius = radius + (datetime_diff_ms / (total - used)) * left;
        }
    }
    last_t = now;
    /* fprintf(stderr, "final radius: %d\n", radius); */
    cvCircle(new, point, radius, CV_RGB(102, 204, 255), -1, 8, 0);
    if ((now - last_send_t) / 1000 > 2000) {
        int c[] = {1, 1, 1, 0};
        send_msg(4, c);
        last_send_t = now;
    }
    return radius;
}

int main(int argc, char *argv[])
{
    init_connection("127.0.0.1", "7770");
    CvCapture* cap = cvCaptureFromCAM(0);
    IplImage* frame = cvQueryFrame(cap);
    /* cvNamedWindow("Res", CV_WINDOW_NORMAL); */
    /* cvSetWindowProperty("Res", CV_WND_PROP_FULLSCREEN, CV_WINDOW_FULLSCREEN); */
    int height = frame->height;
    int width = frame->width;
    int height_new = height;
    int width_new = width;
#ifdef __PI
    height_new = 720;
    width_new = 1280;
#endif
    CvMat* frame1gray = cvCreateMat(frame->height, frame->width, CV_8U);
    CvMat* frame2gray = cvCreateMat(frame->height, frame->width, CV_8U);
    CvMat* res = cvCreateMat(frame->height, frame->width, CV_8U); // 单通道灰度图
    CvMat* new = cvCreateMat(height, width, CV_8UC3);  // 3通道RGB

    IplImage* rgba = cvCreateImage(cvSize(width, height), 8, 4);
    IplImage* img_a = cvCreateImage(cvSize(width, height), 8, 4);
    cvSet(img_a, cvScalar(255, 255, 255, 224), NULL);  // 设置灰色alpha通道图层
    IplImage* resized_mac = cvCreateImage(cvSize(width * 1.6, height * 1.6), 8, 4);
#ifdef __PI
    CvMat* resized = cvCreateMat(height_new, width_new, CV_8UC3);
    cvNamedWindow("Res", CV_WINDOW_NORMAL);
    cvSetWindowProperty("Res", CV_WND_PROP_FULLSCREEN, CV_WINDOW_FULLSCREEN);
#endif
    int x = 0;
    int y = 0;
    int x1 = 0;
    int y1 = 0;
    int n_points = 0;
    int R = 10;
#ifdef __PI
    R = 4;
#endif
    int percent = 0;
    int step = 2 * R;
    unsigned char tmp = 0;
    CvScalar white = CV_RGB(255, 255, 255);
    CvScalar ty_blue = CV_RGB(102,204,255);
    int nb_pixels = height * width;
    int threshold = 10;
    int current_frame_pixels;

#ifdef __Debug
    CvScalar colors[] = {
        CV_RGB(255, 136, 0),
        CV_RGB(255, 102, 0),
        CV_RGB(255, 85, 0),
        ty_blue,
        CV_RGB(102, 107, 255),
        CV_RGB(182, 102, 255),
        CV_RGB(154, 37, 175),
        CV_RGB(154, 37, 175),
        CV_RGB(154, 37, 158),
        CV_RGB(154, 37, 158),
        CV_RGB(154, 37, 101),
        CV_RGB(175, 14, 66)
    };
#else
    CvScalar colors[] = {
        CV_RGB(255, 233, 0),
        CV_RGB(255, 203, 0),
        CV_RGB(255, 179, 0),
        CV_RGB(255, 136, 0),
        CV_RGB(255, 102, 0),
        CV_RGB(255, 85, 0),
        CV_RGB(255, 68, 0),
        CV_RGB(255, 51, 0),
        CV_RGB(255, 34, 0),
        CV_RGB(255, 17, 0),
        CV_RGB(255, 0, 0),
    };
#endif

    int radius = 10;
    int drawing = 0;
    /* CvPoint point = {0, 0}; */
    CvPoint point = {width / 2, height / 2};
    CvScalar rgb;
    rgb.val[0] = 0;
    rgb.val[1] = 0;
    rgb.val[2] = 0;
    for (;;) {
        frame = cvQueryFrame(cap);
        cvCvtColor(frame, frame2gray, CV_RGB2GRAY);
        cvAbsDiff(frame1gray, frame2gray, res);
        cvSmooth(res, res, CV_BLUR, 5, 5, 0, 0);
        cvThreshold(res, res, 10, 255, CV_THRESH_BINARY_INV);
        cvSet(new, white, NULL);
        current_frame_pixels = 0;


#ifdef __DEBUG
        for( x = R; x < height - R; x += step) {
            for (y = R; y < width - R; y += step) {
                n_points = 0;
                for (x1 = x - R; x1 < x+R; x1++) {
                    for (y1 = y - R; y1 < y + R; y1++) {
                        tmp = CV_MAT_ELEM(*res, unsigned char, x1, y1);
                        if (tmp == 0){
                            n_points ++;
                        }
                    }
                }
                current_frame_pixels += n_points;

                percent = ((n_points * 100) / (2 * R * 2 * R));
                if (percent >= 30) {
                    CvPoint Points[3] = {
#ifdef  __PI
                        {(y - 0.866f * R), (x - 0.5f * R)},
                        {(y + 0.866f * R), (x - 0.5f * R)},
                        {y, (x + R)}
#else //__PI
                        {(y - 0.866f * R), (x + 0.5f * R)},
                        {(y + 0.866f * R), (x + 0.5f * R)},
                        {y, (x - R)}
#endif // __PI
                    };

                    // draw circle
                    if ((x < (10 * R)) && (y <  (10 * R)) && !drawing) {
                        fprintf(stderr, "%d: %d\n", x, y);
                        if (radius > 200){
                            radius = 10;
                        }
                        radius = draw_circle(new, radius, point, 1);
                        drawing = 1;
                    } else if (drawing && radius < 200) {
                        radius = draw_circle(new, radius, point, 0);
                    } else {
                        radius = 10;
                        drawing = 0;
                    }

                    cvFillConvexPoly(new, Points, 3, colors[percent % 10], 8, 0);
                }

            }
        }
        movement_detect(current_frame_pixels, nb_pixels, threshold);
#endif // __DEBUG

#ifndef __DEBUG
        cvAddWeighted(img_a, 0.2f, rgba, 0.8f, 0, rgba);
        for( x = 0; x < height; x++) {
            for (y = 0; y < width; y++) {
                tmp = CV_MAT_ELEM(*res, unsigned char, x, y);
                if (tmp == 0){
                    // width - y - 1 is like cvFlip(rgba, rgba, 1)
                    cvSet2D(rgba, x, width - y - 1, rgb);
                }
            }
        }
#endif /* ifndef __DEBUG  */

#ifdef __PI
    cvResize(new, resized, CV_INTER_LINEAR);
    cvFlip(resized, resized, 0);
    cvShowImage("Res", resized);
#else
    cvResize(rgba, resized_mac, CV_INTER_LINEAR);
    cvShowImage("Res", resized_mac);
    /* cvShowImage("Res", rgba); */
    cvNamedWindow("Res", CV_WINDOW_NORMAL);
    cvSetWindowProperty("Res", CV_WND_PROP_FULLSCREEN, CV_WINDOW_FULLSCREEN);
#endif
        cvCopy(frame2gray, frame1gray, NULL);
        if(cvWaitKey(30) >= 0) break;
    }
    cvReleaseCapture(&cap);
    cvDestroyAllWindows();
    return 0;
}

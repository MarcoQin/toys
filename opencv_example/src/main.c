#include <cv.h>
#include <highgui.h>
#include <stdio.h>
#include <sys/time.h>
#include "osc.h"

int note[][16] = {
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
};

long int send_last_t[] = {
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0
};

#ifndef FULL_SCREEN
int thresholds[] = {
    30, 30, 30, 30,
    30, 30, 30, 30,
    30, 30, 30, 30,
    30, 30, 30, 30
};
#else
int thresholds[] = {
    10, 10, 10, 10,
    10, 10, 10, 10,
    10, 10, 10, 10,
    10, 10, 10, 10
};
#endif /* ifndef FULL_SCREEN */


CvFont font;
char buffer[3];

long int now = 0;
struct timeval tv;
double interval = 500; // ms
double datetime_diff_ms  = 0;

int movement_detect(int current_area_pixels, int nb_pixels, int area) {
    int threshold = thresholds[area];
    int percent = current_area_pixels * 100 / nb_pixels;
    int moved = 0;
    if (percent >= threshold) {
        moved = 1;
        /* fprintf(stderr, "something moved!!\n"); */
    }
    /* fprintf(stderr, "%d\n", moved); */
    return moved;
}

void do_send(int area) {
    send_msg(16, note[area]);
}

void send_osc_msg(int area) {
    if (area < 0 || area > 15) {
        return;
    }
    gettimeofday(&tv,NULL);
    now = tv.tv_usec + tv.tv_sec * 1000000L;
    datetime_diff_ms = (now - send_last_t[area]) / 1000.0f;
    if (datetime_diff_ms >= interval) {
        if (datetime_diff_ms < 10000) {
            // First Time the screen is all black
            do_send(area);
        }
        send_last_t[area] = now;
    }
}

int main(int argc, char *argv[])
{
    /* init_connection("127.0.0.1", "7770"); */
    init_connection("192.168.128.113", "8000");
    cvInitFont(&font, CV_FONT_HERSHEY_SIMPLEX, 2, 2, 0, 10, 8);
    CvCapture* cap = cvCaptureFromCAM(0);
    IplImage* frame = cvQueryFrame(cap);

    int height = frame->height;
    int width = frame->width;

    CvMat* frame1gray = cvCreateMat(frame->height, frame->width, CV_8U);
    CvMat* frame2gray = cvCreateMat(frame->height, frame->width, CV_8U);
    CvMat* res = cvCreateMat(frame->height, frame->width, CV_8U); // 单通道灰度图

    IplImage* rgba = cvCreateImage(cvSize(width, height), 8, 4);  // 4通道RGBA图层
    IplImage* img_a = cvCreateImage(cvSize(width, height), 8, 4);
    cvSet(img_a, cvScalar(255, 255, 255, 224), NULL);  // 设置灰色alpha通道图层
#ifdef FULL_SCREEN
    IplImage* resized_mac = cvCreateImage(cvSize(width * 1.6, height * 1.6), 8, 4);
#endif /* ifndef FULL_SCREEN */
    int x = 0;
    int x1 = 0;
    int y = 0;
    int y1 = 0;
    int Rx = (height / 4);
    int Ry = (width / 4);
    int nb_pixels = Rx * Ry;
    unsigned char tmp = 0;

    CvScalar white = CV_RGB(255, 255, 255);
    CvScalar ty_blue = CV_RGB(102,204,255);
    int current_area_pixels;

    CvScalar rgb = cvScalar(0, 0, 0, 0);

    int area = 0;

    for (;;) {
        frame = cvQueryFrame(cap);
        cvCvtColor(frame, frame2gray, CV_RGB2GRAY);
        cvAbsDiff(frame1gray, frame2gray, res);
        cvSmooth(res, res, CV_BLUR, 5, 5, 0, 0);
        cvThreshold(res, res, 10, 255, CV_THRESH_BINARY_INV);


        cvAddWeighted(img_a, 0.1f, rgba, 0.9f, 0, rgba);

#ifdef __NO_OSC
        for( x = 0; x < height; x++) {
            for (y = 0; y < width; y++) {
                tmp = CV_MAT_ELEM(*res, unsigned char, x, y);
                if (tmp == 0){
                    // width - y - 1 is like cvFlip(rgba, rgba, 1)
                    cvSet2D(rgba, x, width - y - 1, rgb);
                }
            }
        }
#else
        area = 0;
        for( x = Rx; x <= height; x+=Rx) {
            for ( y = Ry; y <= width; y+=Ry) {
                current_area_pixels = 0;

                for (x1 = x-Rx; x1 < x; x1++) {
                    for (y1 = y-Ry; y1 < y; y1++) {
                        tmp = CV_MAT_ELEM(*res, unsigned char, x1, y1);
                        if (tmp == 0) {
                            cvSet2D(rgba, x1, width - y1 - 1, rgb);
                            current_area_pixels++;
                        }
                    }
                }

                if (movement_detect(current_area_pixels, nb_pixels, area) == 1) {
                    send_osc_msg(area);
                    sprintf(buffer, "%d", area + 1);
                    cvPutText(rgba, buffer, cvPoint(width - (y - Ry / 2), x - Rx / 2), &font, ty_blue);
                }

                area++;

            }
        }
#endif  // ifdef __NO_OSC

#ifdef FULL_SCREEN
        cvResize(rgba, resized_mac, CV_INTER_LINEAR);
        cvShowImage("Res", resized_mac);
        cvNamedWindow("Res", CV_WINDOW_NORMAL);
        cvSetWindowProperty("Res", CV_WND_PROP_FULLSCREEN, CV_WINDOW_FULLSCREEN);
#else
        cvShowImage("Res", rgba);
#endif // FULL_SCREEN


        cvCopy(frame2gray, frame1gray, NULL);
        if(cvWaitKey(30) >= 0) break;

    }

    cvReleaseCapture(&cap);
    cvDestroyAllWindows();
    return 0;
}

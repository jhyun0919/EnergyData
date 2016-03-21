#include <iostream>
#include <armadillo>
#include <cmath>
#include <cassert>
#include <vector>
#include <sstream>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include "RBM.h"
#include "AutoEncoder.h"

using namespace std;
using namespace arma;

mat RunPCA(const mat &data);
mat LoadData(const char *filename);
void DisplayWeights(const mat &weights);
void DisplayReconstruction(const mat &data, const mat &reconstruction);
void SaveImages(const mat &original, const mat &from_autoencoder, const mat &from_PCA); // images for website

// Dataset
const char DATASET_FILE[] = "/home/nghia/Downloads/cifar-10-batches-bin/data_batch_1.bin";
const int SELECTED_CLASS = 5; // "dog" label
const unsigned int MAX_SAMPLES = 100; // limit the number of samples to train

int main()
{
    // RBM
    // These two variables must be the same length
    const int rbm_layers[] = {256, 64, 8}; // the hidden layers, not including the first input layer
    const RBM::UnitType rbm_layers_hidden_type[] = {RBM::SIGMOID, RBM::SIGMOID, RBM::LINEAR};
    const RBM::UnitType first_layer_visible_type = RBM::LINEAR; // Use LINEAR for real value data, else SIGMOID for binary
    assert(sizeof(rbm_layers) == sizeof(rbm_layers_hidden_type));

    // RBM - trainig parameters
    const int num_rbms = sizeof(rbm_layers) / sizeof(int);
    const int mini_batches = 100;
    const int iterations = 1000;
    const double momentum_rate = 0.9;
    const double weight_decay = 0.0; // not tested
    const bool early_stopping = true;

    vector <RBM> rbms(num_rbms);

    cv::namedWindow("main");

    mat data = LoadData(DATASET_FILE);
    cout << "Total training data: " << data.n_cols << endl;

    double u, s;
    mat data_norm = RBM::Normalise(data, &u, &s);
    mat data_train = data_norm;

    // Stack train the RBM
    {
        rbms[0].Train(data_train, first_layer_visible_type, rbm_layers_hidden_type[0], rbm_layers[0], mini_batches, iterations, 0.01, momentum_rate, weight_decay, early_stopping);
        data_train = rbms[0].FeedForward(data_train);

        // middle layer is all sigmoid
        for(int i=1; i < num_rbms; i++) {
            double learning_rate;

            if(rbm_layers_hidden_type[i-1] == RBM::LINEAR || rbm_layers_hidden_type[i] == RBM::LINEAR) {
                learning_rate = 0.01;
            }
            else {
                learning_rate = 0.1;
            }

            rbms[i].Train(data_train, rbm_layers_hidden_type[i-1], rbm_layers_hidden_type[i], rbm_layers[i], mini_batches, iterations, learning_rate, momentum_rate, weight_decay, early_stopping);

            data_train = rbms[i].FeedForward(data_train);
        }
    }

    AutoEncoder autoencoder;

    autoencoder.SetRBMHalf(rbms); // this will mirror the RBMS
    autoencoder.BackPropagation(data_norm, 100, 0.01, momentum_rate, early_stopping);
   // autoencoder.Save("autoencoder.bin");

    // Visualise the weights
    //DisplayWeights(autoencoder.m_rbms[0].m_weights);

    // Encoding/compression
/*
    mat compressed = autoencoder.Encode(data_norm);
    ofstream output("output.txt");

    if(!output) {
        cerr << "Error writing" << endl;
        return 1;
    }

    cout << "compressed: " << AutoEncoder::PrintSize(compressed) << endl;
    for(unsigned int i=0; i < compressed.n_cols; i++) {
        output << compressed(0,i) << " " << compressed(1,i) << endl;
    }
*/

    // Reconstruction error
    mat reconstruction = autoencoder.FeedForward(data_norm);
    reconstruction = reconstruction*s + u;

    mat err = data - reconstruction;
    err = err % err; // err .* err
    double rmse = sqrt(accu(err) / err.n_elem);
    cout << "Reconstruction error: " << rmse << endl;

    DisplayReconstruction(data, reconstruction);
    mat PCA_reconstruction = RunPCA(data);
    SaveImages(data, reconstruction, PCA_reconstruction);

    return 0;
}

mat LoadData(const char *filename)
{
    mat data;
    char label;
    vector <unsigned char> buffer(32*32*3); // temp buffer for RGB patch

    // Load the data as column vectors
    ifstream input(filename);

    if(!input) {
        cerr << "Error opening dataset: " << filename << endl;
        exit(1);
    }

    while(input.read((char*)&label, sizeof(label))) {
        input.read((char*)&buffer[0], buffer.size());

        if(label == SELECTED_CLASS && data.n_cols < MAX_SAMPLES) {
            cv::Mat img(32, 32, CV_8UC3);

            for(int y=0; y < 32; y++) {
                for(int x=0; x < 32; x++) {
                    img.at<cv::Vec3b>(y,x)[0] = buffer[y*32+x];
                    img.at<cv::Vec3b>(y,x)[1] = buffer[32*32 + y*32+x];
                    img.at<cv::Vec3b>(y,x)[2] = buffer[32*32*2 + y*32+x];
                }
            }

            cv::cvtColor(img, img, cv::COLOR_BGR2GRAY);

            vec col_data(32*32);

            for(int i=0; i < 32*32; i++) {
                col_data(i) = img.at<uchar>(i);
            }

            data = join_rows(data, col_data);
            /*
            cv::resize(img, img, cv::Size(320,320), 0, 0, cv::INTER_NEAREST);
            cv::imshow("main", img);
            cv::waitKey(0);
            */
        }
    }

    return data;
}

mat RunPCA(const mat &data)
{
    //const int PC[] = {2, 4, 8, 16, 32, 64, 128, 256, 512}; // number of principal components
    const int PC[] = {8};
    const int total_pc = sizeof(PC)/sizeof(int);

    mat u = mean(data, 1);
    mat data_norm = data - repmat(u, 1, data.n_cols);
    mat covar = data_norm*data_norm.t();
    mat reconstruction;
    mat U, V;
    vec S;

    svd(U, S, V, covar);

    for(int i=0; i < total_pc; i++) {
        mat VV = V.cols(0, PC[i]); // reduced basis
        reconstruction = VV*VV.t()*data_norm + repmat(u, 1, data.n_cols);

        mat err = reconstruction - data;
        err = err%err;
        double rmse = sqrt(accu(err) / err.n_elem);
        cout << PC[i] << " " << rmse << endl;
    }

    return reconstruction;
}

void DisplayWeights(const mat &weights)
{
    // Scale so that negative values range from [0, 128] and positive from [128, 255]

    int width = sqrt(weights.n_cols); // assume square image

    for(unsigned int j=0; j < weights.n_rows; j++) {
        double a = min(weights.row(j));
        double b = max(weights.row(j));
        double s = max(fabs(a), fabs(b));

        mat tmp = (weights.row(j) / s)*127 + 128;

        cv::Mat img(width, width, CV_8U);

        for(int k=0; k < width*width; k++) {
            int v = tmp(k);

            if(v < 0) v = 0;
            if(v >= 256) v = 255;

            img.at<uchar>(k) = v;
        }

        cv::resize(img, img, cv::Size(width*10, width*10), 0, 0, cv::INTER_NEAREST);
        cv::imshow("main", img);
        cv::waitKey(0);
    }
}

void DisplayReconstruction(const mat &data, const mat &reconstruction)
{
    // Display the resuts
    for(unsigned int i=0; i < reconstruction.n_cols; i++) {
        cv::Mat canvas = cv::Mat::zeros(32, 64+2, CV_8U);
        cv::Mat img1(32, 32, CV_8U);
        cv::Mat img2(32, 32, CV_8U);

        for(int j=0; j < 32*32; j++) {
            img1.at<uchar>(j) = data(j,i);
        }

        for(int j=0; j < 32*32; j++) {
            int v = reconstruction(j,i);

            if(v < 0) v = 0;
            if(v >= 256) v = 255;

            img2.at<uchar>(j) = v;
        }

        img1.copyTo(canvas(cv::Rect(0,0,32,32)));
        img2.copyTo(canvas(cv::Rect(33,0,32,32)));

        cv::resize(canvas, canvas, cv::Size(66*10,32*10), 0, 0, cv::INTER_NEAREST);
        cv::imshow("main", canvas);
        cv::waitKey(0);
    }
}

void SaveImages(const mat &original, const mat &from_autoencoder, const mat &from_PCA)
{
    const int image_size = 32;
    const int image_scale = 5;
    const int spacing = 4;

    for(int i=0; i < 10; i++) {
        cv::Mat canvas = cv::Mat::zeros(image_size + 4, (image_size+spacing)*3, CV_8U);

        cv::Mat img1(image_size, image_size, CV_8U);
        cv::Mat img2(image_size, image_size, CV_8U);
        cv::Mat img3(image_size, image_size, CV_8U);

        for(int j=0; j < image_size*image_size; j++) {
            img1.at<uchar>(j) = original(j,i);
        }

        for(int j=0; j < image_size*image_size; j++) {
            int v = from_autoencoder(j,i);

            if(v < 0) v = 0;
            if(v >= 256) v = 255;

            img2.at<uchar>(j) = v;
        }

        for(int j=0; j < image_size*image_size; j++) {
            int v = from_PCA(j,i);

            if(v < 0) v = 0;
            if(v >= 256) v = 255;

            img3.at<uchar>(j) = v;
        }

        img1.copyTo(canvas(cv::Rect(0, 0, image_size, image_size)));
        img2.copyTo(canvas(cv::Rect((image_size+spacing), 0, image_size, image_size)));
        img3.copyTo(canvas(cv::Rect((image_size+spacing)*2, 0, image_size, image_size)));

        cv::resize(canvas, canvas, cv::Size(canvas.size()*image_scale), 0, 0, cv::INTER_NEAREST);

        int xstep = (image_size+spacing)*image_scale;
        int font_y = canvas.rows - 4;

        cv::putText(canvas, "Original", cv::Point(0, font_y), cv::FONT_HERSHEY_PLAIN, 1.0, 255);
        cv::putText(canvas, "Autoencoder", cv::Point(xstep, font_y), cv::FONT_HERSHEY_PLAIN, 1.0, 255);
        cv::putText(canvas, "PCA", cv::Point(xstep*2, font_y), cv::FONT_HERSHEY_PLAIN, 1.0, 255);

        char file[128];
        sprintf(file, "results-%02d.png", i);
        cv::imwrite(file, canvas);
    }
}

mat Whiten(const mat &data)
{
    int N = data.n_cols;
    mat x = data.t();

    mat u = mean(x);
    mat c = cov(x);

    vec d;
    mat v;

    eig_sym(d, v, c);

    mat p = v * diagmat(sqrt(1/(d + 0.1))) * v.t();
    mat w = (x - repmat(u, N, 1)) * p;

    return w.t();
}

#ifndef __AUTOENCODER_H__
#define __AUTOENCODER_H__

#include "RBM.h"
#include <vector>
#include <string>

class AutoEncoder
{
public:
    void SetRBMHalf(const std::vector <RBM> &rbms);
    void BackPropagation(const arma::mat &data, double iterations, double learning_rate, double momentum_rate, bool early_stopping);
    void Save(const char *filename);
    void Load(const char *filename);

    arma::mat FeedForward(const arma::mat &data);
    arma::mat Encode(const arma::mat &data);
    arma::mat Decode(const arma::mat &data);

    static std::string PrintSize(const arma::mat &M);

public:
    std::vector <RBM> m_rbms;

private:
};

#endif

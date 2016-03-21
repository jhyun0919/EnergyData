#ifndef __RBM_H__
#define __RBM_H__

#include <armadillo>

// Remember to normalise your data before using this class, call RBM::Normalise()

class RBM
{
public:
    enum UnitType {SIGMOID, LINEAR};

    void Train(const arma::mat &data, UnitType visible_type, UnitType hidden_type, int num_hidden, int mini_batches = 100, int iterations = 100, double learning_rate = 0.01, double momentum_rate = 0.9, double weight_decay = 0.0, bool early_stopping = true);

    arma::mat FeedForward(const arma::mat &data);
    arma::mat FeedBackward(const arma::mat &data) const;

public:
    static arma::mat Sigmoid(const arma::mat &M);
    static arma::mat Normalise(const arma::mat &data, double *ret_mean, double *ret_stdev);

    UnitType m_visible_type;
    UnitType m_hidden_type;

    arma::mat m_input;
    arma::mat m_output;

    arma::mat dh_dz();
    arma::mat dz_dh();
    arma::mat dz_dw();

    // Accessible for convenience
    arma::mat m_weights;
    arma::mat m_visible_biases;
    arma::mat m_hidden_biases;

    // Keep copies of useful data for backprop when doing forward pass
    arma::mat m_forward_x; // input
    arma::mat m_forward_z; // z = weights*x
    arma::mat m_forward_h; // h = Sigmoid(z);

private:
    struct Gradients
    {
        arma::mat weights;
        arma::mat visible_biases;
        arma::mat hidden_biases;
    };

    static arma::mat SampleBinary(const arma::mat &input);
    static arma::mat AddGaussianNoise(const arma::mat &M); // matrix values are the mean

    // These two aren't used but here for reference
    double GoodnessSigmoid(const arma::mat &weights, const arma::vec &visible_biases, const arma::vec &hidden_biases, const arma::mat &visible_state, const arma::mat &hidden_state);
    double GoodnessLinear(const arma::mat &weights, const arma::vec &visible_biases, const arma::vec &hidden_biases, const arma::mat &visible_state, const arma::mat &hidden_state);

    arma::mat GradientWeights(const arma::mat &visible_state, const arma::mat &hidden_state);
    arma::vec GradientVisibleBiases(const arma::mat &visible_state, const arma::vec &visible_bias);
    arma::vec GradientHiddenBiases(const arma::mat &hidden_state, const arma::vec &hidden_bias);
    Gradients CD1(const arma::mat &visible_data, const arma::mat &weights, const arma::vec &visible_bias, const arma::vec &hidden_bias);

private:
    UnitType m_input_type;
    double m_weight_decay;
};

#endif

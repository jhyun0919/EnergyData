#include "RBM.h"
#include <cstdlib>
#include <float.h>

using namespace arma;

void RBM::Train(const arma::mat &data, UnitType visible_type, UnitType hidden_type, int num_hidden, int mini_batches, int iterations, double learning_rate, double momentum_rate, double weight_decay, bool early_stopping)
{
    const int max_epoch_without_improvement = 30; // if we don't see any improvement after this amount, then terminate

    m_visible_type = visible_type;
    m_hidden_type = hidden_type;
    m_weight_decay = weight_decay;

    int N = data.n_cols;
    int num_visible = data.n_rows;
    int total_batches = (int)ceil((float)N/mini_batches);

    m_weights.resize(num_hidden, num_visible);
    m_visible_biases.resize(num_visible);
    m_hidden_biases.resize(num_hidden);

    // Keep track of the best parameters
    mat best_weights = m_weights;
    mat best_visible_biases = m_visible_biases;
    mat best_hidden_biases = m_hidden_biases;
    double best_RMSE = DBL_MAX;
    int best_epoch = 0;
    int no_improvement_epoch_count = 0;

    m_weights.randn();
    m_weights *= 0.01;

    mat momentum_weights = zeros(num_hidden, num_visible);
    vec momentum_visible_biases = zeros(num_visible);
    vec momentum_hidden_biases = zeros(num_hidden);

    for(int i=0; i < iterations; i++) {
        int start = (i % total_batches)*mini_batches;
        int end = start + mini_batches;

        if(end >= N) {
            end = N - 1;
        }

        mat batch = data.cols(start, end);

        Gradients g = CD1(batch, m_weights, m_visible_biases, m_hidden_biases);

        momentum_weights = momentum_rate*momentum_weights + g.weights;
        momentum_visible_biases = momentum_rate*momentum_visible_biases + g.visible_biases;
        momentum_hidden_biases = momentum_rate*momentum_hidden_biases + g.hidden_biases;

        m_weights += momentum_weights*learning_rate;
        m_visible_biases += momentum_visible_biases*learning_rate;
        m_hidden_biases += momentum_hidden_biases*learning_rate;

        // Reconstruction error, no sampling done, using raw probability
        mat hidden_state = Sigmoid(m_weights*data + repmat(m_hidden_biases, 1, N));
        mat reconstruction = m_weights.t()*hidden_state + repmat(m_visible_biases, 1, N);

        if(m_visible_type == SIGMOID) {
            reconstruction = Sigmoid(reconstruction);
        }

        mat err = data - reconstruction;
        err = err % err;
        double RMSE = sqrt(accu(err)/err.n_elem);

        if(RMSE < best_RMSE) {
            best_RMSE = RMSE;
            best_weights = m_weights;
            best_visible_biases = m_visible_biases;
            best_hidden_biases = m_hidden_biases;
            best_epoch = i;
            no_improvement_epoch_count = 0;
        }
        else {
            no_improvement_epoch_count++;
        }

        if(early_stopping && no_improvement_epoch_count >= max_epoch_without_improvement) {
            cout << "No improvement noticed after " << max_epoch_without_improvement << " epochs, going to terminate early!" << endl;
            break;
        }

        if((i+1) % 10 == 0) {
            cout << "epoch: " << (i+1) << "/" << iterations << " - RMSE: " << RMSE << endl;
        }
    }

    cout << "Using best weights found at epoch: " << best_epoch << endl;

    m_weights = best_weights;
    m_visible_biases = best_visible_biases;
    m_hidden_biases = best_hidden_biases;
}

arma::mat RBM::FeedForward(const arma::mat &data)
{
    int N = data.n_cols;

    m_input = data;
    m_output = m_weights*m_input + repmat(m_hidden_biases, 1, N);

    if(m_hidden_type == SIGMOID) {
        m_output = Sigmoid(m_output);
    }

    return m_output;
}

arma::mat RBM::SampleBinary(const arma::mat &input)
{
    mat output = zeros(input.n_rows, input.n_cols);

    for(unsigned int i=0; i < input.n_rows; i++) {
        for(unsigned int j=0; j < input.n_cols; j++) {
            double r = (double)rand()/RAND_MAX;

            if(input(i,j) >= r) {
                output(i,j) = 1.0;
            }
            else {
                output(i,j) = 0.0;
            }
        }
    }

    return output;
}

arma::mat RBM::AddGaussianNoise(const arma::mat &M)
{
    mat ret = M + randn(M.n_rows, M.n_cols);

    return ret;
}

arma::mat RBM::Sigmoid(const arma::mat &M)
{
    mat ret(M.n_rows, M.n_cols);

    for(unsigned int i=0; i < M.n_rows; i++) {
        for(unsigned int j=0; j < M.n_cols; j++) {
            double x = M(i,j);
            ret(i,j) = 1.0/(1.0 + exp(-x));
        }
    }

    return ret;
}

arma::mat RBM::GradientWeights(const mat &visible_state, const mat &hidden_state)
{
    mat d_G_by_rbm_w = zeros(hidden_state.n_rows, visible_state.n_rows);
    int N = visible_state.n_cols;

    for(int i=0; i < N; i++) {
        d_G_by_rbm_w += hidden_state.col(i)*visible_state.col(i).t();
    }

    d_G_by_rbm_w /= N;

    // weight penalty
    d_G_by_rbm_w -= m_weight_decay*m_weights;

    return d_G_by_rbm_w;
}

arma::vec RBM::GradientVisibleBiases(const mat &visible_state, const vec &visible_bias)
{
    // For linear visible unit assume:
    // sigma = 1

    int N = visible_state.n_cols;

    vec d_G_by_vbias;

    if(m_visible_type == SIGMOID) {
        return mean(visible_state, 1);
    }
    else if(m_visible_type == LINEAR) {
        d_G_by_vbias = zeros(visible_bias.n_elem);

        for(int i=0; i < N; i++) {
            d_G_by_vbias += visible_state.col(i) - visible_bias; // deriv of -E, not E
        }
    }

    d_G_by_vbias /= N;

    return d_G_by_vbias;
}

arma::vec RBM::GradientHiddenBiases(const mat &hidden_state, const vec &hidden_bias)
{
    int N = hidden_state.n_cols;

    vec d_G_by_hbias;

    if(m_hidden_type == SIGMOID) {
        return mean(hidden_state, 1);
    }
    else if(m_hidden_type == LINEAR) {
        d_G_by_hbias = zeros(hidden_bias.n_elem);

        for(int i=0; i < N; i++) {
            d_G_by_hbias += hidden_state.col(i) - hidden_bias; // deriv of -E, not E
        }
    }

    d_G_by_hbias /= N;

    return d_G_by_hbias;
}

RBM::Gradients RBM::CD1(const mat &visible_data, const mat &weights, const vec &visible_biases, const vec &hidden_biases)
{
    // This versin of CD1 takes a few shortcuts from
    // "Using Very Deep Autoencoders for Content-Based Image Retrieval"

    mat visible_state, visible_probability;
    mat hidden_state, hidden_probability;
    mat gradient1, gradient2;
    vec visible_biases1, visible_biases2;
    vec hidden_biases1, hidden_biases2;

    Gradients ret;

    int N = visible_data.n_cols;

    // Positive phase
    visible_state = visible_data;

    // Can skip sampling
/*
    if(m_visible_type == SIGMOID) {
        visible_state = SampleBinary(visible_state);
    }
    else if(m_visible_type == LINEAR) {
        visible_state = AddGaussianNoise(visible_state);
    }
*/

    if(m_hidden_type == SIGMOID) {
        hidden_probability = Sigmoid(weights*visible_state + repmat(hidden_biases, 1, N));
        hidden_state = SampleBinary(hidden_probability); // sample here, according to esann-deep-final.pdf
    }
    else if(m_hidden_type == LINEAR) {
        hidden_state = AddGaussianNoise(weights*visible_state + repmat(hidden_biases, 1, N));
    }

    gradient1 = GradientWeights(visible_state, hidden_state);
    visible_biases1 = GradientVisibleBiases(visible_state, visible_biases);
    hidden_biases1 = GradientHiddenBiases(hidden_state, hidden_biases);

    // Negative phase
    // Skip sampling here as well
    visible_state = weights.t()*hidden_state + repmat(visible_biases, 1, N);

    if(m_visible_type == SIGMOID) {
        visible_state = Sigmoid(visible_state);
        //visible_probability = Sigmoid(visible_state);
        //visible_state = SampleBinary(visible_probability);
    }

    // skip sampling here
    if(m_hidden_type == SIGMOID) {
        hidden_probability = Sigmoid(weights*visible_state + repmat(hidden_biases, 1, N));
        hidden_state = hidden_probability;
    }
    else if(m_hidden_type == LINEAR) {
        hidden_state = weights*visible_state + repmat(hidden_biases, 1, N);
    }

    gradient2 = GradientWeights(visible_state, hidden_state);
    visible_biases2 = GradientVisibleBiases(visible_state, visible_biases);
    hidden_biases2 = GradientHiddenBiases(hidden_state, hidden_biases);

    // gradients
    ret.weights = gradient1 - gradient2;
    ret.visible_biases = visible_biases1 - visible_biases2;
    ret.hidden_biases= hidden_biases1 - hidden_biases2;

    return ret;
}

arma::mat RBM::Normalise(const arma::mat &data, double *ret_mean, double *ret_stdev)
{
    *ret_mean = accu(data) / data.n_elem;

    mat x = data - *ret_mean;
    mat x2 = x % x; // element-wise multiplication
    *ret_stdev = sqrt(accu(x2)/data.n_elem);

    return x/(*ret_stdev);
}

double RBM::GoodnessSigmoid(const arma::mat &weights, const arma::vec &visible_biases, const arma::vec &hidden_biases, const arma::mat &visible_state, const mat &hidden_state)
{
    // Goodness for sigmoid-sigmoid layers

    int N = visible_state.n_cols;
    double G = 0.0;
    mat tmp;

    for(int i=0; i < N; i++) {
        // visible bias term
        G += dot(visible_biases, visible_state.col(i));

        // hidden bias term
        G += dot(hidden_biases, hidden_state.col(i));

        // weight term
        tmp = hidden_state.col(i).t()*weights*visible_state.col(i);
        G += tmp(0,0);
    }

    G /= N;

    G -= m_weight_decay*0.5*accu(weights%weights);

    return G;
}

double RBM::GoodnessLinear(const arma::mat &weights, const arma::vec &visible_biases, const arma::vec &hidden_biases, const arma::mat &visible_state, const mat &hidden_state)
{
    // Goodness for linear-sigmoid layers

    int N = visible_state.n_cols;
    double G = 0.0;
    mat X, tmp;

    for(int i=0; i < N; i++) {
        // visible bias term
        X = visible_state.col(i) - visible_biases;
        G += -accu(X%X)*0.5; // negative term

        // hidden bias term
        G += dot(hidden_state.col(i), hidden_biases);

        // weight term
        tmp = hidden_state.col(i).t()*weights*visible_state.col(i);
        G += tmp(0,0);
    }

    G /= N;

    G -= m_weight_decay*0.5*accu(weights%weights);

    return G;
}

arma::mat RBM::dz_dh()
{
    return m_weights;
}

arma::mat RBM::dz_dw()
{
    return m_input;
}

arma::mat RBM::dh_dz()
{
    return (1.0 - m_output)%m_output;
}


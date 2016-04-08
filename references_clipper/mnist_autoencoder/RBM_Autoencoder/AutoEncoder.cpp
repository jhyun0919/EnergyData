#include "AutoEncoder.h"
#include <vector>
#include <float.h>
#include <cassert>

using namespace std;
using namespace arma;

void AutoEncoder::SetRBMHalf(const std::vector <RBM> &rbms)
{
    m_rbms.clear();

    // First half of the autoencoder
    for(size_t i=0; i < rbms.size(); i++) {
        m_rbms.push_back(rbms[i]);
    }

    // Mirror the second half of the autoencoder
    for(int i=rbms.size()-1; i >= 0; i--) {
        m_rbms.push_back(rbms[i]);

        // Flip
        m_rbms.back().m_weights = m_rbms.back().m_weights.t();
        std::swap(m_rbms.back().m_visible_biases, m_rbms.back().m_hidden_biases);
        std::swap(m_rbms.back().m_visible_type, m_rbms.back().m_hidden_type);
    }
}

arma::mat AutoEncoder::FeedForward(const arma::mat &data)
{
    mat ret = data;

    for(size_t i=0; i < m_rbms.size(); i++) {
        ret = m_rbms[i].FeedForward(ret);
    }

    return ret;
}

arma::mat AutoEncoder::Encode(const arma::mat &data)
{
    mat ret = data;

    // Use the first half of the autoencoder
    for(size_t i=0; i < m_rbms.size()/2; i++) {
        ret = m_rbms[i].FeedForward(ret);
    }

    return ret;
}

arma::mat AutoEncoder::Decode(const arma::mat &data)
{
    mat ret = data;

    // Use the second half of the autoencoder
    for(size_t i=m_rbms.size()/2; i < m_rbms.size(); i++) {
        ret = m_rbms[i].FeedForward(ret);
    }

    return ret;
}

string AutoEncoder::PrintSize(const mat &M)
{
    stringstream str;

    str << M.n_rows << "x" << M.n_cols;

    return str.str();
}

void AutoEncoder::BackPropagation(const arma::mat &data, double iterations, double learning_rate, double momentum_rate, bool early_stopping)
{
    const int max_epoch_without_improvement = 30; // if we don't see any improvement after this amount, then terminate

    // Assumes the first and last layer are linear units, and the rest being simgoid
    int N = data.n_cols;
    int no_improvement_epoch_count = 0;
    double best_err = DBL_MAX;
    int best_epoch = 0;

    vector <RBM> best_rbms;
    vector <mat> momentum(m_rbms.size());

    assert(N > 0);

    double final_learning_rate = learning_rate*0.1;

    double m = -(learning_rate - final_learning_rate)/iterations;
    double c = learning_rate;

    for(int i=0; i < iterations; i++) {
        // Feed forward, this will fill in values for backprop
        mat X = FeedForward(data);

        // Reconstruction error
        mat err = data - X;
        err = err % err;
        double rmse = sqrt(accu(err) / err.n_elem);

        if(rmse < best_err) {
            best_err = rmse;
            best_rbms = m_rbms;
            best_epoch = i;

            no_improvement_epoch_count = 0;
        }
        else {
            no_improvement_epoch_count++;
        }

        if(no_improvement_epoch_count >= max_epoch_without_improvement) {
            cout << "No improvement noticed after " << max_epoch_without_improvement << " epochs, going to terminate early!" << endl;
            break;
        }

        if((i+1) % 10 == 0) {
            cout << "Backpropagation epoch: " << (i+1) << "/" << iterations << " - RMSE: " << rmse << endl;
        }

        // Backprop part
        mat accum_deriv; // accumulated derivate
        mat grad;

        // Initialise the accumulated derivating using square error E = 0.5*(T-Y)^2
        accum_deriv = -(data - X); // dE/dz

        // backpropagate through the top to bottom
        for(int j=m_rbms.size()-1; j >=0; j--) {
            switch(m_rbms[j].m_hidden_type) {
                case RBM::SIGMOID:
                accum_deriv = accum_deriv % m_rbms[j].dh_dz(); // dh/dz
                break;

                case RBM::LINEAR:
                break;
            }

            grad = (accum_deriv * m_rbms[j].dz_dw().t())/N; // dz/dw

            if(!grad.is_finite() ) {
                cerr << "Weights have blown to infinite! Try reducing the learning rate." << endl;
                exit(1);
            }

            // no point accumulating gradients for the first layer
            if(j > 0) {
                accum_deriv = m_rbms[j].m_weights.t()* accum_deriv; // dz/.. = weights
            }

            if(momentum[j].is_empty()) {
                momentum[j] = grad;
            }
            else {
                momentum[j] = momentum_rate*momentum[j] + grad;
            }

            double lr = m*i + c;
            m_rbms[j].m_weights -= lr*momentum[j];
        }
    }

    cout << "Using best weights found at epoch: " << best_epoch << endl;

    m_rbms = best_rbms;
}

void AutoEncoder::Save(const char *filename)
{
    stringstream str;
    ofstream output(filename);

    if(!output) {
        cerr << "Error opening " << filename << endl;
        exit(1);
    }

    str << m_rbms.size() << endl;

    for(size_t i=0; i < m_rbms.size(); i++) {
        RBM &rbm = m_rbms[i];

        str << rbm.m_visible_type << endl;
        str << rbm.m_hidden_type << endl;
        rbm.m_weights.save(str);
        rbm.m_visible_biases.save(str);
        rbm.m_hidden_biases.save(str);
    }

    output << str.str();
}

void AutoEncoder::Load(const char *filename)
{
    ifstream input(filename);

    if(!input) {
        cerr << "Err opening " << filename << endl;
        exit(1);
    }

    size_t s;

    input >> s;
    m_rbms.resize(s);

    for(size_t i=0; i < m_rbms.size(); i++) {
        RBM &rbm = m_rbms[i];
        int v;
        char line[1024];

        input >> v;
        rbm.m_visible_type = (RBM::UnitType)v;

        input >> v;
        rbm.m_hidden_type = (RBM::UnitType)v;

        // Eat up new lines
        input.getline(line, sizeof(line));

        rbm.m_weights.load(input);
        rbm.m_visible_biases.load(input);
        rbm.m_hidden_biases.load(input);

        cout << PrintSize(rbm.m_weights) << endl;
    }

}

import numpy as np
import pandas as pd


def get_sig_params():
    pars = dict()
    pars["sample_rate"] = 44100  # Hertz
    pars["duration"] = 5   # seconds
    return pars


def GetDistributionParams(model,p):
    """
    Returns parameters for generating different data distributions
    """
    params = dict()
    params["model"] = model
    params["p"] = p
    if model == "gaussian":
        params["rho"] = 0.5
    elif model == "gmm":
        params["rho-list"] = [0.3,0.5,0.7]
    elif model == "mstudent":
        params["df"] = 3
        params["rho"] = 0.5
    elif model == "sparse":
        params["sparsity"] = int(0.3*p)
    else:
        raise Exception('Unknown model generating distribution: ' + model)
    
    return params
        

def GetTrainingHyperParams(model):
    """
    Returns the default hyperparameters for training deep knockoffs
    as described in the paper
    """
    params = dict()
    
    params['GAMMA'] = 1.0
    if model == "gaussian":
        params['LAMBDA'] = 1.0
        params['DELTA'] = 1.0
    elif model == "gmm":
        params['LAMBDA'] = 1.0
        params['DELTA'] = 1.0
    elif model == "mstudent":
        params['LAMBDA'] = 0.01
        params['DELTA'] = 0.01
    elif model == "sparse":
        params['LAMBDA'] = 0.1
        params['DELTA'] = 1.0
    else:
        raise Exception('Unknown data distribution: ' + model)
        
    return params


def GetFDRTestParams(model):
    """
    Returns the default hyperparameters for performing controlled
    variable selection experiments as described in the paper
    """
    params = dict()
    # Test parameters for each model
    if model in ["gaussian", "gmm"]:
        params["n"] = 150
        params["elasticnet_alpha"] = 0.1
    elif model in ["mstudent"]:
        params["n"] = 200
        params["elasticnet_alpha"] = 0.0
    elif model in ["sparse"]:
        params["n"] = 200
        params["elasticnet_alpha"] = 0.0
    
    return params


def get_syn_params():
    # Parameters for synthetic data
    params = {
        'epochs': 150,
        'pred_len': 28,
        'train_len': 555,
        'num_layers': 4,
        'num_cells': 44,
        'num_samples': 10,
        'dropout_rate': 0.1,
        'win_size': 1,
        'dim': 3,
        'batch_size': 32,
        'prior_graph': np.array([[1, 1, 1, 1, 1], [0, 1, 0, 0, 1], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]]),
        'true_graph': [1, 1, 1, 1, 1,  0, 1, 0, 0, 1,  0, 0, 1, 0, 0,  0, 0, 0, 1, 0,  0, 0, 0, 0, 1],
        'freq': '30min',
        'plot_path': f"/home/ahmad/PycharmProjects/deepCausality/plots/"
    }

    return params


def get_real_params():

    params = {
        'epochs': 150,
        'pred_len': 28,
        'train_len': 555,
        'num_layers': 3,
        'num_samples': 10,
        'num_cells': 33,
        'dropout_rate': 0.1,
        'win_size': 1,
        'dim': 3,
        'batch_size': 32,
        'prior_graph': np.array([[1, 1, 0], [0, 1, 0], [0, 0, 1]]),
        'true_graph': [1, 1, 0,   0, 1, 0,   0, 0, 1],
        'freq': 'D',
        'plot_path': f"/home/ahmad/PycharmProjects/deepCausality/plots/"
    }
    return params


def set_all_params(**kwargs):

    a = 2
    return None



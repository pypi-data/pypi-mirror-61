__author__ = 'Srikandan Raju, Sathish Anandha'
__copyright__ = 'Copyright (C) 2007 Free Software Foundation'
__license__ = 'GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007'
__version__ = '1.0.3'
__maintainer__ = 'Srikandan Raju, Sathish Anandha'

# main_regression is the Class
class MainRegression(object):
    
    # Importing required packages
    def import_required_packages():
        try:
            global pd
            global np
            global s_scale
            global grid_class
            global mk_pipeline
            
            import pandas as pd
            import numpy as np
            from sklearn.pipeline import make_pipeline as mk_pipeline
            
            from model_analyzer.gridsearch_cv import gridsearch_model as grid_class
            
            return 'imported'
        except Exception as  e:
            e = 'Kindly install or update Packages \n ' + str(e)
            return e
        
    # regression function identifies the Model Type
    def regression(prob_type, data, alg_type, score_type, tune_param, reg_class, 
                   set_plot):
        global prob
        global set_plotting
        global current_model
        
        prob = prob_type
        set_plotting = set_plot
        
        try:
            import_status = reg_class.import_required_packages()
            
            main_dataframe = pd.DataFrame(columns=['Model', 'Score_Type', 
                                                   'Predicted_Score',
                                                   'Best_Score',
                                                   'Best_Parameter',
                                                   'Plot_Status',
                                                   'Error'])
            result_data = []
            list_data = []
            list_data = data.copy()
            if import_status == 'imported':
                for model in  alg_type:
                    current_model = model
                    if model == 'linear':
                        output = reg_class.linear_regression(list_data, score_type, 
                                                                        tune_param, reg_class)
                    elif model == 'polynomial':
                        output = reg_class.polynomial_regression(list_data, score_type, 
                                                                        tune_param, reg_class)
                    elif model == 'ridge':
                        output = reg_class.ridge_regression(list_data, score_type, 
                                                                        tune_param, reg_class)
                    elif model == 'lasso':
                        output = reg_class.lasso_regression(list_data, score_type, 
                                                                        tune_param, reg_class)
                    elif model == 'elasticnet':
                        output = reg_class.elasticnet_regression(list_data, score_type, 
                                                                        tune_param, reg_class)
                    elif model == 'random_forest_regressor':
                        output = reg_class.randomforest_regression(list_data, score_type, 
                                                                        tune_param, reg_class)
                    elif model == 'xgb_regressor':
                        output = reg_class.xgbregressor_regression(list_data, score_type, 
                                                                        tune_param, reg_class)
                    else:
                        output = [{
                            'Model':model, 
                            'Score_Type':'',
                            'Predicted_Score':'',
                            'Best_Score':'',
                            'Best_Parameter':'',
                            'Plot_Status':'',
                            'Error': 'Not a Valid Model'
                            }]
                    
                    if isinstance(output, list):
                        for out_data in output:
                            result_data.append(out_data)
                main_dataframe = main_dataframe.append(result_data, ignore_index=True)
                    
                return main_dataframe
            else:
                return import_status
        except Exception as e:
            return e
            
        
    # Linear Regression Model
    def linear_regression(data, score_types, tune_param, reg_class):
        try:
            from sklearn.linear_model import LinearRegression
            lin_mod = LinearRegression()
            
            grid_tune_param = {
                              'fit_intercept'       : [True, False],
                              'normalize'           : [True, False],
                              'copy_X'              : [True, False],
                              'n_jobs'              : [ -1]
                            }
            if tune_param == 'default':
                tune_param = grid_tune_param
            else:
                tune_param = tune_param.get('linear')
                if tune_param is None or tune_param == 'default':
                    tune_param = grid_tune_param
            output = reg_class.get_grid_score(score_types, lin_mod, tune_param, data,
                                              'Linear')
            return output
        except Exception as e:
            return e
        
    # Polynomial Regression Model
    def polynomial_regression(data, score_types, tune_param, reg_class):
        try:
            from sklearn.linear_model import LinearRegression
            from sklearn.preprocessing import PolynomialFeatures
            
            grid_tune_param = {
                              'polynomialfeatures__degree'  : np.arange(2),
                              'polynomialfeatures__interaction_only'    : [True, False],
                              'polynomialfeatures__include_bias'        : [True, False],
                              'polynomialfeatures__order'               : ['C', 'F'],
                              'linearregression__fit_intercept': [True, False], 
                              'linearregression__normalize': [True, False]
                            }                
            if tune_param == 'default':
                tune_param = grid_tune_param
            else:
                tune_param = tune_param.get('polynomial')
                if tune_param is None or tune_param == 'default':
                    tune_param = grid_tune_param
            def PolynomialRegression(degree=2, **kwargs):
                return mk_pipeline(PolynomialFeatures(degree), LinearRegression(**kwargs))

            output = reg_class.get_grid_score(score_types, PolynomialRegression(), 
                                              tune_param, data, 'Polynomial')
            return output
        except Exception as e:
            return e
    
    
    # Ridge Regression Model
    def ridge_regression(data, score_types, tune_param, reg_class):
        try:
            from sklearn.linear_model import Ridge
            reg_mod = Ridge()
            
            grid_tune_param = {
                              'alpha':[1e-15, 1e-10, 1e-8, 1e-3, 1e-2, 
                                       1, 5, 10, 15, 20, 40, 50,
                                       85, 100, 300, 500, 1000
                                       ]
                            }
            if tune_param == 'default':
                tune_param = grid_tune_param
            else:
                tune_param = tune_param.get('ridge')
                if tune_param is None or tune_param == 'default':
                    tune_param = grid_tune_param
            output = reg_class.get_grid_score(score_types, reg_mod, tune_param, data,
                                              'Ridge')
            return output
        except Exception as e:
            return e
    
    # Lasso Regression Model
    def lasso_regression(data, score_types, tune_param, reg_class):
        try:
            from sklearn.linear_model import Lasso
            lasso_mod = Lasso()
            
            grid_tune_param = {
                              'alpha':[1e-15, 1e-10, 1e-8, 1e-3, 1e-2, 
                                       1, 5, 10, 15, 20, 40, 50,
                                       85, 100, 300, 500, 1000
                                       ]
                            }
            if tune_param == 'default':
                tune_param = grid_tune_param
            else:
                tune_param = tune_param.get('lasso')
                if tune_param is None or tune_param == 'default':
                    tune_param = grid_tune_param
            output = reg_class.get_grid_score(score_types, lasso_mod, tune_param, data,
                                              'Lasso')
            return output
        except Exception as e:
            return e
        
    # ElasticNet Regression Model
    def elasticnet_regression(data, score_types, tune_param, reg_class):
        try:
            from sklearn.linear_model import ElasticNet
            el_mod = ElasticNet()
            
            grid_tune_param = {
                              'alpha':[1e-15, 1e-10, 1e-8, 1e-3, 1e-2, 
                                       1, 5, 10, 15, 20, 40, 50,
                                       85, 100, 300, 500, 1000
                                       ]
                            }
            if tune_param == 'default':
                tune_param = grid_tune_param
            else:
                tune_param = tune_param.get('elasticnet')
                if tune_param is None or tune_param == 'default':
                    tune_param = grid_tune_param
            output = reg_class.get_grid_score(score_types, el_mod, tune_param, data,
                                              'ElasticNet')
            return output
        except Exception as e:
            return e
        
        
    # Random_Forest Regression Model
    def randomforest_regression(data, score_types, tune_param, reg_class):
        try:
            from sklearn.ensemble import RandomForestRegressor
            rand_mod = RandomForestRegressor()
            
            grid_tune_param = {
                      'n_estimators'        : [300, 500, 1000],
                      'max_features'        : ['sqrt', 'log2'],
                      'max_depth'           : [2, 8],
                      'min_samples_leaf'    : [ 2, 8],
                      'min_samples_split'   : [ 2, 8]
                    }
            if tune_param == 'default':
                tune_param = grid_tune_param
            else:
                tune_param = tune_param.get('random_forest_regressor')
                if tune_param is None or tune_param == 'default':
                    tune_param = grid_tune_param
            output = reg_class.get_grid_score(score_types, rand_mod, tune_param, data,
                                              'Random Forest Regressor')
            return output
        except Exception as e:
            return e
        
    # XG_Boost Regression Model
    def xgbregressor_regression(data, score_types, tune_param, reg_class):
        try:
            from xgboost import XGBRegressor
            xgb_mod = XGBRegressor()
            
            grid_tune_param = {
                          'learning_rate'    : [0.05, 0.10] ,
                          'min_child_weight' : [ 1, 3],
                          'gamma'            : [ 0.0, 0.1],
                          'colsample_bytree' : [ 0.3, 0.4],
                          'n_estimators'     : [300, 500, 100]
                    }
            if tune_param == 'default':
                tune_param = grid_tune_param
            else:
                tune_param = tune_param.get('xgb_regressor')
                if tune_param is None or tune_param == 'default':
                    tune_param = grid_tune_param
            output = reg_class.get_grid_score(score_types, xgb_mod, tune_param, data,
                                              'XG_Boost Regressor')
            return output
        except Exception as e:
            return e
        
    # get_grid_score function calls the gridsearch_cv to get the Grid Search Result
    def get_grid_score(score_types, model, tune_param, data, model_name):
        try:
            score_list = []
            for score_type in score_types:
                score, best_score, best_param, plot_status = grid_class.gridsearch_cv(model, 
                                                                  tune_param,
                                                                  score_type,
                                                                  data,
                                                                  prob,
                                                                  set_plotting,
                                                                  current_model)
                output = {
                            'Model'                    :   model_name,
                            'Score_Type'               :   score_type,
                            'Predicted_Score'          :   score,
                            'Best_Score'               :   best_score,
                            'Best_Parameter'           :   best_param,
                            'Plot_Status'              :   plot_status,
                            'Error'                    :   ''
                        }
                score_list.append(output)
            return score_list   
        except Exception as e:
            error = [{
                'Model':model, 
                'Score_Type':'',
                'Predicted_Score':'',
                'Best_Score':'',
                'Best_Parameter':'',
                'Plot_Status':'',
                'Error': str(e)
                }]
            return error
        
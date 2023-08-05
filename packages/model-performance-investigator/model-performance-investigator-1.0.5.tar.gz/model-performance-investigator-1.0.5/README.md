# Model Performance Investigator


## Short Description

        Model Performance Investigator is used to analyse the performance of Machine Learning and
    Deep learning models. It gives the user, basic idea how the model performance on given data.
    So that user can start work on the right model.
        Current Version supports Regression and Classification type of problems with 
    Visualization support.
    
    
## Installation

    pip install model-performance-investigator
    
    
## How to use ?
    
    * Import the package.
        from model_analyzer.ml_models import MLPredictor as ml
    
    * Call the required function, assign it to a variable and run.
                  
                  
## Functions ?

    1. predector()  ->  Used to get Score for the Models. Returns score data
                        if error is not present else returns error message.
    
    2. draw_plot()  ->  Used to plot Distribution plot of the Features. Return 
                        PDF file if correct dataframe send with only 'int' 
                        featurs only else returns error message.
    

## Parameters ?

    1. predector():
        * prob_type -> It is mandatory parameter.
                           
                       TYPE : String
                       
                       KEYS :
                        * regression
                        * classification      
                       
                       FORMAT :
                           prob_type = ['regression']
        
        * data -> data must contain "train_X, train_y, test_x". train_X, train_y is for fitting
                   the model and test_x is for predicting. It is mandatory.
                   
                   TYPE : List
                   
                   FORMAT :
                       data = [train_X, train_y, test_x]
                   
        * alg_type -> Type of the algorithm. It is optional parameter. Provide the parameter
                      values in list.  
                      Default is "Linear Regression" algorithm.
                       
                      TYPE : List
                       
                      KEYS :
                         Regression :
                             Algorithm Name             | Parameter 
                             ---------------------------|------------------------
                             Linear Regression          | linear
                             Polynomial Regression      | polynomial
                             Redige Regression          | ridge
                             Lasso Regression           | lasso
                             ElasticNet Regression      | elasticnet
                             Random Forest Regression   | random_forest_regressor
                             XG Boost Regressor         | xgb_regressor
                             
                        Classification :
                             Algorithm Name             | Parameter 
                             ---------------------------|------------------------
                             Logistic                   | logistic
                             Decision Tree              | decision_tree
                             Random Forest              | random_forest
                             Naive Bayes                | naive_bayes
                             SVC                        | svc
                             XGB Classifier             | xgb_classifier
                         
                     FORMAT :
                        alg_type = ['linear', 'polynomial']
                    
                        
        * score_type -> Type of the score. It is optional parameter. Provide the parameter
                        values in list. Default is "r2" algorithm.
                        
                        TYPE : List
                        
                        1. Regression:
                           It Supports:
                            * r2
                            * explained_variance
                            * max_error
                            * neg_mean_absolute_error
                            * neg_mean_squared_error
                            * neg_mean_squared_log_error
                            * neg_median_absolute_error
                            * neg_mean_poisson_deviance
                            * neg_mean_gamma_deviance
                           
                        2. Classification:
                            It Supports:
                            * jaccard
                            * f1
                            * neg_log_loss
                            * roc_auc
                            * accuracy
                            * balanced_accuracy
                            * average_precision
                            
                        FORMAT :
                            score_type = ['explained_variance', 'neg_mean_poisson_deviance']
                            
                
        * tune_param ->  Tuning Parameters for the model. It is an optional. By Default, 
                         this package uses some basic parameters for each models.
                         User can provide own Tunning Parameters.
                         
                         TYPE : List of Dict
                         
                         Template:
                             tune_param = {Name of the model: {parameters}}
                             Name of the model -> should be similar like alg_type.
                             
                         FORMAT:
                             linear_tune_param = {
                                  "fit_intercept"       : [True, False],
                                  "normalize"           : [True, False],
                                  "copy_X"              : [True, False],
                                  "n_jobs"              : [ -1]
                                }
                            lasso_tune_param = {
                                  "alpha":[1e-15, 1e-10, 1e-8, 1e-3, 1e-2, 
                                           1, 5, 10, 15, 20, 40, 50,
                                           85, 100, 300, 500, 1000
                                           ]
                                }
                                
                             tune_param = {'linear': linear_tune_param, 
                                          'lasso': lasso_tune_param}
                         
                         Note : User don't have to specify tunning parameters for all the
                                models used in 'alg_type'. If tunning parameters are not provided
                                then this package use default tunning parameters.
                                
        * set_plot -> Creates Residual Plot for regression model only.
                      By default, it is Set as True.
                      
                      TYPE : Boolean
                      
                      FORMAT :
                         set_plot = True
                    
                         
    EXAMPLE :
        from model_analyzer.ml_models import MLPredictor as ml
        
        data = [train_X, train_y, test_x]
        new_out = ml.predector('regression', data, alg_type=['linear','lasso'], 
                  score_type=['r2'], tune_param='default', set_plot=True)
                       
                       
    2. draw_plot():
        * prob_type -> Currently it supports 'regression' only. It is mandatory parameter.
                       
                       TYPE : String
                       
                       FORMAT :
                         prob_type = 'regression'
                         
        * datafarme -> Used needs to send Dataframe objetc. All the features must be 
                       integers only.
        
        * columns -> It is optional parameter. By default all the columns are selected.
                     User can send required features alone.
                     
                     TYPE : List
                     
                     FORMAT :
                         columns = ['ColA', 'ColB', 'ColC']
                         
        * plot_type -> It is optional parameter. By default 'Histograme' plot is selected.
                       User can select Histograme or Scatter plots
                       
                       TYPE : String
                       
                       Keys :
                           Histograme -> hist
                           Scatter    -> scatter
                       
                       FORMAT :
                         plot_type = 'hist'
                
                         
    EXAMPLE :
        from model_analyzer.ml_models import MLPredictor as ml
        
        output = ml.draw_plot('regression', dataframe, columns =  ['ColA', 'ColB', 'ColC'],
                 plot_type='hist')
        
                       
## Project History

        The project was started in 2019 by Srikandan Raju and Sathish Anandha.
        
        
## NOTE :
        Download latest version only.
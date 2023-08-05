__author__ = 'Srikandan Raju, Sathish Anandha'
__copyright__ = 'Copyright (C) 2007 Free Software Foundation'
__license__ = 'GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007'
__version__ = '1.0.3'
__maintainer__ = 'Srikandan Raju, Sathish Anandha'

# main_regression is the Class
class MainRegressionPlot(object):
    
    # Importing required packages
    def import_required_packages():
        try:
            global plt
            global mt
            global os
            global PdfPages
            global pd
            
            import pandas as pd
            import matplotlib.pyplot as plt
            import matplotlib
            from matplotlib.backends.backend_pdf import PdfPages as PdfPages
            import math as mt
            import os as os
            
            matplotlib.style.use('ggplot')
            
            return 'imported'
        except Exception as  e:
            e = 'Kindly install or update Packages \n ' + str(e)
            return e
        
        
    # regression_plot function imports and calls plot and all_plot
    def regression_plot(datafarme, columns, plot_type, reg_main):
        try:
            import_status = reg_main.import_required_packages()
            
            if import_status == 'imported':
                if isinstance(columns, (list)):
                    output = reg_main.plot(datafarme, columns, plot_type, reg_main)
                else:
                    if columns == 'All':
                        output = reg_main.all_plot(datafarme, plot_type, reg_main)
                    else:
                        output = 'Invalid \'columns\' Parameter'
                return output
            else:
                return import_status
        except Exception as e:
            return e
            
    
    # plot function plots the datafarme selected features
    def plot(datafarme, columns, plot_type, reg_main):
        temp_df = datafarme[columns].copy()
        try:
            if plot_type == 'hist':
                output = reg_main.draw_hist_plot_pdf(temp_df)
                return output
            elif plot_type == 'scatter':
                output = reg_main.draw_scatter_plot_pdf(temp_df)
                return output
        except Exception as e:
            return e
        
    
    # all_plot function plots all the features of datafarme
    def all_plot(datafarme, plot_type, reg_main):
        try:
            if plot_type == 'hist':
                output = reg_main.draw_hist_plot_pdf(datafarme)
            elif plot_type == 'scatter':
                output = reg_main.draw_scatter_plot_pdf(datafarme)
            return output
        except Exception as e:
            return e
        
    
    # draw_hist_plot_pdf function draws Histogram Plot
    def draw_hist_plot_pdf(datafarme):
        try:
            with PdfPages('Distribution_Histogram_Plot.pdf') as pdf:
                columns = datafarme.columns
                count = 1
                print(len(columns))
                for column in columns:
                    plt.figure(figsize=(3, 3))
                    value = pd.to_numeric(datafarme[column], downcast ='signed')
                    plt.hist(x=value)
                    plt.title(str(count)+'.'+column)
                    pdf.savefig()
                    plt.close()
                    count+=1
                return 'Distribution_Histogram_Plot is Downloaded' + os.getcwd()
        except Exception as e:
            return e
        
    
    # draw_scatter_plot function draws Scatter Plot
    def draw_scatter_plot_pdf(datafarme):
        try:
            with PdfPages('Distribution_Scatter_Plot.pdf') as pdf:
                columns = datafarme.columns
                count = 1
                print(len(columns))
                for column in columns:
                    plt.figure(figsize=(3, 3))
                    value = pd.to_numeric(datafarme[column], downcast ='signed')
                    plt.scatter(x=value, y=range(len(datafarme)))
                    plt.title(str(count)+'.'+column)
                    pdf.savefig()
                    plt.close()
                    count+=1
                return 'Distribution_Scatter_Plot is Downloaded' + os.getcwd()
        except Exception as e:
            return e
    
    
    # draw_resud_plot draws Residual Plot for Regression Model
    def draw_resud_plot(original_value, predicted_value, current_model):
        try:
            import_status = MainRegressionPlot.import_required_packages()
            
            if import_status == 'imported':
                
                MEDIUM_SIZE = 10
            
                plt.rc('font', size=MEDIUM_SIZE)
                plt.rc('axes', titlesize=MEDIUM_SIZE)
                plt.rc('axes', labelsize=MEDIUM_SIZE)
                plt.rc('xtick', labelsize=MEDIUM_SIZE)
                plt.rc('ytick', labelsize=MEDIUM_SIZE)
                plt.rc('legend', fontsize=MEDIUM_SIZE)
                
                resu_data = original_value - predicted_value
                plt.scatter(x=range(0, len(resu_data)), y=resu_data)
                plt.axhline(y=0, c='r')
                plt.title('Residual Plot', fontsize=20)
                plt.savefig(current_model.upper()+'_Residual_Plot.png')
                return 'Residual Plot is downloaded in : ' + os.getcwd()
            else:
                return import_status
        except Exception as e:
            return e
        
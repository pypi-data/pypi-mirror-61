import statistics
import pandas as pd
from scipy import stats
import seaborn as sns
import pylab as plt
import numpy as np

def normality(df, list_var, print_img, size_x, size_y, font_size):
    """
    Displays histograms to compare your variables 
    to a normal distribution using pvalue.

    Parameters
    df          : DataFrame you would like to analyze.
    list_var    : Name of variables to observe.
    print_img   : input 'y' to print image or 'n' to not print.
    size_x      : width of the image output.
    size_y      : height of the image output.
    font_size   : font size of the titles and headers.
    """
    fig, ax = plt.subplots(figsize = (size_x, size_y))
    inn = 0
    for col in list_var:
        if df[col].dtype.name != 'object':
            inn+=1
    inn = inn * 2 + 2
    i = 0
    for col in list_var:
        i+=1
        if df[col].dtype.name == 'object':
            i-=1
        else:
            try:
                col_test = df[col]
                mu = (col_test).mean()
                sigma = statistics.stdev(col_test)
                sizex = int(col_test.shape[0])
                norm_rand = np.random.normal(mu, sigma, sizex)
                norm_test = col_test.tolist()
                st2, pval_2 = stats.ks_2samp(norm_rand, norm_test)
                stn, pval_n = stats.normaltest(norm_test)

                p = max([pval_n, pval_2])
                p = round(pd.to_numeric(p),4)
                plt.subplot(inn, 2, i)
                plt.xlabel(col, fontsize=font_size*0.75)
                plt.ylabel('Frequency Count', fontsize=font_size*0.75)
                plt.title("HIST: " + col + ", pvalue = " + str(p), fontsize=font_size)
                sns.kdeplot(norm_test, label = col, shade = True)
                sns.kdeplot(norm_rand, label = "Random Normal", color = "g")
                plt.legend(fontsize=font_size*0.65)
            except:
                print("Conflict in variable: " + str(col) + "\n" + "processing")
    plt.tight_layout()
    if print_img == "y":
        plt.savefig('Histrograms_all.png')
    plt.show()



def table(df, n_rows, n_round):
    """
    Displays relevant features to help you on data 
    cleaning and analysis.

    Parameters
    df      : DataFrame you would like to analyze.
    n_rows  : Number of variables to display.
    n_round : Number of decimals to round calculations.
    """
    n_rows +=1
    pd.set_option('display.max_rows', n_rows)
    nulls = df.isnull().sum()
    counts = df.count()
    means = round(df.mean(), n_round)
    types = df.dtypes
    median = round(df.median(), n_round)
    result = pd.concat([nulls, counts, types, means, median], axis = 1, sort=False)
    result.rename(columns={0: 'NULLS', 1: 'COUNT', 2: 'TYPES', 3:'MEAN', 4:'MEDIAN'}, inplace=True)
    result['UNIQUES'] = ''
    result['SAMPLE'] = ''
    result['Outliers'] = ''
    result['pval(Norm)'] = ''
    i1 = 0
    norma = {}
    for i in df.columns:
        list1 = df[i][0:10].to_list()
        result['SAMPLE'].values[i1] = str(list1)
        va = int(df[i].value_counts().shape[0])
        result['UNIQUES'].values[i1] = va

        if df[i].dtype.name != 'object':
            col_data = df[i].dropna()
            IQR_25 = np.percentile(col_data, 25)
            IQR_75 = np.percentile(col_data, 75)
            IQR_1p5 = round(1.5*(IQR_75-IQR_25), n_round)
            lowerLimit = round(IQR_25 - IQR_1p5, n_round)
            upperLimit = round(IQR_75 + IQR_1p5, n_round)

            lower_qty = int(df[i][df[i] < lowerLimit].shape[0])
            high_qty = int(df[i][df[i] > upperLimit].shape[0])
            if (lower_qty > 0 or high_qty > 0) and va > 2:
                result['Outliers'].values[i1] = '[' + str(lower_qty) + ',' + str(high_qty) + ']'
            else:
                result['Outliers'].values[i1] = ''
            p=0
            mu = df[i].mean()
            sigma = statistics.stdev(df[i])
            if not pd.isnull(sigma) and not sigma == 0:
                sizex = int(df[i].shape[0])
                nom_rand = np.random.normal(mu, sigma, sizex)
                rom_test = df[i].tolist()
                st2, pval_2 = stats.ks_2samp(nom_rand, rom_test)
                stn, pval_n = stats.normaltest(rom_test)
                p = max([pval_n, pval_2])

                p = round(pd.to_numeric(p),4)
                result['pval(Norm)'].values[i1] = p
            else:
                result['pval(Norm)'].values[i1] = 0
        else:
            result['pval(Norm)'].values[i1] = 0
        i1+=1
    result.reset_index(inplace=True)
    result=result.rename(columns = {'index':'VARIABLES'})
    return (result)

def scatter(df, explanatory_var, response_var, print_img, size_x, size_y, font_size, green_blue = "g"):
    """
    Scatter plot to identify trends and outliers.

    Parameters
    df               : DataFrame you would like to analyze.
    explanatory_var  : Name of explanatyr variables.
    response_var     : Name of response varialbe.
    print_img        : input 'y' to print image or 'n' to not print.
    size_x           : width of the image output.
    size_y           : height of the image output.
    font_size        : font size of the titles and headers.
    green_blue       : set 'g' or 'b' to define color.
    """
    fig, ax = plt.subplots(figsize = (size_x, size_y))
    inn = 0
    for col in explanatory_var:
        if df[col].dtype.name != 'object':
            inn+=1
    inn = inn * 2 + 2
    i = 0
    for col in explanatory_var:
        i+=1
        if df[col].dtype.name == 'object':
            i-=1
        else:

            try:
                plt.subplot(inn, 2, i)
                x = df[col]
                y = df[response_var]
                plt.xlabel(col, fontsize=font_size*0.75)
                plt.ylabel(response_var, fontsize = font_size*0.75)
                plt.title("SCATTER PLOT: " + col, fontsize=font_size)
                z = np.polyfit(x, y, 1)
                p = np.poly1d(z)

                if green_blue.lower() in ["green", "g"]:
                    plt.scatter(x, y, color = "lightgreen", edgecolors='green')
                    plt.plot(x,p(x),"b")
                else:
                    plt.scatter(x, y, color = "cornflowerblue", edgecolors='white')
                    plt.plot(x,p(x),"orange")
            except:
                print("Conflict in variable: " + str(col) + "\n" + "processing")

    plt.tight_layout()
    if print_img == "y":
        plt.savefig('scatter_plots.png')
    plt.show()
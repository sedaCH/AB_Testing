############################################
# AB TESTİNG
############################################

# Değişkenler
############################################
# Impression – Reklam görüntüleme sayısı
# Click – Tıklama-Görüntülenen reklama tıklanma sayısını belirtir.
# Purchase – Satın alım- Tıklanan reklamlar sonrası satın alınan ürün sayısını belirtir.
# Earning – Kazanç-Satın alınan ürünler sonrası elde edilen kazan

############################################
# AB Testing Aşamaları
############################################
#1.Hipotesi kur
#2.Varsayım kontrolü
#   a. Normallik Varsayımı
#   b. Varyans Homojenliği
# 3. Hipotezin Uygulanması
#  -p-value<0005 se H0 red
#   a. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)
#   b. Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)
# Not:
# - Normallik sağlanmıyorsa direk 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.


############################################
# Imports
############################################
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, pearsonr, spearmanr, kendalltau, \
    f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

############################################
# Veriyi Düzenleme
############################################
def data_preparation(path,sheet,):
    """

    Parameters
    --------
    name: name of the dataframe
    path: path of the excel ile that will be imported
    sheet: sheet name of the file

    Returns
    -------
    first 4 columns of the data in excel file as a dataframe

    """
    name= pd.read_excel(path,sheet_name=sheet)
    name=name.iloc[:,0:4]
    return name
average_bid=data_preparation("hafta5/ödevler/ab_testing.xlsx","Test Group")
max_bid=data_preparation("hafta5/ödevler/ab_testing.xlsx","Control Group")

############################################
# Veriyi Gözlemleme
############################################
from helper.helper import check_df
check_df(average_bid)
check_df(max_bid)

def graphbybox(dataframe,colname):
    """

    Parameters
    ----------
    dataframe: dataframe of the variable will be plotted
    colname: columns name of the variable

    Returns
    -------
    draws boxplot of the given variable

    """
    plt.boxplot(dataframe[colname],vert=False )
    plt.title(colname)
    plt.show()

for i in average_bid.columns:
    graphbybox(average_bid,i)

for i in max_bid:
    graphbybox(max_bid,i)




####################################################################################################################################
# Görev 1: A/B testinin hipotezini tanımlayınız.
####################################################################################################################################

# H0:averagebidding ile maximumbidding'in satınalma sayıları arasında anlamlı bir fark yoktur.
# H1:averagebidding ile maximumbidding'in satınalma sayıları arasında anlamlı bir  fark vardır.


####################################################################################################################################
# Görev 2:Hipotez testini gerçekleştiriniz. Çıkan  sonuçların istatistiksel olarak anlamlı olup  olmadığını yorumlayınız.
####################################################################################################################################

############################################
# 1. Varsayım Kontrolleri
############################################

############################
# a.Normallik Varsayımı
############################
# H0:serixetinin normal dağılımla arasında fark yoktur
# H1:...vardır

test_stat, pvalue = shapiro(max_bid["Purchase"])  #H0:reddedilmedi, normallik sağlanıyor.
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(average_bid["Purchase"]) #H0:reddedilmedi, normallik sağlanıyor.
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

############################
# Varyans Homojenliği
############################
# H0: Varyanslar Homojendir.
# H1: Varyanslar Homojen Değildir.

test_stat, pvalue = levene(max_bid["Purchase"],
                           average_bid["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) #H0:reddedilmedi , varyanslar homojendir.

####################################################################################################################################
# Görev 3:Hangi testi kullandınız, sebeplerini belirtiniz.
####################################################################################################################################


test_stat, pvalue = ttest_ind(max_bid["Purchase"],
                              average_bid["Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) #p:0.3493 #H0:reddedilemez.

####################################################################################################################################
# Görev 4:Görev 2’de verdiğiniz cevaba göre, müşteriye tavsiyeniz nedir?
####################################################################################################################################
# " H0: averagebidding ile maximumbidding'in satınalma sayıları arasında anlamlı bir fark yoktur" hipotezimiz reddedilmedi
#veri setimizdeki  Click ve Earning değişkenlerini de inceleyip, o değişkenler açısında da bir fark var mı yok mu kontrol edip
#ona göre karar vermekte fayda vardır.


####################################################################################################################################
# CLick sayısında bir farklılık var mı?
####################################################################################################################################
# H0:averagebidding ile maximumbidding'in tıklanma  sayıları arasında anlamlı bir fark yoktur.
# H1:averagebidding ile maximumbidding'in tıklanma sayıları arasında anlamlı bir  fark vardır.

test_stat, pvalue = shapiro(max_bid["Click"])  #H0:reddedilmedi, normallik sağlanıyor.
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(average_bid["Click"]) #H0:reddedilmedi, normallik sağlanıyor.
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = levene(max_bid["Click"],
                           average_bid["Click"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))   # H0:reddedildi , varsayımlar homojen değildir.

#varsaynsların homojenliği reddedildiği için equal_var=False giriyoruz
test_stat, pvalue = ttest_ind(max_bid["Click"],
                              average_bid["Click"],
                              equal_var=False)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))  # H0: reddedildi  aralarında anlamlı bir farklılık vardır.

max_bid["Click"].mean()
average_bid["Click"].mean()

#click sayılarının arasında anlamlı bir farklılık olduğu sonucuna ulaştk , dolayısıyla max_bidding yerine average_bidding kullanmak bize daha fazla tıklanma getiriyor.

####################################################################################################################################
# # Earning için bir farklılık var mı?
####################################################################################################################################
# H0:averagebidding ile maximumbidding'in kazançları arasında anlamlı bir fark yoktur
# H1:averagebidding ile maximumbidding'in kazançları arasında anlamlı bir  fark vardır


test_stat, pvalue = shapiro(max_bid["Earning"])  #H0:reddedilmedi, normallik sağlanıyor.
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(average_bid["Earning"]) #H0:reddedilmedi, normallik sağlanıyor.
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = levene(max_bid["Earning"],
                           average_bid["Earning"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))   # H0: reddedilmedi, varyanslar homojendir.

test_stat, pvalue = ttest_ind(max_bid["Click"],
                              average_bid["Click"],
                              equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) #H0: reddedildi.

#kazançlar arasında anlamlı bir farklılık olduğu sonucuna ulaştık , dolayısıyla max_bidding yerine average_bidding kullanmak bize daha fazla kazanç getiriyor.

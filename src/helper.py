import pandas as pd
import os

df_main = pd.read_excel(os.path.join("assets", "parametre_UPD.xlsx"))
df = pd.read_excel(os.path.join("assets", "unique_lat_lon.xlsx"))
longitudes = df["Boylam"].to_frame()
latitudes = df["Enlem"].to_frame()

# PGV values doesn't match with the values with the AFAD website.
def interpolate(head, dyhd_no, x_f, y_f, variables):
    """
    This function performs bi-linear interpolation on the input variables.

    Args:
        head (str): A string representing the parameter name, such as "S1", "SS", "PGA", or "PGV".
        dyhd_no (int): An integer representing the DYHD number, available values are 1,2,3,4.
        x_f (float): A float representing the fractional distance between x1 and x2.
        y_f (float): A float representing the fractional distance between y1 and y2.
        variables (list): A list of Pandas dataframes representing the four variables that
                          need to be interpolated.

    Returns:
        float: The interpolated value of the parameter.

    """
    var1 = variables[0][f"{head}{dyhd_no}"].iloc[0]
    var2 = variables[1][f"{head}{dyhd_no}"].iloc[0]
    var3 = variables[2][f"{head}{dyhd_no}"].iloc[0]
    var4 = variables[3][f"{head}{dyhd_no}"].iloc[0]

    var1_var2 = var1 + x_f * (var2 - var1)
    var3_var4 = var3 + x_f * (var4 - var3)

    return var1_var2 + y_f * (var3_var4 - var1_var2)


def get_spectral_values(dyhd_no, latitude, longitude):
    """
    This function calculates the spectral values for a given DYHD number, latitude, and longitude
    using bi-linear interpolation.

    Args:
        dyhd_no (int): An integer representing the DYHD number, available values are 1,2,3,4.
        latitude (float): A float representing the latitude value.
        longitude (float): A float representing the longitude value.

    Returns:
        Tuple: A tuple containing four floats representing the SS, S1, PGA, and PGV values.

    """
    y, x = latitude, longitude

    df_sort_y = latitudes.iloc[(latitudes["Enlem"] - y).abs().argsort()[:2]]
    df_sort_x = longitudes.iloc[(longitudes["Boylam"] - x).abs().argsort()[:2]]
    numbers_y = df_sort_y["Enlem"].tolist()
    numbers_x = df_sort_x["Boylam"].tolist()
    x1 = min(numbers_x)
    x2 = max(numbers_x)
    y1 = min(numbers_y)
    y2 = max(numbers_y)

    x_f = (x - x1) / (x2 - x1)
    y_f = (y - y1) / (y2 - y1)

    var1_look = str(x1) + str(y1)
    var2_look = str(x2) + str(y1)
    var3_look = str(x1) + str(y2)
    var4_look = str(x2) + str(y2)

    variables_list = [var1_look, var2_look, var3_look, var4_look]
    df_variables = pd.DataFrame(variables_list)
    df_variables.columns = ["Merged"]

    var1_final = df_main.loc[df_main["Merged"] == var1_look]
    var2_final = df_main.loc[df_main["Merged"] == var2_look]
    var3_final = df_main.loc[df_main["Merged"] == var3_look]
    var4_final = df_main.loc[df_main["Merged"] == var4_look]

    var_list = [var1_final, var2_final, var3_final, var4_final]
    s1 = interpolate("S1", dyhd_no, x_f, y_f, var_list)
    ss = interpolate("SS", dyhd_no, x_f, y_f, var_list)
    pga = interpolate("PGA", dyhd_no, x_f, y_f, var_list)
    pgv = interpolate("PGV", dyhd_no, x_f, y_f, var_list)

    return ss, s1, pga, pgv

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio
import scipy.integrate as integrate
pio.renderers.default = "browser"

def f(SVII2, t, v, A):
    S, V, I, I2 = SVII2
    params = [0.25, 3.844E-6, 0.5, 0.4, 0.18, 0.15, 0.15, 0.15]
    m, b, p, k, g, a, c, d = params

    return [A - b * (I - (1 - p) * I2) * S - (m + v) * S + k * V, v*S-g*b*(I-(I - p) * I2) * V - (m + k) * V,
            b*(I+(1-p)*I2) * (S + g * V) - (a + m + d) * I, a*I-(m+c+d)*I2]


def get_model_results(jahren):
    df = pd.read_csv('https://raw.githubusercontent.com/henrycerpa/ica/main/data/final_modelo.csv')
    listdptos = pd.unique(df['departamento'])
    dpts_s = []
    dpts_v = []
    dpts_i = []
    dpts_i2 = []

    for i in listdptos:
        subdf = df[df['departamento'] == i]
        # Se toma el valor inicial como el primer valor que se encuentra en la
        S0 = subdf['S'].iloc[0]
        V0 = subdf['v'].iloc[0]
        I0 = subdf['I'].iloc[0]
        I20 = subdf['I2'].iloc[0]
        SVII20 = [S0, V0, I0, I20]
        v = subdf['v'].mean()
        A = subdf['A'].mean()
        t = np.linspace(0, 9, num=jahren)
        xyz = integrate.odeint(f, SVII20, t, args=(v, A))
        S, V, I, I2 = xyz.T
        dpts_s.append({i: S})
        dpts_v.append({i: V})
        dpts_i.append({i: I})
        dpts_i2.append({i: I2})

    output_s = pd.concat([pd.DataFrame(l) for l in dpts_s], axis=1).T
    output_s.loc['PAIS'] = output_s.sum()
    output_v = pd.concat([pd.DataFrame(l) for l in dpts_v], axis=1).T
    output_v.loc['PAIS'] = output_s.sum()
    output_i = pd.concat([pd.DataFrame(l) for l in dpts_i], axis=1).T
    output_i.loc['PAIS'] = output_s.sum()
    output_i2 = pd.concat([pd.DataFrame(l) for l in dpts_i2], axis=1).T
    output_i2.loc['PAIS'] = output_s.sum()

    return output_s, output_v, output_i, output_i2


def plot_results(s_df, v_df, i_df, i2_df, ldptos):
    """
    Gets model outputs and generates lines plot
    :param s_df: susceptible output
    :param v_df: vaccinated output
    :param i_df: infected output
    :param i2_df: detected and unculled ouput
    :param ldptos: list of departments for which to generate the plots
    :return: a plotly express line object
    """

    sub_s_df = s_df[s_df.index.isin(ldptos)]
    sub_v_df = v_df[v_df.index.isin(ldptos)]
    sub_i_df = i_df[i_df.index.isin(ldptos)]
    sub_i2_df = i2_df[i2_df.index.isin(ldptos)]

    if len(ldptos) > 1:
        sub_s_df.loc['TOTAL'] = sub_s_df.sum()
        sub_v_df.loc['TOTAL'] = sub_v_df.sum()
        sub_i_df.loc['TOTAL'] = sub_i_df.sum()
        sub_i2_df.loc['TOTAL'] = sub_i2_df.sum()
        df_toplot = pd.DataFrame([sub_s_df.loc['TOTAL'], sub_v_df.loc['TOTAL'], sub_i_df.loc['TOTAL'], sub_i2_df.loc['TOTAL']])
    else:
        df_toplot = pd.concat([sub_s_df, sub_v_df, sub_i_df, sub_i2_df])
    df_toplot.index = ['Susceptible', 'Vaccinated', 'Infected', 'Infectious not slaughtered']

    df_toplot = df_toplot.T
    xvals = [i + 1 for i in df_toplot.index]
    plotbx = px.line(df_toplot,
                     x=xvals,
                     y=['Susceptible', 'Vaccinated', 'Infected', 'Infectious not slaughtered'],
                     markers=True,
                     template="ggplot2",
                     labels={'value': 'Quantity',
                             'variable': ''}
                     )
    plotbx.update_layout(xaxis_title='Years Ahead')

    return plotbx
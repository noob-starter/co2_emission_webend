from django.shortcuts import render

# # Create your views here.


import numpy as np 
import pandas as pd
import datetime
# import seaborn as sns 
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go



import pandas as pd
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt
import plotly.offline as opy
# import seaborn as sb
from django.views.decorators.csrf import csrf_exempt

# warnings.filterwarnings("ignore")

co2=pd.read_csv("co2_emission.csv")

df=co2.copy()


df=df.rename(columns={"Annual CO₂ emissions (tonnes )":"CO2"})

total_CO2 = df.groupby(["Code","Entity"])["CO2"].sum()

df_total_CO2 = pd.DataFrame(total_CO2)
df_total_CO2.reset_index(level=0, inplace=True)
df_total_CO2.reset_index(level=0, inplace=True)
# df_total_CO2.head()
# df.head()


# Removing column Code due to null value and non importance in analysis 
df.drop(['Code'],inplace=True,axis=1)
# df.head()


year = sorted(df["Year"].unique())
# print("Year Range from "+str(year[0])+ " to "+ str(year[len(year)-1]))


country =  ["Eu-28","Russia","United States","China","Asia and Pacific (other)","Europe (other)"]
@csrf_exempt
def general_explore(request):
  context = {'options' :country} 

  
  if request.method == "POST":
    print("************************************")
    query_set = request.POST
    
    field1 = query_set['year']
    field2 = query_set['limit']
    field3=""
    if "format" in query_set:
      field3 = query_set['format']
    print("************IMP*****************************")
    print(field1,field2,field3)


    context["show"] = "yes"
    print(len(field1),len(field2),len(field3))
   

    if len(field3)>0:
      context["graph"] = country_emission(str(field3))
    else:
      context["graph"] = country_emission()
    context["graph_a_head"] = "Country's Emission Over Time "
   

    context["graph_c_head"] = "Top CO2 Emitting Countries "
    if len(field1)>0 and len(field2)>0:
      context["graph2"] =  find_top(int(field1),int(field2))
    else:
      context["graph2"] =  find_top()

    if len(field1)>0 and len(field2)>0:
      context["graph3"] = pie_chart(int(field1),int(field2))
    else:

      context["graph3"] = pie_chart()
    context["graph_d_head"] = "Pie Chart"
    
    # context["graph_e_head"] = "Summary Plot"

    # if len(field1)>0:
    #   context["graph4"] =  summary(int(field1))
    # else:

    #   context["graph4"] =  summary()
  else:
    print("OOOOOOOOOOOOOOO")
    context["show"] = "no"


  # print(context)

  return render(request,'explore.html',context)



@csrf_exempt
def world_emission(request):

    context = {'options' :country}
  
    df_World=df[df["Entity"]=="World"]
    fig = go.Figure(data=go.Scatter(x=year,y=df_World['CO2'], mode='lines'))
    fig.update_layout(title='Amount Of CO2  Emission  In World',title_x=0.5,xaxis_title="Year",yaxis_title="Amount of CO2 Emission (tonnes)")
  

    div2 = opy.plot(fig, auto_open=False, output_type='div')

    temp = df.groupby('Entity').sum().reset_index()
    fig = px.treemap(temp,path = ['Entity'],values = 'CO2')
    fig.update_layout(title='Co2 Emission ',title_x=0.5)



    div = opy.plot(fig, auto_open=False, output_type='div')

   
    context['graph'] = div
    
    
    fig = px.choropleth(df_total_CO2,
                          color="CO2", 
                          locations="Code", 
                          hover_name="Entity", 
                          hover_data=['Entity','CO2'],
                          color_continuous_scale="sunset",
                          labels={'Entity':'Country','CO2':'Total CO₂ Emission'})

    fig.update_layout(title="Total CO₂ Emission Between Years 1750 and 2017",title_x=0.25)


      # Make background transparent
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})

      # Show color scale axis
    fig.update(layout_coloraxis_showscale=True)

    div4 = opy.plot(fig, auto_open=False, output_type='div')

    context['graph3'] = div4

    context['graph2'] = div2

    

    return render(request,'index.html',context)





def country_emission(country="India"):

  # context = {'options' :country}


  df_country=df[df["Entity"]==country]
  fig = go.Figure(data=go.Scatter(x=df_country['Year'],y=df_country['CO2'], mode='lines',marker_color='darkred')) 
  fig.update_layout(title='Total Amount of CO2 Emitted In '+str(country)+' between 1950-2017',xaxis_title="Year",yaxis_title="Amount of CO2 Emitted",xaxis_range=['1950','2017'])
  # fig.show()
  div = opy.plot(fig, auto_open=False, output_type='div')
  return div
  
# country_emission("India")
# done




def compare_countries(list_country =["Turkey","Germany","France"]):

  

  dash_styles = ['green', 'brown', 'blue', 'yellow']

  n = len(dash_styles)
  dash_var = 0

  fig = go.Figure()
  for i in list_country:
    df_country = df[df["Entity"]==i]
    fig.add_trace(go.Scatter(x=df_country['Year'], y=df_country['CO2'], name = str(i)+"- solid" ,
                             line=dict(color=dash_styles[(dash_var)%n], width=4,dash="solid")))
    dash_var +=1

  fig.update_layout(title='Co2 Emission Over Time For Fifferent Countries',title_x=0.5,xaxis_title="Years",yaxis_title="Number of Co2 Emission(tonnes)")
  # fig.show()

  div = opy.plot(fig, auto_open=False, output_type='div')

  return div

# done
# countries_list = ["Turkey","Germany","France"]

# compare_countries(countries_list)

def emission_btw_years(limit_a,limit_b,countries = ["Eu-28","Russia","United States","China","Asia and Pacific (other)","Europe (other)"]):
    countries_name  = []
    countries_total = []

    f = ['green', 'brown', 'blue', 'yellow']

    n = len(f)
    for i in range(len(countries)):
        c = df[df["Entity"]==countries[i]]
        countries_name.append(c)

    val = str(limit_b) if limit_b !=-1 else "2017"
    if limit_b == -1:
        for i in range(len(countries_name)):
            temp = countries_name[i]["CO2"][countries_name["Year"]>=limit_a].sum()
            countries_total.append(temp)
    else:
        for i in range(len(countries_name)):
            temp = countries_name[i]["CO2"][(countries_name[i]["Year"]>=limit_a) & (countries_name[i]["Year"]<=limit_b)].sum()
            countries_total.append(temp)

    total_data = {}
    for i in range(len(countries)):
        total_data[countries[i]] = countries_total[i]

    df_total = pd.DataFrame(data=total_data,index=["Total"])
    df_total=df_total.transpose()

    fig = px.bar(df_total, x=countries,y=df_total["Total"])
    fig.update_layout(title="CO2 Emitted By Different Countries",
                    title_x=0.5,
                    xaxis_title="Country",
                    # colorscale=('blue','green'),
                    yaxis_title="Total Co2 Emission "+str(limit_a) +"-" +val)

    fig.show()


def find_top(year=2010,top_limit=10):
  df_2010=df[df["Year"]==year]
  # df_2010=df_2010.drop([20612]) # World
  
  df_2010=df[df["Year"]==year]
  e = (df_2010[df_2010['Entity'] == 'World']).index.values.tolist()

  df_2010 = df_2010.drop(e)

  df_2010=df_2010.sort_values("CO2",ascending=False)[:top_limit]

  fig = go.Figure(go.Bar(
      x=df_2010['Entity'],y=df_2010['CO2'],
      marker={'color': df_2010['CO2'], 
      'colorscale': 'viridis'},  
      text=df_2010['CO2'],
      textposition = "outside",
  ))

  fig.update_layout(title_text=' Top '+str(top_limit) +' Countries CO2 Emission in the Year '+str(year),
                    title_x=0.5,
                    yaxis_title="CO2 Emission Count (tonnes )",
                    xaxis_title=" Entity")
  # fig.show()
  div = opy.plot(fig, auto_open=False, output_type='div')
  return div



def pie_chart(year=2010,top_limit=10):  
  df_2010=df[df["Year"]==year]
  
  e = (df_2010[df_2010['Entity'] == 'World']).index.values.tolist()

  df_2010 = df_2010.drop(e)
  df_2010=df_2010.sort_values("CO2",ascending=False)[:top_limit]
  fig = go.Figure([go.Pie(labels=df_2010['Entity'], values=df_2010['CO2'],
                          pull=[0.2, 0.1, 0, 0],
                          hole=0.3)])  # can change the size of hole 

  fig.update_traces(hoverinfo='label+percent', textinfo='percent', textfont_size=15)
  fig.update_layout(title=str(year)+" CO2 Emission",title_x=0.5,
                  annotations=[dict(text='CO2', x=0.50, y=0.5, font_size=20, showarrow=False)])

  div = opy.plot(fig, auto_open=False, output_type='div')
  return div
# done


def summary(year=2010):
    df_2010=df[df["Year"]==year]
    word_info=df_2010[df_2010["Entity"]=="World"]
    word_co2=word_info["CO2"].values

    df_2010["ratio"]=(df_2010["CO2"]/word_co2)*100
    # df_2010=df_2010.drop([20612])# world 
    
    e = (df_2010[df_2010['Entity'] == 'World']).index.values.tolist()

    df_2010 = df_2010.drop(e)
    df_2010=df_2010.sort_values("ratio",ascending=False)[:10]

                        
    fig = go.Figure(go.Funnel(
        y=df_2010["Entity"],
        x=df_2010["ratio"] ))
    fig.update_layout(title='2010 CO2 Emission Ratio ',xaxis_title="Ratio",yaxis_title=" Entity ",title_x=0.5)
   

    div = opy.plot(fig, auto_open=False, output_type='div')

    return div 

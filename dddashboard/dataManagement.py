import pathlib

import pandas as pd
from .models import *
import plotly.express as px
import plotly.graph_objects as go




def handle_uploaded_file(f):
    #checar extension del archivo "f"
    file_extension = str(f)
    file_extension = pathlib.Path(file_extension).suffix
    
    if file_extension == ".csv":
        #leer archivo csv y crear 'data frame'
        df = pd.read_csv(f, index_col=False)
        #cambiar la leyenda de las columnas a minusculas
        df.columns = df.columns.str.lower()
        #crear nuevo dataframe con las columnas seleccionadas
        seleccionadas = df[["gender code", "aboriginal peoples", "visible minorities", "person with disabilities", "position/role category"]]
        #selecciona una sola columna
        # print(seleccionadas["gender code"])
        #cambia el conteido a minuscula
        # print(seleccionadas["gender code"].str.lower())
    
    elif file_extension == ".xls":
        df = pd.read_excel(f)
        df = df.to_csv(df)
        df = df.read_csv(df, index_col=False)
        df.columns = df.columns.str.lower()
        print(df)
        # seleccionadas = df[["gender code", "aboriginal peoples", "visible minorities", "person with disabilities", "position/role category"]]

    elif file_extension == ".xlsx":
        df = pd.read_excel(f)
        df = df.to_csv(df)
        df = df.read_csv(df, index_col=False)
        df.columns = df.columns.str.lower()
        print(df)
        # seleccionadas = df[["gender code", "aboriginal peoples", "visible minorities", "person with disabilities", "position/role category"]]

    else:
        print("quien sabe")

    return seleccionadas




#chart colours
colour1 = '#2789AB' #blueformale
colour2 = '#8ACAD8' #blueforfemale#noforVisivleminority#noaboriginal#nodisabilitie
colour3 = '#F6CB7F' #othersexamarillo
pie_anotations_font_color = '#174F6D'

#industry data donut charts
 
def sex_donut_industrychart():
    # if filter=='all':
    male = CompanyData.objects.filter(gender_code='M').count()
    female = CompanyData.objects.filter(gender_code='F').count()
    other = CompanyData.objects.filter(gender_code='O').count()
    total = CompanyData.objects.all().count()
    # else:
    #     male = CompanyData.objects.filter(gender_code='M', size=filter).count()
    #     female = CompanyData.objects.filter(gender_code='F', size=filter).count()
    #     other = CompanyData.objects.filter(gender_code='O', size=filter).count()
    #     total = CompanyData.objects.all().count()


    labels = ['Male','Female','Other']
    values = [male, female, other]
    colors = [colour1, colour2, colour3]

    hole_info = ((female*100)/total)
    hole_info = str(round(hole_info))+str('%')

            # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
    fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
        annotations=[ 
        dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
        dict(text='Female', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
         )
    
    fig.update_traces(textinfo='none')
    config = {'displayModeBar': False}

    chart = fig.to_html(config=config, default_height='175')#, default_width='150')

    return chart, hole_info


def minority_donut_industrychart():
    # if filter=='all':
    Yes_minority = CompanyData.objects.filter(visible_minorities='Y').count()
    No_minority = CompanyData.objects.filter(visible_minorities='N').count()
    total = CompanyData.objects.all().count()
    # else:
    #     Yes_minority = CompanyData.objects.filter(visible_minorities='Y', size=filter).count()
    #     No_minority = CompanyData.objects.filter(visible_minorities='N', size=filter).count()



    labels = ['Yes','No']
    values = [Yes_minority, No_minority]
    colors = [colour2, colour3]

        # hole_info
    hole_info = ((Yes_minority*100)/total)
    hole_info = str(round(hole_info))+str('%')
    

            # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.55, marker = dict(colors= colors), automargin=True)])
    fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
        annotations=[ 
        dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
        dict(text='Minority', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
         )

    fig.update_traces(textinfo='none')
    config = {'displayModeBar': False }
    chart = fig.to_html(config=config, default_height='175')#, default_width='150')

    return chart, hole_info


def aboriginal_donut_industrychart():
    # if filter=='all':
    Yes_aboriginal = CompanyData.objects.filter(aboriginal_peoples='Y').count()
    No_aboriginal = CompanyData.objects.filter(aboriginal_peoples='N').count()
    total = CompanyData.objects.all().count()
    # else: 
    #     Yes_aboriginal = CompanyData.objects.filter(aboriginal_peoples='Y', size=filter).count()
    #     No_aboriginal = CompanyData.objects.filter(aboriginal_peoples='N', size=filter).count()
    #     total = CompanyData.objects.all().count()



    labels = ['Yes','No']
    values = [Yes_aboriginal, No_aboriginal]
    colors = [colour2, colour3]

        # hole_info 
    hole_info = ((Yes_aboriginal*100)/total)
    hole_info = str(round(hole_info))+str('%')
    print(hole_info)


            # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
    fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='#F4F9FA',
        annotations=[ 
        dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
        dict(text='Aboriginal', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
         )
    
    
    fig.update_traces(textinfo='none')
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config, default_height='175')#, default_width='150')

    return chart, hole_info

def disability_donut_industrychart():
    # if filter=='all':
    Yes_disability = CompanyData.objects.filter(person_with_disabilities='Y').count()
    No_disability = CompanyData.objects.filter(person_with_disabilities='N').count()
    total = CompanyData.objects.all().count()
    # else:
    #     Yes_disability = CompanyData.objects.filter(person_with_disabilities='Y', size=filter).count()
    #     No_disability = CompanyData.objects.filter(person_with_disabilities='N', size=filter).count()
    #     total = CompanyData.objects.all().count()




    labels = ['Yes','No']
    values = [Yes_disability, No_disability]
    colors = [colour2, colour3]

        # hole_info
    hole_info = ((Yes_disability*100)/total)
    hole_info = str(round(hole_info))+str('%')
    print(hole_info)


            # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
    fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='#F4F9FA',
        annotations=[ 
        dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
        dict(text='Yes', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
         )
    
    
    fig.update_traces(textinfo='none')
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config, default_height='175')#, default_width='150')

    return chart, hole_info

#Company data donut charts
 
def Companydata_sex_donut_industrychart(company):
    male = CompanyData.objects.filter(gender_code='M', name=company).count()
    female = CompanyData.objects.filter(gender_code='F', name=company).count()
    other = CompanyData.objects.filter(gender_code='O', name=company).count()
    total = CompanyData.objects.filter(name=company).count()


    labels = ['Male','Female','Other']
    values = [male, female, other]
    colors = [colour1, colour2, colour3]

        # hole_info 
    hole_info = ((female*100)/total)
    hole_info = str(round(hole_info))+str('%')
    print(hole_info)


            # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
    fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
        annotations=[ 
        dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
        dict(text='Female', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
         )
    
    
    fig.update_traces(textinfo='none')
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config, default_height='175')#, default_width='150')

    return chart, hole_info


def Companydata_minority_donut_industrychart(company):
    Yes_minority = CompanyData.objects.filter(visible_minorities='Y', name=company).count()
    No_minority = CompanyData.objects.filter(visible_minorities='N', name=company).count()
    total = CompanyData.objects.filter(name=company).count()


    labels = ['Yes','No']
    values = [Yes_minority, No_minority]
    colors = [colour2, colour3]

        # hole_info
    hole_info = ((Yes_minority*100)/total)
    hole_info = str(round(hole_info))+str('%')


            # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
    fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
        annotations=[ 
        dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
        dict(text='Minority', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
         )

    
    fig.update_traces(textinfo='none')
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config, default_height='175')#, default_width='150')

    return chart, hole_info


def Companydata_aboriginal_donut_industrychart(company):
    Yes_aboriginal = CompanyData.objects.filter(aboriginal_peoples='Y', name=company).count()
    No_aboriginal = CompanyData.objects.filter(aboriginal_peoples='N', name=company).count()
    total = CompanyData.objects.filter(name=company).count()


    labels = ['Yes','No']
    values = [Yes_aboriginal, No_aboriginal]
    colors = [colour2, colour3]

        # hole_info
    hole_info = ((Yes_aboriginal*100)/total)
    hole_info = str(round(hole_info))+str('%')


            # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
    fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
        annotations=[ 
        dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
        dict(text='Aboriginal', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
         )
    
    # hole_info = ((female*100)/total) + str('%')
    hole_info = ((Yes_aboriginal*100)/total)
    hole_info = str(round(hole_info))+str('%')
    
    fig.update_traces(textinfo='none')
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config, default_height='175')#, default_width='150')

    return chart, hole_info

def Companydata_disability_donut_industrychart(company):
    Yes_disability = CompanyData.objects.filter(person_with_disabilities='Y', name=company).count()
    No_disability = CompanyData.objects.filter(person_with_disabilities='N', name=company).count()
    total = CompanyData.objects.filter(name=company).count()


    labels = ['Yes','No']
    values = [Yes_disability, No_disability]
    colors = [colour2, colour3]

        # hole_info 
    hole_info = ((Yes_disability*100)/total)
    hole_info = str(round(hole_info))+str('%')

            # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
    fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
        annotations=[ 
        dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
        dict(text='Yes', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
         )

    
    fig.update_traces(textinfo='none')
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config, default_height='175')#, default_width='150')

    return chart, hole_info


#chart colours
# colour1 = '#2789AB' #blueformale
# colour2 = '#8ACAD8' #blueforfemale#noforVisivleminority#noaboriginal#nodisabilitie
# colour3 = '#F6CB7F' #othersexamarillo

#BAR CHARTS
#PX.BAR test
def sex_barchart_industrychart(position, cheight):
    male_position = CompanyData.objects.filter(gender_code='M', position_category=position).count()
    female_position = CompanyData.objects.filter(gender_code='F', position_category=position).count()
    other_position = CompanyData.objects.filter(gender_code='O', position_category=position).count()

    fig = go.Figure()
    fig.add_trace(go.Bar(y=[position], x=[male_position], name='M', orientation='h', marker=dict(color=colour1), hovertemplate=male_position))
    fig.add_trace(go.Bar(y=[position], x=[female_position], name='F', orientation='h', marker=dict(color=colour2), hovertemplate=female_position))
    fig.add_trace(go.Bar(y=[position], x=[other_position], name='0', orientation='h', marker=dict(color=colour3), hovertemplate=other_position))

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),

        barmode='stack',
        plot_bgcolor='#F4F9FA',
        paper_bgcolor='#F4F9FA',
        margin=dict(l=0, r=5, t=0, b=0, pad=0),
        showlegend=False,
        # width=410,
        height=cheight,

        autosize=True,
        #hoverlabel={'position':False}, 

        
         )


    
    # fig.update_traces(text='none')
    config = {'displayModeBar': False}
    # chart = fig.to_html(config=config, default_width='220', default_height='24')
    chart = fig.to_html(config=config)#, default_width='175', default_height='24')
    return chart

#PX.BAR test



# def sex_barchart_industrychart(position):
#     male_position = CompanyData.objects.filter(gender_code='M', position_category=position).count()
#     female_position = CompanyData.objects.filter(gender_code='F', position_category=position).count()
#     other_position = CompanyData.objects.filter(gender_code='O', position_category=position).count()

#     fig = go.Figure()
#     fig.add_trace(go.Bar(y=[position], x=[male_position], name='M', orientation='h', marker=dict(color=colour1)))
#     fig.add_trace(go.Bar(y=[position], x=[female_position], name='F', orientation='h', marker=dict(color=colour2)))
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[other_position],
#         name='0',
#         orientation='h',
#         marker=dict(
#             color=colour3,
#         )
#     ))

#     fig.update_layout(
#         xaxis=dict(
#             showgrid=False,
#             showline=False,
#             showticklabels=False,
#             zeroline=False,
#             domain=[0, 1]
#         ),
#         yaxis=dict(
#             showgrid=False,
#             showline=False,
#             showticklabels=False,
#             zeroline=False,
#         ),

#         barmode='stack',
#         plot_bgcolor='#F4F9FA',
#         paper_bgcolor='#F4F9FA',
#         margin=dict(l=0, r=0, t=0, b=0, pad=0),
#         showlegend=False,

#         autosize=True, 
#          )


    
#     # fig.update_traces(text='none')
#     config = {'displayModeBar': False}
#     # chart = fig.to_html(config=config, default_width='220', default_height='24')
#     chart = fig.to_html(config=config, default_width='175', default_height='24')
#     return chart


def minority_barchart_industrychart(position, cheight):
    Yes_minority_executive = CompanyData.objects.filter(visible_minorities='Y', position_category=position).count()
    No_minority_executive = CompanyData.objects.filter(visible_minorities='N', position_category=position).count()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=[position],
        x=[Yes_minority_executive],
        name='Y',
        orientation='h',
        marker=dict(
            color=colour2,
        ), 
        hovertemplate=Yes_minority_executive,
    ))
    fig.add_trace(go.Bar(
        y=[position],
        x=[No_minority_executive],
        name='N',
        orientation='h',
        marker=dict(
            color=colour3,
        ), 
        hovertemplate=No_minority_executive,
    ))

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),

        barmode='stack',
        plot_bgcolor='#F4F9FA',
        paper_bgcolor='#F4F9FA',
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        #width=450,
        height=cheight,
        autosize=True,
    )
    # fig.update_traces(text='none')
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config)#, default_width='175', default_height='24')

    return chart

def aboriginal_barchart_industrychart(position, cheight):
    Yes_aboriginal_executive = CompanyData.objects.filter(aboriginal_peoples='Y', position_category=position).count()
    No_aboriginal_executive = CompanyData.objects.filter(aboriginal_peoples='N', position_category=position).count()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=[position],
        x=[Yes_aboriginal_executive],
        name='Y',
        orientation='h',
        marker=dict(
            color=colour2,
        ), 
        hovertemplate=Yes_aboriginal_executive,
    ))
    fig.add_trace(go.Bar(
        y=[position],
        x=[No_aboriginal_executive],
        name='N',
        orientation='h',
        marker=dict(
            color=colour3,
        ), 
        hovertemplate=No_aboriginal_executive,
    ))

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),

        barmode='stack',
        plot_bgcolor='#F4F9FA',
        paper_bgcolor='#F4F9FA',
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        #width=450,
        height=cheight,
        autosize=True,
    )
    # fig.update_traces(text='none')
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config)#, default_width='175', default_height='24')

    return chart

def disability_barchart_industrychart(position, cheight):
    Yes_disability = CompanyData.objects.filter(person_with_disabilities='Y', position_category=position).count()
    No_disability = CompanyData.objects.filter(person_with_disabilities='N', position_category=position).count()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=[position],
        x=[Yes_disability],
        name='Y',
        orientation='h',
        marker=dict(
            color=colour2,
        ), 
        hovertemplate=Yes_disability,
    ))
    fig.add_trace(go.Bar(
        y=[position],
        x=[No_disability],
        name='N',
        orientation='h',
        marker=dict(
            color=colour3,
        ), 
        hovertemplate=No_disability,
    ))

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),

        barmode='stack',
        plot_bgcolor='#F4F9FA',
        paper_bgcolor='#F4F9FA',
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        #width=450,
        height=cheight,
        autosize=True,
    )
    # fig.update_traces(text='none')
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config)#, default_width='175', default_height='24')

    return chart



#COMPANY BAR CHARTS 

def c_sex_barchart_industrychart(position, company, cheight):
    male_position = CompanyData.objects.filter(gender_code='M', position_category=position, name=company).count()
    female_position = CompanyData.objects.filter(gender_code='F', position_category=position, name=company).count()
    other_position = CompanyData.objects.filter(gender_code='O', position_category=position, name=company).count()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=[position],
        x=[male_position],
        name='M',
        orientation='h',
        marker=dict(
            color=colour1,
        ), 
        hovertemplate=male_position,
    ))
    fig.add_trace(go.Bar(
        y=[position],
        x=[female_position],
        name='F',
        orientation='h',
        marker=dict(
            color=colour2,
        ), 
        hovertemplate=female_position,
    ))
    fig.add_trace(go.Bar(
        y=[position],
        x=[other_position],
        name='0',
        orientation='h',
        marker=dict(
            color=colour3,
        ), 
        hovertemplate=other_position,
    ))

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),

        barmode='stack',
        plot_bgcolor='#F4F9FA',
        paper_bgcolor='#F4F9FA',
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        #width=450,
        height=cheight,
        autosize=True,
    )
    # fig.update_traces(text='none')
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config)#, default_width='175', default_height='24')

    return chart


def c_minority_barchart_industrychart(position, company, cheight):
    Yes_minority_executive = CompanyData.objects.filter(visible_minorities='Y', position_category=position, name=company).count()
    No_minority_executive = CompanyData.objects.filter(visible_minorities='N', position_category=position, name=company).count()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=[position],
        x=[Yes_minority_executive],
        name='Y',
        orientation='h',
        marker=dict(
            color=colour2,
        ), 
        hovertemplate=Yes_minority_executive,
    ))
    fig.add_trace(go.Bar(
        y=[position],
        x=[No_minority_executive],
        name='N',
        orientation='h',
        marker=dict(
            color=colour3,
        ), 
        hovertemplate=No_minority_executive,
    ))

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),

        barmode='stack',
        plot_bgcolor='#F4F9FA',
        paper_bgcolor='#F4F9FA',
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        #width=450,
        height=cheight,
        autosize=True,
    )
    # fig.update_traces(text='none')
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config)#, default_width='175', default_height='24')

    return chart

def c_aboriginal_barchart_industrychart(position, company, cheight):
    Yes_aboriginal_executive = CompanyData.objects.filter(aboriginal_peoples='Y', position_category=position, name=company).count()
    No_aboriginal_executive = CompanyData.objects.filter(aboriginal_peoples='N', position_category=position, name=company).count()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=[position],
        x=[Yes_aboriginal_executive],
        name='Y',
        orientation='h',
        marker=dict(
            color=colour2,
        ), 
        hovertemplate=Yes_aboriginal_executive,
    ))
    fig.add_trace(go.Bar(
        y=[position],
        x=[No_aboriginal_executive],
        name='N',
        orientation='h',
        marker=dict(
            color=colour3,
        ), 
        hovertemplate=No_aboriginal_executive,
    ))

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),

        barmode='stack',
        plot_bgcolor='#F4F9FA',
        paper_bgcolor='#F4F9FA',
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        #width=450,
        height=cheight,
        autosize=True,
    )
    # fig.update_traces(text='none')
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config)#, default_width='175', default_height='24')

    return chart

def c_disability_barchart_industrychart(position, company, cheight):
    Yes_disability = CompanyData.objects.filter(person_with_disabilities='Y', position_category=position, name=company).count()
    No_disability = CompanyData.objects.filter(person_with_disabilities='N', position_category=position, name=company).count()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=[position],
        x=[Yes_disability],
        name='Y',
        orientation='h',
        marker=dict(
            color=colour2,
        ), 
        hovertemplate=Yes_disability,
    ))
    fig.add_trace(go.Bar(
        y=[position],
        x=[No_disability],
        name='N',
        orientation='h',
        marker=dict(
            color=colour3,
        ), 
        hovertemplate=No_disability,
    ))

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),

        barmode='stack',
        plot_bgcolor='#F4F9FA',
        paper_bgcolor='#F4F9FA',
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        #width=450,
        height=cheight,
        autosize=True,
    )
    # fig.update_traces(text='none')
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config)#, default_width='175', default_height='24')

    return chart






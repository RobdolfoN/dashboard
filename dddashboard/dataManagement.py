import pathlib

import pandas as pd
from .models import *
import plotly.express as px
import plotly.graph_objects as go
from django.db.models import Count, Q
from django.core.cache import cache
from datetime import datetime, timedelta




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
 
# def sex_donut_industrychart():
#     # if filter=='all':
#     male = CompanyData.objects.filter(gender_code='M').count()
#     female = CompanyData.objects.filter(gender_code='F').count()
#     other = CompanyData.objects.filter(gender_code='O').count()
#     total = CompanyData.objects.all().count()
#     # else:
#     #     male = CompanyData.objects.filter(gender_code='M', size=filter).count()
#     #     female = CompanyData.objects.filter(gender_code='F', size=filter).count()
#     #     other = CompanyData.objects.filter(gender_code='O', size=filter).count()
#     #     total = CompanyData.objects.all().count()


#     labels = ['Male','Female','Other']
#     values = [male, female, other]
#     colors = [colour1, colour2, colour3]

#     hole_info = ((female*100)/total)
#     hole_info = str(round(hole_info))+str('%')

#             # Use `hole` to create a donut-like pie chart
#     fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
#     fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
#         annotations=[ 
#         dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
#         dict(text='Female', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
#          )
    
#     fig.update_traces(textinfo='none')
#     config = {'displayModeBar': False}

#     chart = fig.to_html(config=config, default_height='175')#, default_width='150')

#     return chart, hole_info


# def minority_donut_industrychart():
    
#     Yes_minority = CompanyData.objects.filter(visible_minorities='Y').count()
#     No_minority = CompanyData.objects.filter(visible_minorities='N').count()
#     total = CompanyData.objects.all().count()



#     labels = ['Yes','No']
#     values = [Yes_minority, No_minority]
#     colors = [colour2, colour3]

#         # hole_info
#     hole_info = ((Yes_minority*100)/total)
#     hole_info = str(round(hole_info))+str('%')
    

#             # Use `hole` to create a donut-like pie chart
#     fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.55, marker = dict(colors= colors), automargin=True)])
#     fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
#         annotations=[ 
#         dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
#         dict(text='Minority', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
#          )

#     fig.update_traces(textinfo='none')
#     config = {'displayModeBar': False }
#     chart = fig.to_html(config=config, default_height='175')#, default_width='150')

#     return chart, hole_info


# def aboriginal_donut_industrychart():
#     # if filter=='all':
#     Yes_aboriginal = CompanyData.objects.filter(aboriginal_peoples='Y').count()
#     No_aboriginal = CompanyData.objects.filter(aboriginal_peoples='N').count()
#     total = CompanyData.objects.all().count()
#     # else: 
#     #     Yes_aboriginal = CompanyData.objects.filter(aboriginal_peoples='Y', size=filter).count()
#     #     No_aboriginal = CompanyData.objects.filter(aboriginal_peoples='N', size=filter).count()
#     #     total = CompanyData.objects.all().count()



#     labels = ['Yes','No']
#     values = [Yes_aboriginal, No_aboriginal]
#     colors = [colour2, colour3]

#         # hole_info 
#     hole_info = ((Yes_aboriginal*100)/total)
#     hole_info = str(round(hole_info))+str('%')
#     print(hole_info)


#             # Use `hole` to create a donut-like pie chart
#     fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
#     fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='#F4F9FA',
#         annotations=[ 
#         dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
#         dict(text='Aboriginal', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
#          )
    
    
#     fig.update_traces(textinfo='none')
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config, default_height='175')#, default_width='150')

#     return chart, hole_info

# def disability_donut_industrychart():
#     # if filter=='all':
#     Yes_disability = CompanyData.objects.filter(person_with_disabilities='Y').count()
#     No_disability = CompanyData.objects.filter(person_with_disabilities='N').count()
#     total = CompanyData.objects.all().count()
#     # else:
#     #     Yes_disability = CompanyData.objects.filter(person_with_disabilities='Y', size=filter).count()
#     #     No_disability = CompanyData.objects.filter(person_with_disabilities='N', size=filter).count()
#     #     total = CompanyData.objects.all().count()




#     labels = ['Yes','No']
#     values = [Yes_disability, No_disability]
#     colors = [colour2, colour3]

#         # hole_info
#     hole_info = ((Yes_disability*100)/total)
#     hole_info = str(round(hole_info))+str('%')
#     print(hole_info)


#             # Use `hole` to create a donut-like pie chart
#     fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
#     fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='#F4F9FA',
#         annotations=[ 
#         dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
#         dict(text='Yes', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
#          )
    
    
#     fig.update_traces(textinfo='none')
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config, default_height='175')#, default_width='150')

#     return chart, hole_info

#Company data donut charts

# def create_donut_chart(category, category_field, labels, colors, hole_info_text):
#     """
#     Creates a donut chart for the given category

#     Args:
#     category (str): The name of the category for the chart (e.g. 'Disability')
#     category_field (str): The field of the CompanyData object to filter on (e.g. 'person_with_disabilities')
#     labels (list of str): The labels for the chart's segments
#     colors (list of str): The colors for the chart's segments
#     hole_info_text (str): The text to be displayed in the center of the chart

#     Returns:
#     tuple: containing chart data in html format and hole_info
#     """
#     # filter the data and count the number of items that match the filter
#     data = {}
#     for label, value in zip(labels, ['Y', 'N', 'O']):
#         data[label] = CompanyData.objects.filter(**{category_field: value}).count()
#     total = CompanyData.objects.all().count()

#     # calculate the percentage of the hole_info
#     hole_info = ((data[hole_info_text]*100)/total)
#     hole_info = str(round(hole_info))+str('%')

#     # Create the donut chart
#     fig = go.Figure(data=[go.Pie(labels=labels, values=list(data.values()), hole=.6, marker = dict(colors= colors))])
#     fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
#         annotations=[ 
#         dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
#         dict(text=hole_info_text, x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
#          )
#     fig.update_traces(textinfo='none')
#     config = {'displayModeBar': False}

#     chart = fig.to_html(config=config, default_height='175')#, default_width='150')

#     return chart, hole_info


# def disability_donut_industrychart():
#     labels = ['Yes','No']
#     colors = [colour2, colour3]
#     return create_donut_chart("Disability", "person_with_disabilities", labels, colors, "Yes")

# def sex_donut_industrychart():
#     labels = ['Male','Female','Other']
#     colors = [colour1, colour2, colour3]
#     return create_donut_chart("Sex", "gender_code", labels, colors, "Female")

# def minority_donut_industrychart():
#     labels = ['Yes','No']
#     colors = [colour2, colour3]
#     return create_donut_chart("Minority", "visible_minorities", labels, colors, "Yes")

# def aboriginal_donut_industrychart():
#     labels = ['Yes','No']
#     colors = [colour2, colour3]
#     return create_donut_chart('Aboriginal', "aboriginal_peoples", labels, colors, "Yes")

 ###########  DEPRECATED 2023_01_19 (IT WORKS!) ###################
# def Companydata_sex_donut_industrychart(company):
#     male = CompanyData.objects.filter(gender_code='M', name=company).count()
#     female = CompanyData.objects.filter(gender_code='F', name=company).count()
#     other = CompanyData.objects.filter(gender_code='O', name=company).count()
#     total = CompanyData.objects.filter(name=company).count()


#     labels = ['Male','Female','Other']
#     values = [male, female, other]
#     colors = [colour1, colour2, colour3]

#         # hole_info 
#     hole_info = ((female*100)/total)
#     hole_info = str(round(hole_info))+str('%')
#     print(hole_info)


#             # Use `hole` to create a donut-like pie chart
#     fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
#     fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
#         annotations=[ 
#         dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
#         dict(text='Female', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
#          )
    
    
#     fig.update_traces(textinfo='none')
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config, default_height='175')#, default_width='150')

#     return chart, hole_info
###################################################################

# def Companydata_minority_donut_industrychart(company):
#     Yes_minority = CompanyData.objects.filter(visible_minorities='Y', name=company).count()
#     No_minority = CompanyData.objects.filter(visible_minorities='N', name=company).count()
#     total = CompanyData.objects.filter(name=company).count()


#     labels = ['Yes','No']
#     values = [Yes_minority, No_minority]
#     colors = [colour2, colour3]

#         # hole_info
#     hole_info = ((Yes_minority*100)/total)
#     hole_info = str(round(hole_info))+str('%')


#             # Use `hole` to create a donut-like pie chart
#     fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
#     fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
#         annotations=[ 
#         dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
#         dict(text='Minority', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
#          )

    
#     fig.update_traces(textinfo='none')
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config, default_height='175')#, default_width='150')

#     return chart, hole_info


# def Companydata_aboriginal_donut_industrychart(company):
#     Yes_aboriginal = CompanyData.objects.filter(aboriginal_peoples='Y', name=company).count()
#     No_aboriginal = CompanyData.objects.filter(aboriginal_peoples='N', name=company).count()
#     total = CompanyData.objects.filter(name=company).count()


#     labels = ['Yes','No']
#     values = [Yes_aboriginal, No_aboriginal]
#     colors = [colour2, colour3]

#         # hole_info
#     hole_info = ((Yes_aboriginal*100)/total)
#     hole_info = str(round(hole_info))+str('%')


#             # Use `hole` to create a donut-like pie chart
#     fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
#     fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
#         annotations=[ 
#         dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
#         dict(text='Aboriginal', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
#          )
    
#     # hole_info = ((female*100)/total) + str('%')
#     hole_info = ((Yes_aboriginal*100)/total)
#     hole_info = str(round(hole_info))+str('%')
    
#     fig.update_traces(textinfo='none')
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config, default_height='175')#, default_width='150')

#     return chart, hole_info

# def Companydata_disability_donut_industrychart(company):
#     Yes_disability = CompanyData.objects.filter(person_with_disabilities='Y', name=company).count()
#     No_disability = CompanyData.objects.filter(person_with_disabilities='N', name=company).count()
#     total = CompanyData.objects.filter(name=company).count()


#     labels = ['Yes','No']
#     values = [Yes_disability, No_disability]
#     colors = [colour2, colour3]

#         # hole_info 
#     hole_info = ((Yes_disability*100)/total)
#     hole_info = str(round(hole_info))+str('%')

#             # Use `hole` to create a donut-like pie chart
#     fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
#     fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
#         annotations=[ 
#         dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
#         dict(text='Yes', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
#          )

    
#     fig.update_traces(textinfo='none')
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config, default_height='175')#, default_width='150')

#     return chart, hole_info

##### Company Specific Donut Chart GPT optimized ####


####################### DEPRECATED 2023_01_19 (IT WORKS!) ###############################
# def Companydata_create_donut_chart(field_name, company):
#     # Get the count of 'Y' and 'N' values for the field
#     data = CompanyData.objects.filter(name=company).values(field_name).annotate(count=Count(field_name))
#     yes_count = next((item for item in data if item[field_name] == 'Y'), {'count': 0})['count']
#     no_count = next((item for item in data if item[field_name] == 'N'), {'count': 0})['count']
#     total = yes_count + no_count

#     labels = ['Yes','No']
#     values = [yes_count, no_count]
#     colors = [colour2, colour3]

#     # hole_info
#     hole_info = ((yes_count*100)/total)
#     hole_info = str(round(hole_info)) + '%'

#     # Create the donut chart
#     fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors=colors))])
#     fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
#         annotations=[ 
#         dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
#         dict(text='Yes', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
#          )

#     # Disable hover text
#     fig.update_traces(textinfo='none')
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config, default_height='175')

#     return chart, hole_info
# ###########################################################################################


##### Company Specific Donut Chart GPT optimized ####






#chart colours
# colour1 = '#2789AB' #blueformale
# colour2 = '#8ACAD8' #blueforfemale#noforVisivleminority#noaboriginal#nodisabilitie
# colour3 = '#F6CB7F' #othersexamarillo

#BAR CHARTS


# def sex_barchart_industrychart(position, cheight):
#     male_position = CompanyData.objects.filter(gender_code='M', position_category=position).count()
#     female_position = CompanyData.objects.filter(gender_code='F', position_category=position).count()
#     other_position = CompanyData.objects.filter(gender_code='O', position_category=position).count()

#     fig = go.Figure()
#     fig.add_trace(go.Bar(y=[position], x=[male_position], name='M', orientation='h', marker=dict(color=colour1), hovertemplate=male_position))
#     fig.add_trace(go.Bar(y=[position], x=[female_position], name='F', orientation='h', marker=dict(color=colour2), hovertemplate=female_position))
#     fig.add_trace(go.Bar(y=[position], x=[other_position], name='0', orientation='h', marker=dict(color=colour3), hovertemplate=other_position))

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
#         margin=dict(l=0, r=5, t=0, b=0, pad=0),
#         showlegend=False,
#         # width=410,
#         height=cheight,

#         autosize=True,
#         #hoverlabel={'position':False}, 

        
#          )


    
#     # fig.update_traces(text='none')
#     config = {'displayModeBar': False}
#     # chart = fig.to_html(config=config, default_width='220', default_height='24')
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')
#     return chart

# def minority_barchart_industrychart(position, cheight):
#     Yes_minority_executive = CompanyData.objects.filter(visible_minorities='Y', position_category=position).count()
#     No_minority_executive = CompanyData.objects.filter(visible_minorities='N', position_category=position).count()

#     fig = go.Figure()
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[Yes_minority_executive],
#         name='Y',
#         orientation='h',
#         marker=dict(
#             color=colour2,
#         ), 
#         hovertemplate=Yes_minority_executive,
#     ))
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[No_minority_executive],
#         name='N',
#         orientation='h',
#         marker=dict(
#             color=colour3,
#         ), 
#         hovertemplate=No_minority_executive,
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
#         margin=dict(l=0, r=0, t=0, b=0),
#         showlegend=False,
#         #width=450,
#         height=cheight,
#         autosize=True,
#     )
#     # fig.update_traces(text='none')
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')

#     return chart

# def aboriginal_barchart_industrychart(position, cheight):
#     Yes_aboriginal_executive = CompanyData.objects.filter(aboriginal_peoples='Y', position_category=position).count()
#     No_aboriginal_executive = CompanyData.objects.filter(aboriginal_peoples='N', position_category=position).count()

#     fig = go.Figure()
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[Yes_aboriginal_executive],
#         name='Y',
#         orientation='h',
#         marker=dict(
#             color=colour2,
#         ), 
#         hovertemplate=Yes_aboriginal_executive,
#     ))
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[No_aboriginal_executive],
#         name='N',
#         orientation='h',
#         marker=dict(
#             color=colour3,
#         ), 
#         hovertemplate=No_aboriginal_executive,
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
#         margin=dict(l=0, r=0, t=0, b=0),
#         showlegend=False,
#         #width=450,
#         height=cheight,
#         autosize=True,
#     )
#     # fig.update_traces(text='none')
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')

#     return chart

# def disability_barchart_industrychart(position, cheight):
#     Yes_disability = CompanyData.objects.filter(person_with_disabilities='Y', position_category=position).count()
#     No_disability = CompanyData.objects.filter(person_with_disabilities='N', position_category=position).count()

#     fig = go.Figure()
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[Yes_disability],
#         name='Y',
#         orientation='h',
#         marker=dict(
#             color=colour2,
#         ), 
#         hovertemplate=Yes_disability,
#     ))
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[No_disability],
#         name='N',
#         orientation='h',
#         marker=dict(
#             color=colour3,
#         ), 
#         hovertemplate=No_disability,
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
#         margin=dict(l=0, r=0, t=0, b=0),
#         showlegend=False,
#         #width=450,
#         height=cheight,
#         autosize=True,
#     )
#     # fig.update_traces(text='none')
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')

#     return chart


#### BAR CHARTS GPT OPTIMIZED (OPTION 1) ######


# def sex_barchart_industrychart(position, cheight):
#     male_position = CompanyData.objects.filter(gender_code='M', position_category=position).values('id').count()
#     female_position = CompanyData.objects.filter(gender_code='F', position_category=position).values('id').count()
#     other_position = CompanyData.objects.filter(gender_code='O', position_category=position).values('id').count()

#     fig = go.Figure()
#     fig.add_trace(go.Bar(y=[position], x=[male_position], name='M', orientation='h', marker=dict(color=colour1), hovertemplate=male_position))
#     fig.add_trace(go.Bar(y=[position], x=[female_position], name='F', orientation='h', marker=dict(color=colour2), hovertemplate=female_position))
#     fig.add_trace(go.Bar(y=[position], x=[other_position], name='0', orientation='h', marker=dict(color=colour3), hovertemplate=other_position))

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
#         margin=dict(l=0, r=5, t=0, b=0, pad=0),
#         showlegend=False,
#         # width=410,
#         height=cheight,

#         autosize=True,
#         #hoverlabel={'position':False}, 

        
#          )


    
#     # fig.update_traces(text='none')
#     config = {'displayModeBar': False}
#     # chart = fig.to_html(config=config, default_width='220', default_height='24')
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')
#     return chart

# def minority_barchart_industrychart(position, cheight):
#     Yes_minority_executive = CompanyData.objects.filter(visible_minorities='Y', position_category=position).values('id').count()
#     No_minority_executive = CompanyData.objects.filter(visible_minorities='N', position_category=position).values('id').count()

#     fig = go.Figure()
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[Yes_minority_executive],
#         name='Y',
#         orientation='h',
#         marker=dict(
#             color=colour2,
#         ), 
#         hovertemplate=Yes_minority_executive,
#     ))
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[No_minority_executive],
#         name='N',
#         orientation='h',
#         marker=dict(
#             color=colour3,
#         ), 
#         hovertemplate=No_minority_executive,
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
#         margin=dict(l=0, r=0, t=0, b=0),
#         showlegend=False,
#         #width=450,
#         height=cheight,
#         autosize=True,
#     )
#     # fig.update_traces(text='none')
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')

#     return chart

# def aboriginal_barchart_industrychart(position, cheight):
#     Yes_aboriginal_executive = CompanyData.objects.filter(aboriginal_peoples='Y', position_category=position).values('id').count()
#     No_aboriginal_executive = CompanyData.objects.filter(aboriginal_peoples='N', position_category=position).values('id').count()

#     fig = go.Figure()
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[Yes_aboriginal_executive],
#         name='Y',
#         orientation='h',
#         marker=dict(
#             color=colour2,
#         ), 
#         hovertemplate=Yes_aboriginal_executive,
#     ))
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[No_aboriginal_executive],
#         name='N',
#         orientation='h',
#         marker=dict(
#             color=colour3,
#         ), 
#         hovertemplate=No_aboriginal_executive,
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
#         margin=dict(l=0, r=0, t=0, b=0),
#         showlegend=False,
#         #width=450,
#         height=cheight,
#         autosize=True,
#     )
#     # fig.update_traces(text='none')
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')

#     return chart

# def disability_barchart_industrychart(position, cheight):
#     Yes_disability = CompanyData.objects.filter(person_with_disabilities='Y', position_category=position).values('id').count()
#     No_disability = CompanyData.objects.filter(person_with_disabilities='N', position_category=position).values('id').count()


#     fig = go.Figure()
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[Yes_disability],
#         name='Y',
#         orientation='h',
#         marker=dict(
#             color=colour2,
#         ), 
#         hovertemplate=Yes_disability,
#     ))
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[No_disability],
#         name='N',
#         orientation='h',
#         marker=dict(
#             color=colour3,
#         ), 
#         hovertemplate=No_disability,
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
#         margin=dict(l=0, r=0, t=0, b=0),
#         showlegend=False,
#         #width=450,
#         height=cheight,
#         autosize=True,
#     )
#     # fig.update_traces(text='none')
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')

#     return chart


#### BAR CHARTS GPT OPTIMIZED (OPTION 3 with cache WORKS) ######

# def sex_barchart_industrychart(position, cheight):
#     cache_key = f'sex_chart_{position}'
#     data = cache.get(cache_key)
#     if data is None:
#         male_position = CompanyData.objects.filter(Q(gender_code='M') & Q(position_category=position)).aggregate(Count('id'))['id__count']
#         female_position = CompanyData.objects.filter(Q(gender_code='F') & Q(position_category=position)).aggregate(Count('id'))['id__count']
#         other_position = CompanyData.objects.filter(Q(gender_code='O') & Q(position_category=position)).aggregate(Count('id'))['id__count']
#         data = (male_position, female_position, other_position) 
#         cache.set(cache_key, data, 3600)
#     else:
#         male_position, female_position, other_position = data

    
#     fig = go.Figure()
#     fig.add_trace(go.Bar(y=[position], x=[male_position], name='M', orientation='h', marker=dict(color=colour1), hovertemplate=male_position))
#     fig.add_trace(go.Bar(y=[position], x=[female_position], name='F', orientation='h', marker=dict(color=colour2), hovertemplate=female_position))
#     fig.add_trace(go.Bar(y=[position], x=[other_position], name='0', orientation='h', marker=dict(color=colour3), hovertemplate=other_position))

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
#         margin=dict(l=0, r=5, t=0, b=0, pad=0),
#         showlegend=False,
#         # width=410,
#         height=cheight,

#         autosize=True,
#         #hoverlabel={'position':False}, 

        
#          )


    
#     # fig.update_traces(text='none')
#     config = {'displayModeBar': False}
#     # chart = fig.to_html(config=config, default_width='220', default_height='24')
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')
#     return chart

# def minority_barchart_industrychart(position, cheight):
#     cache_key = f'minority_chart_{position}'
#     data = cache.get(cache_key)
#     if data is None:
#         Yes_minority_executive = CompanyData.objects.filter(Q(visible_minorities='Y') & Q(position_category=position)).aggregate(Count('id'))['id__count']
#         No_minority_executive = CompanyData.objects.filter(Q(visible_minorities='N') & Q(position_category=position)).aggregate(Count('id'))['id__count']
#         data = (Yes_minority_executive, No_minority_executive) 
#         cache.set(cache_key, data, 3600)
#     else:
#         Yes_minority_executive, No_minority_executive = data


#     fig = go.Figure()
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[Yes_minority_executive],
#         name='Y',
#         orientation='h',
#         marker=dict(
#             color=colour2,
#         ), 
#         hovertemplate=Yes_minority_executive,
#     ))
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[No_minority_executive],
#         name='N',
#         orientation='h',
#         marker=dict(
#             color=colour3,
#         ), 
#         hovertemplate=No_minority_executive,
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
#         margin=dict(l=0, r=0, t=0, b=0),
#         showlegend=False,
#         #width=450,
#         height=cheight,
#         autosize=True,
#     )
#     # fig.update_traces(text='none')
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')

#     return chart

# def aboriginal_barchart_industrychart(position, cheight):
#     cache_key = f'aboriginal_chart_{position}'
#     data = cache.get(cache_key)
#     if data is None:
#         Yes_aboriginal_executive = CompanyData.objects.filter(Q(aboriginal_peoples='Y') & Q(position_category=position)).aggregate(Count('id'))['id__count']
#         No_aboriginal_executive = CompanyData.objects.filter(Q(aboriginal_peoples='N') & Q(position_category=position)).aggregate(Count('id'))['id__count']
#         data = (Yes_aboriginal_executive, No_aboriginal_executive) 
#         cache.set(cache_key, data, 3600)
#     else:
#         Yes_aboriginal_executive, No_aboriginal_executive = data



#     fig = go.Figure()
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[Yes_aboriginal_executive],
#         name='Y',
#         orientation='h',
#         marker=dict(
#             color=colour2,
#         ), 
#         hovertemplate=Yes_aboriginal_executive,
#     ))
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[No_aboriginal_executive],
#         name='N',
#         orientation='h',
#         marker=dict(
#             color=colour3,
#         ), 
#         hovertemplate=No_aboriginal_executive,
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
#         margin=dict(l=0, r=0, t=0, b=0),
#         showlegend=False,
#         #width=450,
#         height=cheight,
#         autosize=True,
#     )
#     # fig.update_traces(text='none')
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')

#     return chart

# def disability_barchart_industrychart(position, cheight):
#     cache_key = f'disability_chart_{position}'
#     data = cache.get(cache_key)
#     if data is None:
#         Yes_disability = CompanyData.objects.filter(Q(person_with_disabilities='Y') & Q(position_category=position)).aggregate(Count('id'))['id__count']
#         No_disability = CompanyData.objects.filter(Q(person_with_disabilities='N') & Q(position_category=position)).aggregate(Count('id'))['id__count']
#         data = (Yes_disability, No_disability) 
#         cache.set(cache_key, data, 3600)
#     else:
#         Yes_disability, No_disability = data


#     fig = go.Figure()
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[Yes_disability],
#         name='Y',
#         orientation='h',
#         marker=dict(
#             color=colour2,
#         ), 
#         hovertemplate=Yes_disability,
#     ))
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[No_disability],
#         name='N',
#         orientation='h',
#         marker=dict(
#             color=colour3,
#         ), 
#         hovertemplate=No_disability,
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
#         margin=dict(l=0, r=0, t=0, b=0),
#         showlegend=False,
#         #width=450,
#         height=cheight,
#         autosize=True,
#     )
#     # fig.update_traces(text='none')
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')

#     return chart



#COMPANY BAR CHARTS WORKS 

# def c_sex_barchart_industrychart(position, company, cheight):
        
#     male_position = CompanyData.objects.filter(Q(gender_code='M') & Q(position_category=position) & Q(name=company)).aggregate(Count('id'))['id__count']
#     female_position = CompanyData.objects.filter(Q(gender_code='F') & Q(position_category=position) & Q(name=company)).aggregate(Count('id'))['id__count']
#     other_position = CompanyData.objects.filter(Q(gender_code='O') & Q(position_category=position) & Q(name=company)).aggregate(Count('id'))['id__count']


#     fig = go.Figure()
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[male_position],
#         name='M',
#         orientation='h',
#         marker=dict(
#             color=colour1,
#         ), 
#         hovertemplate=male_position,
#     ))
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[female_position],
#         name='F',
#         orientation='h',
#         marker=dict(
#             color=colour2,
#         ), 
#         hovertemplate=female_position,
#     ))
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[other_position],
#         name='0',
#         orientation='h',
#         marker=dict(
#             color=colour3,
#         ), 
#         hovertemplate=other_position,
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
#         margin=dict(l=0, r=0, t=0, b=0),
#         showlegend=False,
#         #width=450,
#         height=cheight,
#         autosize=True,
#     )
#     # fig.update_traces(text='none')
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')

#     return chart

# def c_minority_barchart_industrychart(position, company, cheight):
#     Yes_minority_executive = CompanyData.objects.filter(Q(visible_minorities='Y') & Q(position_category=position) & Q(name=company)).aggregate(Count('id'))['id__count']
#     No_minority_executive = CompanyData.objects.filter(Q(visible_minorities='N') & Q(position_category=position) & Q(name=company)).aggregate(Count('id'))['id__count']


#     fig = go.Figure()
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[Yes_minority_executive],
#         name='Y',
#         orientation='h',
#         marker=dict(
#             color=colour2,
#         ), 
#         hovertemplate=Yes_minority_executive,
#     ))
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[No_minority_executive],
#         name='N',
#         orientation='h',
#         marker=dict(
#             color=colour3,
#         ), 
#         hovertemplate=No_minority_executive,
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
#         margin=dict(l=0, r=0, t=0, b=0),
#         showlegend=False,
#         #width=450,
#         height=cheight,
#         autosize=True,
#     )
#     # fig.update_traces(text='none')
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')

#     return chart

# def c_aboriginal_barchart_industrychart(position, company, cheight):
#     Yes_aboriginal_executive = CompanyData.objects.filter(Q(aboriginal_peoples='Y') & Q(position_category=position) & Q(name=company)).aggregate(Count('id'))['id__count']
#     No_aboriginal_executive = CompanyData.objects.filter(Q(aboriginal_peoples='N') & Q(position_category=position) & Q(name=company)).aggregate(Count('id'))['id__count']

#     fig = go.Figure()
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[Yes_aboriginal_executive],
#         name='Y',
#         orientation='h',
#         marker=dict(
#             color=colour2,
#         ), 
#         hovertemplate=Yes_aboriginal_executive,
#     ))
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[No_aboriginal_executive],
#         name='N',
#         orientation='h',
#         marker=dict(
#             color=colour3,
#         ), 
#         hovertemplate=No_aboriginal_executive,
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
#         margin=dict(l=0, r=0, t=0, b=0),
#         showlegend=False,
#         #width=450,
#         height=cheight,
#         autosize=True,
#     )
#     # fig.update_traces(text='none')
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')

#     return chart

# def c_disability_barchart_industrychart(position, company, cheight):
#     Yes_disability = CompanyData.objects.filter(Q(person_with_disabilities='Y') & Q(position_category=position) & Q(name=company)).aggregate(Count('id'))['id__count']
#     No_disability = CompanyData.objects.filter(Q(person_with_disabilities='N') & Q(position_category=position) & Q(name=company)).aggregate(Count('id'))['id__count']

#     fig = go.Figure()
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[Yes_disability],
#         name='Y',
#         orientation='h',
#         marker=dict(
#             color=colour2,
#         ), 
#         hovertemplate=Yes_disability,
#     ))
#     fig.add_trace(go.Bar(
#         y=[position],
#         x=[No_disability],
#         name='N',
#         orientation='h',
#         marker=dict(
#             color=colour3,
#         ), 
#         hovertemplate=No_disability,
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
#         margin=dict(l=0, r=0, t=0, b=0),
#         showlegend=False,
#         #width=450,
#         height=cheight,
#         autosize=True,
#     )
#     # fig.update_traces(text='none')
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')

#     return chart


############# DEPRECATED 2023_01_19 (THEY WORK!) #############################


# def customize_chart(fig, cheight):
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
#         margin=dict(l=0, r=0, t=0, b=0),
#         showlegend=False,
#         #width=450,
#         height=cheight,
#         autosize=True,
#     )
    
#     config = {'displayModeBar': False}
#     return fig

# def sex_barchart_industrychart(position, cheight):
#     gender_codes = ['M', 'F', 'O']
#     data = CompanyData.objects.filter(Q(gender_code__in=gender_codes) & Q(position_category=position)).values('gender_code').annotate(count=Count('gender_code'))
    
#     fig = go.Figure()
#     for d in data:
#         fig.add_trace(go.Bar(
#             y=[position],
#             x=[d['count']],
#             name=d['gender_code'],
#             text=d['gender_code'] + ': ' + str(d['count']),
#             textposition='inside',
#             textfont=dict(color='white'),
#             orientation='h',
#             marker=dict(
#                 color=colour1 if d['gender_code'] == 'M' else colour2 if d['gender_code'] == 'F' else colour3,
#             ), 
#             hovertemplate=d['count'],
#         ))
#     customize_chart(fig, cheight)
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')

#     return chart

# def c_sex_barchart_industrychart(position, company, cheight):
#     gender_codes = ['M', 'F', 'O']
#     data = CompanyData.objects.filter(Q(gender_code__in=gender_codes) & Q(position_category=position) & Q(name=company)).values('gender_code').annotate(count=Count('gender_code'))

#     fig = go.Figure()
#     for d in data:
#         fig.add_trace(go.Bar(
#             y=[position],
#             x=[d['count']],
#             name=d['gender_code'],
#             text=d['gender_code'] + ': ' + str(d['count']),
#             textposition='inside',
#             textfont=dict(color='white'),
#             orientation='h',
#             marker=dict(
#                 color=colour1 if d['gender_code'] == 'M' else colour2 if d['gender_code'] == 'F' else colour3,
#             ), 
#             hovertemplate=d['count'],
#         ))
#     customize_chart(fig, cheight)
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')

#     return chart



# def minority_barchart_industrychart(position, cheight):
#     visible_minorities = ['Y', 'N']
#     data = CompanyData.objects.filter(Q(visible_minorities__in=visible_minorities) & Q(position_category=position)).values('visible_minorities').annotate(count=Count('visible_minorities'))

#     fig = go.Figure()
#     for d in data:
#         fig.add_trace(go.Bar(
#             y=[position],
#             x=[d['count']],
#             name=d['visible_minorities'],
#             orientation='h',
#             marker=dict(
#                 color=colour2 if d['visible_minorities'] == 'Y' else colour3,
#             ), 
#             hovertemplate=d['count'],
#         ))
#     customize_chart(fig, cheight)
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')

#     return chart

# def c_minority_barchart_industrychart(position, company, cheight):
#     visible_minorities = ['Y', 'N']
#     data = CompanyData.objects.filter(Q(visible_minorities__in=visible_minorities) & Q(position_category=position) & Q(name=company)).values('visible_minorities').annotate(count=Count('visible_minorities'))

#     fig = go.Figure()
#     for d in data:
#         fig.add_trace(go.Bar(
#             y=[position],
#             x=[d['count']],
#             name=d['visible_minorities'],
#             orientation='h',
#             marker=dict(
#                 color=colour2 if d['visible_minorities'] == 'Y' else colour3,
#             ), 
#             hovertemplate=d['count'],
#         ))
#     customize_chart(fig, cheight)
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')

#     return chart

# def aboriginal_barchart_industrychart(position, cheight):
#     aboriginal_peoples = ['Y', 'N']
#     data = CompanyData.objects.filter(Q(visible_minorities__in=aboriginal_peoples) & Q(position_category=position)).values('aboriginal_peoples').annotate(count=Count('aboriginal_peoples'))

#     fig = go.Figure()
#     for d in data:
#         fig.add_trace(go.Bar(
#             y=[position],
#             x=[d['count']],
#             name=d['aboriginal_peoples'],
#             orientation='h',
#             marker=dict(
#                 color=colour2 if d['aboriginal_peoples'] == 'Y' else colour3,
#             ), 
#             hovertemplate=d['count'],
#         ))
#     customize_chart(fig, cheight)
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')

#     return chart

# def c_aboriginal_barchart_industrychart(position, company, cheight):
#     aboriginal_peoples = ['Y', 'N']
#     data = CompanyData.objects.filter(Q(visible_minorities__in=aboriginal_peoples) & Q(position_category=position) & Q(name=company)).values('aboriginal_peoples').annotate(count=Count('aboriginal_peoples'))

#     fig = go.Figure()
#     for d in data:
#         fig.add_trace(go.Bar(
#             y=[position],
#             x=[d['count']],
#             name=d['aboriginal_peoples'],
#             orientation='h',
#             marker=dict(
#                 color=colour2 if d['aboriginal_peoples'] == 'Y' else colour3,
#             ), 
#             hovertemplate=d['count'],
#         ))
#     customize_chart(fig, cheight)
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')

#     return chart

# def disability_barchart_industrychart(position, cheight):
#     person_with_disabilities = ['Y', 'N']
#     data = CompanyData.objects.filter(Q(visible_minorities__in=person_with_disabilities) & Q(position_category=position)).values('person_with_disabilities').annotate(count=Count('person_with_disabilities'))

#     fig = go.Figure()
#     for d in data:
#         fig.add_trace(go.Bar(
#             y=[position],
#             x=[d['count']],
#             name=d['person_with_disabilities'],
#             orientation='h',
#             marker=dict(
#                 color=colour2 if d['person_with_disabilities'] == 'Y' else colour3,
#             ), 
#             hovertemplate=d['count'],
#         ))
#     customize_chart(fig, cheight)
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')

#     return chart

# def c_disability_barchart_industrychart(position, company, cheight):
#     person_with_disabilities = ['Y', 'N']
#     data = CompanyData.objects.filter(Q(visible_minorities__in=person_with_disabilities) & Q(position_category=position) & Q(name=company)).values('person_with_disabilities').annotate(count=Count('person_with_disabilities'))

#     fig = go.Figure()
#     for d in data:
#         fig.add_trace(go.Bar(
#             y=[position],
#             x=[d['count']],
#             name=d['person_with_disabilities'],
#             orientation='h',
#             marker=dict(
#                 color=colour2 if d['person_with_disabilities'] == 'Y' else colour3,
#             ), 
#             hovertemplate=d['count'],
#         ))
#     customize_chart(fig, cheight)
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')

#     return chart

# ### company size  filter##
# def size_sex_barchart_industrychart(position, size, cheight):
#     gender_codes = ['M', 'F', 'O']
#     data = CompanyData.objects.filter(Q(gender_code__in=gender_codes) & Q(position_category=position) & Q(company_size=size)).values('gender_code').annotate(count=Count('gender_code'))

#     fig = go.Figure()
#     for d in data:
#         fig.add_trace(go.Bar(
#             y=[position],
#             x=[d['count']],
#             name=d['gender_code'],
#             orientation='h',
#             marker=dict(
#                 color=colour1 if d['gender_code'] == 'M' else colour2 if d['gender_code'] == 'F' else colour3,
#             ), 
#             hovertemplate=d['count'],
#         ))
#     customize_chart(fig, cheight)
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')

#     return chart

# def size_minority_barchart_industrychart(position, size, cheight):
#     visible_minorities = ['Y', 'N']
#     data = CompanyData.objects.filter(Q(visible_minorities__in=visible_minorities) & Q(position_category=position) & Q(company_size=size)).values('visible_minorities').annotate(count=Count('visible_minorities'))

#     fig = go.Figure()
#     for d in data:
#         fig.add_trace(go.Bar(
#             y=[position],
#             x=[d['count']],
#             name=d['visible_minorities'],
#             orientation='h',
#             marker=dict(
#                 color=colour2 if d['visible_minorities'] == 'Y' else colour3,
#             ), 
#             hovertemplate=d['count'],
#         ))
#     customize_chart(fig, cheight)
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')

#     return chart

# def size_aboriginal_barchart_industrychart(position, size, cheight):
#     aboriginal_peoples = ['Y', 'N']
#     data = CompanyData.objects.filter(Q(visible_minorities__in=aboriginal_peoples) & Q(position_category=position) & Q(company_size=size)).values('aboriginal_peoples').annotate(count=Count('aboriginal_peoples'))

#     fig = go.Figure()
#     for d in data:
#         fig.add_trace(go.Bar(
#             y=[position],
#             x=[d['count']],
#             name=d['aboriginal_peoples'],
#             orientation='h',
#             marker=dict(
#                 color=colour2 if d['aboriginal_peoples'] == 'Y' else colour3,
#             ), 
#             hovertemplate=d['count'],
#         ))
#     customize_chart(fig, cheight)
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')

#     return chart

# def size_disability_barchart_industrychart(position, size, cheight):
#     person_with_disabilities = ['Y', 'N']
#     data = CompanyData.objects.filter(Q(visible_minorities__in=person_with_disabilities) & Q(position_category=position) & Q(company_size=size)).values('person_with_disabilities').annotate(count=Count('person_with_disabilities'))

#     fig = go.Figure()
#     for d in data:
#         fig.add_trace(go.Bar(
#             y=[position],
#             x=[d['count']],
#             name=d['person_with_disabilities'],
#             orientation='h',
#             marker=dict(
#                 color=colour2 if d['person_with_disabilities'] == 'Y' else colour3,
#             ), 
#             hovertemplate=d['count'],
#         ))
#     customize_chart(fig, cheight)
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config)#, default_width='175', default_height='24')

#     return chart

########################################################################

# def contextCreator(dashboardusercompany):

        

# 	#Industry data donut charts
# 	sex_dchart1, sexchart_hole_info =  sex_donut_industrychart()
# 	minority_dchart1, minority_hole_info =  minority_donut_industrychart()
# 	aboriginal_dchart1, aboriginal_hole_info =  aboriginal_donut_industrychart()
# 	disability_dchart1, disability_hole_info =  disability_donut_industrychart()


# 	Companydata_sex_dchart1, Companydata_sexchart_hole_info =  Companydata_sex_donut_industrychart(dashboardusercompany)
# 	Companydata_minority_dchart1, Companydata_minority_hole_info =  Companydata_create_donut_chart('visible_minorities', dashboardusercompany)
# 	Companydata_aboriginal_dchart1, Companydata_aboriginal_hole_info =  Companydata_create_donut_chart('aboriginal_peoples', dashboardusercompany)
# 	Companydata_disability_dchart1, Companydata_disability_hole_info =  Companydata_create_donut_chart('person_with_disabilities', dashboardusercompany)




# # # INDUSTRY DATA QUERIES
# # 	#SEX DATA PER POSITION
	
# 	sex_executive_barchart = sex_barchart_industrychart('Executive', 24)
# 	sex_senior_leader_barchart = sex_barchart_industrychart('Senior Leader', 24)
# 	sex_manager_s_s_leader_barchart = sex_barchart_industrychart('Manager/Supervisor/Superintendent', 24)
# 	sex_foreperson_leader_barchart = sex_barchart_industrychart('Foreperson', 24)
# 	sex_individual_contributor_leader_barchart = sex_barchart_industrychart('Individual Contributor', 24)

# 	#VISIBLE MINORITY DATA PER POSITION
# 	minority_executive_barchart = minority_barchart_industrychart('Executive', 24)
# 	minority_senior_leader_barchart = minority_barchart_industrychart('Senior Leader', 24)
# 	minority_manager_s_s_leader_barchart = minority_barchart_industrychart('Manager/Supervisor/Superintendent', 24)
# 	minority_foreperson_leader_barchart = minority_barchart_industrychart('Foreperson', 24)
# 	minority_individual_contributor_leader_barchart = minority_barchart_industrychart('Individual Contributor', 24)

# 	#aboriginal DATA PER POSITION
# 	aboriginal_executive_barchart = aboriginal_barchart_industrychart('Executive', 24)
# 	aboriginal_senior_leader_barchart = aboriginal_barchart_industrychart('Senior Leader', 24)
# 	aboriginal_manager_s_s_leader_barchart = aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', 24)
# 	aboriginal_foreperson_leader_barchart = aboriginal_barchart_industrychart('Foreperson', 24)
# 	aboriginal_individual_contributor_leader_barchart = aboriginal_barchart_industrychart('Individual Contributor', 24)

# 	#disabilities DATA PER POSITION
# 	disability_executive_barchart = disability_barchart_industrychart('Executive', 24)
# 	disability_senior_leader_barchart = disability_barchart_industrychart('Senior Leader', 24)
# 	disability_manager_s_s_leader_barchart = disability_barchart_industrychart('Manager/Supervisor/Superintendent', 24)
# 	disability_foreperson_leader_barchart = disability_barchart_industrychart('Foreperson', 24)
# 	disability_individual_contributor_leader_barchart = disability_barchart_industrychart('Individual Contributor', 24)

# # Company DATA QUERIES
# 	#SEX DATA PER POSITION
	
# 	c_sex_executive_barchart = c_sex_barchart_industrychart('Executive', dashboardusercompany, 24)
# 	c_sex_senior_leader_barchart = c_sex_barchart_industrychart('Senior Leader', dashboardusercompany, 24)
# 	c_sex_manager_s_s_leader_barchart = c_sex_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 24)
# 	c_sex_foreperson_leader_barchart = c_sex_barchart_industrychart('Foreperson', dashboardusercompany, 24)
# 	c_sex_individual_contributor_leader_barchart = c_sex_barchart_industrychart('Individual Contributor', dashboardusercompany, 24)

# 	#VISIBLE MINORITY DATA PER POSITION
# 	c_minority_executive_barchart = c_minority_barchart_industrychart('Executive', dashboardusercompany, 24)
# 	c_minority_senior_leader_barchart = c_minority_barchart_industrychart('Senior Leader', dashboardusercompany, 24)
# 	c_minority_manager_s_s_leader_barchart = c_minority_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 24)
# 	c_minority_foreperson_leader_barchart = c_minority_barchart_industrychart('Foreperson', dashboardusercompany, 24)
# 	c_minority_individual_contributor_leader_barchart = c_minority_barchart_industrychart('Individual Contributor', dashboardusercompany, 24)

# 	#aboriginal DATA PER POSITION
# 	c_aboriginal_executive_barchart = c_aboriginal_barchart_industrychart('Executive', dashboardusercompany, 24)
# 	c_aboriginal_senior_leader_barchart = c_aboriginal_barchart_industrychart('Senior Leader', dashboardusercompany, 24)
# 	c_aboriginal_manager_s_s_leader_barchart = c_aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 24)
# 	c_aboriginal_foreperson_leader_barchart = c_aboriginal_barchart_industrychart('Foreperson', dashboardusercompany, 24)
# 	c_aboriginal_individual_contributor_leader_barchart = c_aboriginal_barchart_industrychart('Individual Contributor', dashboardusercompany, 24)

# 	#disabilities DATA PER POSITION
# 	c_disability_executive_barchart = c_disability_barchart_industrychart('Executive', dashboardusercompany, 24)
# 	c_disability_senior_leader_barchart = c_disability_barchart_industrychart('Senior Leader', dashboardusercompany, 24)
# 	c_disability_manager_s_s_leader_barchart = c_disability_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 24)
# 	c_disability_foreperson_leader_barchart = c_disability_barchart_industrychart('Foreperson', dashboardusercompany, 24)
# 	c_disability_individual_contributor_leader_barchart = c_disability_barchart_industrychart('Individual Contributor', dashboardusercompany, 24)




# 	context = {'sex_dchart1': sex_dchart1, 'minority_dchart1':minority_dchart1, 'aboriginal_dchart1':aboriginal_dchart1, 'disability_dchart1':disability_dchart1, 'Companydata_sex_dchart1':Companydata_sex_dchart1, 'Companydata_minority_dchart1':Companydata_minority_dchart1, 'Companydata_aboriginal_dchart1':Companydata_aboriginal_dchart1, 'Companydata_disability_dchart1':Companydata_disability_dchart1,
# 		'sex_executive_barchart':sex_executive_barchart, 'sex_senior_leader_barchart':sex_senior_leader_barchart, 'sex_manager_s_s_leader_barchart':sex_manager_s_s_leader_barchart, 'sex_foreperson_leader_barchart':sex_foreperson_leader_barchart, 'sex_individual_contributor_leader_barchart':sex_individual_contributor_leader_barchart, 'minority_executive_barchart':minority_executive_barchart, 'minority_senior_leader_barchart':minority_senior_leader_barchart, 'minority_manager_s_s_leader_barchart':minority_manager_s_s_leader_barchart, 'minority_foreperson_leader_barchart':minority_foreperson_leader_barchart, 'minority_individual_contributor_leader_barchart':minority_individual_contributor_leader_barchart, 'aboriginal_executive_barchart':aboriginal_executive_barchart, 'aboriginal_senior_leader_barchart':aboriginal_senior_leader_barchart, 'aboriginal_manager_s_s_leader_barchart':aboriginal_manager_s_s_leader_barchart, 'aboriginal_foreperson_leader_barchart':aboriginal_foreperson_leader_barchart, 'aboriginal_individual_contributor_leader_barchart':aboriginal_individual_contributor_leader_barchart, 'disability_executive_barchart':disability_executive_barchart, 'disability_senior_leader_barchart':disability_senior_leader_barchart, 'disability_manager_s_s_leader_barchart':disability_manager_s_s_leader_barchart, 'disability_foreperson_leader_barchart':disability_foreperson_leader_barchart, 'disability_individual_contributor_leader_barchart':disability_individual_contributor_leader_barchart,
# 		'c_sex_executive_barchart':c_sex_executive_barchart, 'c_sex_senior_leader_barchart':c_sex_senior_leader_barchart, 'c_sex_manager_s_s_leader_barchart':c_sex_manager_s_s_leader_barchart, 'c_sex_foreperson_leader_barchart':c_sex_foreperson_leader_barchart, 'c_sex_individual_contributor_leader_barchart':c_sex_individual_contributor_leader_barchart, 'c_minority_executive_barchart':c_minority_executive_barchart, 'c_minority_senior_leader_barchart':c_minority_senior_leader_barchart, 'c_minority_manager_s_s_leader_barchart':c_minority_manager_s_s_leader_barchart, 'c_minority_foreperson_leader_barchart':c_minority_foreperson_leader_barchart, 'c_minority_individual_contributor_leader_barchart':c_minority_individual_contributor_leader_barchart, 'c_aboriginal_executive_barchart':c_aboriginal_executive_barchart, 'c_aboriginal_senior_leader_barchart':c_aboriginal_senior_leader_barchart, 'c_aboriginal_manager_s_s_leader_barchart':c_aboriginal_manager_s_s_leader_barchart, 'c_aboriginal_foreperson_leader_barchart':c_aboriginal_foreperson_leader_barchart, 'c_aboriginal_individual_contributor_leader_barchart':c_aboriginal_individual_contributor_leader_barchart, 'c_disability_executive_barchart':c_disability_executive_barchart, 'c_disability_senior_leader_barchart':c_disability_senior_leader_barchart, 'c_disability_manager_s_s_leader_barchart':c_disability_manager_s_s_leader_barchart, 'c_disability_foreperson_leader_barchart':c_disability_foreperson_leader_barchart, 'c_disability_individual_contributor_leader_barchart':c_disability_individual_contributor_leader_barchart,
# 		}

# 	return context

# def size_Companydata_sex_donut_industrychart(size):
#     male = CompanyData.objects.filter(gender_code='M', company_size=size).count()
#     female = CompanyData.objects.filter(gender_code='F', company_size=size).count()
#     other = CompanyData.objects.filter(gender_code='O', company_size=size).count()
#     total = CompanyData.objects.filter(name=company).count()


#     labels = ['Male','Female','Other']
#     values = [male, female, other]
#     colors = [colour1, colour2, colour3]

#         # hole_info 
#     hole_info = ((female*100)/total)
#     hole_info = str(round(hole_info))+str('%')
#     print(hole_info)


#             # Use `hole` to create a donut-like pie chart
#     fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
#     fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
#         annotations=[ 
#         dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
#         dict(text='Female', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
#          )
    
    
#     fig.update_traces(textinfo='none')
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config, default_height='175')#, default_width='150')

#     return chart, hole_info

# def size_Companydata_create_donut_chart(field_name, size):
#     # Get the count of 'Y' and 'N' values for the field
#     data = CompanyData.objects.filter(company_size=size).values(field_name).annotate(count=Count(field_name))
#     yes_count = next((item for item in data if item[field_name] == 'Y'), {'count': 0})['count']
#     no_count = next((item for item in data if item[field_name] == 'N'), {'count': 0})['count']
#     total = yes_count + no_count

#     labels = ['Yes','No']
#     values = [yes_count, no_count]
#     colors = [colour2, colour3]

#     # hole_info
#     hole_info = ((yes_count*100)/total)
#     hole_info = str(round(hole_info)) + '%'

#     # Create the donut chart
#     fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors=colors))])
#     fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
#         annotations=[ 
#         dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
#         dict(text='Yes', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
#          )

#     # Disable hover text
#     fig.update_traces(textinfo='none')
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config, default_height='175')

#     return chart, hole_info

############### DEPRECATED 2023_01_19 (THEY WORK!) ################

# def create_donut_chart(category, category_field, labels, colors, hole_info_text):
#     """
#     Creates a donut chart for the given category

#     Args:
#     category (str): The name of the category for the chart (e.g. 'Disability')
#     category_field (str): The field of the CompanyData object to filter on (e.g. 'person_with_disabilities')
#     labels (list of str): The labels for the chart's segments
#     colors (list of str): The colors for the chart's segments
#     hole_info_text (str): The text to be displayed in the center of the chart

#     Returns:
#     tuple: containing chart data in html format and hole_info
#     """
#     # filter the data and count the number of items that match the filter
#     data = {}
#     for label, value in zip(labels, ['Y', 'N', 'O']):
#         data[label] = CompanyData.objects.filter(**{category_field: value}).count()
#     total = CompanyData.objects.all().count()

#     # calculate the percentage of the hole_info
#     hole_info = ((data[hole_info_text]*100)/total)
#     hole_info = str(round(hole_info))+str('%')

#     # Create the donut chart
#     fig = go.Figure(data=[go.Pie(labels=labels, values=list(data.values()), hole=.6, marker = dict(colors= colors))])
#     fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
#         annotations=[ 
#         dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
#         dict(text=hole_info_text, x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
#          )
#     fig.update_traces(textinfo='none')
#     config = {'displayModeBar': False}

#     chart = fig.to_html(config=config, default_height='175')#, default_width='150')

#     return chart, hole_info

# def sex_donut_industrychart():
#     # if filter=='all':
#     male = CompanyData.objects.filter(gender_code='M').count()
#     female = CompanyData.objects.filter(gender_code='F').count()
#     other = CompanyData.objects.filter(gender_code='O').count()
#     total = CompanyData.objects.all().count()
#     # else:
#     #     male = CompanyData.objects.filter(gender_code='M', size=filter).count()
#     #     female = CompanyData.objects.filter(gender_code='F', size=filter).count()
#     #     other = CompanyData.objects.filter(gender_code='O', size=filter).count()
#     #     total = CompanyData.objects.all().count()


#     labels = ['Male','Female','Other']
#     values = [male, female, other]
#     colors = [colour1, colour2, colour3]

#     hole_info = ((female*100)/total)
#     hole_info = str(round(hole_info))+str('%')

#             # Use `hole` to create a donut-like pie chart
#     fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
#     fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
#         annotations=[ 
#         dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
#         dict(text='Female', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
#          )
    
#     fig.update_traces(textinfo='none')
#     config = {'displayModeBar': False}

#     chart = fig.to_html(config=config, default_height='175')#, default_width='150')

#     return chart, hole_info

# def minority_donut_industrychart():
#     labels = ['Yes','No']
#     colors = [colour2, colour3]
#     return create_donut_chart("Minority", "visible_minorities", labels, colors, "Yes")

# def aboriginal_donut_industrychart():
#     labels = ['Yes','No']
#     colors = [colour2, colour3]
#     return create_donut_chart('Aboriginal', "aboriginal_peoples", labels, colors, "Yes")

# def disability_donut_industrychart():
#     labels = ['Yes','No']
#     colors = [colour2, colour3]
#     return create_donut_chart("Disability", "person_with_disabilities", labels, colors, "Yes")


# ############### For Size ##########################

# def size_create_donut_chart(field_name, size):
#     # Get the count of 'Y' and 'N' values for the field
#     data = CompanyData.objects.filter(company_size=size).values(field_name).annotate(count=Count(field_name))
#     yes_count = next((item for item in data if item[field_name] == 'Y'), {'count': 0})['count']
#     no_count = next((item for item in data if item[field_name] == 'N'), {'count': 0})['count']
#     total = yes_count + no_count

#     labels = ['Yes','No']
#     values = [yes_count, no_count]
#     colors = [colour2, colour3]

#     # hole_info
#     hole_info = ((yes_count*100)/total)
#     hole_info = str(round(hole_info)) + '%'

#     # Create the donut chart
#     fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors=colors))])
#     fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
#         annotations=[ 
#         dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
#         dict(text='Yes', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
#          )

#     # Disable hover text
#     fig.update_traces(textinfo='none')
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config, default_height='175')

#     return chart, hole_info

# def size_sex_donut_industrychart(size):
#     male = CompanyData.objects.filter(gender_code='M', company_size=size).count()
#     print(male)
#     female = CompanyData.objects.filter(gender_code='F', company_size=size).count()
#     other = CompanyData.objects.filter(gender_code='O', company_size=size).count()
#     total = CompanyData.objects.filter(company_size=size).count()
#     print(female)
#     print(total)


#     labels = ['Male','Female','Other']
#     values = [male, female, other]
#     colors = [colour1, colour2, colour3]

#         # hole_info 
#     hole_info = ((female*100)/total)
#     hole_info = str(round(hole_info))+str('%')
#     print(hole_info)


#             # Use `hole` to create a donut-like pie chart
#     fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
#     fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
#         annotations=[ 
#         dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
#         dict(text='Female', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
#          )
    
    
#     fig.update_traces(textinfo='none')
#     config = {'displayModeBar': False}
#     chart = fig.to_html(config=config, default_height='175')#, default_width='150')

#     return chart, hole_info


#####################################################

########### FUNCTIONS WITH MostRecentDate FILTER ADDED #########################3

def Companydata_sex_donut_industrychart(company):
    most_recent_date = datetime.now().year
    male = CompanyData.objects.filter(gender_code='M', name=company, year_created=most_recent_date).count()
    female = CompanyData.objects.filter(gender_code='F', name=company, year_created=most_recent_date).count()
    other = CompanyData.objects.filter(gender_code='O', name=company, year_created=most_recent_date).count()
    total = CompanyData.objects.filter(name=company, year_created=most_recent_date).count()


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

def Companydata_create_donut_chart(field_name, company):
    # Get the count of 'Y' and 'N' values for the field
    most_recent_date = datetime.now().year
    data = CompanyData.objects.filter(name=company, year_created=most_recent_date).values(field_name).annotate(count=Count(field_name))
    yes_count = next((item for item in data if item[field_name] == 'Y'), {'count': 0})['count']
    no_count = next((item for item in data if item[field_name] == 'N'), {'count': 0})['count']
    total = yes_count + no_count

    labels = ['Yes','No']
    values = [yes_count, no_count]
    colors = [colour2, colour3]

    # hole_info
    hole_info = ((yes_count*100)/total)
    hole_info = str(round(hole_info)) + '%'

    # Create the donut chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors=colors))])
    fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
        annotations=[ 
        dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
        dict(text='Yes', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
         )

    # Disable hover text
    fig.update_traces(textinfo='none')
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config, default_height='175')

    return chart, hole_info

def customize_chart(fig, cheight):
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
    
    config = {'displayModeBar': False}
    return fig

def sex_barchart_industrychart(position, cheight):
    most_recent_date = datetime.now().year
    gender_codes = ['M', 'F', 'O']
    data = CompanyData.objects.filter(Q(gender_code__in=gender_codes) & Q(position_category=position) & Q(year_created=most_recent_date)).values('gender_code').annotate(count=Count('gender_code'))
    
    fig = go.Figure()
    for d in data:
        fig.add_trace(go.Bar(
            y=[position],
            x=[d['count']],
            name=d['gender_code'],
            text=d['gender_code'] + ': ' + str(d['count']),
            textposition='inside',
            textfont=dict(color='white'),
            orientation='h',
            marker=dict(
                color=colour1 if d['gender_code'] == 'M' else colour2 if d['gender_code'] == 'F' else colour3,
            ), 
            hovertemplate=d['count'],
        ))
    customize_chart(fig, cheight)
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config)#, default_width='175', default_height='24')

    return chart

def c_sex_barchart_industrychart(position, company, cheight):
    most_recent_date = datetime.now().year
    gender_codes = ['M', 'F', 'O']
    data = CompanyData.objects.filter(Q(gender_code__in=gender_codes) & Q(position_category=position) & Q(name=company) & Q(year_created=most_recent_date)).values('gender_code').annotate(count=Count('gender_code'))

    fig = go.Figure()
    for d in data:
        fig.add_trace(go.Bar(
            y=[position],
            x=[d['count']],
            name=d['gender_code'],
            text=d['gender_code'] + ': ' + str(d['count']),
            textposition='inside',
            textfont=dict(color='white'),
            orientation='h',
            marker=dict(
                color=colour1 if d['gender_code'] == 'M' else colour2 if d['gender_code'] == 'F' else colour3,
            ), 
            hovertemplate=d['count'],
        ))
    customize_chart(fig, cheight)
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config)#, default_width='175', default_height='24')

    return chart

def minority_barchart_industrychart(position, cheight):
    most_recent_date = datetime.now().year
    visible_minorities = ['Y', 'N']
    data = CompanyData.objects.filter(Q(visible_minorities__in=visible_minorities) & Q(position_category=position) & Q(year_created=most_recent_date)).values('visible_minorities').annotate(count=Count('visible_minorities'))

    fig = go.Figure()
    for d in data:
        fig.add_trace(go.Bar(
            y=[position],
            x=[d['count']],
            name=d['visible_minorities'],
            text=d['visible_minorities'] + ': ' + str(d['count']),
            textposition='inside',
            textfont=dict(color='white'),
            orientation='h',
            marker=dict(
                color=colour2 if d['visible_minorities'] == 'Y' else colour3,
            ), 
            hovertemplate=d['count'],
        ))
    customize_chart(fig, cheight)
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config)#, default_width='175', default_height='24')

    return chart

def c_minority_barchart_industrychart(position, company, cheight):
    most_recent_date = datetime.now().year
    visible_minorities = ['Y', 'N']
    data = CompanyData.objects.filter(Q(visible_minorities__in=visible_minorities) & Q(position_category=position) & Q(name=company) & Q(year_created=most_recent_date)).values('visible_minorities').annotate(count=Count('visible_minorities'))

    fig = go.Figure()
    for d in data:
        fig.add_trace(go.Bar(
            y=[position],
            x=[d['count']],
            name=d['visible_minorities'],
            text=d['visible_minorities'] + ': ' + str(d['count']),
            textposition='inside',
            textfont=dict(color='white'),
            orientation='h',
            marker=dict(
                color=colour2 if d['visible_minorities'] == 'Y' else colour3,
            ), 
            hovertemplate=d['count'],
        ))
    customize_chart(fig, cheight)
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config)#, default_width='175', default_height='24')

    return chart

def aboriginal_barchart_industrychart(position, cheight):
    most_recent_date = datetime.now().year
    aboriginal_peoples = ['Y', 'N']
    data = CompanyData.objects.filter(Q(visible_minorities__in=aboriginal_peoples) & Q(position_category=position) & Q(year_created=most_recent_date)).values('aboriginal_peoples').annotate(count=Count('aboriginal_peoples'))

    fig = go.Figure()
    for d in data:
        fig.add_trace(go.Bar(
            y=[position],
            x=[d['count']],
            name=d['aboriginal_peoples'],
            text=d['aboriginal_peoples'] + ': ' + str(d['count']),
            textposition='inside',
            textfont=dict(color='white'),

            orientation='h',
            marker=dict(
                color=colour2 if d['aboriginal_peoples'] == 'Y' else colour3,
            ), 
            hovertemplate=d['count'],
        ))
    customize_chart(fig, cheight)
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config)#, default_width='175', default_height='24')

    return chart

def c_aboriginal_barchart_industrychart(position, company, cheight):
    most_recent_date = datetime.now().year
    aboriginal_peoples = ['Y', 'N']
    data = CompanyData.objects.filter(Q(visible_minorities__in=aboriginal_peoples) & Q(position_category=position) & Q(name=company) & Q(year_created=most_recent_date)).values('aboriginal_peoples').annotate(count=Count('aboriginal_peoples'))

    fig = go.Figure()
    for d in data:
        fig.add_trace(go.Bar(
            y=[position],
            x=[d['count']],
            name=d['aboriginal_peoples'],
            text=d['aboriginal_peoples'] + ': ' + str(d['count']),
            textposition='inside',
            textfont=dict(color='white'),

            orientation='h',
            marker=dict(
                color=colour2 if d['aboriginal_peoples'] == 'Y' else colour3,
            ), 
            hovertemplate=d['count'],
        ))
    customize_chart(fig, cheight)
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config)#, default_width='175', default_height='24')

    return chart

def disability_barchart_industrychart(position, cheight):
    most_recent_date = datetime.now().year
    person_with_disabilities = ['Y', 'N']
    data = CompanyData.objects.filter(Q(visible_minorities__in=person_with_disabilities) & Q(position_category=position) & Q(year_created=most_recent_date)).values('person_with_disabilities').annotate(count=Count('person_with_disabilities'))

    fig = go.Figure()
    for d in data:
        fig.add_trace(go.Bar(
            y=[position],
            x=[d['count']],
            name=d['person_with_disabilities'],
            text=d['person_with_disabilities'] + ': ' + str(d['count']),
            textposition='inside',
            textfont=dict(color='white'),

            orientation='h',
            marker=dict(
                color=colour2 if d['person_with_disabilities'] == 'Y' else colour3,
            ), 
            hovertemplate=d['count'],
        ))
    customize_chart(fig, cheight)
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config)#, default_width='175', default_height='24')

    return chart

def c_disability_barchart_industrychart(position, company, cheight):
    most_recent_date = datetime.now().year
    person_with_disabilities = ['Y', 'N']
    data = CompanyData.objects.filter(Q(visible_minorities__in=person_with_disabilities) & Q(position_category=position) & Q(name=company) & Q(year_created=most_recent_date)).values('person_with_disabilities').annotate(count=Count('person_with_disabilities'))

    fig = go.Figure()
    for d in data:
        fig.add_trace(go.Bar(
            y=[position],
            x=[d['count']],
            name=d['person_with_disabilities'],
            text=d['person_with_disabilities'] + ': ' + str(d['count']),
            textposition='inside',
            textfont=dict(color='white'),
            orientation='h',
            marker=dict(
                color=colour2 if d['person_with_disabilities'] == 'Y' else colour3,
            ), 
            hovertemplate=d['count'],
        ))
    customize_chart(fig, cheight)
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config)#, default_width='175', default_height='24')

    return chart

### company size  filter##
def size_sex_barchart_industrychart(position, size, cheight):
    most_recent_date = datetime.now().year
    gender_codes = ['M', 'F', 'O']
    data = CompanyData.objects.filter(Q(gender_code__in=gender_codes) & Q(position_category=position) & Q(company_size=size) & Q(year_created=most_recent_date)).values('gender_code').annotate(count=Count('gender_code'))

    fig = go.Figure()
    for d in data:
        fig.add_trace(go.Bar(
            y=[position],
            x=[d['count']],
            name=d['gender_code'],
            text=d['gender_code'] + ': ' + str(d['count']),
            textposition='inside',
            textfont=dict(color='white'),

            orientation='h',
            marker=dict(
                color=colour1 if d['gender_code'] == 'M' else colour2 if d['gender_code'] == 'F' else colour3,
            ), 
            hovertemplate=d['count'],
        ))
    customize_chart(fig, cheight)
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config)#, default_width='175', default_height='24')

    return chart

def size_minority_barchart_industrychart(position, size, cheight):
    most_recent_date = datetime.now().year
    visible_minorities = ['Y', 'N']
    data = CompanyData.objects.filter(Q(visible_minorities__in=visible_minorities) & Q(position_category=position) & Q(company_size=size) & Q(year_created=most_recent_date)).values('visible_minorities').annotate(count=Count('visible_minorities'))

    fig = go.Figure()
    for d in data:
        fig.add_trace(go.Bar(
            y=[position],
            x=[d['count']],
            name=d['visible_minorities'],
            text=d['visible_minorities'] + ': ' + str(d['count']),
            textposition='inside',
            textfont=dict(color='white'),

            orientation='h',
            marker=dict(
                color=colour2 if d['visible_minorities'] == 'Y' else colour3,
            ), 
            hovertemplate=d['count'],
        ))
    customize_chart(fig, cheight)
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config)#, default_width='175', default_height='24')

    return chart

def size_aboriginal_barchart_industrychart(position, size, cheight):
    most_recent_date = datetime.now().year
    aboriginal_peoples = ['Y', 'N']
    data = CompanyData.objects.filter(Q(visible_minorities__in=aboriginal_peoples) & Q(position_category=position) & Q(company_size=size) & Q(year_created=most_recent_date)).values('aboriginal_peoples').annotate(count=Count('aboriginal_peoples'))

    fig = go.Figure()
    for d in data:
        fig.add_trace(go.Bar(
            y=[position],
            x=[d['count']],
            name=d['aboriginal_peoples'],
            text=d['aboriginal_peoples'] + ': ' + str(d['count']),
            textposition='inside',
            textfont=dict(color='white'),

            orientation='h',
            marker=dict(
                color=colour2 if d['aboriginal_peoples'] == 'Y' else colour3,
            ), 
            hovertemplate=d['count'],
        ))
    customize_chart(fig, cheight)
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config)#, default_width='175', default_height='24')

    return chart

def size_disability_barchart_industrychart(position, size, cheight):
    most_recent_date = datetime.now().year
    person_with_disabilities = ['Y', 'N']
    data = CompanyData.objects.filter(Q(visible_minorities__in=person_with_disabilities) & Q(position_category=position) & Q(company_size=size) & Q(year_created=most_recent_date)).values('person_with_disabilities').annotate(count=Count('person_with_disabilities'))

    fig = go.Figure()
    for d in data:
        fig.add_trace(go.Bar(
            y=[position],
            x=[d['count']],
            name=d['person_with_disabilities'],
            text=d['person_with_disabilities'] + ': ' + str(d['count']),
            textposition='inside',
            textfont=dict(color='white'),

            orientation='h',
            marker=dict(
                color=colour2 if d['person_with_disabilities'] == 'Y' else colour3,
            ), 
            hovertemplate=d['count'],
        ))
    customize_chart(fig, cheight)
    config = {'displayModeBar': False}
    chart = fig.to_html(config=config)#, default_width='175', default_height='24')

    return chart

def size_create_donut_chart(field_name, size):
    # Get the count of 'Y' and 'N' values for the field
    most_recent_date = datetime.now().year
    data = CompanyData.objects.filter(company_size=size, year_created=most_recent_date).values(field_name).annotate(count=Count(field_name))
    yes_count = next((item for item in data if item[field_name] == 'Y'), {'count': 0})['count']
    no_count = next((item for item in data if item[field_name] == 'N'), {'count': 0})['count']
    total = yes_count + no_count

    labels = ['Yes','No']
    values = [yes_count, no_count]
    colors = [colour2, colour3]

    if total is not 0:

        hole_info = ((yes_count*100)/total)
        hole_info = str(round(hole_info)) + '%'

        # Create the donut chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors=colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Yes', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )

        # Disable hover text
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}
        chart = fig.to_html(config=config, default_height='175')

        return chart, hole_info
    
    else:
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors=colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text="0", x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Yes', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )

        # Disable hover text
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}
        chart = fig.to_html(config=config, default_height='175')

        return chart, "0"

def size_sex_donut_industrychart(size):
    most_recent_date = datetime.now().year
    male = CompanyData.objects.filter(gender_code='M', company_size=size, year_created=most_recent_date).count()
    female = CompanyData.objects.filter(gender_code='F', company_size=size, year_created=most_recent_date).count()
    other = CompanyData.objects.filter(gender_code='O', company_size=size, year_created=most_recent_date).count()
    total = CompanyData.objects.filter(company_size=size, year_created=most_recent_date).count()


    labels = ['Male','Female','Other']
    values = [male, female, other]
    colors = [colour1, colour2, colour3]

    if total is not 0: 
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

    else:
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text="0", x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Female', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )
        
        
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}
        chart = fig.to_html(config=config, default_height='175')#, default_width='150')

        return chart, "0"

def create_donut_chart(category, category_field, labels, colors, hole_info_text):
    """
    Creates a donut chart for the given category

    Args:
    category (str): The name of the category for the chart (e.g. 'Disability')
    category_field (str): The field of the CompanyData object to filter on (e.g. 'person_with_disabilities')
    labels (list of str): The labels for the chart's segments
    colors (list of str): The colors for the chart's segments
    hole_info_text (str): The text to be displayed in the center of the chart

    Returns:
    tuple: containing chart data in html format and hole_info
    """
    # filter the data and count the number of items that match the filter
    most_recent_date = datetime.now().year
    data = {}
    for label, value in zip(labels, ['Y', 'N', 'O']):
        data[label] = CompanyData.objects.filter(**{category_field: value}, year_created=most_recent_date).count()
    total = CompanyData.objects.all().count()

    # calculate the percentage of the hole_info
    hole_info = ((data[hole_info_text]*100)/total)
    hole_info = str(round(hole_info))+str('%')

    # Create the donut chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=list(data.values()), hole=.6, marker = dict(colors= colors))])
    fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
        annotations=[ 
        dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
        dict(text=hole_info_text, x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
         )
    fig.update_traces(textinfo='none')
    config = {'displayModeBar': False}

    chart = fig.to_html(config=config, default_height='175')#, default_width='150')

    return chart, hole_info

def sex_donut_industrychart():
    most_recent_date = datetime.now().year
    male = CompanyData.objects.filter(gender_code='M', year_created=most_recent_date).count()
    female = CompanyData.objects.filter(gender_code='F', year_created=most_recent_date).count()
    other = CompanyData.objects.filter(gender_code='O', year_created=most_recent_date).count()
    total = CompanyData.objects.filter(year_created=most_recent_date).count()

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
    labels = ['Yes','No']
    colors = [colour2, colour3]
    return create_donut_chart("Minority", "visible_minorities", labels, colors, "Yes")

def aboriginal_donut_industrychart():
    labels = ['Yes','No']
    colors = [colour2, colour3]
    return create_donut_chart('Aboriginal', "aboriginal_peoples", labels, colors, "Yes")

def disability_donut_industrychart():
    labels = ['Yes','No']
    colors = [colour2, colour3]
    return create_donut_chart("Disability", "person_with_disabilities", labels, colors, "Yes")


############### For Size ##########################








############## DEMOGRAPHIC VARIABLES DATE FILTERED FUNCTIONS _ second most recentd date ###############

def sex_donut_second_mostrecent_industrychart(position):
    most_recent_date = datetime.now().year
    second_most_recent_date = (most_recent_date - 1)
    male = CompanyData.objects.filter(gender_code='M', position_category=position, year_created=second_most_recent_date).count()
    female = CompanyData.objects.filter(gender_code='F', position_category=position, year_created=second_most_recent_date).count()
    other = CompanyData.objects.filter(gender_code='O', position_category=position, year_created=second_most_recent_date).count()
    total = CompanyData.objects.filter(position_category=position, year_created=most_recent_date).count()

    print('second most recent',male)

    labels = ['Male','Female','Other']
    values = [male, female, other]
    colors = [colour1, colour2, colour3]
    
    if total is not 0:

        hole_info = ((female*100)/total)
        hole_info = str(round(hole_info))+str('%')

                # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker = dict(colors= colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text=hole_info, x=0.5, y=0.55, font_size=11, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Female', x=0.5, y=0.47, font_size=9, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )
        
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}

        chart = fig.to_html(config=config, default_height='150')#, default_width='150')
        return chart, second_most_recent_date
    else:
                        # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker = dict(colors= colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text="0", x=0.5, y=0.55, font_size=11, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Female', x=0.5, y=0.47, font_size=9, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )
        
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}

        chart = fig.to_html(config=config, default_height='150')#, default_width='150')


        return chart, second_most_recent_date

def size_sex_donut_second_mostrecent_industrychart(position, size):
    most_recent_date = datetime.now().year
    second_most_recent_date = (most_recent_date - 1)
    male = CompanyData.objects.filter(gender_code='M', position_category=position, year_created=second_most_recent_date, company_size=size).count()
    female = CompanyData.objects.filter(gender_code='F', position_category=position, year_created=second_most_recent_date, company_size=size).count()
    other = CompanyData.objects.filter(gender_code='O', position_category=position, year_created=second_most_recent_date, company_size=size).count()
    total = CompanyData.objects.filter(position_category=position, year_created=most_recent_date).count()

    print('second most recent',male)

    labels = ['Male','Female','Other']
    values = [male, female, other]
    colors = [colour1, colour2, colour3]
    
    if total is not 0:

        hole_info = ((female*100)/total)
        hole_info = str(round(hole_info))+str('%')

                # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker = dict(colors= colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text=hole_info, x=0.5, y=0.55, font_size=11, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Female', x=0.5, y=0.47, font_size=9, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )
        
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}

        chart = fig.to_html(config=config, default_height='150')#, default_width='150')
        return chart, second_most_recent_date
    else:
                        # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker = dict(colors= colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text="0", x=0.5, y=0.55, font_size=11, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Female', x=0.5, y=0.47, font_size=9, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )
        
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}

        chart = fig.to_html(config=config, default_height='150')#, default_width='150')


        return chart, second_most_recent_date


def Companydata_sex_donut_second_mostrecent_industrychart(company, position):
    most_recent_date = datetime.now().year
    second_most_recent_date = (most_recent_date - 1)
    male = CompanyData.objects.filter(gender_code='M', name=company, position_category=position, year_created=second_most_recent_date).count()
    female = CompanyData.objects.filter(gender_code='F', name=company, position_category=position, year_created=second_most_recent_date).count()
    other = CompanyData.objects.filter(gender_code='O', name=company, position_category=position, year_created=second_most_recent_date).count()
    total = CompanyData.objects.filter(name=company, position_category=position, year_created=second_most_recent_date).count()


    labels = ['Male','Female','Other']
    values = [male, female, other]
    colors = [colour1, colour2, colour3]

    if total is not 0:

            # hole_info 
        hole_info = ((female*100)/total)
        hole_info = str(round(hole_info))+str('%')
        print(hole_info)


                # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker = dict(colors= colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text=hole_info, x=0.5, y=0.55, font_size=11, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Female', x=0.5, y=0.47, font_size=9, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )
        
        
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}
        chart = fig.to_html(config=config, default_height='150')#, default_width='150')

        return chart, second_most_recent_date
    
    else:
                        # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, marker = dict(colors= colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text="0", x=0.5, y=0.55, font_size=11, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Female', x=0.5, y=0.47, font_size=9, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )
        
        
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}
        chart = fig.to_html(config=config, default_height='150')#, default_width='150')

        return chart, second_most_recent_date

def size_Companydata_sex_donut_second_mostrecent_industrychart(company, position, size):
    most_recent_date = datetime.now().year
    second_most_recent_date = (most_recent_date - 1)
    male = CompanyData.objects.filter(gender_code='M', name=company, position_category=position, year_created=second_most_recent_date, company_size=size).count()
    female = CompanyData.objects.filter(gender_code='F', name=company, position_category=position, year_created=second_most_recent_date, company_size=size).count()
    other = CompanyData.objects.filter(gender_code='O', name=company, position_category=position, year_created=second_most_recent_date, company_size=size).count()
    total = CompanyData.objects.filter(name=company, position_category=position, year_created=second_most_recent_date).count()


    labels = ['Male','Female','Other']
    values = [male, female, other]
    colors = [colour1, colour2, colour3]

    if total is not 0:

            # hole_info 
        hole_info = ((female*100)/total)
        hole_info = str(round(hole_info))+str('%')
        print(hole_info)


                # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker = dict(colors= colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text=hole_info, x=0.5, y=0.55, font_size=11, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Female', x=0.5, y=0.47, font_size=9, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )
        
        
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}
        chart = fig.to_html(config=config, default_height='150')#, default_width='150')

        return chart, second_most_recent_date
    
    else:
                        # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, marker = dict(colors= colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text="0", x=0.5, y=0.55, font_size=11, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Female', x=0.5, y=0.47, font_size=9, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )
        
        
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}
        chart = fig.to_html(config=config, default_height='150')#, default_width='150')

        return chart, second_most_recent_date


def create_second_mostrecent_donut_chart(position, category, category_field, labels, colors, hole_info_text):
    """
    Creates a donut chart for the given category

    Args:
    category (str): The name of the category for the chart (e.g. 'Disability')
    category_field (str): The field of the CompanyData object to filter on (e.g. 'person_with_disabilities')
    labels (list of str): The labels for the chart's segments
    colors (list of str): The colors for the chart's segments
    hole_info_text (str): The text to be displayed in the center of the chart

    Returns:
    tuple: containing chart data in html format and hole_info
    """
    # filter the data and count the number of items that match the filter
    data = {}
    most_recent_date = datetime.now().year
    second_most_recent_date = (most_recent_date - 1)
    for label, value in zip(labels, ['Y', 'N', 'O']):
        data[label] = CompanyData.objects.filter(**{category_field: value}, year_created=second_most_recent_date, position_category=position).count()
    total = CompanyData.objects.all().count()

    # calculate the percentage of the hole_info
    hole_info = ((data[hole_info_text]*100)/total)
    hole_info = str(round(hole_info))+str('%')

    # Create the donut chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=list(data.values()), hole=.6, marker = dict(colors= colors))])
    fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
        annotations=[ 
        dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
        dict(text=hole_info_text, x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
         )
    fig.update_traces(textinfo='none')
    config = {'displayModeBar': False}

    chart = fig.to_html(config=config, default_height='175')#, default_width='150')

    return chart, second_most_recent_date

def size_create_second_mostrecent_donut_chart(position, category, category_field, labels, colors, hole_info_text, size):
    """
    Creates a donut chart for the given category

    Args:
    category (str): The name of the category for the chart (e.g. 'Disability')
    category_field (str): The field of the CompanyData object to filter on (e.g. 'person_with_disabilities')
    labels (list of str): The labels for the chart's segments
    colors (list of str): The colors for the chart's segments
    hole_info_text (str): The text to be displayed in the center of the chart

    Returns:
    tuple: containing chart data in html format and hole_info
    """
    # filter the data and count the number of items that match the filter
    data = {}
    most_recent_date = datetime.now().year
    second_most_recent_date = (most_recent_date - 1)
    for label, value in zip(labels, ['Y', 'N', 'O']):
        data[label] = CompanyData.objects.filter(**{category_field: value}, year_created=second_most_recent_date, position_category=position).count()
    total = CompanyData.objects.all().count()

    # calculate the percentage of the hole_info
    hole_info = ((data[hole_info_text]*100)/total)
    hole_info = str(round(hole_info))+str('%')

    # Create the donut chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=list(data.values()), hole=.6, marker = dict(colors= colors))])
    fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
        annotations=[ 
        dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
        dict(text=hole_info_text, x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
         )
    fig.update_traces(textinfo='none')
    config = {'displayModeBar': False}

    chart = fig.to_html(config=config, default_height='175')#, default_width='150')

    return chart, second_most_recent_date


def minority_second_mostrecent_donut_industrychart(position):
    labels = ['Yes','No']
    colors = [colour2, colour3]
    return create_second_mostrecent_donut_chart(position, "Minority", "visible_minorities", labels, colors, "Yes")

def aboriginal_second_mostrecent_donut_industrychart(position):
    labels = ['Yes','No']
    colors = [colour2, colour3]
    return create_second_mostrecent_donut_chart(position, 'Aboriginal', "aboriginal_peoples", labels, colors, "Yes")

def disability_second_mostrecent_donut_industrychart(position):
    labels = ['Yes','No']
    colors = [colour2, colour3]
    return create_second_mostrecent_donut_chart(position, "Disability", "person_with_disabilities", labels, colors, "Yes")

def Companydata_create_donut_second_mostrecent_chart(field_name, company, position):
    most_recent_date = datetime.now().year
    second_most_recent_date = (most_recent_date - 1)

    # Get the count of 'Y' and 'N' values for the field
    data = CompanyData.objects.filter(name=company, position_category=position, year_created=second_most_recent_date).values(field_name).annotate(count=Count(field_name))
    yes_count = next((item for item in data if item[field_name] == 'Y'), {'count': 0})['count']
    no_count = next((item for item in data if item[field_name] == 'N'), {'count': 0})['count']
    total = yes_count + no_count

    labels = ['Yes','No']
    values = [yes_count, no_count]
    colors = [colour2, colour3]

    if total is not 0:

        # hole_info
        hole_info = ((yes_count*100)/total)
        hole_info = str(round(hole_info)) + '%'

        # Create the donut chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors=colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Yes', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )

        # Disable hover text
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}
        chart = fig.to_html(config=config, default_height='175')

        return chart, second_most_recent_date
    else:
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors=colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text=0, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Yes', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )

        # Disable hover text
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}
        chart = fig.to_html(config=config, default_height='175')

        return chart, second_most_recent_date





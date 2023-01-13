from .models import *


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

def Companydata_create_donut_chart(field_name, company):
    # Get the count of 'Y' and 'N' values for the field
    data = CompanyData.objects.filter(name=company).values(field_name).annotate(count=Count(field_name))
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

def sex_barchart_industrychart(position, cheight):
    cache_key = f'sex_chart_{position}'
    data = cache.get(cache_key)
    if data is None:
        male_position = CompanyData.objects.filter(Q(gender_code='M') & Q(position_category=position)).aggregate(Count('id'))['id__count']
        female_position = CompanyData.objects.filter(Q(gender_code='F') & Q(position_category=position)).aggregate(Count('id'))['id__count']
        other_position = CompanyData.objects.filter(Q(gender_code='O') & Q(position_category=position)).aggregate(Count('id'))['id__count']
        data = (male_position, female_position, other_position) 
        cache.set(cache_key, data, 3600)
    else:
        male_position, female_position, other_position = data

    
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

def minority_barchart_industrychart(position, cheight):
    cache_key = f'minority_chart_{position}'
    data = cache.get(cache_key)
    if data is None:
        Yes_minority_executive = CompanyData.objects.filter(Q(visible_minorities='Y') & Q(position_category=position)).aggregate(Count('id'))['id__count']
        No_minority_executive = CompanyData.objects.filter(Q(visible_minorities='N') & Q(position_category=position)).aggregate(Count('id'))['id__count']
        data = (Yes_minority_executive, No_minority_executive) 
        cache.set(cache_key, data, 3600)
    else:
        Yes_minority_executive, No_minority_executive = data


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
    cache_key = f'aboriginal_chart_{position}'
    data = cache.get(cache_key)
    if data is None:
        Yes_aboriginal_executive = CompanyData.objects.filter(Q(aboriginal_peoples='Y') & Q(position_category=position)).aggregate(Count('id'))['id__count']
        No_aboriginal_executive = CompanyData.objects.filter(Q(aboriginal_peoples='N') & Q(position_category=position)).aggregate(Count('id'))['id__count']
        data = (Yes_aboriginal_executive, No_aboriginal_executive) 
        cache.set(cache_key, data, 3600)
    else:
        Yes_aboriginal_executive, No_aboriginal_executive = data



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
    cache_key = f'disability_chart_{position}'
    data = cache.get(cache_key)
    if data is None:
        Yes_disability = CompanyData.objects.filter(Q(person_with_disabilities='Y') & Q(position_category=position)).aggregate(Count('id'))['id__count']
        No_disability = CompanyData.objects.filter(Q(person_with_disabilities='N') & Q(position_category=position)).aggregate(Count('id'))['id__count']
        data = (Yes_disability, No_disability) 
        cache.set(cache_key, data, 3600)
    else:
        Yes_disability, No_disability = data


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

def c_sex_barchart_industrychart(position, company, cheight):
    cache_key = f'sex_chart_{position}_{company}'
    data = cache.get(cache_key)
    if data is None:
        
        male_position = CompanyData.objects.filter(Q(gender_code='M') & Q(position_category=position) & Q(name=company)).aggregate(Count('id'))['id__count']
        female_position = CompanyData.objects.filter(Q(gender_code='F') & Q(position_category=position) & Q(name=company)).aggregate(Count('id'))['id__count']
        other_position = CompanyData.objects.filter(Q(gender_code='O') & Q(position_category=position) & Q(name=company)).aggregate(Count('id'))['id__count']

        data = (male_position, female_position, other_position)
        cache.set(cache_key, data, 3600)
    else:
        male_position, female_position, other_position = data



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
    
    cache.set(cache_key, chart)
    return chart

def c_minority_barchart_industrychart(position, company, cheight):
    cache_key = f'minority_chart_{position}_{company}'
    data = cache.get(cache_key)
    if data is None:
        
        Yes_minority_executive = CompanyData.objects.filter(Q(visible_minorities='Y') & Q(position_category=position) & Q(name=company)).aggregate(Count('id'))['id__count']
        No_minority_executive = CompanyData.objects.filter(Q(visible_minorities='N') & Q(position_category=position) & Q(name=company)).aggregate(Count('id'))['id__count']
        data = (Yes_minority_executive, No_minority_executive)    
        cache.set(cache_key, data, 3600)
    else:
        Yes_minority_executive, No_minority_executive = data


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
    
    cache.set(cache_key, chart)
    return chart

def c_aboriginal_barchart_industrychart(position, company, cheight):
    cache_key = f'c_aboriginal_{position}_{company}'
    data = cache.get(cache_key)
    if data is None:

        Yes_aboriginal_executive = CompanyData.objects.filter(Q(aboriginal_peoples='Y') & Q(position_category=position) & Q(name=company)).aggregate(Count('id'))['id__count']
        No_aboriginal_executive = CompanyData.objects.filter(Q(aboriginal_peoples='N') & Q(position_category=position) & Q(name=company)).aggregate(Count('id'))['id__count']
        data = (Yes_aboriginal_executive, No_aboriginal_executive)
        cache.set(cache_key, data)
    else:
        Yes_aboriginal_executive, No_aboriginal_executive = data



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
    
    cache.set(cache_key, chart)
    return chart

def c_disability_barchart_industrychart(position, company, cheight):
    cache_key = f'c_disability_{position}_{company}'
    data = cache.get(cache_key)
    if data is None:
        Yes_disability = CompanyData.objects.filter(Q(person_with_disabilities='Y') & Q(position_category=position) & Q(name=company)).aggregate(Count('id'))['id__count']
        No_disability = CompanyData.objects.filter(Q(person_with_disabilities='N') & Q(position_category=position) & Q(name=company)).aggregate(Count('id'))['id__count']
        data = (Yes_disability, No_disability)
        cache.set(cache_key, data, 3600)
    else:
        Yes_disability, No_disability = data



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
    
    cache.set(cache_key, chart)
    return chart





def contextCreator(dashboardusercompany):

        

	#Industry data donut charts
	sex_dchart1, sexchart_hole_info =  sex_donut_industrychart()
	minority_dchart1, minority_hole_info =  minority_donut_industrychart()
	aboriginal_dchart1, aboriginal_hole_info =  aboriginal_donut_industrychart()
	disability_dchart1, disability_hole_info =  disability_donut_industrychart()


	Companydata_sex_dchart1, Companydata_sexchart_hole_info =  Companydata_sex_donut_industrychart(dashboardusercompany)
	Companydata_minority_dchart1, Companydata_minority_hole_info =  Companydata_create_donut_chart('visible_minorities', dashboardusercompany)
	Companydata_aboriginal_dchart1, Companydata_aboriginal_hole_info =  Companydata_create_donut_chart('aboriginal_peoples', dashboardusercompany)
	Companydata_disability_dchart1, Companydata_disability_hole_info =  Companydata_create_donut_chart('person_with_disabilities', dashboardusercompany)




# # INDUSTRY DATA QUERIES
# 	#SEX DATA PER POSITION
	
	sex_executive_barchart = sex_barchart_industrychart('Executive', 24)
	sex_senior_leader_barchart = sex_barchart_industrychart('Senior Leader', 24)
	sex_manager_s_s_leader_barchart = sex_barchart_industrychart('Manager/Supervisor/Superintendent', 24)
	sex_foreperson_leader_barchart = sex_barchart_industrychart('Foreperson', 24)
	sex_individual_contributor_leader_barchart = sex_barchart_industrychart('Individual Contributor', 24)

	#VISIBLE MINORITY DATA PER POSITION
	minority_executive_barchart = minority_barchart_industrychart('Executive', 24)
	minority_senior_leader_barchart = minority_barchart_industrychart('Senior Leader', 24)
	minority_manager_s_s_leader_barchart = minority_barchart_industrychart('Manager/Supervisor/Superintendent', 24)
	minority_foreperson_leader_barchart = minority_barchart_industrychart('Foreperson', 24)
	minority_individual_contributor_leader_barchart = minority_barchart_industrychart('Individual Contributor', 24)

	#aboriginal DATA PER POSITION
	aboriginal_executive_barchart = aboriginal_barchart_industrychart('Executive', 24)
	aboriginal_senior_leader_barchart = aboriginal_barchart_industrychart('Senior Leader', 24)
	aboriginal_manager_s_s_leader_barchart = aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', 24)
	aboriginal_foreperson_leader_barchart = aboriginal_barchart_industrychart('Foreperson', 24)
	aboriginal_individual_contributor_leader_barchart = aboriginal_barchart_industrychart('Individual Contributor', 24)

	#disabilities DATA PER POSITION
	disability_executive_barchart = disability_barchart_industrychart('Executive', 24)
	disability_senior_leader_barchart = disability_barchart_industrychart('Senior Leader', 24)
	disability_manager_s_s_leader_barchart = disability_barchart_industrychart('Manager/Supervisor/Superintendent', 24)
	disability_foreperson_leader_barchart = disability_barchart_industrychart('Foreperson', 24)
	disability_individual_contributor_leader_barchart = disability_barchart_industrychart('Individual Contributor', 24)

# Company DATA QUERIES
	#SEX DATA PER POSITION
	
	c_sex_executive_barchart = c_sex_barchart_industrychart('Executive', dashboardusercompany, 24)
	c_sex_senior_leader_barchart = c_sex_barchart_industrychart('Senior Leader', dashboardusercompany, 24)
	c_sex_manager_s_s_leader_barchart = c_sex_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 24)
	c_sex_foreperson_leader_barchart = c_sex_barchart_industrychart('Foreperson', dashboardusercompany, 24)
	c_sex_individual_contributor_leader_barchart = c_sex_barchart_industrychart('Individual Contributor', dashboardusercompany, 24)

	#VISIBLE MINORITY DATA PER POSITION
	c_minority_executive_barchart = c_minority_barchart_industrychart('Executive', dashboardusercompany, 24)
	c_minority_senior_leader_barchart = c_minority_barchart_industrychart('Senior Leader', dashboardusercompany, 24)
	c_minority_manager_s_s_leader_barchart = c_minority_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 24)
	c_minority_foreperson_leader_barchart = c_minority_barchart_industrychart('Foreperson', dashboardusercompany, 24)
	c_minority_individual_contributor_leader_barchart = c_minority_barchart_industrychart('Individual Contributor', dashboardusercompany, 24)

	#aboriginal DATA PER POSITION
	c_aboriginal_executive_barchart = c_aboriginal_barchart_industrychart('Executive', dashboardusercompany, 24)
	c_aboriginal_senior_leader_barchart = c_aboriginal_barchart_industrychart('Senior Leader', dashboardusercompany, 24)
	c_aboriginal_manager_s_s_leader_barchart = c_aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 24)
	c_aboriginal_foreperson_leader_barchart = c_aboriginal_barchart_industrychart('Foreperson', dashboardusercompany, 24)
	c_aboriginal_individual_contributor_leader_barchart = c_aboriginal_barchart_industrychart('Individual Contributor', dashboardusercompany, 24)

	#disabilities DATA PER POSITION
	c_disability_executive_barchart = c_disability_barchart_industrychart('Executive', dashboardusercompany, 24)
	c_disability_senior_leader_barchart = c_disability_barchart_industrychart('Senior Leader', dashboardusercompany, 24)
	c_disability_manager_s_s_leader_barchart = c_disability_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 24)
	c_disability_foreperson_leader_barchart = c_disability_barchart_industrychart('Foreperson', dashboardusercompany, 24)
	c_disability_individual_contributor_leader_barchart = c_disability_barchart_industrychart('Individual Contributor', dashboardusercompany, 24)




	context = {'sex_dchart1': sex_dchart1, 'minority_dchart1':minority_dchart1, 'aboriginal_dchart1':aboriginal_dchart1, 'disability_dchart1':disability_dchart1, 'Companydata_sex_dchart1':Companydata_sex_dchart1, 'Companydata_minority_dchart1':Companydata_minority_dchart1, 'Companydata_aboriginal_dchart1':Companydata_aboriginal_dchart1, 'Companydata_disability_dchart1':Companydata_disability_dchart1,
		'sex_executive_barchart':sex_executive_barchart, 'sex_senior_leader_barchart':sex_senior_leader_barchart, 'sex_manager_s_s_leader_barchart':sex_manager_s_s_leader_barchart, 'sex_foreperson_leader_barchart':sex_foreperson_leader_barchart, 'sex_individual_contributor_leader_barchart':sex_individual_contributor_leader_barchart, 'minority_executive_barchart':minority_executive_barchart, 'minority_senior_leader_barchart':minority_senior_leader_barchart, 'minority_manager_s_s_leader_barchart':minority_manager_s_s_leader_barchart, 'minority_foreperson_leader_barchart':minority_foreperson_leader_barchart, 'minority_individual_contributor_leader_barchart':minority_individual_contributor_leader_barchart, 'aboriginal_executive_barchart':aboriginal_executive_barchart, 'aboriginal_senior_leader_barchart':aboriginal_senior_leader_barchart, 'aboriginal_manager_s_s_leader_barchart':aboriginal_manager_s_s_leader_barchart, 'aboriginal_foreperson_leader_barchart':aboriginal_foreperson_leader_barchart, 'aboriginal_individual_contributor_leader_barchart':aboriginal_individual_contributor_leader_barchart, 'disability_executive_barchart':disability_executive_barchart, 'disability_senior_leader_barchart':disability_senior_leader_barchart, 'disability_manager_s_s_leader_barchart':disability_manager_s_s_leader_barchart, 'disability_foreperson_leader_barchart':disability_foreperson_leader_barchart, 'disability_individual_contributor_leader_barchart':disability_individual_contributor_leader_barchart,
		'c_sex_executive_barchart':c_sex_executive_barchart, 'c_sex_senior_leader_barchart':c_sex_senior_leader_barchart, 'c_sex_manager_s_s_leader_barchart':c_sex_manager_s_s_leader_barchart, 'c_sex_foreperson_leader_barchart':c_sex_foreperson_leader_barchart, 'c_sex_individual_contributor_leader_barchart':c_sex_individual_contributor_leader_barchart, 'c_minority_executive_barchart':c_minority_executive_barchart, 'c_minority_senior_leader_barchart':c_minority_senior_leader_barchart, 'c_minority_manager_s_s_leader_barchart':c_minority_manager_s_s_leader_barchart, 'c_minority_foreperson_leader_barchart':c_minority_foreperson_leader_barchart, 'c_minority_individual_contributor_leader_barchart':c_minority_individual_contributor_leader_barchart, 'c_aboriginal_executive_barchart':c_aboriginal_executive_barchart, 'c_aboriginal_senior_leader_barchart':c_aboriginal_senior_leader_barchart, 'c_aboriginal_manager_s_s_leader_barchart':c_aboriginal_manager_s_s_leader_barchart, 'c_aboriginal_foreperson_leader_barchart':c_aboriginal_foreperson_leader_barchart, 'c_aboriginal_individual_contributor_leader_barchart':c_aboriginal_individual_contributor_leader_barchart, 'c_disability_executive_barchart':c_disability_executive_barchart, 'c_disability_senior_leader_barchart':c_disability_senior_leader_barchart, 'c_disability_manager_s_s_leader_barchart':c_disability_manager_s_s_leader_barchart, 'c_disability_foreperson_leader_barchart':c_disability_foreperson_leader_barchart, 'c_disability_individual_contributor_leader_barchart':c_disability_individual_contributor_leader_barchart,
		}

	if request.htmx:
		return render(request, 'partials/chart.html', context)
	return render(request, 'dddashboard/industry.html', context)


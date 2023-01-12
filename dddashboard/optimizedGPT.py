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



	#SEX DATA PER POSITION
	
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

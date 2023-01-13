

def customize_chart(fig):
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

def c_sex_barchart_industrychart(position, company, cheight):
    gender_codes = ['M', 'F', 'O']
    data = CompanyData.objects.filter(Q(gender_code__in=gender_codes) & Q(position_category=position) & Q(name=company)).values('gender_code').annotate(count=Count('gender_code'))

    fig = go.Figure()
    for d in data:
        fig.add_trace(go.Bar(
            y=[position],
            x=[d['count']],
            name=d['gender_code'],
            orientation='h',
            marker=dict(
                color=colour1 if d['gender_code'] == 'M' else colour2 if d['gender_code'] == 'F' else colour3,
            ), 
            hovertemplate=d['count'],
        ))
    customize_chart(fig)
    chart = fig.to_html(config=config)#, default_width='175', default_height='24')

    return chart

sex_executive_barchart = c_sex_barchart_industrychart('Executive', 24)
sex_senior_leader_barchart = c_sex_barchart_industrychart('Senior Leader', 24)
sex_manager_s_s_leader_barchart = c_sex_barchart_industrychart('Manager/Supervisor/Superintendent', 24)
sex_foreperson_leader_barchart = c_sex_barchart_industrychart('Foreperson', 24)
sex_individual_contributor_leader_barchart = c_sex_barchart_industrychart('Individual Contributor', 24)




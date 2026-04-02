import pandas as pd
import datetime as dt 
import plotly.express as px
import plotly.graph_objects as go 
import plotly.colors

data = pd.read_csv('coastal_retail.csv')
data.dropna(subset=['CustomerID'], inplace=True)

data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
data['TotalPrice'] = data['Quantity'] * data['UnitPrice']

reference_date = data['InvoiceDate'].max() + dt.timedelta(days=1) #for irl scenarios, date would be today's date
reference_date

rfm = data.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (reference_date - x.max()).days,
    'InvoiceNo': 'count',
    'TotalPrice': 'sum'
}).reset_index()
rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
rfm.head()

#Define quantiles
quantiles = rfm[['Recency', 'Frequency', 'Monetary']].quantile(q=[0.25, 0.5, 0.75])

#Assign RFM scores
def RScore(x, p, d):
    if p == 'Recency':
        if x <= d[p][0.25]:
            return 4
        elif x <= d[p][0.50]:
            return 3
        elif x <= d[p][0.75]: 
            return 2
        else:
            return 1
    else:
        if x <= d[p][0.25]:
            return 1
        elif x <= d[p][0.50]:
            return 2
        elif x <= d[p][0.75]: 
            return 3
        else:
            return 4
rfm['R'] = rfm['Recency'].apply(RScore, args=('Recency', quantiles))
rfm['F'] = rfm['Frequency'].apply(RScore, args=('Frequency', quantiles))
rfm['M'] = rfm['Monetary'].apply(RScore, args=('Monetary', quantiles))
rfm.head()  

rfm['RFM_Segment'] = rfm['R'].astype(str) + rfm['F'].astype(str) + rfm['M'].astype(str)
rfm['RFM_Score'] = rfm[['R', 'F', 'M']].sum(axis=1)

segment_labels = ['Low Value', 'Mid-Value', 'High Value']

def segment_label(score):
    if score < 5:
        return 'Low Value'
    elif score < 9:
        return 'Mid-Value'
    else:
        return 'High Value' 
rfm['Segment_Label'] = rfm['RFM_Score'].apply(segment_label)
rfm.head()

fig = px.bar(segment_counts, 
                 x='Segment_Label', 
                 y='Count', 
                 title='Customer Segments based on RFM Analysis',
                 labels={'Segment_Label': 'Customer Segment', 'Count': 'Number of Customers'},
                 color='Segment_Label',
                 color_discrete_sequence=plotly.colors.qualitative.Plotly)
fig.show()

rfm['RFM_Customer_Segments'] = ''

rfm.loc[rfm['RFM_Score'] >= 10, 'RFM_Customer_Segments'] = 'VIP'
rfm.loc[(rfm['RFM_Score'] >= 9) & (rfm['RFM_Score'] < 10), 'RFM_Customer_Segments'] = 'Loyal'
rfm.loc[(rfm['RFM_Score'] >= 7) & (rfm['RFM_Score'] < 9), 'RFM_Customer_Segments'] = 'Potential Loyal'
rfm.loc[(rfm['RFM_Score'] >= 5) & (rfm['RFM_Score'] < 7), 'RFM_Customer_Segments'] = 'At Risk'
rfm.loc[(rfm['RFM_Score'] >= 4) & (rfm['RFM_Score'] < 5), 'RFM_Customer_Segments'] = "Can't Lose"
rfm.loc[(rfm['RFM_Score'] >= 3) & (rfm['RFM_Score'] < 4), 'RFM_Customer_Segments'] = 'Lost'
segment_counts= rfm['RFM_Customer_Segments'].value_counts().sort_index()

vip_segment = rfm[rfm['RFM_Customer_Segments'] == 'VIP']
vip_segment.head()

fig = go.Figure()
fig.add_trace(go.Box(x=vip_segment['Recency'], name='Recency', marker_color='blue'))
fig.add_trace(go.Box(x=vip_segment['Frequency'], name='Frequency', marker_color='green'))
fig.add_trace(go.Box(x=vip_segment['Monetary'], name='Monetary', marker_color='orange'))
fig.show()

correlation_matrix = vip_segment[['Recency', 'Frequency', 'Monetary']].corr()
print(correlation_matrix)

fig_heatmap = go.Figure(data=go.Heatmap(
    z=correlation_matrix.values,
    x=correlation_matrix.columns,
    y=correlation_matrix.index,
    colorscale='RdBu'
))
fig_heatmap.update_layout(title='Correlation Heatmap for VIP Segment')
fig_heatmap.show()

colors = plotly.colors.qualitative.Prism
vip_color = 'rgb(205,92,92)'

marker_colors = [vip_color if label == 'VIP' else colors[i % len(colors)] 
                 for i, label in enumerate(segment_counts.index)]

fig = go.Figure(data=go.Bar(
    x=segment_counts.index,
    y=segment_counts.values,
    marker=dict(color=marker_colors)
))

fig.update_layout(
    title='Customer Segments Distribution with VIP Highlighted',
    xaxis_title='Customer Segment',
    yaxis_title='Number of Customers'
)

fig.show()

segment_scores = rfm.groupby('RFM_Customer_Segments')[['R','F','M']].mean().reset_index()
fig = go.Figure()

#For Recency score
fig.add_trace(go.Bar(
    x=segment_scores['RFM_Customer_Segments'], 
    y=segment_scores['R'], 
    name='Recency', 
    marker_color='blue'))

#For Frequency score
fig.add_trace(go.Bar(
    x=segment_scores['RFM_Customer_Segments'], 
    y=segment_scores['F'], 
    name='Frequency', 
    marker_color='green'))  

#For Monetary score
fig.add_trace(go.Bar(
    x=segment_scores['RFM_Customer_Segments'], 
    y=segment_scores['M'], 
    name='Monetary', 
    marker_color='orange'))

fig.update_layout(
    title='Average R, F, M Scores by Customer Segment',
    xaxis_title='Customer Segment',
    yaxis_title='Average Score',
    barmode='group',
    showlegend=True
)
fig.show()  

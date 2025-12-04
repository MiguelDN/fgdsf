from pdb import run
from .ids import *
from monday_client import MondayClient







def get_item_values(item_id,monday:MondayClient):
    item = monday.get_item(item_id)
    
    print(f'item = {item}')
    
    item_name = item['name']
    
    stage = None
    deal_value = None
    timeline_from = None
    timeline_to = None
    division = None
    
    for column in item['column_values']:
        if column['column']['id'] == opps_board_stage:
            stage = column['label']
        elif column['column']['id'] == opps_board_deal_value:
            deal_value = column['text']
        elif column['column']['id'] == opps_board_timeline:
            if column['from']:
                timeline_from = column['from'].split('T')[0]
            if column['to']:
                timeline_to = column['to'].split('T')[0]
        elif column['column']['id'] == opps_board_acco_owner:
            owner = column['persons_and_teams'][0]
        elif column['column']['id'] == opps_board_division:
            division = column['label']
        elif column['column']['id'] == opps_board_account:
            account = column['linked_items'][0]['name']
    
        
            
    print(f'stage = {stage}')
    print(f'deal_value = {deal_value}')
    print(f'timeline_from = {timeline_from}')
    print(f'timeline_to = {timeline_to}')
    print(f'Division = {division}')
    print(f'Account = {account}')
    print(f'owner = {owner}')
    
    data = {
        'name': item_name,
        'stage': stage,
        'deal_value': deal_value,
        'timeline_from': timeline_from,
        'timeline_to': timeline_to,
        'division': division,
        'account': account,
        'owner': owner
    }
    
    
    return data




def get_delay(division,monday: MondayClient):
    
    # if division:
    buffer_data = monday.get_items_by_column_value(buffer_board, 'name', division,limit=1,fields = f'id name column_values(ids:"{buffer_board_days}"){{text}}')
    print(f'buffer = {buffer_data}')
    
    if len(buffer_data)==0:
        delay = 0
    else:
        delay = buffer_data[0]['column_values'][0]['text']
        
        
    return delay


def create_items(item_data,semanas,item_id,monday: MondayClient):
    
    if item_data['stage'].lower().strip()=='won':
        stage = 'Secured'
    elif item_data['stage'].lower().strip()=='lost':
        stage = 'Lost'
    else:
        stage = 'Pipeline'
    
    if stage!= 'Lost':
        
        deal_value = float(int(item_data['deal_value'])/len(semanas))
        
        for i,day in enumerate(semanas,start=1):
            print(f"item_data['owner'] = {item_data['owner']}")
            values=[
                {'id':runrate_board_owner,'type':'people','value':[item_data['owner']]},
                {'id':runrate_board_status,'type':'status','value':stage},
                {'id':runrate_board_client,'type':'text','value':str(item_data['account'])},
                {'id':runrate_board_value,'type':'numbers','value':deal_value},
                {'id':runrate_board_date,'type':'date','value':{'date':day}},
                {'id':runrate_board_project_name,'type':'text','value':str(item_data['name'])},
                {'id':runrate_board_origin_item_id,'type':'text','value':str(item_id)},
                {'id':runrate_board_division,'type':'status','value':str(item_data['division'])}
            ]
            print(f'values = {values}')
            r = monday.create_item(runrate_board,f"{item_data['name']} Week {i}",columns=values)





def get_items_created(monday: MondayClient, item_id):
    
    items = monday.get_items_by_column_value(runrate_board, runrate_board_origin_item_id, (item_id), fields = f'id name column_values(ids:"{runrate_board_value}"){{text}}')
    
    return items
    
def delete_items(items,monday: MondayClient):
    for item in items:
        monday.delete_item(item['id'])
    
    
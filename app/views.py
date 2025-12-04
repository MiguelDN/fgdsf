import trace
import traceback
from django.http import HttpResponse
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from .ids import *
from monday_client import MondayClient
from .calculo_semanas import fechas_inicio_semanas_str
from .functions import *

# Create your views here.

@csrf_exempt
def health(request):
    print('TEST')
    return HttpResponse('ok')


@csrf_exempt
def main(request):
    
    print('entro en main')
    
    # headers = request.headers
    # print(f'headers = {headers}')
    
    try:
        # Obtener datos del requests
        data = json.loads(request.body.decode('utf-8'))
        print(f'data = {data}')
        
        board_id = data['payload']['inboundFieldValues']['boardId']
        item_id = data['payload']['inboundFieldValues']['itemId']
        column_id = data['payload']['inboundFieldValues']['columnId']
        print(f'board_id: {board_id}')
        print(f'item_id: {item_id}')
        
        # Objeto Monday
        monday = MondayClient(token)
        
        # Obtener items ya creados por semanas de el proyecto disparado si existen
        item_data = get_item_values(item_id,monday)
        
        
        already_created_items = get_items_created(monday, item_id)
        print(f"already_created_items = {already_created_items}")
        
        if item_data['stage'].lower().strip()!='lost':
            
            stage_ok = bool(item_data["stage"])
            deal_ok = bool(item_data["deal_value"] and str(item_data["deal_value"]).strip())
            timeline_ok = any([item_data["timeline_from"], item_data["timeline_to"]])
        
            if stage_ok and deal_ok and timeline_ok:
                print('Cumple condiciones')
                
                
                delay = get_delay(item_data['division'], monday)
                
                print(f'delay = {delay}')
                
                semanas = fechas_inicio_semanas_str(item_data['timeline_from'], item_data['timeline_to'], int(delay))
                
                print(f'semanas = {semanas}')
                if len(already_created_items)>0:
                    delete_items(already_created_items,monday)
                
                create_items(item_data,semanas,item_id,monday)
                
                
                
                
            else:
                print('Faltan datos')
                return HttpResponse('Faltan datos')
            
                
        else:
            print('logica para borrar los items')
            delete_items(already_created_items,monday)
            
            
            
    except Exception as e:
        print(f'Error: {e}, traceback = {traceback.format_exc()}')
        return HttpResponse('Error')
        
        
        
        
        
        
        
        
        
        
        
        
    
        
            

    
    
    
        
        
        
    return HttpResponse('OK')
    
    
    
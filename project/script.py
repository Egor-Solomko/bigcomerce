# script.py
import requests
import time
from flask import Flask, render_template_string



api_key_racechip = 'b1ddd97910d0c400a31b87cc534d24eb'
hach = 'co0icmrzz6'
header = {'X-auth-token': 'bemqw95yr8h3ynb4v7ju0casco51ebn'}


output = 'evsvdfbdfb'


def get_all_motor():

    mistake_list = []
    try:
        manufacture_response = requests.get(f"https://www.racechip.de/reseller_api/v3/manufacturer?apikey={api_key_racechip}")
        manufacturers = []
        if manufacture_response.status_code == 200:  
            manufacturer_data = manufacture_response.json()  
            for key in manufacturer_data.keys():
                manufacturers.append(key)
        
        else:
            print("Can't get data about manufacturers")
            return mistake_list

        models_id = []
        car_manufacturer_name = {}
        for id_model in manufacturers:
            models_responce = requests.get(f'https://www.racechip.de/reseller_api/v3/manufacturer/id/{id_model}?apikey={api_key_racechip}')
            models_data = models_responce.json()
            for id in models_data['models'].keys():
                models_id.append(id)
                car_manufacturer_name[id] = models_data['car_manufacturer_name']
        print("тут еще работаем")        
        motors_id = []
        car_manufacturer_name1 = {}
        for engine_id in models_id:
            engine_responce = requests.get(f'https://www.racechip.de/reseller_api/v3/model/id/{engine_id}?apikey={api_key_racechip}')
            engine_data = engine_responce.json()
            try:
                for id in engine_data['motors'].keys():
                    motors_id.append(id)

                    car_manufacturer_name1[id] = car_manufacturer_name[engine_id]
            except:
                pass
        print("тут еще работаем1")  
        for motor_id in motors_id:

            motor_responce = requests.get(f'https://www.racechip.de/reseller_api/v3/motor/id/{motor_id}?apikey={api_key_racechip}')
            motor_data = motor_responce.json()
            for i in motor_data['products']:
                data = {}
                print(motor_data)
                print(i)
                data['car_short_name'] = motor_data['car_short_name']
                data['car_motor_name'] = motor_data['car_motor_name']
                data['name'] = motor_data['products'][i]['name']
                data['price'] = motor_data['products'][i]['price']
                data['gtin'] = motor_data['products'][i]['gtin']
                #data['car_manufacturer_name'] = car_manufacturer_name1[motor_id]
                try:
                    data['details'] = motor_data['products'][i]['details']

                    if data['details'] != False:
                        data['performance_nm'] = motor_data['products'][i]['details']['performance_nm']
                        data['performance_ps'] = motor_data['products'][i]['details']['performance_ps']
                        data['performance_fuel'] = motor_data['products'][i]['details']['performance_fuel']
                        data['details'] = True


                    elif data['details'] == False:
                        try:
                            info_product = requests.get(f'https://www.racechip.de/reseller_api/v3/product/id/{i}?apikey=b1ddd97910d0c400a31b87cc534d24eb')
                            a = info_product.json()
                            
                            data['performance_nm'] = a[i]['details']['performance_nm']
                            data['performance_ps'] = a[i]['details']['performance_ps']
                            data['performance_fuel'] = a[i]['details']['performance_fuel']
                            if data['performance_nm'] and data['performance_ps'] and data['performance_fuel'] != False:
                                data['details'] = True
                        except:
                            data['details'] = False

                except:
                        try:                             
                            info_product = requests.get(f'https://www.racechip.de/reseller_api/v3/product/id/{i}?apikey=b1ddd97910d0c400a31b87cc534d24eb')
                            a = info_product.json()
                            data['performance_nm'] = a[i]['details']['performance_nm']
                            data['performance_ps'] = a[i]['details']['performance_ps']
                            data['performance_fuel'] = a[i]['details']['performance_fuel']
                            data['details'] = True
                        except:
                            data['details'] = False
                
                Bigcommerce_Product_Name = f'{data["name"]} / {data["car_motor_name"]}'
                print("тут еще работаем3")  
                if data['details'] == True:
                    Bigcommerce_Product_Description = f'{data["name"]} - {data["car_short_name"]} <br\/>Performance Fuel : {data["performance_fuel"]}<br\/>Performance nm : {data["performance_nm"]}<br\/>Performance ps : {data["performance_ps"]}'
                else:
                    Bigcommerce_Product_Description = f'{data["name"]} - {data["car_short_name"]}'

                Bigcommerce_GTIN_fields = f'{data["gtin"]}'

                payload = {
                    "name": Bigcommerce_Product_Name,
                    "type": "physical",
                    "description": Bigcommerce_Product_Description, 
                    "weight": 1,
                    "price": data['price'],
                    "gtin": Bigcommerce_GTIN_fields, 
                    "categories": [11913]
                }




                #request_co_create_product = requests.post(f'https://api.bigcommerce.com/stores/{hach}/v3/catalog/products', headers=header, json=payload)


    except:
        mistake_list.append("Connection failed")


    if len(mistake_list) == 0:
        return ["Adding items completed correctly."]
    else:
        return mistake_list



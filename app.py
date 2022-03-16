from flask import Flask
from flask import request
import json,requests,random
#from pprint import pprint



app = Flask(__name__)

@app.route('/download',methods=['POST'])
def download_sub():
    try :
        # VARIABLES
        global token
        req = request.form.to_dict()
        id = str(req['id'])
        try:
            fname = str(req['filename'])
        except Exception, e:
            pass
        try:
            language = str(req['language'])
        except:
            language = 'en'
        
        
        # API LIST
        api_list= ['8N3cWyJvYvWL5KDLxt0aKzu4vhNkUCnr','1J8MVetljab3wYO4ancDmuk0We1RieMB']
        api = random.choice(list(api_list))
        
        # LOGIN TO GET TOKEN
        token_url ="https://api.opensubtitles.com/api/v1/login"
        token_headers ={
            'Api-Key':api,
            'content-type': 'application/json'
        }
        token_data ={
  		    'username': 'filmvision',
  		    'password': 'filmvision'
        }
        token_req = requests.post(token_url, data= json.dumps(token_data), headers=token_headers)
        token_req_json = token_req.json()
        
        if token_req.status_code == 200:
            token = token_req_json['token']
        else :
            token = "None"
            
        # GENERATING DOWNLOAD URL & HANDLING RESPONSES
        download_url = "https://www.opensubtitles.com/api/v1/download"
        download_headers = {
                'Api-Key': api,
                'Authorization': token ,
                'content-type': 'application/json'
        }
        download_file_id = {'file_id': id}
        download_response = requests.post(download_url, data=json.dumps(download_file_id), headers=download_headers)
        download_json_response = download_response.json()
        
        if (download_response.status_code == 200) :
            print ("\n\n# Successful :: 200 \n")
            r = {
                'response':200,
                'link': download_json_response['link'],
                'remaining': download_json_response['remaining']
            }
            return (json.dumps(r))
        else :
            if 'remains' in download_response:
                r ={
                    'again' : 'true',
                    'response' : download_response.status_code,
                    'message'  : download_json_response['message']
                }
            else:
                try:
                    r ={
                        'again' : 'false',
                        'response' : download_response.status_code,
                        'message'  : download_json_response['message']
                    }
                except:
                    r ={
                        'response' : download_response.status_code
                    }
            return (json.dumps(r))
    except Exception as e:
        error = (f"Error detected on filmvision download server ::: {e}")
        
        h = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Apikey eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI1Yzc5NjAyMC1hNTM5LTExZWMtYjhhYy04Zjk2YjExMDNmYzkiLCJzdWIiOiJTSE9VVE9VVF9BUElfVVNFUiIsImlhdCI6MTY0NzQ0MjYzMiwiZXhwIjoxOTYzMDYxODMyLCJzY29wZXMiOnsiYWN0aXZpdGllcyI6WyJyZWFkIiwid3JpdGUiXSwibWVzc2FnZXMiOlsicmVhZCIsIndyaXRlIl0sImNvbnRhY3RzIjpbInJlYWQiLCJ3cml0ZSJdfSwic29fdXNlcl9pZCI6IjY2MDE5Iiwic29fdXNlcl9yb2xlIjoidXNlciIsInNvX3Byb2ZpbGUiOiJhbGwiLCJzb191c2VyX25hbWUiOiIiLCJzb19hcGlrZXkiOiJub25lIn0.nwgRCXa-tQ6s9L-n6QRjFlfqR11UPjIj3Solr43Weck'
        }
        
        d = {
            "source": "ShoutDEMO",
            "destinations": [
                "94751354842"
            ],
            "transports": [
                "sms"
            ],
            "content": {
                "sms": error
            }
        }
        r = requests.post('https://api.getshoutout.com/coreservice/messages', data= json.dumps(d) ,headers = h)
  
  
  
if __name__ == '__main__':
	app.run(debug=True)







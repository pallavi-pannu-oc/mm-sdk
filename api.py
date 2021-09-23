### Model monitor apis ##########
    
    def create_modelmonitor(self,modelmonitor:DkubeModelMonitor,wait_for_completion=True):
        assert type(modelmonitor) == DkubeModelMonitor, "Invalid type for model monitor, value must be instance of rsrcs:DkubeModelMonitor class"
        response = super().create_model_monitor(modelmonitor)
        while wait_for_completion:
            ls = self.list_modelmonitor()
            for i in ls:
                if i["name"] == modelmonitor.modelmonitor.name:
                    status = i["status"]
            state = status['state']
            if state.lower() in ['ready','error']:
                print(
                    "ModelMonitor {} - completed with state {} and reason {}".format(modelmonitor.name, state, response['message']))
                break
            else:
                print(
                    "ModelMonitor {} - waiting for completion, current state {}".format(modelmonitor.name, state))
                time.sleep(self.wait_interval)
   
    def list_modelmonitor(self):
        return super().list_modelmonitor()

    def get_modelmonitor_id(self,name):
        response = super().list_modelmonitor()
        for mm in response:
            if mm['name'] == name:
                return mm['id']
        return None
    
    def get_modelmonitor_alertid(self,name,alert_name):
        mm_id = self.get_modelmonitor_id(name)
        response = super().get_modelmonitor_alerts(mm_id)
        for alert in response['data']:
            if alert['name'] == alert_name:
                return alert['id']
        return None
    
    def get_modelmonitor_configuration(self,name):
        mm_id = self.get_modelmonitor_id(name)
        return super().get_modelmonitor_configuration(mm_id)

    def get_modelmonitor_dataset(self,name):
        mm_id = self.get_modelmonitor_id(name)
        return super().get_modelmonitor_dataset(mm_id)

    def get_modelmonitor_alerts(self,name):
        mm_id = self.get_modelmonitor_id(name)
        return super().get_modelmonitor_alerts(mm_id)

    def delete_modelmonitors(self,delete_list):
        mm_list = []
        for mm in delete_list:
            mm_id = self.get_modelmonitor_id(mm)
            mm_list.append(mm_id)
        return super().delete_modelmonitor(mm_list)

    def get_modelmonitor_dataid(self,name,data_name):
        response = self.get_modelmonitor_dataset(name)
        #print(response)
        for data in response:
            if data["name"] == data_name:
                return data['id']

    def delete_modelmonitor_dataset(self,name,dataset_names):
        mm_id = self.get_modelmonitor_id(name)
        delete_dataset_ids = []
        for data in dataset_names:
            data_id = self.get_modelmonitor_dataid(name,data)
            delete_dataset_ids.append(data_id)
        return super().delete_modelmonitor_dataset(mm_id,delete_dataset_ids)
    
    def get_modelmonitor_features(self,name):
        mm_id = self.get_modelmonitor_id(name)
        return super().get_modelmonitor_features(mm_id)

    def get_modelmonitor_template(self):
        return super().get_modelmonitor_template()

    def delete_modelmonitor_alert(self,name,alert_name):
        mm_id = self.get_modelmonitor_id(name)
        delete_alertsid_list = []
        for data in alert_name:
            alert_id = self.get_modelmonitor_alertid(data)
            delete_alertsid_list.append(alert_id)
        return super().delete_modelmonitor_alert(mm_id,delete_alertsid_list)
    
    def modelmonitor_addalert(self,name,alert_data:DkubeModelMonitorAlert):
        mm_id = self.get_modelmonitor_id(name)
        alert = alert_data.to_JSON()
        alert_dict = json.loads(alert)
        alert_dict['class'] = alert_dict.pop('_class')
        alert_conds,alert_list = [],[]
        alert_conds.append({'id': None,'feature':alert_dict['feature'],'op':alert_dict['op'],'threshold':alert_dict['threshold']})
        alert_dict['conditions'] = alert_conds
        rem_list = ['feature','op','threshold']
        [alert_dict.pop(key) for key in rem_list]
        response = super().modelmonitor_addalert(mm_id,{"data":alert_list.append(alert_dict)})
        return response['response']

    def modelmonitor_adddataset(self,name,data:DkubeModelMonitorDataset):
        mm_id = self.get_modelmonitor_id(name)
        dataset = data.to_JSON()
        data_dict = json.loads(dataset)
        data_dict['class'] = data_dict.pop('_class')
        response = super().modelmonitor_adddataset(mm_id,{"data":data_dict})
        return response['response']


    def archive_modelmonitor(self,name,archive):
        mm_id = self.get_modelmonitor_id(name)
        return super().modelmonitor_archive(mm_id,archive)

    def changestate_modelmonitor(self,name,state):
        mm_id = self.get_modelmonitor_id(name)
        mm_state = self.get_modelmonitor_configuration(name)['status']['state']
        if mm_state.lower() in ['ready','init'] and state == 'stop':
            print("Please start the model monitor first")
        return super().modelmonitor_state(mm_id,state)
    

    def update_modelmonitor_dataset(self,user,name,data_name,data:DkubeModelMonitorDataset):
        mm_id = self.get_modelmonitor_id(name)
        data_id = self.get_modelmonitor_dataid(name,data_name+":"+user)
        dataset = data.to_JSON()
        data_dict = json.loads(dataset)
        data_dict['class'] = data_dict.pop('_class')
        return super().update_modelmonitor_dataset(mm_id,data_id,data_dict)

    def update_modelmonitor_alert(self,name,alert_name,alert:DkubeModelMonitorAlert):
        mm_id = self.get_modelmonitor_id(name)
        alert_id = self.get_modelmonitor_alertid(name,alert_name)
        alert_data = alert.to_JSON()
        alert_dict = json.loads(alert_data)
        alert_dict['class'] = alert_dict.pop('_class')
        alert_conds = []
        alert_conds.append({'id': None,'feature':alert_dict['feature'],'op':alert_dict['op'],'threshold':alert_dict['threshold']})
        alert_dict['conditions'] = alert_conds
        rem_list = ['feature','op','threshold']
        [alert_dict.pop(key) for key in rem_list]
        return super().update_modelmonitor_alert(mm_id,alert_id,alert_dict)
    
        
        
        
        

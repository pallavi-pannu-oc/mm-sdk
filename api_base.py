    def create_model_monitor(self,modelmonitor):
        response = self._mmapi.modelmonitor_add_one(data=modelmonitor.modelmonitor)
        return response.to_dict()
    
    def get_modelmonitor(self,modelmonitor):
        response = self._mmapi.modelmonitor_get(modelmonitor)
        return response

    def list_modelmonitor(self):
        response = self._mmapi.modelmonitor_list()
        return response.to_dict()['data']

    def get_modelmonitor_configuration(self,modelmonitor_id):
        response = self._mmapi.modelmonitor_get(modelmonitor_id)
        return response.to_dict()['data']
    
    def get_modelmonitor_dataset(self,modelmonitor):
        response = self._mmapi.modelmonitor_datasets_list(modelmonitor)
        return response.to_dict()['data']

    def get_modelmonitor_alerts(self,modelmonitor_id):
        response = self._mmapi.modelmonitor_alerts_list(modelmonitor_id)
        return response.to_dict()
    
    def get_modelmonitor_features(self,modelmonitor):
        response = self._mmapi.modelmonitor_get_features(modelmonitor)
        print(response)
        return response.to_dict()['data']
    
    def get_modelmonitor_template(self):
        response = self._mmapi.modelmonitor_get_metrics_template()
        return response.to_dict()

    def delete_modelmonitors(self,delete_list):
        response = self._mmapi.modelmonitor_delete({'data': delete_list})
        return response.to_dict()

    def delete_modelmonitor_dataset(self,mm_id,delete_dataset_list):
        response = self._mmapi.modelmonitor_delete_datasets(mm_id,{'data':delete_dataset_list})
        return response.to_dict()
    
    def delete_modelmonitor_alert(self,mm_data,delete_alerts_list):
        response = self._mmapi.modelmonitor_delete_alerts(mm_id,{data:delete_alerts_list})
        return response.to_dict()
   
    def modelmonitor_addalert(self,modelmonitor,alert_data):
        response = self._mmapi.modelmonitor_add_alerts(modelmonitor,alert_data)
        return response.to_dict()
    
    def modelmonitor_adddataset(self,modelmonitor,dataset):
        response = self._mmapi.modelmonitor_add_datasets(modelmonitor,dataset)
        return response.to_dict()

    def modelmonitor_archive(self,modelmonitor,archive):
        response = self._mmapi.modelmonitor_archive(modelmonitor,archive)
        return response.to_dict()

    def modelmonitor_state(self,modelmonitor,state):
        response = self._mmapi.modelmonitor_state(modelmonitor,state)
        return response.to_dict()
    
    def update_modelmonitor_dataset(self,modelmonitor,dataset,data):
        response = self._mmapi.modelmonitor_update_dataset(modelmonitor,dataset,data)
        return response.to_dict()
    
    def update_modelmonitor_alert(self,modelmonitor,alert,data):
        response = self._mmapi.modelmonitor_update_alert(modelmonitor,alert,data)
        return response.to_dict()

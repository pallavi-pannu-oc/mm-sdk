### Model monitor apis ##########
    
    def modelmonitor_create(self,modelmonitor:DkubeModelmonitor,wait_for_completion=True):
        """
            Method to create Model Monitor on Dkube

        *Inputs*

            modelmonitor
                    Instance of :bash:`dkube.sdk.rsrcs.modelmonitor.DkubeModelmonitor class.
                    Please see the :bash:`Resources` section for details on this class.


            wait_for_completion
                    When set to :bash:`True` this method will wait for modelmonitor resource to get into one of the complete state.
                    modelmonitor is declared complete if it is one of the :bash:`init/ready/error` state    
        
        Outputs*
                a dictionary object with response status
        """
        assert type(modelmonitor) == DkubeModelmonitor, "Invalid type for model monitor, value must be instance of rsrcs:DkubeModelmonitor class"
        response = super().create_model_monitor(modelmonitor)
        while wait_for_completion:
            mm_config = super().get_modelmonitor_configuration(response['uuid'])
            state = mm_config['status']['state']
            if state.lower() in ['init','ready','error']:
                print(
                    "ModelMonitor {} - completed with state {} and reason {}".format(modelmonitor.name, state, response['message']))
                break
            else:
                print(
                    "ModelMonitor {} - waiting for completion, current state {}".format(modelmonitor.name, state))
                time.sleep(self.wait_interval)
        return response

    def modelmonitor_list(self,**kwargs):
        """
            Method to list the modelmonitors.
            *Inputs*

                **kwargs
                    tags: string
                    page : integer
                    archived : boolean
                    when archived=True, list the archived modelmonitors
            
            *Outputs*
                A list containing the modelmonitors       
        """
        tags = kwargs.get('tags')
        page = kwargs.get('page')
        archived = kwargs.get('archived',False)
        query_params = {}
        if tags:
            query_params['tags'] = tags
        if page:
            query_params['page'] = page
        if archived:
            query_params['archived'] = archived
        return super().list_modelmonitor(query_params)

    def modelmonitor_get_id(self,name=None):
        """
            Method to get the id  of a model monitor.

            *Inputs*

                name
                    Name of the modelmonitor

            *Outputs*
                An uuid of the modelmonitor 
        """
        response = super().get_modelmonitor_id(name).to_dict()["data"]
        if response!=None:
            return response.get(name)
        else:
            return None
    
    def modelmonitor_get_alertid(self,name=None,alert_name=None):
        """
            Method to get the alert id  of a modelmonitor.

            *Inputs*

                name
                    Name of the modelmonitor
                alert_name
                    Name of the alert

            Outputs*
                an id of the alert
                
        """
        mm_id = self.modelmonitor_get_id(name)
        response = super().get_modelmonitor_alerts(mm_id)
        for alert in response:
            if alert['name'] == alert_name:
                return alert['id']
        return None
    
    def modelmonitor_get(self,name=None,id=None):
        """
            Method to get the modelmonitor.

            *Inputs*

                name or id
                    name of the modelmonitor or id of modelmonitor
            *Outputs*
                A dictionary containing the configuration of the modelmonitor       
        """

        if id == None:
            id = self.modelmonitor_get_id(name)
        return super().get_modelmonitor_configuration(id)

    def modelmonitor_get_datasets(self,name=None,id=None,data_class:DatasetClass=None):
        """
            Method to get the datasets of the modelmonitor.

            *Inputs*

                name or id
                    name of the modelmonitor or id of modelmonitor


                data_class
                    data class of the dataset in the modelmonitor must be one of ["TrainData","PredictData","LabelledData"]
                    by default set to None
            
            *Outputs*
                if data_class is None:
                    A list of dictionaries containing all the datasets information.
                
                if data_class is 'PredictData' or 'LabelledData':
                    An individual data dictionary for that data class.
        """
        if id == None:
            id = self.modelmonitor_get_id(name)
        datasets = super().get_modelmonitor_dataset(id)
        if data_class == None:
            return datasets
        else:
            for data in datasets:
                if(data['_class'] == data_class):
                    return data

    def modelmonitor_get_alerts(self,name=None,id=None):
        """
            Method to get the alerts of the modelmonitor.

            *Inputs*

                name or id
                    name of the modelmonitor or id of modelmonitor
            
            *Outputs*
                a list of dictionaries containing individual alerts information
        """
        if id == None:
            id = self.modelmonitor_get_id(name)
        return super().get_modelmonitor_alerts(id)

    def modelmonitors_delete(self,names=[],delete_ids=[]):
        """
            Method to delete the multiple modelmonitors.

            *Inputs*

                names or delete_ids
                    names of the modelmonitor or ids of modelmonitor, should be a list eg: names=["mm1","mm2"] or delete_ids=["cd123","345fg"]
            
            *Outputs*
                A list of dictionaries containing all the alerts
        """
        mm_list = []
        if delete_ids == []:
            for mm in names:
                mm_id = self.modelmonitor_get_id(mm)
                mm_list.append(mm_id)
        if mm_list == []:
            return super().delete_modelmonitors(delete_ids)
        else:
            return super().delete_modelmonitors(mm_list)
        
    def modelmonitor_delete(self,name=None,id=None):
        """
            Method to delete the single modelmonitor.

            *Inputs*

                name or id
                    name of the modelmonitor or id of modelmonitor
            *Outputs*
                a dictionary object with response status
        """
        if id == None:
            id = self.modelmonitor_get_id(name)
        
        return super().delete_modelmonitors([id])


    def modelmonitor_get_metricstemplate(self):
        """
            Method to get the metrics supported for the modelmonitor.
        
        Outputs*
                a list of dictionaries containing metrics template for Regression and Classification
        
        """
        return super().get_modelmonitor_template()

    def modelmonitor_delete_alert(self,name=None,id=None,alert_name=None):
        """
            Method to delete the alerts in the modelmonitor

            *Inputs*

                name or id
                    name of the modelmonitor or id of modelmonitor
                alert_name
                    class of the modelmonitor dataset, must be one of ["TrainData","PredictData","LabelledData]              
        """
        if id == None:
            id = self.modelmonitor_get_id(name)
        delete_alertsid_list = []
        for data in alert_name:
            alert_id = self.get_modelmonitor_alertid(data)
            delete_alertsid_list.append(alert_id)
        return super().delete_modelmonitor_alert(id,delete_alertsid_list)
    
    def modelmonitor_add_alert(self,alert_data:DkubeModelmonitoralert=None,name=None,id=None):
        """
            Method to add the alerts in the modelmonitor

            *Inputs*
                alert_data
                    Instance of :bash:`dkube.sdk.rsrcs.modelmonitor.DkubeModelmonitoralert` class.
                    Please see the :bash:`Resources` section for details on this class.

                
                name or id
                    name of the modelmonitor or id of modelmonitor      

            Outputs*
                a dictionary object with response status
               
        """
        if id == None:
            id = self.modelmonitor_get_id(name)
        if self.modelmonitor_get_datasets(id=id,data_class='TrainData') and self.modelmonitor_get_datasets(id=id,data_class='PredictData'):
            alert_dict = json.loads(alert_data.to_JSON())
            alert_dict['class'] = alert_dict.pop('_class')
            response = super().modelmonitor_addalert(id,{"data":[alert_dict]})
            return response
        else:
            print("Add train and predict data before adding alerts")

    def modelmonitor_add_dataset(self,data:DkubeModelmonitordataset=None,name=None,id=None,wait_for_completion=True):
        """
            Method to add the dataset in the modelmonitor

            *Inputs*
                data
                    Instance of :bash:`dkube.sdk.rsrcs.modelmonitor.DkubeModelmonitordataset` class.
                    Please see the :bash:`Resources` section for details on this class.

                
                name or id
                    name of the modelmonitor or id of modelmonitor             
                wait_for_completion
                    When set to :bash:`True` this method will wait for modelmonitor resource to get into one of the complete state and then add the datasets.
                    modelmonitor is declared complete if it is one of the :bash:`init/ready/error` state
            
            Outputs*
                a dictionary object with response status
        
        """
        if id == None:
            id = self.modelmonitor_get_id(name)
        while wait_for_completion and (self.modelmonitor_get_datasets(id=id,data_class='TrainData')==[]):
            mm_config = super().get_modelmonitor_configuration(id)
            state = mm_config['status']['state']
            if state.lower() in ['init','ready','error']:
                break
            else:
               print("Model Monitor creation not completed yet, current state {}".format(state))
               time.sleep(self.wait_interval)
        
        data_dict = json.loads(data.to_JSON())
        data_dict['class'] = data_dict.pop('_class')
        response = super().modelmonitor_adddataset(id,{"data":data_dict})
        return response['response']

    def modelmonitor_archive(self,name=None,id=None):
        """
            Method to archive the modelmonitor

            *Inputs*
                name or id
                    name of the modelmonitor or id of modelmonitor  

            Outputs*
                a dictionary object with response status           
        """
        if id == None:
            id = self.modelmonitor_get_id(name)
        return super().modelmonitor_archive(id,archive=True)

    def modelmonitor_unarchive(self,name=None,id=None):
        """
            Method to unarchive the modelmonitor

            *Inputs*
                name or id
                    name of the modelmonitor or id of modelmonitor    

            Outputs*
                a dictionary object with response status         
        """
        if id == None:
            id = self.modelmonitor_get_id(name)
        return super().modelmonitor_archive(id,archive=False)
    
    def modelmonitor_start(self,name=None,id=None,wait_for_completion=True):
        """
            Method to start the modelmonitor

            *Inputs*
                name or id
                    name of the modelmonitor or id of modelmonitor        
                wait_for_completion
                    When set to :bash:`True` this method will wait for modelmonitor resource to get into one of the complete state.
                    modelmonitor is declared complete if it is one of the :bash:`init/ready/error` state , when it reaches ready state, it starts the modelmonitor
            
            Outputs*
                a dictionary object with response status
        
        """
        if id == None:
            id = self.modelmonitor_get_id(name)
        while wait_for_completion:
            mm_state = self.modelmonitor_get(id=id)['status']['state']
            if mm_state.lower() in ["init","active","error"]:
                print("ModelMonitor {} - is in {} state".format(id, mm_state))
                time.sleep(self.wait_interval)
            else:
                return super().modelmonitor_state(id,"start")

    def modelmonitor_stop(self,name=None,id=None):
        """
            Method to stop the modelmonitor

            *Inputs*
                name or id
                    name of the modelmonitor or id of modelmonitor             
            
            Outputs*
                a dictionary object with response status
        
        """
        if id == None:
            id = self.modelmonitor_get_id(name)
        return super().modelmonitor_state(id,"stop")
    

    def modelmonitor_update_dataset(self,data_class:DatasetClass,data:DkubeModelmonitordataset=None,name=None,id=None,wait_for_completion=True):
        """
            Method to update the modelmonitor dataset

            *Inputs*
                
                data
                    Instance of :bash:`dkube.sdk.rsrcs.modelmonitor.DkubeModelmonitordataset` class.
                    Please see the :bash:`Resources` section for details on this class.
                
                data_class
                    Instance of :bash:`dkube.sdk.rsrcs.modelmonitor.DatasetClass` class.
                    Enum = ["TrainData","PredictData","LabelledData"]
                    Please see the :bash:`Resources` section for details on this class.

                name or id
                    name of the modelmonitor or id of modelmonitor             
                wait_for_completion
                    When set to :bash:`True` this method will wait for modelmonitor resource to get into one of the complete state and then update the datasets
                    modelmonitor is declared complete if it is one of the :bash:`init/ready/error` state , if it is in active state, modelmonitor update to datasets not allowed
            
            
            Outputs*
                a dictionary object with response status
        
        """
        if id == None:
            id = self.modelmonitor_get_id(name)
            data_id = self.modelmonitor_get_datasets(name,data_class=data_class)['id']
        else:
            data_id = self.modelmonitor_get_datasets(id,data_class=data_class)['id']
        while wait_for_completion:
            mm_state = self.modelmonitor_get(id=id)['status']['state']
            if mm_state.lower() in ['init','error','ready']:
                data_dict = json.loads(data.to_JSON())
                for k in list(data_dict.keys()):
                    if(data_dict[k]==None and k!='_class'):
                        del data_dict[k]
                data_dict['class']=data_dict['_class']
                if data_dict['class'] == None:
                    data_dict['class'] = data_class
                return super().update_modelmonitor_dataset(id,data_id,data_dict)
            elif mm_state.lower() == "active":
                    print("no update to active monitor is allowed")
            else:
                print("ModelMonitor {} - is in {} state".format(id, mm_state))
                time.sleep(self.wait_interval)

    def modelmonitor_update_alert(self,alert:DkubeModelmonitoralert=None,alert_name=None,name=None,id=None):
        """
            Method to update the modelmonitor alert

            *Inputs*
                
                data
                    Instance of :bash:`dkube.sdk.rsrcs.modelmonitor.DkubeModelmonitoralert` class.
                    Please see the :bash:`Resources` section for details on this class.
                
                alert_name
                    name of the alert you want to update in the modelmonitor

                name or id
                    name of the modelmonitor or id of modelmonitor             
            
            Outputs*
                a dictionary object with response status
        
        """
        if id == None:
            id = self.modelmonitor_get_id(name)
            alert_id = self.modelmonitor_get_alertid(name,alert_name=alert_name)
        else:
            alert_id = self.modelmonitor_get_alertid(id,alert_name=alert_name)
        
        alert_dict = json.loads(alert.to_JSON())
        alert_dict['class'] = alert_dict.pop('_class')
        return super().update_modelmonitor_alert(id,alert_id,alert_dict)


    def modelmonitor_update(self,config:DkubeModelmonitor=None,name=None,id=None):
        """
            Method to update the modelmonitor

            *Inputs*
                
                config
                    Instance of :bash:`dkube.sdk.rsrcs.modelmonitor.DkubeModelmonitor` class.
                    Please see the :bash:`Resources` section for details on this class to check
                    what can be updated.

                name or id
                    name of the modelmonitor or id of modelmonitor 

            Outputs*
                a dictionary object with response status            
        """
        if id == None:
            id = self.modelmonitor_get_id(name)
        config_dict=config.__dict__["modelmonitor"].__dict__
        config_dict = {k.replace('_', '',1):v for k,v in config_dict.items()}
        rem_list = ['datasets','model','alerts','performance_metrics_template','updated_at','id','drift_detection_algorithm','created_at','pipeline_component','status','owner','name','discriminator']
        [config_dict.pop(key) for key in rem_list]
        for k in list(config_dict.keys()):
            if(config_dict[k]==None or config_dict[k]==[]):
                del config_dict[k]
        return super().update_modelmonitor_config(id,config_dict)

    def modelmonitor_update_schema(self,label=None,name=None,id=None,selected=True,schema_class='Categorical',schema_type='InputFeature'):
        """
            Method to update the schema in the modelmonitor

            *Inputs*
                
                label
                    feature in the schema to be updated
                name or id
                    name of the modelmonitor or id of modelmonitor
                selected
                    boolean (True or False), by default True
                schema_class
                    class of the schema (Categorical,Continuous) 
                schema_type
                    type of schema (Input Feature, PredictionOutput, Rowid, Timestamp)

            Outputs*
                a dictionary object with response status                         
        """
        
        if id == None:
            id = self.modelmonitor_get_id(name)
        config = self.modelmonitor_get(id=id)
        for feature in config["schema"]["features"]:
            if feature["label"] == label:
                feature["_class"] = schema_class
                feature["type"] = schema_type
                feature["selected"] = selected
        for d in config["schema"]["features"]:
            d['class'] = d.pop('_class')
        mm  = DkubeModelmonitor(model_name=config["model"],description=config["description"])
        mm.__dict__["modelmonitor"].__dict__['_schema'] = config["schema"]
        return self.modelmonitor_update(mm,id=id) 
        
        
        
        




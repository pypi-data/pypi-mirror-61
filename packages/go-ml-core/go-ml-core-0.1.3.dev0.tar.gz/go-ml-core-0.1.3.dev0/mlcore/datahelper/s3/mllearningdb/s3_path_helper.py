class RawDataPathHelper():

    def __init__(self, s3baseprefix='ml/'):
        self.s3_root_dir = '%s%s' % (s3baseprefix, 'rawdata-workspace')
        self.local_root_dir = 'tmpdata/rawdata-workspace'

    def get_rawdata_key(self, name):
        return {
            'vm_list': 'vm-list',
            'vm_nearby': 'vm-nearby',
            'es_rate': 'es-rate',
            'battery_status': 'battery-status'
        }[name]

    def get_es_rates_dirs(self, update_time_str=''):
        return self.get_dirs_by_name('es_rate', update_time_str=update_time_str)

    def get_vm_list_dirs(self, update_time_str=''):
        return self.get_dirs_by_name('vm_list', update_time_str=update_time_str)

    def get_vm_nearby_dirs(self, update_time_str=''):
        return self.get_dirs_by_name('vm_nearby', update_time_str=update_time_str)

    def get_dirs_by_name(self, name, update_time_str=''):
        key = self.get_rawdata_key(name)
        path = {}
        path['s3folder'] = '%s/%s/%s/' % (self.s3_root_dir, key, update_time_str)
        path['s3folder_latest'] = '%s/%s/%s/' % (self.s3_root_dir, key, 'latest')
        path['local_dir'] = '%s/%s/%s/' % (self.local_root_dir, key, update_time_str)
        path['s3prefix'] = '%s/%s/' % (self.s3_root_dir, key)
        path['local_prefix'] = '%s/%s/' % (self.local_root_dir, key)
        return path

    def get_dirs_by_etl_key(self, etl_key, dt_hour_str, update_time_str=''):
        path = {}
        path['s3folder'] = '%s/%s/dt=%s/%s/' % (self.s3_root_dir, etl_key, dt_hour_str, update_time_str)
        path['local_dir'] = '%s/%s/%s/%s/' % (self.local_root_dir, etl_key, dt_hour_str, update_time_str)
        path['s3prefix'] = '%s/%s/dt=%s/' % (self.s3_root_dir, etl_key, dt_hour_str)
        path['local_prefix'] = '%s/%s/%s/' % (self.local_root_dir, etl_key, dt_hour_str)
        return path


class ETLPathHelper():

    def __init__(self, s3baseprefix='ml/'):
        self.s3_root_dir = '%s%s' % (s3baseprefix, 'etl-workspace')
        self.local_root_dir = 'tmpdata/etl-workspace'

    def get_etl_key(self, etl_name):
        return {
            'battery_status': 'battery-status',
            'battery_swap_log': 'battery-swap-log',
            'vm_battery_count': 'vm-battery-count',
            'vm_battery_count_all': 'vm-battery-count-all',
            'vm_exchange_count': 'vm-exchange-count',
            'vm_status': 'vm-status'
        }[etl_name]


    def get_battery_status_dirs(self, dt_hour_str, update_time_str=''):
        etl_key = self.get_etl_key('battery_status')
        return self.get_dirs_by_etl_key(etl_key, dt_hour_str, update_time_str=update_time_str)

    def get_battery_swap_log_dirs(self, dt_hour_str, update_time_str=''):
        etl_key = self.get_etl_key('battery_swap_log')
        return self.get_dirs_by_etl_key(etl_key, dt_hour_str, update_time_str=update_time_str)

    def get_vm_battery_count_dirs(self, dt_hour_str, update_time_str=''):
        etl_key = self.get_etl_key('vm_battery_count')
        return self.get_dirs_by_etl_key(etl_key, dt_hour_str, update_time_str=update_time_str)

    def get_vm_exchange_count_dirs(self, dt_hour_str, update_time_str=''):
        etl_key = self.get_etl_key('vm_exchange_count')
        return self.get_dirs_by_etl_key(etl_key, dt_hour_str, update_time_str=update_time_str)
    
    def get_vm_status_dirs(self, dt_hour_str, update_time_str=''):
        etl_key = self.get_etl_key('vm_status')
        return self.get_dirs_by_etl_key(etl_key, dt_hour_str, update_time_str=update_time_str)

    def get_dirs_by_etl_key(self, etl_key, dt_hour_str, update_time_str=''):
        path = {}
        path['s3folder'] = '%s/%s/%s/%s/' % (self.s3_root_dir, etl_key, dt_hour_str, update_time_str)
        path['s3folder_latest'] = '%s/%s/%s/%s/' % (self.s3_root_dir, etl_key, dt_hour_str, 'latest')
        path['local_dir'] = '%s/%s/%s/%s/' % (self.local_root_dir, etl_key, dt_hour_str, update_time_str)
        path['s3prefix'] = '%s/%s/%s/' % (self.s3_root_dir, etl_key, dt_hour_str)
        path['local_prefix'] = '%s/%s/%s/' % (self.local_root_dir, etl_key, dt_hour_str)

        path['s3folder_wpn'] = '%s/%s/dt=%s/' % (self.s3_root_dir, etl_key, dt_hour_str)
        path['local_dir_wpn'] = '%s/%s/%s/' % (self.local_root_dir, etl_key, dt_hour_str)
        return path


class JobPathHelper():

    def __init__(self, s3baseprefix='ml/'):
        self.s3_root_dir = '%s%s' % (s3baseprefix, 'job-workspace')
        self.local_root_dir = 'tmpdata/job-workspace'

    def get_job_key(self, job_name):
        return {
            'demand_prediction': 'demand-prediction',
            'demand_prediction_2h': 'demand-prediction-2h',
            'demand_prediction_4h': 'demand-prediction-4h',
            'demand_prediction_1d': 'demand-prediction-1d',
        }[job_name]

    def get_demand_prediction_dirs(self, dt_hour_str, update_time_str=''):
        return self.get_dirs_by_demand_prediction_key('demand_prediction', dt_hour_str, update_time_str=update_time_str)

    def get_demand_prediction_2h_dirs(self, dt_hour_str, update_time_str=''):
        return self.get_dirs_by_demand_prediction_key('demand_prediction_2h', dt_hour_str, update_time_str=update_time_str)

    def get_demand_prediction_4h_dirs(self, dt_hour_str, update_time_str=''):
        return self.get_dirs_by_demand_prediction_key('demand_prediction_4h', dt_hour_str, update_time_str=update_time_str)

    def get_demand_prediction_1d_dirs(self, dt_hour_str, update_time_str=''):
        return self.get_dirs_by_demand_prediction_key('demand_prediction_1d', dt_hour_str, update_time_str=update_time_str)

    def get_dirs_by_demand_prediction_name(self, job_name, dt_hour_str, update_time_str=''):
        job_key = self.get_job_key(job_name)
        path = {}
        path['s3folder'] = '%s/%s/%s/%s/' % (self.s3_root_dir, job_key, dt_hour_str, update_time_str)
        path['local_dir'] = '%s/%s/%s/%s/' % (self.local_root_dir, job_key, dt_hour_str, update_time_str)
        path['s3prefix'] = '%s/%s/%s/' % (self.s3_root_dir, job_key, dt_hour_str)
        path['local_prefix'] = '%s/%s/%s/' % (self.local_root_dir, job_key, dt_hour_str)
        return path
        



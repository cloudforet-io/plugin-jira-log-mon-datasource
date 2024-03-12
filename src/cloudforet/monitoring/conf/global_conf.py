CONNECTORS = {
}

LOG = {
    'filters': {
        'masking': {
            'rules': {
                'DataSource.verify': [
                    'secret_data'
                ],
                'Log.list_logs': [
                    'secret_data'
                ],
            }
        }
    }
}
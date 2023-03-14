CONNECTORS = {
}

LOG = {
    'filters': {
        'masking': {
            'rules': {
                'DataSource.verify': [
                    'secret_data'
                ],
                'Log.list': [
                    'secret_data'
                ],
            }
        }
    }
}
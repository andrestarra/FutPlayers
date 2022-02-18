import json


def extract_information(response):
    status = response.status_code
    text = response.text
    # print(response)
    try:
        response = response.json()
        # print(response)

        if status == 200:
            success = response['success']
            details = response['data'][0]
            return [ status, success, details ]
        elif status == 500:
            errors = text
            return [ status, str(errors) ]
        else:
            errors = response['errors']
            return [ status, str(errors) ]
    except Exception as errors:
        status |= 500
        return [ status, str(errors) ]

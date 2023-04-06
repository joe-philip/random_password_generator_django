def success(data) -> dict:
    response = {
        'status': True,
        'message': 'success'
    }
    if data is not None:
        response['data'] = data
    return response

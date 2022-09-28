import pickle


def dictionary_value_to_bytes(search_result: dict) -> dict:
    """
    Helper function for taking the searched result and pickle all field values except for search_used_time and check_time
    :param search_result: The DNS search result
    :type: dict

    :return: The altered dictionary
    :rtype: dict
    """
    for record_key in search_result:
        if record_key in ["search_used_time", "check_time"]:
            continue

        search_result[record_key] = pickle.dumps(search_result[record_key])

    return search_result


def bytes_decrypt(bytes_form_data: bytes) -> any:
    """
    Helper function to decrypt the given data

    :param bytes_form_data: Data to decrypt
    :type: bytes

    :return: The original form of the data
    :rtype: any
    """
    return pickle.loads(bytes_form_data)